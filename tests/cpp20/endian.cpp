// feature: endian
// macro: __cpp_lib_endian
// standard: cpp20
// category: library
// description: std::endian
#include <bit>
auto main() -> int {
    return (std::endian::native == std::endian::big ||
            std::endian::native == std::endian::little) ? 0 : 1;
}
