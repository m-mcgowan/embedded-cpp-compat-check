// feature: boyer_moore_searcher
// macro: __cpp_lib_boyer_moore_searcher
// standard: cpp17
// category: library
// description: Boyer-Moore string searcher

#include <functional>
#include <algorithm>
#include <string>
auto main() -> int { std::string haystack = "hello world"; std::string needle = "world"; auto it = std::search(haystack.begin(), haystack.end(), std::boyer_moore_searcher(needle.begin(), needle.end())); return it != haystack.end() ? 0 : 1; }
