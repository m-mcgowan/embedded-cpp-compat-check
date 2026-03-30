// feature: filesystem
// macro: __cpp_lib_filesystem
// standard: cpp17
// category: library
// description: std::filesystem
#include <filesystem>
auto main() -> int {
    std::filesystem::path p("/tmp");
    return p.empty() ? 1 : 0;
}
