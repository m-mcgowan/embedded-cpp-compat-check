// feature: syncbuf
// macro: __cpp_lib_syncbuf
// standard: cpp20
// category: library
// description: std::syncbuf and std::osyncstream

#include <syncstream>
#include <sstream>
auto main() -> int { std::ostringstream oss; std::osyncstream sync(oss); sync << "hi"; sync.emit(); return oss.str() == "hi" ? 0 : 1; }
