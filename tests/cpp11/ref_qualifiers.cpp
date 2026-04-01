// feature: ref_qualifiers
// macro: __cpp_ref_qualifiers
// standard: cpp11
// category: language
// description: Ref-qualified member functions

struct S { int f() & { return 1; } int f() && { return 2; } };
auto main() -> int { S s; return s.f() == 1 ? 0 : 1; }
