// feature: threadsafe_static_init
// macro: __cpp_threadsafe_static_init
// standard: cpp11
// category: language
// description: Thread-safe initialization of static local variables

int f() { static int x = 42; return x; }
auto main() -> int { return f() - 42; }
