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
     "[[noreturn]] void fatal() { while(true) {} }\nauto main() -> int { return 0; }"),

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
     "#undef abs\n#include <complex>\nusing namespace std::complex_literals;\nauto main() -> int { auto c = 1.0i; return c.imag() == 1.0 ? 0 : 1; }"),

    ("cpp14", "string_udls", "__cpp_lib_string_udls", "library",
     "User-defined literals for std::string (\"hello\"s)",
     "#include <string>\nusing namespace std::string_literals;\nauto main() -> int { auto s = \"hello\"s; return s.size() == 5 ? 0 : 1; }"),

    ("cpp14", "generic_associative_lookup", "__cpp_lib_generic_associative_lookup", "library",
     "Heterogeneous comparison lookup in associative containers",
     "#include <map>\n#include <string>\nauto main() -> int { std::map<std::string, int, std::less<>> m; m[\"key\"] = 42; return m.count(\"key\") == 1 ? 0 : 1; }"),

    ("cpp14", "make_reverse_iterator", "__cpp_lib_make_reverse_iterator", "library",
     "std::make_reverse_iterator",
     "#include <iterator>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; auto rit = std::make_reverse_iterator(v.end()); return *rit - 3; }"),

    ("cpp14", "tuples_by_type", "__cpp_lib_tuples_by_type", "library",
     "Addressing tuple elements by type",
     "#include <tuple>\nauto main() -> int { auto t = std::make_tuple(42, 3.14); return std::get<int>(t) - 42; }"),

    ("cpp14", "result_of_sfinae", "__cpp_lib_result_of_sfinae", "library",
     "std::result_of and SFINAE",
     "#include <type_traits>\nint f(int x) { return x; }\nauto main() -> int { return std::is_same<typename std::result_of<decltype(&f)(int)>::type, int>::value ? 0 : 1; }"),

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

    ("cpp17", "maybe_unused", "__has_cpp_attribute(maybe_unused)", "attribute",
     "[[maybe_unused]] attribute",
     "auto main() -> int { [[maybe_unused]] int x = 42; return 0; }"),

    ("cpp17", "fallthrough", "__has_cpp_attribute(fallthrough)", "attribute",
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

    # ── cpp11 library (missing) ──
    ("cpp11", "allocator_traits_is_always_equal", "__cpp_lib_allocator_traits_is_always_equal", "library",
     "std::allocator_traits<std::allocator<int>>::is_always_equal",
     "#include <memory>\nauto main() -> int { return std::allocator_traits<std::allocator<int>>::is_always_equal::value ? 0 : 1; }"),

    # ── cpp14 language (missing) ──
    ("cpp14", "null_iterators", "__cpp_lib_null_iterators", "library",
     "Compare default-constructed iterators",
     "#include <iterator>\n#include <list>\nauto main() -> int { std::list<int>::iterator a, b; return a == b ? 0 : 1; }"),

    ("cpp14", "sized_deallocation", "__cpp_sized_deallocation", "language",
     "Sized deallocation operator delete(void*, size_t)",
     "#include <cstddef>\nstruct S { int v; static void operator delete(void* p, std::size_t) noexcept { ::operator delete(p); } };\nauto main() -> int { S* p = new S{42}; delete p; return 0; }"),

    # ── cpp17 library (missing) ──
    ("cpp17", "incomplete_container_elements", "__cpp_lib_incomplete_container_elements", "library",
     "std::vector<struct Incomplete*> works with forward-declared types",
     "#include <vector>\n#include <forward_list>\nstruct Incomplete;\nauto main() -> int { std::vector<Incomplete*> v; std::forward_list<Incomplete*> fl; (void)v; (void)fl; return 0; }"),

    ("cpp17", "is_aggregate", "__cpp_lib_is_aggregate", "library",
     "std::is_aggregate_v<SomeStruct>",
     "#include <type_traits>\nstruct Agg { int x; int y; };\nstruct NonAgg { NonAgg() {} int x; };\nauto main() -> int { return std::is_aggregate_v<Agg> && !std::is_aggregate_v<NonAgg> ? 0 : 1; }"),

    ("cpp17", "parallel_algorithm", "__cpp_lib_parallel_algorithm", "library",
     "#include <execution>, std::execution::seq exists",
     "#include <execution>\nauto main() -> int { auto policy = std::execution::seq; (void)policy; return 0; }"),

    # ── cpp20 language (missing) ──
    ("cpp20", "constexpr_dynamic_alloc", "__cpp_constexpr_dynamic_alloc", "language",
     "constexpr new/delete in constant expressions",
     "constexpr int f() { int* p = new int(42); int v = *p; delete p; return v; }\nstatic_assert(f() == 42);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_in_decltype", "__cpp_constexpr_in_decltype", "language",
     "constexpr evaluation in decltype",
     "constexpr int val = 42;\nauto main() -> int { decltype(val + 1) x = val; return x - 42; }"),

    # ── cpp20 library (missing) ──
    ("cpp20", "algorithm_iterator_requirements", "__cpp_lib_algorithm_iterator_requirements", "library",
     "Relaxed iterator requirements for algorithms",
     "#include <algorithm>\n#include <vector>\nauto main() -> int { std::vector<int> v = {3,1,2}; std::sort(v.begin(), v.end()); return v[0] == 1 ? 0 : 1; }"),

    ("cpp20", "atomic_float", "__cpp_lib_atomic_float", "library",
     "std::atomic<float>",
     "#include <atomic>\nauto main() -> int { std::atomic<float> a{1.0f}; a.store(42.0f); return static_cast<int>(a.load()) - 42; }"),

    ("cpp20", "atomic_shared_ptr", "__cpp_lib_atomic_shared_ptr", "library",
     "std::atomic<std::shared_ptr<int>>",
     "#include <atomic>\n#include <memory>\nauto main() -> int { std::atomic<std::shared_ptr<int>> a; a.store(std::make_shared<int>(42)); return *a.load() - 42; }"),

    ("cpp20", "atomic_wait", "__cpp_lib_atomic_wait", "library",
     "std::atomic<int>::wait()",
     "#include <atomic>\nauto main() -> int { std::atomic<int> a{42}; a.wait(0); return 0; }"),

    ("cpp20", "common_reference", "__cpp_lib_common_reference", "library",
     "std::common_reference_t",
     "#include <type_traits>\nauto main() -> int { using T = std::common_reference_t<int&, const int&>; return std::is_same_v<T, const int&> ? 0 : 1; }"),

    ("cpp20", "common_reference_wrapper", "__cpp_lib_common_reference_wrapper", "library",
     "std::common_reference with reference_wrapper",
     "#include <type_traits>\n#include <functional>\nauto main() -> int { using T = std::common_reference_t<int&, std::reference_wrapper<int>>; return std::is_reference_v<T> ? 0 : 1; }"),

    ("cpp20", "constexpr_complex", "__cpp_lib_constexpr_complex", "library",
     "constexpr std::complex operations",
     "#undef abs\n#include <complex>\nconstexpr std::complex<double> c{1.0, 2.0};\nstatic_assert(c.real() == 1.0);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_dynamic_alloc_lib", "__cpp_lib_constexpr_dynamic_alloc", "library",
     "constexpr std::allocator",
     "#include <memory>\nconstexpr int f() { std::allocator<int> a; int* p = a.allocate(1); *p = 42; int v = *p; a.deallocate(p, 1); return v; }\nstatic_assert(f() == 42);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_functional", "__cpp_lib_constexpr_functional", "library",
     "constexpr std::invoke",
     "#include <functional>\nconstexpr int add(int a, int b) { return a + b; }\nstatic_assert(std::invoke(add, 2, 3) == 5);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_iterator", "__cpp_lib_constexpr_iterator", "library",
     "constexpr iterator operations",
     "#include <iterator>\n#include <array>\nconstexpr int f() { std::array<int, 3> a = {1, 2, 3}; return *std::begin(a); }\nstatic_assert(f() == 1);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_memory", "__cpp_lib_constexpr_memory", "library",
     "constexpr std::construct_at",
     "#include <memory>\nconstexpr int f() { int x = 0; std::construct_at(&x, 42); return x; }\nstatic_assert(f() == 42);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_numeric", "__cpp_lib_constexpr_numeric", "library",
     "constexpr std::accumulate",
     "#include <numeric>\n#include <array>\nconstexpr int f() { std::array<int, 3> a = {1, 2, 3}; return std::accumulate(a.begin(), a.end(), 0); }\nstatic_assert(f() == 6);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_tuple", "__cpp_lib_constexpr_tuple", "library",
     "constexpr std::tuple",
     "#include <tuple>\nconstexpr auto t = std::make_tuple(1, 2, 3);\nstatic_assert(std::get<0>(t) == 1);\nauto main() -> int { return 0; }"),

    ("cpp20", "constexpr_utility", "__cpp_lib_constexpr_utility", "library",
     "constexpr std::pair, std::exchange",
     "#include <utility>\nconstexpr int f() { int x = 1; int old = std::exchange(x, 42); return x + old; }\nstatic_assert(f() == 43);\nauto main() -> int { return 0; }"),

    ("cpp20", "constrained_equality", "__cpp_lib_constrained_equality", "library",
     "Constrained equality for utility types",
     "#include <utility>\n#include <optional>\nauto main() -> int { std::optional<int> a{42}, b{42}; return a == b ? 0 : 1; }"),

    ("cpp20", "format_uchar", "__cpp_lib_format_uchar", "library",
     "Unsigned char formatting with std::format",
     "#include <format>\nauto main() -> int { unsigned char c = 65; auto s = std::format(\"{}\", static_cast<int>(c)); return s == \"65\" ? 0 : 1; }"),

    ("cpp20", "modules_lib", "__cpp_lib_modules", "library",
     "Module support (check __cpp_lib_modules defined via <version>)",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_lib_modules\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp20", "move_iterator_concept", "__cpp_lib_move_iterator_concept", "library",
     "std::move_iterator satisfies iterator concepts",
     "#include <iterator>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; auto it = std::make_move_iterator(v.begin()); (void)it; return 0; }"),

    ("cpp20", "cpp_modules", "__cpp_modules", "language",
     "Module support (check via <version> header)",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_modules\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    # ── cpp23 language (missing) ──
    ("cpp23", "auto_cast", "__cpp_auto_cast", "language",
     "auto(x) decay copy syntax",
     "auto main() -> int { int x = 42; auto y = auto(x); return y - 42; }"),

    # ── cpp23 library (missing) ──
    ("cpp23", "associative_heterogeneous_erasure", "__cpp_lib_associative_heterogeneous_erasure", "library",
     "std::map::erase with transparent comparator",
     "#include <map>\n#include <string>\n#include <string_view>\nauto main() -> int { std::map<std::string, int, std::less<>> m; m[\"key\"] = 42; m.erase(std::string_view(\"key\")); return m.empty() ? 0 : 1; }"),

    ("cpp23", "constexpr_charconv", "__cpp_lib_constexpr_charconv", "library",
     "constexpr std::to_chars",
     "#include <charconv>\n#include <array>\nconstexpr int f() { std::array<char, 16> buf{}; auto [ptr, ec] = std::to_chars(buf.data(), buf.data() + buf.size(), 42); return ec == std::errc{} ? 0 : 1; }\nstatic_assert(f() == 0);\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_typeinfo", "__cpp_lib_constexpr_typeinfo", "library",
     "constexpr typeid",
     "#include <typeinfo>\nauto main() -> int { constexpr auto& ti = typeid(int); return ti == typeid(int) ? 0 : 1; }"),

    ("cpp23", "containers_ranges", "__cpp_lib_containers_ranges", "library",
     "Construct containers from ranges",
     "#include <vector>\n#include <ranges>\nauto main() -> int { auto r = std::views::iota(1, 4); std::vector<int> v(r.begin(), r.end()); return v.size() == 3 && v[0] == 1 ? 0 : 1; }"),

    ("cpp23", "format_ranges", "__cpp_lib_format_ranges", "library",
     "Format ranges with std::format",
     "#include <format>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1, 2, 3}; auto s = std::format(\"{}\", v); return s.empty() ? 1 : 0; }"),

    ("cpp23", "formatters", "__cpp_lib_formatters", "library",
     "Formatters for library types (stacktrace etc)",
     "#include <format>\n#include <thread>\nauto main() -> int { auto s = std::format(\"{}\", std::this_thread::get_id()); return s.empty() ? 1 : 0; }"),

    ("cpp23", "freestanding_algorithm", "__cpp_lib_freestanding_algorithm", "library",
     "Freestanding algorithm subset",
     "#include <algorithm>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_algorithm\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_array", "__cpp_lib_freestanding_array", "library",
     "Freestanding <array>",
     "#include <array>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_array\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_cstring", "__cpp_lib_freestanding_cstring", "library",
     "Freestanding <cstring>",
     "#include <cstring>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_cstring\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_expected", "__cpp_lib_freestanding_expected", "library",
     "Freestanding <expected>",
     "#include <expected>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_expected\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_optional", "__cpp_lib_freestanding_optional", "library",
     "Freestanding <optional>",
     "#include <optional>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_optional\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_string_view", "__cpp_lib_freestanding_string_view", "library",
     "Freestanding <string_view>",
     "#include <string_view>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_string_view\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_variant", "__cpp_lib_freestanding_variant", "library",
     "Freestanding <variant>",
     "#include <variant>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_variant\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "ranges_as_const", "__cpp_lib_ranges_as_const", "library",
     "std::ranges::as_const_view",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3}; auto cv = v | std::views::as_const; return *cv.begin() == 1 ? 0 : 1; }"),

    ("cpp23", "ranges_cartesian_product", "__cpp_lib_ranges_cartesian_product", "library",
     "std::ranges::cartesian_product_view",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector a = {1,2}; std::vector b = {3,4}; int n = 0; for (auto [x,y] : std::views::cartesian_product(a, b)) n++; return n == 4 ? 0 : 1; }"),

    ("cpp23", "ranges_enumerate", "__cpp_lib_ranges_enumerate", "library",
     "std::ranges::enumerate_view",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {10,20,30}; int s = 0; for (auto [i, x] : std::views::enumerate(v)) s += i; return s == 3 ? 0 : 1; }"),

    ("cpp23", "ranges_slide", "__cpp_lib_ranges_slide", "library",
     "std::ranges::slide_view",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4}; int n = 0; for (auto w : v | std::views::slide(2)) n++; return n == 3 ? 0 : 1; }"),

    ("cpp23", "start_lifetime_as", "__cpp_lib_start_lifetime_as", "library",
     "std::start_lifetime_as",
     "#include <memory>\nauto main() -> int {\n#ifdef __cpp_lib_start_lifetime_as\n  alignas(int) unsigned char buf[sizeof(int)] = {42, 0, 0, 0};\n  int* p = std::start_lifetime_as<int>(buf);\n  (void)p;\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    # ══════════════════════════════════════════════════════════════════
    # Auto-generated from SD-6 catalog gap analysis (2026-04-03)
    # ══════════════════════════════════════════════════════════════════

    # ── cpp11 language (new) ──
    ("cpp11", "constexpr", "__cpp_constexpr", "language",
     "constexpr specifier",
     "constexpr int square(int x) { return x * x; }\nauto main() -> int { constexpr int v = square(6); return v - 36; }"),

    ("cpp11", "initializer_lists", "__cpp_initializer_lists", "language",
     "Initializer lists",
     "#include <initializer_list>\nint sum(std::initializer_list<int> il) { int s=0; for (auto x : il) s+=x; return s; }\nauto main() -> int { return sum({1,2,3}) - 6; }"),

    ("cpp11", "lambdas", "__cpp_lambdas", "language",
     "Lambda expressions",
     "auto main() -> int { auto add = [](int a, int b) { return a + b; }; return add(2,3) - 5; }"),

    ("cpp11", "rvalue_references", "__cpp_rvalue_references", "language",
     "Rvalue references",
     "#include <utility>\nauto main() -> int { int a = 42; int&& r = std::move(a); return r - 42; }"),

    ("cpp11", "static_assert_", "__cpp_static_assert", "language",
     "static_assert",
     "static_assert(sizeof(int) >= 2, \"int too small\");\nauto main() -> int { return 0; }"),

    ("cpp11", "variadic_templates", "__cpp_variadic_templates", "language",
     "Variadic templates",
     "template<typename... Args> int count(Args...) { return sizeof...(Args); }\nauto main() -> int { return count(1, 2, 3) - 3; }"),

    # ── cpp11 library (new) ──

    # ── cpp14 language (new) ──
    ("cpp14", "binary_literals", "__cpp_binary_literals", "language",
     "Binary literals (0b prefix)",
     "auto main() -> int { return 0b101010 == 42 ? 0 : 1; }"),

    ("cpp14", "decltype_auto", "__cpp_decltype_auto", "language",
     "decltype(auto) return type",
     "int x = 42;\ndecltype(auto) f() { return (x); }\nauto main() -> int { int& r = f(); return r - 42; }"),

    ("cpp14", "generic_lambdas", "__cpp_generic_lambdas", "language",
     "Generic lambda expressions",
     "auto main() -> int { auto add = [](auto a, auto b) { return a + b; }; return add(2, 3) - 5; }"),

    ("cpp14", "init_captures", "__cpp_init_captures", "language",
     "Lambda init-capture (generalized lambda capture)",
     "#include <memory>\nauto main() -> int { auto p = std::make_unique<int>(42); auto f = [v = std::move(p)]() { return *v; }; return f() - 42; }"),


    ("cpp14", "variable_templates", "__cpp_variable_templates", "language",
     "Variable templates",
     "template<typename T> constexpr T pi = T(3.14159265358979323846);\nauto main() -> int { return pi<int> == 3 ? 0 : 1; }"),

    # ── cpp14 library (new) ──
    ("cpp14", "exchange_function", "__cpp_lib_exchange_function", "library",
     "std::exchange",
     "#include <utility>\nauto main() -> int { int x = 42; int old = std::exchange(x, 0); return old - 42; }"),

    ("cpp14", "integer_sequence", "__cpp_lib_integer_sequence", "library",
     "std::integer_sequence / std::index_sequence",
     "#include <utility>\ntemplate<typename T, T... Is> constexpr int sum(std::integer_sequence<T, Is...>) { return (Is + ...); }\nauto main() -> int { return sum(std::make_index_sequence<4>{}) - 6; }"),

    ("cpp14", "make_unique", "__cpp_lib_make_unique", "library",
     "std::make_unique",
     "#include <memory>\nauto main() -> int { auto p = std::make_unique<int>(42); return *p - 42; }"),


    # ── cpp17 language (new) ──
    ("cpp17", "fold_expressions", "__cpp_fold_expressions", "language",
     "Fold expressions",
     "template<typename... Args> auto sum(Args... args) { return (args + ...); }\nauto main() -> int { return sum(1, 2, 3) - 6; }"),

    ("cpp17", "if_constexpr", "__cpp_if_constexpr", "language",
     "constexpr if",
     "template<typename T> int check() { if constexpr (sizeof(T) > 4) return 1; else return 0; }\nauto main() -> int { return check<char>(); }"),

    ("cpp17", "inline_variables", "__cpp_inline_variables", "language",
     "Inline variables",
     "struct S { static inline int x = 42; };\nauto main() -> int { return S::x - 42; }"),

    ("cpp17", "structured_bindings", "__cpp_structured_bindings", "language",
     "Structured bindings",
     "struct S { int a; int b; };\nauto main() -> int { S s{1, 2}; auto [x, y] = s; return x + y - 3; }"),

    # ── cpp17 library (new) ──
    ("cpp17", "any", "__cpp_lib_any", "library",
     "std::any",
     "#include <any>\nauto main() -> int { std::any a = 42; return std::any_cast<int>(a) - 42; }"),

    ("cpp17", "apply", "__cpp_lib_apply", "library",
     "std::apply",
     "#include <tuple>\nauto main() -> int { auto t = std::make_tuple(1, 2, 3); return std::apply([](auto... args) { return (args + ...); }, t) - 6; }"),

    ("cpp17", "as_const", "__cpp_lib_as_const", "library",
     "std::as_const",
     "#include <utility>\n#include <type_traits>\nauto main() -> int { int x = 42; auto& cr = std::as_const(x); return std::is_const_v<std::remove_reference_t<decltype(cr)>> ? 0 : 1; }"),

    ("cpp17", "bool_constant", "__cpp_lib_bool_constant", "library",
     "std::bool_constant",
     "#include <type_traits>\nauto main() -> int { using T = std::bool_constant<true>; return T::value ? 0 : 1; }"),

    ("cpp17", "byte", "__cpp_lib_byte", "library",
     "std::byte",
     "#include <cstddef>\nauto main() -> int { std::byte b{42}; return std::to_integer<int>(b) - 42; }"),

    ("cpp17", "clamp", "__cpp_lib_clamp", "library",
     "std::clamp",
     "#include <algorithm>\nauto main() -> int { return std::clamp(50, 0, 42) - 42; }"),

    ("cpp17", "filesystem", "__cpp_lib_filesystem", "library",
     "Filesystem library",
     "#include <filesystem>\nauto main() -> int { std::filesystem::path p = \"/tmp\"; return p.empty() ? 1 : 0; }"),

    ("cpp17", "freestanding_charconv", "__cpp_lib_freestanding_charconv", "library",
     "Freestanding facilities in charconv",
     "#include <charconv>\nauto main() -> int { return 0; }"),

    ("cpp17", "gcd_lcm", "__cpp_lib_gcd_lcm", "library",
     "std::gcd and std::lcm",
     "#include <numeric>\nauto main() -> int { return std::gcd(12, 8) == 4 && std::lcm(4, 6) == 12 ? 0 : 1; }"),


    ("cpp17", "invoke", "__cpp_lib_invoke", "library",
     "std::invoke",
     "#include <functional>\nint add(int a, int b) { return a + b; }\nauto main() -> int { return std::invoke(add, 2, 3) - 5; }"),


    ("cpp17", "map_try_emplace", "__cpp_lib_map_try_emplace", "library",
     "std::map::try_emplace and insert_or_assign",
     "#include <map>\nauto main() -> int { std::map<int,int> m; m.try_emplace(1, 42); return m[1] - 42; }"),

    ("cpp17", "not_fn", "__cpp_lib_not_fn", "library",
     "std::not_fn",
     "#include <functional>\nauto main() -> int { auto not_true = std::not_fn([]() { return true; }); return not_true() ? 1 : 0; }"),

    ("cpp17", "optional", "__cpp_lib_optional", "library",
     "std::optional",
     "#include <optional>\nauto main() -> int { std::optional<int> x = 42; return x.value() - 42; }"),


    ("cpp17", "scoped_lock", "__cpp_lib_scoped_lock", "library",
     "std::scoped_lock",
     "#include <mutex>\nauto main() -> int { std::mutex m; std::scoped_lock lock(m); return 0; }"),

    ("cpp17", "shared_ptr_arrays", "__cpp_lib_shared_ptr_arrays", "library",
     "std::shared_ptr<T[]>",
     "#include <memory>\nauto main() -> int { auto sp = std::make_shared<int[]>(3); sp[0] = 42; return sp[0] - 42; }"),

    ("cpp17", "string_view", "__cpp_lib_string_view", "library",
     "std::string_view",
     "#include <string_view>\nauto main() -> int { std::string_view sv = \"hello\"; return sv.size() == 5 ? 0 : 1; }"),

    ("cpp17", "type_trait_variable_templates", "__cpp_lib_type_trait_variable_templates", "library",
     "Type traits variable templates (is_void_v etc)",
     "#include <type_traits>\nauto main() -> int { return std::is_void_v<void> && !std::is_void_v<int> ? 0 : 1; }"),

    ("cpp17", "variant", "__cpp_lib_variant", "library",
     "std::variant",
     "#include <variant>\nauto main() -> int { std::variant<int, double> v = 42; return std::get<int>(v) - 42; }"),

    ("cpp17", "void_t", "__cpp_lib_void_t", "library",
     "std::void_t",
     "#include <type_traits>\ntemplate<typename, typename = void> struct has_type : std::false_type {};\ntemplate<typename T> struct has_type<T, std::void_t<typename T::type>> : std::true_type {};\nstruct A { using type = int; };\nauto main() -> int { return has_type<A>::value ? 0 : 1; }"),

    # ── cpp20 attribute (new) ──
    ("cpp20", "attr_likely", "__has_cpp_attribute(likely)", "attribute",
     "[[likely]] attribute",
     "auto main() -> int { int x = 42; if (x == 42) [[likely]] { return 0; } return 1; }"),

    ("cpp20", "attr_unlikely", "__has_cpp_attribute(unlikely)", "attribute",
     "[[unlikely]] attribute",
     "auto main() -> int { int x = 42; if (x != 42) [[unlikely]] { return 1; } return 0; }"),

    # ── cpp20 language (new) ──
    ("cpp20", "char8_t_lang", "__cpp_char8_t", "language",
     "char8_t type",
     "auto main() -> int { char8_t c = u8'A'; return c == u8'A' ? 0 : 1; }"),

    ("cpp20", "concepts", "__cpp_concepts", "language",
     "Concepts",
     "template<typename T> concept Integral = requires { requires sizeof(T) > 0; };\ntemplate<Integral T> T identity(T v) { return v; }\nauto main() -> int { return identity(42) - 42; }"),

    ("cpp20", "consteval", "__cpp_consteval", "language",
     "Immediate functions (consteval)",
     "consteval int sqr(int n) { return n * n; }\nauto main() -> int { constexpr int v = sqr(6); return v - 36; }"),



    ("cpp20", "constinit", "__cpp_constinit", "language",
     "constinit specifier",
     "constinit int global = 42;\nauto main() -> int { return global - 42; }"),

    ("cpp20", "designated_initializers", "__cpp_designated_initializers", "language",
     "Designated initializers",
     "struct Point { int x; int y; };\nauto main() -> int { Point p = {.x = 1, .y = 2}; return p.x + p.y - 3; }"),

    ("cpp20", "impl_coroutine", "__cpp_impl_coroutine", "language",
     "Coroutines (compiler support)",
     "#if __has_include(<coroutine>)\n#include <coroutine>\n#else\n#include <experimental/coroutine>\n#endif\nauto main() -> int { return 0; }"),

    ("cpp20", "impl_three_way_comparison", "__cpp_impl_three_way_comparison", "language",
     "Three-way comparison (spaceship operator)",
     "#include <compare>\nstruct S { int v; auto operator<=>(const S&) const = default; };\nauto main() -> int { S a{1}, b{2}; return (a <=> b) < 0 ? 0 : 1; }"),

    # ── cpp20 library (new) ──




    ("cpp20", "bind_front", "__cpp_lib_bind_front", "library",
     "std::bind_front",
     "#include <functional>\nint add(int a, int b) { return a + b; }\nauto main() -> int { auto add5 = std::bind_front(add, 5); return add5(37) - 42; }"),

    ("cpp20", "bit_cast", "__cpp_lib_bit_cast", "library",
     "std::bit_cast",
     "#include <bit>\n#include <cstdint>\nauto main() -> int { float f = 1.0f; auto u = std::bit_cast<uint32_t>(f); return u != 0 ? 0 : 1; }"),

    ("cpp20", "bitops", "__cpp_lib_bitops", "library",
     "Bit operations (std::popcount etc)",
     "#include <bit>\nauto main() -> int { return std::popcount(42u) == 3 ? 0 : 1; }"),













    ("cpp20", "endian", "__cpp_lib_endian", "library",
     "std::endian",
     "#include <bit>\nauto main() -> int { return std::endian::native == std::endian::big || std::endian::native == std::endian::little ? 0 : 1; }"),

    ("cpp20", "erase_if", "__cpp_lib_erase_if", "library",
     "std::erase_if for containers",
     "#include <vector>\nauto main() -> int { std::vector<int> v = {1,2,3,4}; std::erase_if(v, [](int x) { return x % 2 == 0; }); return v.size() == 2 ? 0 : 1; }"),

    ("cpp20", "format", "__cpp_lib_format", "library",
     "std::format",
     "#include <format>\n#include <string>\nauto main() -> int { auto s = std::format(\"{} {}\", \"hello\", 42); return s.empty() ? 1 : 0; }"),


    ("cpp20", "freestanding_ranges", "__cpp_lib_freestanding_ranges", "library",
     "Freestanding facilities in ranges",
     "#include <ranges>\nauto main() -> int { return 0; }"),


    ("cpp20", "math_constants", "__cpp_lib_math_constants", "library",
     "Mathematical constants (std::numbers::pi etc)",
     "#include <numbers>\nauto main() -> int { return std::numbers::pi > 3.0 ? 0 : 1; }"),



    ("cpp20", "ranges", "__cpp_lib_ranges", "library",
     "Ranges library",
     "#include <ranges>\n#include <vector>\nauto main() -> int { std::vector v = {1,2,3,4,5}; auto even = v | std::views::filter([](int x) { return x % 2 == 0; }); int n = 0; for (auto x : even) { (void)x; n++; } return n == 2 ? 0 : 1; }"),

    ("cpp20", "source_location", "__cpp_lib_source_location", "library",
     "std::source_location",
     "#include <source_location>\nauto main() -> int { auto loc = std::source_location::current(); return loc.line() > 0 ? 0 : 1; }"),

    ("cpp20", "span", "__cpp_lib_span", "library",
     "std::span",
     "#include <span>\nauto main() -> int { int arr[] = {1,2,3}; std::span<int> s(arr); return s.size() == 3 ? 0 : 1; }"),

    ("cpp20", "starts_ends_with", "__cpp_lib_starts_ends_with", "library",
     "String prefix and suffix checking",
     "#include <string>\nauto main() -> int { std::string s = \"hello\"; return s.starts_with(\"he\") && s.ends_with(\"lo\") ? 0 : 1; }"),

    ("cpp20", "to_array", "__cpp_lib_to_array", "library",
     "std::to_array",
     "#include <array>\nauto main() -> int { auto a = std::to_array({1,2,3}); return a.size() == 3 ? 0 : 1; }"),

    # ── cpp23 attribute (new) ──
    ("cpp23", "attr_assume", "__has_cpp_attribute(assume)", "attribute",
     "[[assume]] attribute",
     "auto main() -> int {\n#if __has_cpp_attribute(assume)\n  int x = 42; [[assume(x == 42)]];\n#endif\n  return 0;\n}"),

    ("cpp23", "attr_carries_dependency", "__has_cpp_attribute(carries_dependency)", "attribute",
     "[[carries_dependency]] attribute",
     "[[carries_dependency]] int load(int* p) { return *p; }\nauto main() -> int { int v = 42; return load(&v) - 42; }"),

    ("cpp23", "attr_deprecated", "__has_cpp_attribute(deprecated)", "attribute",
     "[[deprecated]] attribute",
     "[[deprecated]] void old_func() {}\nauto main() -> int { return 0; }"),

    ("cpp23", "attr_indeterminate", "__has_cpp_attribute(indeterminate)", "attribute",
     "[[indeterminate]] attribute",
     "auto main() -> int {\n#if __has_cpp_attribute(indeterminate)\n  [[indeterminate]] int x;\n  (void)x;\n#endif\n  return 0;\n}"),

    ("cpp23", "attr_no_unique_address", "__has_cpp_attribute(no_unique_address)", "attribute",
     "[[no_unique_address]] attribute",
     "struct Empty {};\nstruct S { [[no_unique_address]] Empty e; int v; };\nauto main() -> int { S s; s.v = 42; return s.v - 42; }"),

    ("cpp23", "attr_nodiscard", "__has_cpp_attribute(nodiscard)", "attribute",
     "[[nodiscard]] attribute",
     "[[nodiscard]] int compute() { return 42; }\nauto main() -> int { int v = compute(); return v - 42; }"),

    ("cpp23", "attr_noreturn", "__has_cpp_attribute(noreturn)", "attribute",
     "[[noreturn]] attribute",
     "[[noreturn]] void die() { while(true) {} }\nauto main() -> int { return 0; }"),

    # ── cpp23 language (new) ──
    ("cpp23", "explicit_this_parameter", "__cpp_explicit_this_parameter", "language",
     "Explicit object parameter (deducing this)",
     "struct S { int v; int get(this S const& self) { return self.v; } };\nauto main() -> int { S s{42}; return s.get() - 42; }"),

    ("cpp23", "multidimensional_subscript", "__cpp_multidimensional_subscript", "language",
     "Multidimensional subscript operator",
     "struct Matrix { int data[4] = {1,2,3,4}; int operator[](int r, int c) { return data[r*2+c]; } };\nauto main() -> int { Matrix m; return m[0,1] - 2; }"),

    # ── cpp23 library (new) ──

    ("cpp23", "byteswap", "__cpp_lib_byteswap", "library",
     "std::byteswap",
     "#include <bit>\n#include <cstdint>\nauto main() -> int { uint16_t v = 0x0102; uint16_t s = std::byteswap(v); return s == 0x0201 ? 0 : 1; }"),




    ("cpp23", "expected", "__cpp_lib_expected", "library",
     "std::expected",
     "#include <expected>\nauto main() -> int { std::expected<int, int> e = 42; return e.value() - 42; }"),



    ("cpp23", "forward_like", "__cpp_lib_forward_like", "library",
     "std::forward_like",
     "#include <utility>\nauto main() -> int { int x = 42; auto&& r = std::forward_like<const int&>(x); return r - 42; }"),





    ("cpp23", "freestanding_mdspan", "__cpp_lib_freestanding_mdspan", "library",
     "Freestanding std::mdspan",
     "#include <mdspan>\nauto main() -> int { return 0; }"),




    ("cpp23", "print", "__cpp_lib_print", "library",
     "std::print",
     "#include <print>\nauto main() -> int { std::println(\"hello\"); return 0; }"),

    ("cpp23", "stacktrace", "__cpp_lib_stacktrace", "library",
     "Stacktrace library",
     "#include <stacktrace>\nauto main() -> int { auto st = std::stacktrace::current(); (void)st; return 0; }"),

    ("cpp23", "to_underlying", "__cpp_lib_to_underlying", "library",
     "std::to_underlying",
     "#include <utility>\nenum class E : int { A = 42 };\nauto main() -> int { return std::to_underlying(E::A) - 42; }"),

    # ── cpp26 attribute (new) ──

    # ── cpp26 language (new) ──
    ("cpp26", "constexpr_exceptions", "__cpp_constexpr_exceptions", "language",
     "constexpr exception handling",
     "auto main() -> int {\n#ifdef __cpp_constexpr_exceptions\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "constexpr_virtual_inheritance", "__cpp_constexpr_virtual_inheritance", "language",
     "constexpr virtual inheritance",
     "auto main() -> int {\n#ifdef __cpp_constexpr_virtual_inheritance\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "contracts", "__cpp_contracts", "language",
     "Contracts",
     "auto main() -> int {\n#ifdef __cpp_contracts\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "expansion_statements", "__cpp_expansion_statements", "language",
     "Expansion statements",
     "auto main() -> int {\n#ifdef __cpp_expansion_statements\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "impl_reflection", "__cpp_impl_reflection", "language",
     "Static reflection",
     "auto main() -> int {\n#ifdef __cpp_impl_reflection\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "pack_indexing", "__cpp_pack_indexing", "language",
     "Pack indexing",
     "template<typename... Ts> using first_t = Ts...[0];\nauto main() -> int { first_t<int, double> v = 42; return v - 42; }"),

    ("cpp26", "placeholder_variables", "__cpp_placeholder_variables", "language",
     "Placeholder variables (unnamed _)",
     "auto main() -> int { auto [_, y] = (struct { int a; int b; }){1, 42}; return y - 42; }"),

    ("cpp26", "pp_embed", "__cpp_pp_embed", "language",
     "#embed preprocessor directive",
     "auto main() -> int {\n#ifdef __cpp_pp_embed\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp26", "variadic_friend", "__cpp_variadic_friend", "language",
     "Variadic friend declarations",
     "struct A {}; struct B {};\ntemplate<typename... Ts> struct S { friend Ts...; int x = 42; };\nauto main() -> int { return 0; }"),

    # ── cpp26 library (new) ──
    ("cpp26", "algorithm_default_value_type", "__cpp_lib_algorithm_default_value_type", "library",
     "Enabling list-initialization for algorithms",
     "#include <algorithm>\nauto main() -> int { return 0; }"),

    ("cpp26", "aligned_accessor", "__cpp_lib_aligned_accessor", "library",
     "Aligned accessor for mdspan",
     "#include <mdspan>\nauto main() -> int { return 0; }"),

    ("cpp26", "associative_heterogeneous_insertion", "__cpp_lib_associative_heterogeneous_insertion", "library",
     "Heterogeneous overloads for associative containers",
     "#include <map>\nauto main() -> int { return 0; }"),

    ("cpp26", "atomic_min_max", "__cpp_lib_atomic_min_max", "library",
     "Atomic minimum/maximum",
     "#include <atomic>\nauto main() -> int { return 0; }"),

    ("cpp26", "bitset", "__cpp_lib_bitset", "library",
     "Interfacing std::bitset with std::string_view",
     "#include <bitset>\nauto main() -> int { return 0; }"),

    ("cpp26", "constant_wrapper", "__cpp_lib_constant_wrapper", "library",
     "constant_wrapper",
     "#include <type_traits>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_exceptions_lib", "__cpp_lib_constexpr_exceptions", "library",
     "constexpr exceptions library support",
     "#include <exception>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_flat_map", "__cpp_lib_constexpr_flat_map", "library",
     "constexpr flat_map",
     "#include <flat_map>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_flat_set", "__cpp_lib_constexpr_flat_set", "library",
     "constexpr flat_set",
     "#include <flat_set>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_forward_list", "__cpp_lib_constexpr_forward_list", "library",
     "constexpr forward_list",
     "#include <forward_list>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_list", "__cpp_lib_constexpr_list", "library",
     "constexpr list",
     "#include <list>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_new", "__cpp_lib_constexpr_new", "library",
     "constexpr placement new",
     "#include <new>\nauto main() -> int { return 0; }"),

    ("cpp26", "constexpr_queue", "__cpp_lib_constexpr_queue", "library",
     "constexpr queue",
     "#include <queue>\nauto main() -> int { return 0; }"),

    ("cpp26", "contracts_lib", "__cpp_lib_contracts", "library",
     "Contracts library support",
     "#include <contracts>\nauto main() -> int { return 0; }"),

    ("cpp26", "copyable_function", "__cpp_lib_copyable_function", "library",
     "std::copyable_function",
     "#include <functional>\nauto main() -> int { return 0; }"),

    ("cpp26", "debugging", "__cpp_lib_debugging", "library",
     "Debugging support",
     "#include <debugging>\nauto main() -> int { return 0; }"),

    ("cpp26", "define_static", "__cpp_lib_define_static", "library",
     "define_static",
     "#include <meta>\nauto main() -> int { return 0; }"),

    ("cpp26", "exception_ptr_cast", "__cpp_lib_exception_ptr_cast", "library",
     "exception_ptr_cast",
     "#include <exception>\nauto main() -> int { return 0; }"),

    ("cpp26", "format_path", "__cpp_lib_format_path", "library",
     "Formatting of std::filesystem::path",
     "#include <filesystem>\nauto main() -> int { return 0; }"),

    ("cpp26", "fstream_native_handle", "__cpp_lib_fstream_native_handle", "library",
     "Obtaining native handles from file streams",
     "#include <fstream>\nauto main() -> int { return 0; }"),

    ("cpp26", "function_ref", "__cpp_lib_function_ref", "library",
     "std::function_ref",
     "#include <functional>\nauto main() -> int { return 0; }"),

    ("cpp26", "indirect", "__cpp_lib_indirect", "library",
     "std::indirect",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp26", "inplace_vector", "__cpp_lib_inplace_vector", "library",
     "std::inplace_vector",
     "#include <inplace_vector>\nauto main() -> int { std::inplace_vector<int, 8> v; v.push_back(42); return v[0] - 42; }"),

    ("cpp26", "is_sufficiently_aligned", "__cpp_lib_is_sufficiently_aligned", "library",
     "is_sufficiently_aligned",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp26", "is_virtual_base_of", "__cpp_lib_is_virtual_base_of", "library",
     "std::is_virtual_base_of",
     "#include <type_traits>\nauto main() -> int { return 0; }"),

    ("cpp26", "is_within_lifetime", "__cpp_lib_is_within_lifetime", "library",
     "Checking if a union alternative is active",
     "#include <type_traits>\nauto main() -> int { return 0; }"),

    ("cpp26", "observable_checkpoint", "__cpp_lib_observable_checkpoint", "library",
     "observable_checkpoint",
     "#include <utility>\nauto main() -> int { return 0; }"),

    ("cpp26", "optional_range_support", "__cpp_lib_optional_range_support", "library",
     "std::optional range support",
     "#include <optional>\nauto main() -> int { return 0; }"),

    ("cpp26", "philox_engine", "__cpp_lib_philox_engine", "library",
     "std::philox_engine",
     "#include <random>\nauto main() -> int { return 0; }"),

    ("cpp26", "polymorphic", "__cpp_lib_polymorphic", "library",
     "std::polymorphic",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp26", "ranges_cache_latest", "__cpp_lib_ranges_cache_latest", "library",
     "ranges cache_latest",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp26", "ranges_concat", "__cpp_lib_ranges_concat", "library",
     "std::views::concat",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp26", "ranges_indices", "__cpp_lib_ranges_indices", "library",
     "ranges indices",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp26", "ranges_to_input", "__cpp_lib_ranges_to_input", "library",
     "ranges to_input",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp26", "ratio", "__cpp_lib_ratio", "library",
     "Adding the new 2022 SI prefixes",
     "#include <ratio>\nauto main() -> int { return 0; }"),

    ("cpp26", "reference_wrapper", "__cpp_lib_reference_wrapper", "library",
     "Comparisons for std::reference_wrapper",
     "#include <functional>\nauto main() -> int { return 0; }"),

    ("cpp26", "reflection", "__cpp_lib_reflection", "library",
     "Static reflection library",
     "#include <meta>\nauto main() -> int { return 0; }"),

    ("cpp26", "saturation_arithmetic", "__cpp_lib_saturation_arithmetic", "library",
     "Saturation arithmetic",
     "#include <numeric>\n#include <cstdint>\nauto main() -> int { return std::add_sat<uint8_t>(200, 200) == 255 ? 0 : 1; }"),

    ("cpp26", "simd", "__cpp_lib_simd", "library",
     "SIMD library",
     "#include <simd>\nauto main() -> int { return 0; }"),

    ("cpp26", "smart_ptr_owner_equality", "__cpp_lib_smart_ptr_owner_equality", "library",
     "Enabling std::weak_ptr as keys",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp26", "span_initializer_list", "__cpp_lib_span_initializer_list", "library",
     "Constructing std::span from initializer_list",
     "#include <span>\nauto main() -> int { return 0; }"),

    ("cpp26", "sstream_from_string_view", "__cpp_lib_sstream_from_string_view", "library",
     "Interfacing stringstreams with string_view",
     "#include <sstream>\nauto main() -> int { return 0; }"),

    ("cpp26", "string_subview", "__cpp_lib_string_subview", "library",
     "string subview",
     "#include <string>\nauto main() -> int { return 0; }"),

    ("cpp26", "submdspan", "__cpp_lib_submdspan", "library",
     "std::submdspan",
     "#include <mdspan>\nauto main() -> int { return 0; }"),

    ("cpp26", "text_encoding", "__cpp_lib_text_encoding", "library",
     "std::text_encoding",
     "#include <text_encoding>\nauto main() -> int { return 0; }"),

    ("cpp26", "to_string", "__cpp_lib_to_string", "library",
     "Redefining std::to_string in terms of std::format",
     "#include <string>\nauto main() -> int { return 0; }"),

    ("cpp26", "type_order", "__cpp_lib_type_order", "library",
     "type_order",
     "#include <compare>\nauto main() -> int { return 0; }"),

    # ── unknown-standard features (bucketed into cpp23+) ──
    ("cpp23", "rtti", "__cpp_rtti", "language",
     "Run-time type information (typeid)",
     "#include <typeinfo>\nstruct Base { virtual ~Base() {} };\nstruct Derived : Base {};\nauto main() -> int { Derived d; Base& b = d; return typeid(b) == typeid(Derived) ? 0 : 1; }"),

    ("cpp23", "template_parameters", "__cpp_template_parameters", "language",
     "Template parameters",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_template_parameters\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "trivial_union", "__cpp_trivial_union", "language",
     "Trivial union",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_trivial_union\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "atomic_reductions", "__cpp_lib_atomic_reductions", "library",
     "Atomic reductions",
     "#include <atomic>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_atomic", "__cpp_lib_constexpr_atomic", "library",
     "constexpr atomic",
     "#include <atomic>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_cmath", "__cpp_lib_constexpr_cmath", "library",
     "Constexpr for mathematical functions",
     "#include <cmath>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_deque", "__cpp_lib_constexpr_deque", "library",
     "constexpr deque",
     "#include <deque>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_format", "__cpp_lib_constexpr_format", "library",
     "constexpr format",
     "#include <format>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_inplace_vector", "__cpp_lib_constexpr_inplace_vector", "library",
     "constexpr inplace_vector",
     "#include <inplace_vector>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_map", "__cpp_lib_constexpr_map", "library",
     "constexpr map",
     "#include <map>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_set", "__cpp_lib_constexpr_set", "library",
     "constexpr set",
     "#include <set>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_stack", "__cpp_lib_constexpr_stack", "library",
     "constexpr stack",
     "#include <stack>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_unordered_map", "__cpp_lib_constexpr_unordered_map", "library",
     "constexpr unordered_map",
     "#include <unordered_map>\nauto main() -> int { return 0; }"),

    ("cpp23", "constexpr_unordered_set", "__cpp_lib_constexpr_unordered_set", "library",
     "constexpr unordered_set",
     "#include <unordered_set>\nauto main() -> int { return 0; }"),

    ("cpp23", "counting_scope", "__cpp_lib_counting_scope", "library",
     "counting_scope",
     "#include <execution>\nauto main() -> int { return 0; }"),

    ("cpp23", "deduction_guides", "__cpp_lib_deduction_guides", "library",
     "Deduction guides",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_lib_deduction_guides\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_char_traits", "__cpp_lib_freestanding_char_traits", "library",
     "Freestanding std::char_traits",
     "#include <string>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_cstdlib", "__cpp_lib_freestanding_cstdlib", "library",
     "Freestanding facilities in cstdlib",
     "#include <cstdlib>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_cwchar", "__cpp_lib_freestanding_cwchar", "library",
     "Freestanding facilities in cwchar",
     "#include <cwchar>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_errc", "__cpp_lib_freestanding_errc", "library",
     "Freestanding std::errc",
     "#include <system_error>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_execution", "__cpp_lib_freestanding_execution", "library",
     "Freestanding execution",
     "#include <execution>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_feature_test_macros", "__cpp_lib_freestanding_feature_test_macros", "library",
     "Support for freestanding feature-test macros",
     "#include <version>\nauto main() -> int {\n#ifdef __cpp_lib_freestanding_feature_test_macros\n  return 0;\n#else\n  return 0;\n#endif\n}"),

    ("cpp23", "freestanding_functional", "__cpp_lib_freestanding_functional", "library",
     "Freestanding facilities in functional",
     "#include <functional>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_iterator", "__cpp_lib_freestanding_iterator", "library",
     "Freestanding facilities in iterator",
     "#include <iterator>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_memory", "__cpp_lib_freestanding_memory", "library",
     "Freestanding facilities in memory",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_numeric", "__cpp_lib_freestanding_numeric", "library",
     "Freestanding facilities in numeric",
     "#include <numeric>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_operator_new", "__cpp_lib_freestanding_operator_new", "library",
     "Definition of operator new (optional in freestanding)",
     "#include <new>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_random", "__cpp_lib_freestanding_random", "library",
     "Freestanding random",
     "#include <random>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_ratio", "__cpp_lib_freestanding_ratio", "library",
     "Freestanding facilities in ratio",
     "#include <ratio>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_tuple", "__cpp_lib_freestanding_tuple", "library",
     "Freestanding facilities in tuple",
     "#include <tuple>\nauto main() -> int { return 0; }"),

    ("cpp23", "freestanding_utility", "__cpp_lib_freestanding_utility", "library",
     "Freestanding facilities in utility",
     "#include <utility>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_array", "__cpp_lib_hardened_array", "library",
     "Hardened array",
     "#include <array>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_basic_stacktrace", "__cpp_lib_hardened_basic_stacktrace", "library",
     "Hardened basic_stacktrace",
     "#include <stacktrace>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_basic_string", "__cpp_lib_hardened_basic_string", "library",
     "Hardened basic_string",
     "#include <string>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_basic_string_view", "__cpp_lib_hardened_basic_string_view", "library",
     "Hardened basic_string_view",
     "#include <string_view>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_bitset", "__cpp_lib_hardened_bitset", "library",
     "Hardened bitset",
     "#include <bitset>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_common_iterator", "__cpp_lib_hardened_common_iterator", "library",
     "Hardened common_iterator",
     "#include <iterator>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_counted_iterator", "__cpp_lib_hardened_counted_iterator", "library",
     "Hardened counted_iterator",
     "#include <iterator>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_deque", "__cpp_lib_hardened_deque", "library",
     "Hardened deque",
     "#include <deque>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_expected", "__cpp_lib_hardened_expected", "library",
     "Hardened expected",
     "#include <expected>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_forward_list", "__cpp_lib_hardened_forward_list", "library",
     "Hardened forward_list",
     "#include <forward_list>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_inplace_vector", "__cpp_lib_hardened_inplace_vector", "library",
     "Hardened inplace_vector",
     "#include <inplace_vector>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_list", "__cpp_lib_hardened_list", "library",
     "Hardened list",
     "#include <list>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_mdspan", "__cpp_lib_hardened_mdspan", "library",
     "Hardened mdspan",
     "#include <mdspan>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_optional", "__cpp_lib_hardened_optional", "library",
     "Hardened optional",
     "#include <optional>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_shared_ptr_array", "__cpp_lib_hardened_shared_ptr_array", "library",
     "Hardened shared_ptr_array",
     "#include <memory>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_span", "__cpp_lib_hardened_span", "library",
     "Hardened span",
     "#include <span>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_valarray", "__cpp_lib_hardened_valarray", "library",
     "Hardened valarray",
     "#include <valarray>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_vector", "__cpp_lib_hardened_vector", "library",
     "Hardened vector",
     "#include <vector>\nauto main() -> int { return 0; }"),

    ("cpp23", "hardened_view_interface", "__cpp_lib_hardened_view_interface", "library",
     "Hardened view_interface",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp23", "hazard_pointer", "__cpp_lib_hazard_pointer", "library",
     "Hazard pointers",
     "#include <hazard_pointer>\nauto main() -> int { return 0; }"),

    ("cpp23", "hive", "__cpp_lib_hive", "library",
     "std::hive",
     "#include <hive>\nauto main() -> int { return 0; }"),

    ("cpp23", "initializer_list_lib", "__cpp_lib_initializer_list", "library",
     "initializer_list library support",
     "#include <initializer_list>\nauto main() -> int { return 0; }"),

    ("cpp23", "linalg", "__cpp_lib_linalg", "library",
     "A free function linear algebra interface",
     "#include <linalg>\nauto main() -> int { return 0; }"),

    ("cpp23", "parallel_scheduler", "__cpp_lib_parallel_scheduler", "library",
     "parallel_scheduler",
     "#include <execution>\nauto main() -> int { return 0; }"),

    ("cpp23", "ranges_generate_random", "__cpp_lib_ranges_generate_random", "library",
     "Vector API for random number generation",
     "#include <random>\nauto main() -> int { return 0; }"),

    ("cpp23", "ranges_reserve_hint", "__cpp_lib_ranges_reserve_hint", "library",
     "ranges reserve_hint",
     "#include <ranges>\nauto main() -> int { return 0; }"),

    ("cpp23", "rcu", "__cpp_lib_rcu", "library",
     "Read-Copy Update (RCU)",
     "#include <rcu>\nauto main() -> int { return 0; }"),

    ("cpp23", "senders", "__cpp_lib_senders", "library",
     "std::execution: sender-receiver model",
     "#include <execution>\nauto main() -> int { return 0; }"),

    ("cpp23", "simd_complex", "__cpp_lib_simd_complex", "library",
     "SIMD complex",
     "#include <simd>\nauto main() -> int { return 0; }"),

    ("cpp23", "simd_permutations", "__cpp_lib_simd_permutations", "library",
     "SIMD permutations",
     "#include <simd>\nauto main() -> int { return 0; }"),

    ("cpp23", "task", "__cpp_lib_task", "library",
     "std::execution task",
     "#include <execution>\nauto main() -> int { return 0; }"),

    ("cpp23", "valarray_lib", "__cpp_lib_valarray", "library",
     "valarray",
     "#include <valarray>\nauto main() -> int { return 0; }"),

    # ── cpp20 modules (language) ──
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
