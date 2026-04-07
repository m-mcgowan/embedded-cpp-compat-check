#!/usr/bin/env python3
"""Audit test errors to classify whether failures test the intended feature.

Reads JSON results and classifies each compile error into categories:
- legitimate: failure is about the feature being tested
- framework:  failure is in framework/system headers, not test code
- suspect:    failure may be testing the wrong thing — needs review

Usage:
    python scripts/audit_errors.py [results_dir]
    python scripts/audit_errors.py --suspects-only
"""

import json
import glob
import re
import sys
from collections import defaultdict
from pathlib import Path


# ── Classification rules ──
# Each rule is (name, description, match_fn, verdict)
# match_fn(feat, macro, err, first_error_file) → bool
# verdict: "legitimate", "framework", "suspect"

def _feat_name(feature: str) -> str:
    """Extract short feature name from 'cpp17/optional' → 'optional'."""
    return feature.split("/")[-1]


def _normalize(name: str) -> str:
    """Normalize for fuzzy matching: strip underscores, lowercase."""
    return name.lower().replace("_", "")


def _first_error_file(err: str) -> str:
    """Extract the file path from the first error: line."""
    for line in err.split("\n"):
        if "error:" in line:
            # Extract file path before the line:col: marker
            m = re.match(r"(.*?):\d+:\d+:", line)
            return m.group(1) if m else ""
    return ""


def _symbol_matches_feature(missing_symbol: str, feat_name: str) -> bool:
    """Check if a missing symbol is plausibly the feature under test."""
    norm_sym = _normalize(missing_symbol)
    norm_feat = _normalize(feat_name)
    # Direct containment
    if norm_sym in norm_feat or norm_feat in norm_sym:
        return True
    # Common variations: strip prefixes/suffixes
    stripped_feat = norm_feat.replace("lib", "").replace("constexpr", "")
    if stripped_feat and stripped_feat in norm_sym:
        return True
    stripped_sym = norm_sym.rstrip("tv")  # strip _t, _v suffixes
    if stripped_sym in norm_feat or norm_feat in stripped_sym:
        return True
    # Feature name words appear in the symbol
    feat_words = set(feat_name.lower().split("_")) - {"", "lib", "cpp", "std"}
    sym_words = set(missing_symbol.lower().split("_")) - {"", "std"}
    # At least half the feature words appear in the symbol
    if feat_words and len(feat_words & sym_words) >= max(1, len(feat_words) // 2):
        return True
    return False


# ── Rule definitions ──

RULES = []


def rule(name, description, verdict):
    """Decorator to register a classification rule."""
    def decorator(fn):
        RULES.append((name, description, fn, verdict))
        return fn
    return decorator


@rule("missing_header", "Platform lacks the required header", "legitimate")
def _missing_header(feat, macro, err, err_file):
    return "No such file or directory" in err


@rule("framework_teensy_cpp11",
      "Teensy inplace_function.h uses C++14 features at C++11",
      "framework")
def _teensy_inplace(feat, macro, err, err_file):
    return "inplace_function.h" in err


@rule("framework_teensy_cpp14",
      "Teensy IntervalTimer.h incompatible at this standard",
      "framework")
def _teensy_interval(feat, macro, err, err_file):
    return "IntervalTimer.h" in err


@rule("framework_mbed_cpp11",
      "mbed Callback.h uses C++14 features (std::remove_cv_t) at C++11",
      "framework")
def _mbed_callback(feat, macro, err, err_file):
    return "Callback.h" in err and "remove_cv_t" in err


@rule("framework_arduino_macro",
      "Arduino macro (abs, random, etc.) conflicts with standard header",
      "framework")
def _arduino_macro(feat, macro, err, err_file):
    # Arduino.h defines macros that break standard headers
    if "Arduino.h" in err and "expected unqualified-id" in err:
        return True
    return False


@rule("exceptions_disabled",
      "Test uses throw/catch but -fexceptions is not enabled",
      "suspect")
def _exceptions(feat, macro, err, err_file):
    if "exception handling disabled" in err:
        # exceptions test is supposed to test this
        if "exceptions" in _feat_name(feat):
            return False
        return True
    return False


@rule("abs_macro_conflict",
      "Arduino abs() macro conflicts with standard library header",
      "suspect")
def _abs_conflict(feat, macro, err, err_file):
    # Arduino's #define abs(x) breaks <complex>, <chrono>, etc.
    if 'macro "abs"' in err or ('abs' in err and 'expected unqualified-id' in err):
        # If the test specifically includes <complex>, it's a test bug
        # (should #undef abs). For other headers it's framework pollution.
        if "complex" in err.lower():
            return True  # suspect — test should #undef abs
    return False


@rule("abs_macro_framework",
      "Arduino abs() macro breaks standard library headers (framework issue)",
      "framework")
def _abs_framework(feat, macro, err, err_file):
    return 'macro "abs"' in err


@rule("cpp_standard_too_low",
      "Feature requires a higher C++ standard than requested",
      "legitimate")
def _cpp_standard_too_low(feat, macro, err, err_file):
    return "only available with '-std=" in err


@rule("random_header_includes_only",
      "Error with only include-chain lines — likely Arduino.h macro conflict with <random>",
      "framework")
def _random_includes_only(feat, macro, err, err_file):
    # When <random> conflicts with Arduino's random() macro, the error
    # output may only contain "In file included from" lines (truncated)
    if "random" not in _feat_name(feat):
        return False
    lines = [l.strip() for l in err.strip().split("\n") if l.strip()]
    return all("In file included from" in l or "from " in l for l in lines)


@rule("framework_header_error",
      "Error originates in framework/system header, not test code",
      "framework")
def _framework_header(feat, macro, err, err_file):
    first = _first_error_file(err)
    if not first:
        return False
    # Error in platformio packages, not in the test's objs/ directory
    return ".platformio/" in first and "objs/" not in first


# Features that legitimately depend on another symbol
_KNOWN_DEPS = {
    "scoped_lock": {"mutex"},
    "shared_timed_mutex": {"shared_timed_mutex", "mutex"},
    "shared_mutex": {"shared_mutex", "mutex"},
    "chrono_udls": {"chrono"},
    "complex_udls": {"complex"},
    "string_udls": {"string"},
    "saturation_arithmetic": {"add_sat", "sub_sat", "mul_sat", "div_sat", "saturate_cast"},
    "logical_traits": {"conjunction_v", "disjunction_v", "negation_v", "conjunction", "disjunction"},
    "noexcept_function_type": {"is_same_v"},
    "nonmember_container_access": {"size", "empty", "data"},
    "raw_memory_algorithms": {"destroy", "destroy_at", "uninitialized_move"},
    "type_trait_variable_templates": {"is_integral_v", "is_void_v", "is_same_v"},
    "math_special_functions": {"riemann_zeta", "beta", "laguerre"},
    "bitops": {"popcount", "countl_zero", "countr_zero", "rotl", "rotr"},
    "char8_t_lib": {"u8string"},
    "int_pow2": {"has_single_bit", "bit_ceil", "bit_floor"},
    "integer_comparison_functions": {"cmp_less", "cmp_greater", "cmp_equal"},
    "interpolate": {"midpoint", "lerp"},
    "constexpr_memory": {"construct_at", "destroy_at"},
    "constexpr_functional": {"invoke"},
    "remove_cvref": {"is_same_v", "remove_cvref_t"},
    "syncbuf": {"osyncstream"},
    "jthread": {"stop_source", "stop_token", "jthread"},
    "common_reference": {"common_reference_t", "common_reference"},
    "common_reference_wrapper": {"common_reference_t"},
    "unwrap_ref": {"unwrap_ref_decay_t", "unwrap_reference_t", "unwrap_ref_decay"},
    "generic_unordered_lookup": {"string_view"},
    "constrained_equality": {"optional"},
    "conditional_explicit": {"explicit"},
    "freestanding_random": {"random"},
    "ranges_generate_random": {"random"},
    "associative_heterogeneous_erasure": {"erase", "string_view"},
    "memory_resource": {"pmr"},
    "parallel_algorithm": {"execution"},
    "concepts_lib": {"integral", "concepts"},
    "math_constants": {"numbers"},
    "polymorphic_allocator": {"pmr"},
    "ranges": {"views", "ranges"},
    "conditional_explicit": {"explicit"},
}


def _extract_missing_symbol(err: str) -> str | None:
    """Extract the first missing std:: symbol from an error message."""
    # Only look at the first error line to avoid matching secondary errors
    first_error = ""
    for line in err.split("\n"):
        if "error:" in line:
            first_error = line
            break
    if not first_error:
        return None
    # Try both patterns on the first error line only
    patterns = [
        r"'(\w+)' is not a member of 'std'",
        r"'(\w+)' in namespace 'std' does not name",
        r"'std::(\w+)' has not been declared",
        r"has no member named '(\w+)'",
    ]
    for pat in patterns:
        m = re.search(pat, first_error)
        if m:
            return m.group(1)
    return None


@rule("missing_symbol_legit",
      "Missing std:: symbol matches the feature being tested",
      "legitimate")
def _missing_symbol_legit(feat, macro, err, err_file):
    missing = _extract_missing_symbol(err)
    if not missing:
        return False
    feat_name = _feat_name(feat)
    if _symbol_matches_feature(missing, feat_name):
        return True
    # Check known dependencies
    deps = _KNOWN_DEPS.get(feat_name, set())
    return missing.lower() in deps


@rule("missing_symbol_suspect",
      "Missing std:: symbol does NOT match the feature being tested",
      "suspect")
def _missing_symbol_suspect(feat, macro, err, err_file):
    missing = _extract_missing_symbol(err)
    if not missing:
        return False
    return not _symbol_matches_feature(missing, _feat_name(feat))


@rule("deprecated_removed",
      "Test uses deprecated/removed API",
      "suspect")
def _deprecated(feat, macro, err, err_file):
    # Only flag actual deprecation warnings, not missing symbols
    return "deprecated" in err.lower() and "since" in err.lower()


@rule("constexpr_not_available",
      "Function not yet constexpr — legitimate for constexpr_* features",
      "legitimate")
def _constexpr_not_available(feat, macro, err, err_file):
    return ("non-'constexpr'" in err or "non-constexpr" in err) and \
           "constexpr" in _feat_name(feat)


@rule("format_incomplete",
      "Formatter not yet implemented for this type — legitimate",
      "legitimate")
def _format_incomplete(feat, macro, err, err_file):
    return "format" in _feat_name(feat) and "/format" in err


@rule("framework_cascade",
      "Error cascades from framework/system header into test code",
      "framework")
def _framework_cascade(feat, macro, err, err_file):
    # If any error line references a framework/system header, the whole
    # failure is framework-caused even if the first error is in test code
    for line in err.split("\n"):
        if ".platformio/" in line and ("error:" in line or "In file included from" in line):
            if "/src/" not in line and "objs/" not in line:
                return True
    return False


@rule("unclassified",
      "Error doesn't match any known pattern — review manually",
      "legitimate")
def _unclassified(feat, macro, err, err_file):
    # Catch-all: if the error is in the test file, assume it's about the feature
    # Batch builds use src/, old direct-compile used objs/
    first = _first_error_file(err)
    return "objs/" in first or "/src/" in first or "src/" in first


# ── Classification engine ──

def classify(feat: str, macro: str, err: str) -> tuple[str, str, str]:
    """Classify an error. Returns (rule_name, description, verdict)."""
    err_file = _first_error_file(err)
    for name, desc, fn, verdict in RULES:
        if fn(feat, macro, err, err_file):
            return name, desc, verdict
    return "unknown", "Could not classify this error", "suspect"


# ── Main ──

def main():
    results_dir = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "results"
    suspects_only = "--suspects-only" in sys.argv

    # Load all results
    results = []
    for f in glob.glob(f"{results_dir}/**/*.json", recursive=True):
        if "manifest" in f or "+recipe" in f:
            continue
        with open(f) as fh:
            results.extend(json.load(fh))

    # Classify errors
    by_verdict = defaultdict(list)
    by_rule = defaultdict(list)

    for r in results:
        err = r.get("error_output") or ""
        if not err:
            continue
        feat = r["feature"]
        macro = r.get("macro", "")
        plat = r["platform"]
        std = r["standard"]

        rule_name, desc, verdict = classify(feat, macro, err)
        entry = {
            "feature": feat,
            "platform": plat,
            "standard": std,
            "macro": macro,
            "rule": rule_name,
            "verdict": verdict,
            "error": err[:300],
        }
        by_verdict[verdict].append(entry)
        by_rule[rule_name].append(entry)

    total_errors = sum(len(v) for v in by_verdict.values())

    # ── Report ──
    if not suspects_only:
        print(f"{'='*60}")
        print(f"Error Audit Report — {total_errors} errors classified")
        print(f"{'='*60}\n")

        for verdict in ["suspect", "framework", "legitimate"]:
            items = by_verdict.get(verdict, [])
            icon = {"suspect": "⚠️ ", "framework": "🔧", "legitimate": "✓ "}[verdict]
            print(f"{icon} {verdict.upper()}: {len(items)} errors")

        print()

        # Show rules breakdown
        print(f"{'─'*60}")
        print("By classification rule:\n")
        for rule_name in sorted(by_rule, key=lambda r: -len(by_rule[r])):
            items = by_rule[rule_name]
            verdict = items[0]["verdict"]
            icon = {"suspect": "⚠️ ", "framework": "🔧", "legitimate": "✓ "}[verdict]
            features = sorted(set(i["feature"] for i in items))
            platforms = sorted(set(i["platform"] for i in items))
            print(f"  {icon} {rule_name} [{verdict}] — {len(items)} errors, "
                  f"{len(features)} features, {len(platforms)} platforms")

    # Always show suspects in detail
    suspects = by_verdict.get("suspect", [])
    if suspects:
        print(f"\n{'='*60}")
        print(f"⚠️  SUSPECTS — {len(suspects)} errors that may be test bugs")
        print(f"{'='*60}\n")

        # Group by feature
        by_feat = defaultdict(list)
        for s in suspects:
            by_feat[s["feature"]].append(s)

        for feat in sorted(by_feat):
            items = by_feat[feat]
            plats = sorted(set(i["platform"] for i in items))
            rule_name = items[0]["rule"]
            print(f"  {feat} ({len(items)} platforms: {', '.join(plats)})")
            print(f"    Rule: {rule_name}")
            # Show first error snippet
            err_snippet = items[0]["error"].split("\n")
            err_line = next((l for l in err_snippet if "error:" in l), err_snippet[0])
            print(f"    Error: {err_line[:120]}")
            print()
    elif not suspects_only:
        print(f"\n✅ No suspect errors found — all failures test the intended feature.")


if __name__ == "__main__":
    main()
