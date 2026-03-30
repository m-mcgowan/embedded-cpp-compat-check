// feature: capture_star_this
// macro: __cpp_capture_star_this
// standard: cpp17
// category: language
// description: Lambda capture of *this by value

struct S { int v=42; auto f() { return [*this]() { return v; }; } };
auto main() -> int { S s; return s.f()() - 42; }
