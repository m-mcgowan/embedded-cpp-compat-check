// feature: semaphore
// macro: __cpp_lib_semaphore
// standard: cpp20
// category: library
// description: std::counting_semaphore and std::binary_semaphore

#include <semaphore>
auto main() -> int { std::binary_semaphore s(1); s.acquire(); s.release(); return 0; }
