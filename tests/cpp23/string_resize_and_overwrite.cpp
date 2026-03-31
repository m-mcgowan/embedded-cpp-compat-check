// feature: string_resize_and_overwrite
// macro: __cpp_lib_string_resize_and_overwrite
// standard: cpp23
// category: library
// description: std::string::resize_and_overwrite

#include <string>
auto main() -> int { std::string s; s.resize_and_overwrite(5, [](char* p, std::size_t n) { for (std::size_t i=0; i<n; ++i) p[i]='x'; return n; }); return s.size() == 5 ? 0 : 1; }
