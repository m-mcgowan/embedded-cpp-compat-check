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

    ("cpp11", "ref_qualifiers", "__cpp_ref_qualifiers", "language",
     "Ref-qualified member functions",
     "struct S { int f() & { return 1; } int f() && { return 2; } };\nauto main() -> int { S s; return s.f() == 1 ? 0 : 1; }"),

    ("cpp11", "exceptions", "__cpp_exceptions", "language",
     "Exception handling",
     "auto main() -> int { try { throw 42; } catch (int e) { return e - 42; } return 1; }"),

    ("cpp11", "threadsafe_static_init", "__cpp_threadsafe_static_init", "language",
     "Thread-safe initialization of static local variables",
     "int f() { static int x = 42; return x; }\nauto main() -> int { return f() - 42; }"),

    ("cpp11", "unicode_literals", "__cpp_unicode_literals", "language",
     "Unicode string literals (u\"\", U\"\", u8\"\")",
     "auto main() -> int { const char16_t* s16 = u\"hello\"; const char32_t* s32 = U\"world\"; return (s16[0] == u'h' && s32[0] == U'w') ? 0 : 1; }"),

    # ── cpp14 language ──
    ("cpp14", "return_type_deduction", "__cpp_return_type_deduction", "language",
     "Return type deduction for normal functions",
     "auto add(int a, int b) { return a + b; }\nauto main() -> int { return add(2, 3) - 5; }"),

    ("cpp14", "aggregate_nsdmi", "__cpp_aggregate_nsdmi", "language",
     "Aggregate classes with default member initializers",
     "struct S { int x = 1; int y = 2; };\nauto main() -> int { S s{10}; return s.x + s.y - 12; }"),

    # ── cpp11 language (additional) ──
    ("cpp11", "attributes", "__cpp_attributes", "language",
     "Basic attribute syntax [[noreturn]] etc",
     "[[noreturn]] void fatal() { throw 42; }\nauto main() -> int { return 0; }"),

    ("cpp11", "unicode_characters", "__cpp_unicode_characters", "language",
     "char16_t and char32_t Unicode character types",
     "auto main() -> int { char16_t c16 = u'A'; char32_t c32 = U'A'; return (c16 == u'A' && c32 == U'A') ? 0 : 1; }"),

    # ── cpp14 library ──
    ("cpp14", "shared_timed_mutex", "__cpp_lib_shared_timed_mutex", "library",
     "std::shared_timed_mutex",
     "#include <shared_mutex>\nauto main() -> int { std::shared_timed_mutex m; return 0; }"),

    ("cpp14", "to_chars", "__cpp_lib_to_chars", "library",
     "std::to_chars / std::from_chars",
     "#include <charconv>\n#include <array>\nauto main() -> int { std::array<char, 16> buf; auto [ptr, ec] = std::to_chars(buf.data(), buf.data() + buf.size(), 42); return ec == std::errc{} ? 0 : 1; }"),

    ("cpp14", "transparent_operators", "__cpp_lib_transparent_operators", "library",
     "Transparent function objects (std::less<> etc)",
     "#include <functional>\nauto main() -> int { std::less<> cmp; return cmp(1, 2) ? 0 : 1; }"),

    ("cpp14", "robust_nonmodifying_seq_ops", "__cpp_lib_robust_nonmodifying_seq_ops", "library",
     "Two-range overloads of std::equal and std::is_permutation",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector<int> a = {1,2,3}, b = {1,2,3}; return std::equal(a.begin(), a.end(), b.begin(), b.end()) ? 0 : 1; }"),

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

    ("cpp14", "chrono_udls", "__cpp_lib_chrono_udls", "library",
     "User-defined literals for chrono duration types (1s, 1ms, etc)",
     "#include <chrono>\nusing namespace std::chrono_literals;\nauto main() -> int { auto d = 1s; return d.count() == 1 ? 0 : 1; }"),

    ("cpp14", "complex_udls", "__cpp_lib_complex_udls", "library",
     "User-defined literals for std::complex (1i, 1if, etc)",
     "#include <complex>\nusing namespace std::complex_literals;\nauto main() -> int { auto c = 1.0i; return c.imag() == 1.0 ? 0 : 1; }"),

    ("cpp14", "string_udls", "__cpp_lib_string_udls", "library",
     "User-defined literals for std::string (\"hello\"s)",
     "#include <string>\nusing namespace std::string_literals;\nauto main() -> int { auto s = \"hello\"s; return s.size() == 5 ? 0 : 1; }"),

    ("cpp14", "generic_associative_lookup", "__cpp_lib_generic_associative_lookup", "library",
     "Heterogeneous comparison lookup in associative containers",
     "#include <map>\n#include <string>\n#include <string_view>\nauto main() -> int { std::map<std::string, int, std::less<>> m; m[\"key\"] = 42; return m.count(std::string_view(\"key\")) == 1 ? 0 : 1; }"),

    ("cpp14", "make_reverse_iterator", "__cpp_lib_make_reverse_iterator", "library",
     "std::make_reverse_iterator",
     "#include <iterator>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; auto rit = std::make_reverse_iterator(v.end()); return *rit - 3; }"),

    ("cpp14", "tuples_by_type", "__cpp_lib_tuples_by_type", "library",
     "Addressing tuple elements by type",
     "#include <tuple>\nauto main() -> int { auto t = std::make_tuple(42, 3.14); return std::get<int>(t) - 42; }"),

    ("cpp14", "result_of_sfinae", "__cpp_lib_result_of_sfinae", "library",
     "std::result_of and SFINAE",
     "#include <type_traits>\nint f(int x) { return x; }\nauto main() -> int { return std::is_same<std::result_of<decltype(f)(int)>::type, int>::value ? 0 : 1; }"),

    ("cpp14", "quoted_string_io", "__cpp_lib_quoted_string_io", "library",
     "std::quoted for I/O of quoted strings",
     "#include <iomanip>\n#include <sstream>\nauto main() -> int { std::ostringstream oss; oss << std::quoted(\"hello\"); return oss.str() == \"\\\"hello\\\"\" ? 0 : 1; }"),

    # ── cpp17 language ──
    ("cpp17", "aggregate_bases", "__cpp_aggregate_bases", "language",
     "Aggregate classes with public base classes",
     "struct Base { int x; };\nstruct Derived : Base { int y; };\nauto main() -> int { Derived d{{1}, 2}; return d.x + d.y - 3; }"),

    ("cpp17", "enumerator_attributes", "__cpp_enumerator_attributes", "language",
     "Attributes on enumerators (e.g. [[deprecated]])",
     "enum class E { A, B [[deprecated]] };\nauto main() -> int { return static_cast<int>(E::A); }"),

    ("cpp17", "nontype_template_args", "__cpp_nontype_template_args", "language",
     "Allow constant evaluation for all non-type template arguments",
     "struct S { int v; constexpr S(int x) : v(x) {} };\ntemplate<S s> constexpr int get() { return s.v; }\nauto main() -> int { return get<S{42}>() - 42; }"),

    ("cpp17", "template_template_args", "__cpp_template_template_args", "language",
     "Matching of template template-arguments",
     "template<template<typename> class C, typename T> struct Wrap { C<T> c; };\n#include <vector>\nauto main() -> int { Wrap<std::vector, int> w; w.c.push_back(42); return w.c[0] - 42; }"),

    ("cpp17", "nontype_template_parameter_auto", "__cpp_nontype_template_parameter_auto", "language",
     "auto non-type template parameters",
     "template<auto N> constexpr auto value = N;\nauto main() -> int { return value<42> - 42; }"),

    ("cpp17", "namespace_attributes", "__cpp_namespace_attributes", "language",
     "Attributes on namespaces and enumerators",
     "namespace [[deprecated]] old_ns { inline int x = 0; }\nauto main() -> int { return 0; }"),

    ("cpp17", "noexcept_function_type", "__cpp_noexcept_function_type", "language",
     "noexcept as part of function type",
     "#include <type_traits>\nauto main() -> int { return std::is_same_v<void() noexcept, void()> ? 1 : 0; }"),

    ("cpp17", "guaranteed_copy_elision", "__cpp_guaranteed_copy_elision", "language",
     "Guaranteed copy elision (prvalue materialization)",
     "struct NoCopy { NoCopy() = default; NoCopy(const NoCopy&) = delete; NoCopy(NoCopy&&) = delete; };\nNoCopy make() { return NoCopy{}; }\nauto main() -> int { NoCopy x = make(); (void)x; return 0; }"),

    ("cpp17", "deleted_function", "__cpp_deleted_function", "language",
     "Explicitly deleted functions",
     "void f() = delete;\ntemplate<typename T> void g(T) = delete;\nvoid g(int) {}\nauto main() -> int { g(42); return 0; }"),

    ("cpp17", "aligned_new", "__cpp_aligned_new", "language",
     "Dynamic memory allocation with over-aligned types",
     "#include <new>\nstruct alignas(64) Aligned { int x; };\nauto main() -> int { auto* p = new Aligned; p->x = 42; int v = p->x; delete p; return v - 42; }"),

    ("cpp17", "variadic_using", "__cpp_variadic_using", "language",
     "Pack expansions in using-declarations",
     "template<typename... Bases> struct Overloaded : Bases... { using Bases::operator()...; };\nstruct A { int operator()(int) { return 1; } };\nstruct B { int operator()(double) { return 2; } };\nauto main() -> int { Overloaded<A, B> o; return o(1) == 1 && o(1.0) == 2 ? 0 : 1; }"),

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

    ("cpp17", "shared_mutex", "__cpp_lib_shared_mutex", "library",
     "std::shared_mutex",
     "#include <shared_mutex>\nauto main() -> int { std::shared_mutex m; return 0; }"),

    ("cpp17", "is_swappable", "__cpp_lib_is_swappable", "library",
     "std::is_swappable and std::is_nothrow_swappable",
     "#include <type_traits>\nauto main() -> int { return std::is_swappable_v<int> ? 0 : 1; }"),

    ("cpp17", "uncaught_exceptions", "__cpp_lib_uncaught_exceptions", "library",
     "std::uncaught_exceptions (plural)",
     "#include <exception>\nauto main() -> int { return std::uncaught_exceptions() == 0 ? 0 : 1; }"),

    ("cpp17", "memory_resource", "__cpp_lib_memory_resource", "library",
     "Polymorphic memory resources <memory_resource>",
     "#include <memory_resource>\nauto main() -> int { auto* r = std::pmr::get_default_resource(); return r != nullptr ? 0 : 1; }"),

    ("cpp17", "execution", "__cpp_lib_execution", "library",
     "Execution policies for parallel algorithms",
     "#include <execution>\n#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector<int> v = {3,1,2}; std::sort(std::execution::seq, v.begin(), v.end()); return v[0] == 1 ? 0 : 1; }"),

    ("cpp17", "raw_memory_algorithms", "__cpp_lib_raw_memory_algorithms", "library",
     "std::uninitialized_move, uninitialized_value_construct etc",
     "#include <memory>\nauto main() -> int { int src[] = {1,2,3}; alignas(int) unsigned char buf[sizeof(src)]; auto* dst = reinterpret_cast<int*>(buf); std::uninitialized_copy(src, src+3, dst); int v = dst[0] + dst[1] + dst[2]; std::destroy(dst, dst+3); return v - 6; }"),

    ("cpp17", "addressof_constexpr", "__cpp_lib_addressof_constexpr", "library",
     "constexpr std::addressof",
     "#include <memory>\nconstexpr int x = 42;\nconstexpr const int* p = std::addressof(x);\nauto main() -> int { return *p - 42; }"),

    ("cpp17", "atomic_is_always_lock_free", "__cpp_lib_atomic_is_always_lock_free", "library",
     "std::atomic<T>::is_always_lock_free",
     "#include <atomic>\nauto main() -> int { (void)std::atomic<int>::is_always_lock_free; return 0; }"),

    ("cpp17", "hardware_interference_size", "__cpp_lib_hardware_interference_size", "library",
     "std::hardware_destructive_interference_size",
     "#include <new>\nauto main() -> int { return std::hardware_destructive_interference_size > 0 ? 0 : 1; }"),

    ("cpp17", "boyer_moore_searcher", "__cpp_lib_boyer_moore_searcher", "library",
     "Boyer-Moore string searcher",
     "#include <functional>\n#include <algorithm>\n#include <string>\nauto main() -> int { std::string haystack = \"hello world\"; std::string needle = \"world\"; auto it = std::search(haystack.begin(), haystack.end(), std::boyer_moore_searcher(needle.begin(), needle.end())); return it != haystack.end() ? 0 : 1; }"),

    ("cpp17", "enable_shared_from_this", "__cpp_lib_enable_shared_from_this", "library",
     "std::enable_shared_from_this::weak_from_this",
     "#include <memory>\nstruct S : std::enable_shared_from_this<S> {};\nauto main() -> int { auto sp = std::make_shared<S>(); auto wp = sp->weak_from_this(); return wp.expired() ? 1 : 0; }"),

    ("cpp17", "shared_ptr_weak_type", "__cpp_lib_shared_ptr_weak_type", "library",
     "std::shared_ptr<T>::weak_type",
     "#include <memory>\nauto main() -> int { using W = std::shared_ptr<int>::weak_type; auto sp = std::make_shared<int>(42); W wp = sp; return wp.expired() ? 1 : 0; }"),

    ("cpp17", "unordered_map_try_emplace", "__cpp_lib_unordered_map_try_emplace", "library",
     "std::unordered_map::try_emplace and insert_or_assign",
     "#include <unordered_map>\n#include <string>\nauto main() -> int { std::unordered_map<std::string, int> m; m.try_emplace(\"key\", 42); return m[\"key\"] - 42; }"),

    ("cpp17", "math_special_functions", "__cpp_lib_math_special_functions", "library",
     "Mathematical special functions (std::cyl_bessel_j etc)",
     "#include <cmath>\nauto main() -> int { double v = std::riemann_zeta(2.0); return v > 1.6 && v < 1.7 ? 0 : 1; }"),

    # ── cpp20 language ──
    ("cpp20", "using_enum", "__cpp_using_enum", "language",
     "using enum declaration",
     "enum class Color { Red, Green, Blue };\nauto main() -> int { using enum Color; return static_cast<int>(Green) == 1 ? 0 : 1; }"),

    ("cpp20", "conditional_explicit", "__cpp_conditional_explicit", "language",
     "explicit(bool)",
     "struct S { template<typename T> explicit(!std::is_same_v<T, int>) S(T) {} };\n#include <type_traits>\nauto main() -> int { S s(42); return 0; }"),

    ("cpp20", "aggregate_paren_init", "__cpp_aggregate_paren_init", "language",
     "Aggregate initialization using parentheses",
     "struct S { int x; int y; };\nauto main() -> int { S s(1, 2); return s.x + s.y - 3; }"),

    ("cpp20", "impl_destroying_delete", "__cpp_impl_destroying_delete", "language",
     "Destroying operator delete (compiler support)",
     "#include <new>\nstruct S { int v; static void operator delete(S* p, std::destroying_delete_t) { p->~S(); ::operator delete(p); } };\nauto main() -> int { auto* p = new S{42}; delete p; return 0; }"),

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

    ("cpp20", "atomic_ref", "__cpp_lib_atomic_ref", "library",
     "std::atomic_ref — atomic operations on non-atomic objects",
     "#include <atomic>\nauto main() -> int { int x = 0; std::atomic_ref<int> r(x); r.store(42); return r.load() - 42; }"),

    ("cpp20", "latch", "__cpp_lib_latch", "library",
     "std::latch — single-use countdown synchronization",
     "#include <latch>\nauto main() -> int { std::latch l(1); l.count_down(); return l.try_wait() ? 0 : 1; }"),

    ("cpp20", "semaphore", "__cpp_lib_semaphore", "library",
     "std::counting_semaphore and std::binary_semaphore",
     "#include <semaphore>\nauto main() -> int { std::binary_semaphore s(1); s.acquire(); s.release(); return 0; }"),

    ("cpp20", "barrier", "__cpp_lib_barrier", "library",
     "std::barrier — reusable thread barrier",
     "#include <barrier>\nauto main() -> int { std::barrier b(1); b.arrive_and_drop(); return 0; }"),

    ("cpp20", "jthread", "__cpp_lib_jthread", "library",
     "std::jthread and std::stop_token",
     "#include <stop_token>\nauto main() -> int { std::stop_source src; std::stop_token tok = src.get_token(); return tok.stop_requested() ? 1 : 0; }"),

    ("cpp20", "coroutine", "__cpp_lib_coroutine", "library",
     "Coroutine support library <coroutine>",
     "#include <coroutine>\nauto main() -> int { std::coroutine_handle<> h; (void)h; return 0; }"),

    ("cpp20", "smart_ptr_for_overwrite", "__cpp_lib_smart_ptr_for_overwrite", "library",
     "std::make_unique_for_overwrite / make_shared_for_overwrite",
     "#include <memory>\nauto main() -> int { auto p = std::make_unique_for_overwrite<int>(); *p = 42; return *p - 42; }"),

    ("cpp20", "polymorphic_allocator", "__cpp_lib_polymorphic_allocator", "library",
     "std::pmr::polymorphic_allocator",
     "#include <memory_resource>\nauto main() -> int { std::pmr::polymorphic_allocator<int> alloc; return 0; }"),

    ("cpp20", "shift", "__cpp_lib_shift", "library",
     "std::shift_left and std::shift_right",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4,5}; std::shift_left(v.begin(), v.end(), 2); return v[0] == 3 ? 0 : 1; }"),

    ("cpp20", "syncbuf", "__cpp_lib_syncbuf", "library",
     "std::syncbuf and std::osyncstream",
     "#include <syncstream>\n#include <sstream>\nauto main() -> int { std::ostringstream oss; std::osyncstream sync(oss); sync << \"hi\"; sync.emit(); return oss.str() == \"hi\" ? 0 : 1; }"),

    ("cpp20", "assume_aligned", "__cpp_lib_assume_aligned", "library",
     "std::assume_aligned",
     "#include <memory>\nauto main() -> int { alignas(64) int buf[4] = {42}; auto* p = std::assume_aligned<64>(buf); return p[0] - 42; }"),

    ("cpp20", "atomic_flag_test", "__cpp_lib_atomic_flag_test", "library",
     "std::atomic_flag::test()",
     "#include <atomic>\nauto main() -> int { std::atomic_flag f = ATOMIC_FLAG_INIT; return f.test() ? 1 : 0; }"),

    ("cpp20", "atomic_lock_free_type_aliases", "__cpp_lib_atomic_lock_free_type_aliases", "library",
     "std::atomic_signed_lock_free and std::atomic_unsigned_lock_free",
     "#include <atomic>\nauto main() -> int { std::atomic_signed_lock_free a{0}; a.store(42); return a.load() - 42; }"),

    ("cpp20", "atomic_value_initialization", "__cpp_lib_atomic_value_initialization", "library",
     "Value-initialized std::atomic<T> (zero-initialized by default)",
     "#include <atomic>\nauto main() -> int { std::atomic<int> a{}; return a.load(); }"),

    ("cpp20", "bounded_array_traits", "__cpp_lib_bounded_array_traits", "library",
     "std::is_bounded_array and std::is_unbounded_array",
     "#include <type_traits>\nauto main() -> int { return std::is_bounded_array_v<int[3]> && !std::is_bounded_array_v<int[]> ? 0 : 1; }"),

    ("cpp20", "char8_t_lib", "__cpp_lib_char8_t", "library",
     "Library support for char8_t",
     "#include <string>\nauto main() -> int { std::u8string s = u8\"hello\"; return s.size() == 5 ? 0 : 1; }"),

    ("cpp20", "concepts_lib", "__cpp_lib_concepts", "library",
     "Standard library concepts (<concepts> header)",
     "#include <concepts>\ntemplate<std::integral T> T add(T a, T b) { return a + b; }\nauto main() -> int { return add(2, 3) - 5; }"),

    ("cpp20", "destroying_delete", "__cpp_lib_destroying_delete", "library",
     "Destroying operator delete (library support: std::destroying_delete_t)",
     "#include <new>\nstruct Node { int v; static void operator delete(Node* p, std::destroying_delete_t) { p->~Node(); ::operator delete(p); } };\nauto main() -> int { auto* n = new Node{42}; delete n; return 0; }"),

    ("cpp20", "generic_unordered_lookup", "__cpp_lib_generic_unordered_lookup", "library",
     "Heterogeneous lookup in unordered containers",
     "#include <unordered_map>\n#include <string>\nstruct Hash { using is_transparent = void; size_t operator()(std::string_view sv) const { return std::hash<std::string_view>{}(sv); } };\nstruct Eq { using is_transparent = void; bool operator()(std::string_view a, std::string_view b) const { return a == b; } };\nauto main() -> int { std::unordered_map<std::string, int, Hash, Eq> m; m[\"key\"] = 42; return m.find(std::string_view(\"key\"))->second - 42; }"),

    ("cpp20", "interpolate", "__cpp_lib_interpolate", "library",
     "std::lerp and std::midpoint",
     "#include <numeric>\nauto main() -> int { auto m = std::midpoint(1, 3); auto l = std::lerp(0.0, 1.0, 0.5); return (m == 2 && l == 0.5) ? 0 : 1; }"),

    ("cpp20", "is_nothrow_convertible", "__cpp_lib_is_nothrow_convertible", "library",
     "std::is_nothrow_convertible",
     "#include <type_traits>\nauto main() -> int { return std::is_nothrow_convertible_v<int, double> ? 0 : 1; }"),

    ("cpp20", "list_remove_return_type", "__cpp_lib_list_remove_return_type", "library",
     "std::list::remove returns removed count",
     "#include <list>\nauto main() -> int { std::list<int> l = {1, 2, 2, 3}; auto n = l.remove(2); return n == 2 ? 0 : 1; }"),

    ("cpp20", "three_way_comparison_lib", "__cpp_lib_three_way_comparison", "library",
     "Three-way comparison library support (<compare>)",
     "#include <compare>\nauto main() -> int { auto r = (1 <=> 2); return (r < 0) ? 0 : 1; }"),

    ("cpp20", "unwrap_ref", "__cpp_lib_unwrap_ref", "library",
     "std::unwrap_reference and std::unwrap_ref_decay",
     "#include <type_traits>\nauto main() -> int { int x = 42; auto ref = std::ref(x); using T = std::unwrap_ref_decay_t<decltype(ref)>; return std::is_same_v<T, int&> ? 0 : 1; }"),

    # ── cpp23 language ──
    ("cpp23", "if_consteval", "__cpp_if_consteval", "language",
     "if consteval",
     "constexpr int f() { if consteval { return 1; } else { return 0; } }\nauto main() -> int { constexpr int v = f(); return v == 1 ? 0 : 1; }"),

    ("cpp23", "size_t_suffix", "__cpp_size_t_suffix", "language",
     "Literal suffixes for size_t",
     "auto main() -> int { auto n = 42uz; return n == 42 ? 0 : 1; }"),

    ("cpp23", "static_call_operator", "__cpp_static_call_operator", "language",
     "static operator() in function objects",
     "struct Adder { static int operator()(int a, int b) { return a + b; } };\nauto main() -> int { return Adder{}(2, 3) - 5; }"),

    ("cpp23", "implicit_move", "__cpp_implicit_move", "language",
     "Simpler implicit move from local variables",
     "struct S { S() = default; S(S&&) = default; S(const S&) = delete; };\nS make() { S s; return s; }\nauto main() -> int { S s = make(); (void)s; return 0; }"),

    ("cpp23", "named_character_escapes", "__cpp_named_character_escapes", "language",
     "Named character escapes (e.g. \\N{LATIN SMALL LETTER A})",
     "auto main() -> int { char c = '\\N{LATIN SMALL LETTER A}'; return c == 'a' ? 0 : 1; }"),

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

    ("cpp23", "spanstream", "__cpp_lib_spanstream", "library",
     "std::spanstream — stream over a fixed buffer",
     "#include <spanstream>\nauto main() -> int { char buf[32]; std::ospanstream ss(buf); ss << 42; return 0; }"),

    ("cpp23", "constexpr_bitset", "__cpp_lib_constexpr_bitset", "library",
     "Constexpr std::bitset",
     "#include <bitset>\nconstexpr std::bitset<8> b(0b10101010);\nstatic_assert(b.count() == 4);\nauto main() -> int { return 0; }"),

    ("cpp23", "out_ptr", "__cpp_lib_out_ptr", "library",
     "std::out_ptr and std::inout_ptr",
     "#include <memory>\nstatic void alloc_int(int** p) { *p = new int(42); }\nauto main() -> int { std::unique_ptr<int> up; alloc_int(std::out_ptr(up)); return *up - 42; }"),

    ("cpp23", "reference_from_temporary", "__cpp_lib_reference_from_temporary", "library",
     "std::reference_constructs_from_temporary",
     "#include <type_traits>\nauto main() -> int { return std::reference_constructs_from_temporary_v<const int&, int> ? 0 : 1; }"),

    ("cpp23", "string_resize_and_overwrite", "__cpp_lib_string_resize_and_overwrite", "library",
     "std::string::resize_and_overwrite",
     "#include <string>\nauto main() -> int { std::string s; s.resize_and_overwrite(5, [](char* p, std::size_t n) { for (std::size_t i=0; i<n; ++i) p[i]='x'; return n; }); return s.size() == 5 ? 0 : 1; }"),

    ("cpp23", "ranges_zip", "__cpp_lib_ranges_zip", "library",
     "std::views::zip",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector a = {1,2,3}; std::vector b = {4,5,6}; int s = 0; for (auto [x,y] : std::views::zip(a, b)) s += x + y; return s - 21; }"),

    ("cpp23", "flat_set", "__cpp_lib_flat_set", "library",
     "std::flat_set",
     "#include <flat_set>\nauto main() -> int { std::flat_set<int> s = {3, 1, 2}; return *s.begin() == 1 ? 0 : 1; }"),

    ("cpp23", "ranges_as_rvalue", "__cpp_lib_ranges_as_rvalue", "library",
     "std::views::as_rvalue (move-only view)",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; auto r = v | std::views::as_rvalue; int s = 0; for (auto x : r) s += x; return s - 6; }"),

    ("cpp23", "ranges_chunk", "__cpp_lib_ranges_chunk", "library",
     "std::views::chunk — partition range into fixed-size chunks",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4}; int n = 0; for (auto c : v | std::views::chunk(2)) n++; return n == 2 ? 0 : 1; }"),

    ("cpp23", "ranges_chunk_by", "__cpp_lib_ranges_chunk_by", "library",
     "std::views::chunk_by — partition range by adjacent predicate",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {1,1,2,2,3}; int n = 0; for (auto c : v | std::views::chunk_by(std::equal_to<>{})) n++; return n == 3 ? 0 : 1; }"),

    ("cpp23", "ranges_find_last", "__cpp_lib_ranges_find_last", "library",
     "std::ranges::find_last",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,2,1}; auto r = std::ranges::find_last(v, 2); return *r.begin() == 2 && r.begin() == v.begin()+3 ? 0 : 1; }"),

    ("cpp23", "ranges_iota", "__cpp_lib_ranges_iota", "library",
     "std::ranges::iota",
     "#include <numeric>\n#include <vector>\nauto main() -> int { std::vector<int> v(5); std::ranges::iota(v, 1); return v[0] == 1 && v[4] == 5 ? 0 : 1; }"),

    ("cpp23", "ranges_join_with", "__cpp_lib_ranges_join_with", "library",
     "std::views::join_with — join ranges with a delimiter",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector<std::vector<int>> v = {{1,2},{3,4}}; int s = 0; for (auto x : v | std::views::join_with(0)) s += x; return s == 10 ? 0 : 1; }"),

    ("cpp23", "ranges_repeat", "__cpp_lib_ranges_repeat", "library",
     "std::views::repeat",
     "#include <ranges>\nauto main() -> int { int n = 0; for (auto x : std::views::repeat(42) | std::views::take(3)) n += x; return n == 126 ? 0 : 1; }"),

    ("cpp23", "ranges_starts_ends_with", "__cpp_lib_ranges_starts_ends_with", "library",
     "std::ranges::starts_with and std::ranges::ends_with",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4,5}; std::vector p = {1,2}; return std::ranges::starts_with(v, p) ? 0 : 1; }"),

    ("cpp23", "ranges_stride", "__cpp_lib_ranges_stride", "library",
     "std::views::stride",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4,5,6}; int s = 0; for (auto x : v | std::views::stride(2)) s += x; return s == 9 ? 0 : 1; }"),

    ("cpp23", "ranges_to_container", "__cpp_lib_ranges_to_container", "library",
     "std::ranges::to — convert range to container",
     "#include <ranges>\n#include <vector>\nauto main() -> int { auto v = std::views::iota(1, 4) | std::ranges::to<std::vector>(); return v.size() == 3 && v[0] == 1 ? 0 : 1; }"),

    ("cpp23", "stdatomic_h", "__cpp_lib_stdatomic_h", "library",
     "C-compatible <stdatomic.h> header",
     "#include <stdatomic.h>\nauto main() -> int { atomic_int a = 0; atomic_store(&a, 42); return atomic_load(&a) - 42; }"),

    ("cpp23", "tuple_like", "__cpp_lib_tuple_like", "library",
     "Tuple protocol for std::pair, std::array, std::subrange",
     "#include <tuple>\n#include <utility>\nauto main() -> int { auto p = std::pair(1, 2); auto [a, b] = p; return a + b - 3; }"),

    ("cpp23", "is_implicit_lifetime", "__cpp_lib_is_implicit_lifetime", "library",
     "std::is_implicit_lifetime type trait",
     "#include <type_traits>\nstruct S { int x; };\nauto main() -> int { return std::is_implicit_lifetime_v<S> ? 0 : 1; }"),

    ("cpp23", "ios_noreplace", "__cpp_lib_ios_noreplace", "library",
     "std::ios::noreplace open mode flag",
     "#include <ios>\nauto main() -> int { auto mode = std::ios::noreplace; (void)mode; return 0; }"),

    ("cpp23", "adaptor_iterator_pair_constructor", "__cpp_lib_adaptor_iterator_pair_constructor", "library",
     "Iterator-pair constructors for std::stack and std::queue",
     "#include <queue>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; std::queue<int> q(v.begin(), v.end()); return q.size() == 3 ? 0 : 1; }"),

    ("cpp23", "allocate_at_least", "__cpp_lib_allocate_at_least", "library",
     "std::allocator::allocate_at_least",
     "#include <memory>\nauto main() -> int { std::allocator<int> a; auto [ptr, n] = a.allocate_at_least(4); a.deallocate(ptr, n); return n >= 4 ? 0 : 1; }"),

    ("cpp23", "is_layout_compatible", "__cpp_lib_is_layout_compatible", "library",
     "std::is_layout_compatible type trait",
     "#include <type_traits>\nstruct A { int x; }; struct B { int y; };\nauto main() -> int { return std::is_layout_compatible_v<A, B> ? 0 : 1; }"),

    ("cpp23", "is_pointer_interconvertible", "__cpp_lib_is_pointer_interconvertible", "library",
     "std::is_pointer_interconvertible_with_class",
     "#include <type_traits>\nstruct S { int x; int y; };\nauto main() -> int { return std::is_pointer_interconvertible_with_class<S, int>(&S::x) ? 0 : 1; }"),
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
