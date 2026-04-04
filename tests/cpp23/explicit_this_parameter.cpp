// feature: explicit_this_parameter
// macro: __cpp_explicit_this_parameter
// standard: cpp23
// category: language
// description: Explicit object parameter (deducing this)

struct S { int v; int get(this S const& self) { return self.v; } };
auto main() -> int { S s{42}; return s.get() - 42; }
