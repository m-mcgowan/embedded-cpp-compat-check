// feature: three_way_comparison
// macro: __cpp_impl_three_way_comparison
// standard: cpp20
// category: language
// description: Three-way comparison operator (spaceship)

#include <compare>

struct Point {
    int x, y;
    auto operator<=>(const Point&) const = default;
};

auto main() -> int {
    Point a{1, 2}, b{1, 2};
    return ((a <=> b) == std::strong_ordering::equal) ? 0 : 1;
}
