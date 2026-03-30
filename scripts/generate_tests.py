#!/usr/bin/env python3
"""Generate test files for C++ feature compatibility checks.

Each test is a minimal .cpp file that includes the relevant header and
exercises the feature just enough to verify it compiles.
"""

from pathlib import Path

# (standard, filename, macro, category, description, source)
# Source should use 'auto main() -> int { ... }' pattern, return 0 on success.
TESTS = [
    # ── cpp11 language ──
    ("cpp11", "alias_templates", "__cpp_alias_templates", "language",
     "Alias templates",
     "template<typename T> using Ptr = T*;\nauto main() -> int { Ptr<int> p = nullptr; return p == nullptr ? 0 : 1; }"),

    ("cpp11", "decltype", "__cpp_decltype", "language",
     "decltype specifier",
     "auto main() -> int { int x = 42; decltype(x) y = x; return y - 42; }"),

    ("cpp11", "delegating_constructors", "__cpp_delegating_constructors", "language",
     "Delegating constructors",
     "struct S { int v; S(int x) : v(x) {} S() : S(42) {} };\nauto main() -> int { S s; return s.v - 42; }"),

    ("cpp11", "range_based_for", "__cpp_range_based_for", "language",
     "Range-based for loop",
     "auto main() -> int { int a[] = {1,2,3}; int s=0; for(auto x:a) s+=x; return s-6; }"),

    ("cpp11", "raw_strings", "__cpp_raw_strings", "language",
     "Raw string literals",
     'auto main() -> int { const char* s = R"(hello)"; return s[0]==\'h\' ? 0 : 1; }'),

    ("cpp11", "user_defined_literals", "__cpp_user_defined_literals", "language",
     "User-defined literals",
     "constexpr long long operator\"\"_km(unsigned long long v) { return v * 1000; }\nauto main() -> int { return 5_km == 5000 ? 0 : 1; }"),

    ("cpp11", "nsdmi", "__cpp_nsdmi", "language",
     "Non-static data member initializers",
     "struct S { int x = 42; };\nauto main() -> int { S s; return s.x - 42; }"),

    ("cpp11", "inheriting_constructors", "__cpp_inheriting_constructors", "language",
     "Inheriting constructors",
     "struct Base { int v; Base(int x) : v(x) {} };\nstruct Derived : Base { using Base::Base; };\nauto main() -> int { Derived d(42); return d.v - 42; }"),

    # ── cpp14 language ──
    ("cpp14", "return_type_deduction", "__cpp_return_type_deduction", "language",
     "Return type deduction for normal functions",
     "auto add(int a, int b) { return a + b; }\nauto main() -> int { return add(2, 3) - 5; }"),

    ("cpp14", "aggregate_nsdmi", "__cpp_aggregate_nsdmi", "language",
     "Aggregate classes with default member initializers",
     "struct S { int x = 1; int y = 2; };\nauto main() -> int { S s{10}; return s.x + s.y - 12; }"),

    # ── cpp14 library ──
    ("cpp14", "is_final", "__cpp_lib_is_final", "library",
     "std::is_final",
     "#include <type_traits>\nstruct A {}; struct B final {};\nauto main() -> int { return std::is_final<B>::value && !std::is_final<A>::value ? 0 : 1; }"),

    ("cpp14", "is_null_pointer", "__cpp_lib_is_null_pointer", "library",
     "std::is_null_pointer",
     "#include <type_traits>\nauto main() -> int { return std::is_null_pointer<decltype(nullptr)>::value ? 0 : 1; }"),

    ("cpp14", "transformation_trait_aliases", "__cpp_lib_transformation_trait_aliases", "library",
     "TransformationTrait aliases (remove_const_t etc)",
     "#include <type_traits>\nauto main() -> int { return std::is_same<std::remove_const_t<const int>, int>::value ? 0 : 1; }"),

    ("cpp14", "tuple_element_t", "__cpp_lib_tuple_element_t", "library",
     "std::tuple_element_t",
     "#include <tuple>\nauto main() -> int { using T = std::tuple<int, double>; std::tuple_element_t<0, T> x = 42; return x - 42; }"),

    ("cpp14", "integral_constant_callable", "__cpp_lib_integral_constant_callable", "library",
     "std::integral_constant::operator()",
     "#include <type_traits>\nauto main() -> int { std::true_type t; return t() ? 0 : 1; }"),

    # ── cpp17 language ──
    ("cpp17", "capture_star_this", "__cpp_capture_star_this", "language",
     "Lambda capture of *this by value",
     "struct S { int v=42; auto f() { return [*this]() { return v; }; } };\nauto main() -> int { S s; return s.f()() - 42; }"),

    ("cpp17", "hex_float", "__cpp_hex_float", "language",
     "Hexadecimal floating literals",
     "auto main() -> int { double d = 0x1.0p0; return d == 1.0 ? 0 : 1; }"),

    ("cpp17", "deduction_guides", "__cpp_deduction_guides", "language",
     "Class template argument deduction (CTAD)",
     "#include <utility>\nauto main() -> int { auto p = std::pair(1, 2.0); return p.first - 1; }"),

    ("cpp17", "maybe_unused", "maybe_unused", "attribute",
     "[[maybe_unused]] attribute",
     "auto main() -> int { [[maybe_unused]] int x = 42; return 0; }"),

    ("cpp17", "fallthrough", "fallthrough", "attribute",
     "[[fallthrough]] attribute",
     "auto main() -> int { int x = 1; switch(x) { case 1: x = 2; [[fallthrough]]; case 2: break; } return x - 2; }"),

    # ── cpp17 library ──
    ("cpp17", "has_unique_object_representations", "__cpp_lib_has_unique_object_representations", "library",
     "std::has_unique_object_representations",
     "#include <type_traits>\nauto main() -> int { return std::has_unique_object_representations_v<int> ? 0 : 1; }"),

    ("cpp17", "is_invocable", "__cpp_lib_is_invocable", "library",
     "std::is_invocable and std::invoke_result",
     "#include <type_traits>\nint add(int a, int b) { return a+b; }\nauto main() -> int { return std::is_invocable_v<decltype(add), int, int> ? 0 : 1; }"),

    ("cpp17", "logical_traits", "__cpp_lib_logical_traits", "library",
     "Logical operations on type traits (conjunction, disjunction, negation)",
     "#include <type_traits>\nauto main() -> int { return std::conjunction_v<std::true_type, std::true_type> ? 0 : 1; }"),

    ("cpp17", "nonmember_container_access", "__cpp_lib_nonmember_container_access", "library",
     "std::size(), std::data(), std::empty()",
     "#include <iterator>\nauto main() -> int { int a[] = {1,2,3}; return std::size(a) == 3 ? 0 : 1; }"),

    ("cpp17", "make_from_tuple", "__cpp_lib_make_from_tuple", "library",
     "std::make_from_tuple",
     "#include <tuple>\nstruct S { int x; int y; S(int a, int b) : x(a), y(b) {} };\nauto main() -> int { auto s = std::make_from_tuple<S>(std::make_tuple(1, 2)); return s.x + s.y - 3; }"),

    ("cpp17", "launder", "__cpp_lib_launder", "library",
     "std::launder",
     "#include <new>\nauto main() -> int { int x = 42; auto* p = std::launder(&x); return *p - 42; }"),

    ("cpp17", "sample", "__cpp_lib_sample", "library",
     "std::sample",
     "#include <algorithm>\n#include <iterator>\n#include <random>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3,4,5}; std::vector<int> out; std::sample(v.begin(), v.end(), std::back_inserter(out), 2, std::mt19937{}); return out.size() == 2 ? 0 : 1; }"),

    ("cpp17", "hypot", "__cpp_lib_hypot", "library",
     "3-argument overload of std::hypot",
     "#include <cmath>\nauto main() -> int { double h = std::hypot(1.0, 2.0, 2.0); return h > 2.9 && h < 3.1 ? 0 : 1; }"),

    ("cpp17", "array_constexpr", "__cpp_lib_array_constexpr", "library",
     "Constexpr std::array",
     "#include <array>\nconstexpr std::array<int,3> a = {1,2,3};\nauto main() -> int { return a[0] + a[1] + a[2] - 6; }"),

    ("cpp17", "chrono", "__cpp_lib_chrono", "library",
     "Rounding functions for chrono duration and time_point",
     "#include <chrono>\nauto main() -> int { auto d = std::chrono::milliseconds(1500); auto s = std::chrono::floor<std::chrono::seconds>(d); return s.count() == 1 ? 0 : 1; }"),

    ("cpp17", "node_extract", "__cpp_lib_node_extract", "library",
     "Splicing maps and sets (extract, merge)",
     "#include <map>\nauto main() -> int { std::map<int,int> a = {{1,2}}, b; auto nh = a.extract(1); b.insert(std::move(nh)); return b[1] - 2; }"),

    # ── cpp20 language ──
    ("cpp20", "using_enum", "__cpp_using_enum", "language",
     "using enum declaration",
     "enum class Color { Red, Green, Blue };\nauto main() -> int { using enum Color; return static_cast<int>(Green) == 1 ? 0 : 1; }"),

    ("cpp20", "conditional_explicit", "__cpp_conditional_explicit", "language",
     "explicit(bool)",
     "struct S { template<typename T> explicit(!std::is_same_v<T, int>) S(T) {} };\n#include <type_traits>\nauto main() -> int { S s(42); return 0; }"),

    # ── cpp20 library ──
    ("cpp20", "remove_cvref", "__cpp_lib_remove_cvref", "library",
     "std::remove_cvref",
     "#include <type_traits>\nauto main() -> int { return std::is_same_v<std::remove_cvref_t<const int&>, int> ? 0 : 1; }"),

    ("cpp20", "is_constant_evaluated", "__cpp_lib_is_constant_evaluated", "library",
     "std::is_constant_evaluated",
     "#include <type_traits>\nconstexpr int f() { if (std::is_constant_evaluated()) return 1; return 0; }\nauto main() -> int { constexpr int v = f(); return v == 1 ? 0 : 1; }"),

    ("cpp20", "type_identity", "__cpp_lib_type_identity", "library",
     "std::type_identity",
     "#include <type_traits>\ntemplate<typename T> void f(T, std::type_identity_t<T>) {}\nauto main() -> int { f(1, 2); return 0; }"),

    ("cpp20", "integer_comparison_functions", "__cpp_lib_integer_comparison_functions", "library",
     "Safe integer comparison (cmp_less etc)",
     "#include <utility>\nauto main() -> int { return std::cmp_less(-1, 1u) ? 0 : 1; }"),

    ("cpp20", "constexpr_string_view", "__cpp_lib_constexpr_string_view", "library",
     "Constexpr std::string_view",
     "#include <string_view>\nconstexpr std::string_view sv = \"hello\";\nstatic_assert(sv.size() == 5);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_vector", "__cpp_lib_constexpr_vector", "library",
     "Constexpr std::vector",
     "#include <vector>\nconstexpr int f() { std::vector<int> v = {1,2,3}; return v.size(); }\nstatic_assert(f() == 3);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_string", "__cpp_lib_constexpr_string", "library",
     "Constexpr std::string",
     "#include <string>\nconstexpr int f() { std::string s = \"hi\"; return s.size(); }\nstatic_assert(f() == 2);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_algorithms", "__cpp_lib_constexpr_algorithms", "library",
     "Constexpr algorithms",
     "#include <algorithm>\n#include <array>\nconstexpr auto f() { std::array a{3,1,2}; std::sort(a.begin(), a.end()); return a[0]; }\nstatic_assert(f() == 1);\nauto main() -> int { return 0; }"),

    ("cpp20", "ssize", "__cpp_lib_ssize", "library",
     "std::ssize",
     "#include <iterator>\nauto main() -> int { int a[] = {1,2,3}; return std::ssize(a) == 3 ? 0 : 1; }"),

    ("cpp20", "to_address", "__cpp_lib_to_address", "library",
     "std::to_address",
     "#include <memory>\nauto main() -> int { int x = 42; int* p = &x; return *std::to_address(p) - 42; }"),

    ("cpp20", "int_pow2", "__cpp_lib_int_pow2", "library",
     "Integral power-of-2 operations (bit_ceil, has_single_bit, etc)",
     "#include <bit>\nauto main() -> int { return std::has_single_bit(8u) && std::bit_ceil(5u) == 8 ? 0 : 1; }"),

    # ── cpp23 language ──
    ("cpp23", "if_consteval", "__cpp_if_consteval", "language",
     "if consteval",
     "constexpr int f() { if consteval { return 1; } else { return 0; } }\nauto main() -> int { constexpr int v = f(); return v == 1 ? 0 : 1; }"),

    ("cpp23", "size_t_suffix", "__cpp_size_t_suffix", "language",
     "Literal suffixes for size_t",
     "auto main() -> int { auto n = 42uz; return n == 42 ? 0 : 1; }"),

    # ── cpp23 library ──
    ("cpp23", "unreachable", "__cpp_lib_unreachable", "library",
     "std::unreachable",
     "#include <utility>\nauto main() -> int { int x = 1; if (x == 1) return 0; std::unreachable(); }"),

    ("cpp23", "string_contains", "__cpp_lib_string_contains", "library",
     "string::contains",
     "#include <string>\nauto main() -> int { std::string s = \"hello world\"; return s.contains(\"world\") ? 0 : 1; }"),

    ("cpp23", "is_scoped_enum", "__cpp_lib_is_scoped_enum", "library",
     "std::is_scoped_enum",
     "#include <type_traits>\nenum A { X }; enum class B { Y };\nauto main() -> int { return std::is_scoped_enum_v<B> && !std::is_scoped_enum_v<A> ? 0 : 1; }"),

    ("cpp23", "invoke_r", "__cpp_lib_invoke_r", "library",
     "std::invoke_r",
     "#include <functional>\nint add(int a, int b) { return a+b; }\nauto main() -> int { return std::invoke_r<long>(add, 2, 3) - 5; }"),

    ("cpp23", "move_only_function", "__cpp_lib_move_only_function", "library",
     "std::move_only_function",
     "#include <functional>\nauto main() -> int { std::move_only_function<int()> f = []{ return 42; }; return f() - 42; }"),

    ("cpp23", "ranges_contains", "__cpp_lib_ranges_contains", "library",
     "std::ranges::contains",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3}; return std::ranges::contains(v, 2) ? 0 : 1; }"),

    ("cpp23", "ranges_fold", "__cpp_lib_ranges_fold", "library",
     "std::ranges::fold_left",
     "#include <algorithm>\n#include <numeric>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3}; return std::ranges::fold_left(v, 0, std::plus{}) - 6; }"),

    ("cpp23", "flat_map", "__cpp_lib_flat_map", "library",
     "std::flat_map",
     "#include <flat_map>\nauto main() -> int { std::flat_map<int,int> m; m[1] = 42; return m[1] - 42; }"),

    ("cpp23", "mdspan", "__cpp_lib_mdspan", "library",
     "std::mdspan",
     "#include <mdspan>\nauto main() -> int { int data[] = {1,2,3,4}; std::mdspan m(data, 2, 2); return m[1, 1] - 4; }"),

    ("cpp23", "generator", "__cpp_lib_generator", "library",
     "std::generator",
     "#include <generator>\n#include <ranges>\nstd::generator<int> iota(int n) { for (int i=0; i<n; ++i) co_yield i; }\nauto main() -> int { int s=0; for (auto i : iota(4)) s+=i; return s-6; }"),

    ("cpp23", "bind_back", "__cpp_lib_bind_back", "library",
     "std::bind_back",
     "#include <functional>\nint sub(int a, int b) { return a - b; }\nauto main() -> int { auto sub5 = std::bind_back(sub, 5); return sub5(8) - 3; }"),
]


def main():
    test_dir = Path(__file__).parent.parent / 'tests'
    created = 0
    skipped = 0
    for std, name, macro, category, desc, source in TESTS:
        path = test_dir / std / f'{name}.cpp'
        if path.exists():
            skipped += 1
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        header = (
            f'// feature: {name}\n'
            f'// macro: {macro}\n'
            f'// standard: {std}\n'
            f'// category: {category}\n'
            f'// description: {desc}\n\n'
        )
        path.write_text(header + source.strip() + '\n')
        created += 1
        print(f'  Created {path}')

    print(f'\nCreated {created}, skipped {skipped} existing')


if __name__ == '__main__':
    main()
