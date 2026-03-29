// feature: initializer_lists
// macro: __cpp_initializer_lists
// standard: cpp11
// category: language
// description: List-initialization and std::initializer_list

#include <initializer_list>

int sum(std::initializer_list<int> vals) {
    int s = 0;
    for (auto v : vals) s += v;
    return s;
}

auto main() -> int {
    return sum({1, 2, 3}) - 6;
}
