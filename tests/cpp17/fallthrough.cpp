// feature: fallthrough
// macro: fallthrough
// standard: cpp17
// category: attribute
// description: [[fallthrough]] attribute

auto main() -> int { int x = 1; switch(x) { case 1: x = 2; [[fallthrough]]; case 2: break; } return x - 2; }
