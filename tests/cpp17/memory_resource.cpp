// feature: memory_resource
// macro: __cpp_lib_memory_resource
// standard: cpp17
// category: library
// description: Polymorphic memory resources <memory_resource>

#include <memory_resource>
auto main() -> int { auto* r = std::pmr::get_default_resource(); return r != nullptr ? 0 : 1; }
