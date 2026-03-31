// feature: smart_ptr_for_overwrite
// macro: __cpp_lib_smart_ptr_for_overwrite
// standard: cpp20
// category: library
// description: std::make_unique_for_overwrite / make_shared_for_overwrite

#include <memory>
auto main() -> int { auto p = std::make_unique_for_overwrite<int>(); *p = 42; return *p - 42; }
