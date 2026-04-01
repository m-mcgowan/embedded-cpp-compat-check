// feature: deleted_function
// macro: __cpp_deleted_function
// standard: cpp17
// category: language
// description: Explicitly deleted functions

void f() = delete;
template<typename T> void g(T) = delete;
void g(int) {}
auto main() -> int { g(42); return 0; }
