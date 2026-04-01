// feature: formatters
// macro: __cpp_lib_formatters
// standard: cpp23
// category: library
// description: Formatters for library types (stacktrace etc)

#include <format>
#include <thread>
auto main() -> int { auto s = std::format("{}", std::this_thread::get_id()); return s.empty() ? 1 : 0; }
