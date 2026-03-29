// feature: designated_initializers
// macro: __cpp_designated_initializers
// standard: cpp20
// category: language
// description: Designated initializers

struct Point { int x; int y; };

auto main() -> int {
    Point p = {.x = 3, .y = 4};
    return p.x + p.y - 7;
}
