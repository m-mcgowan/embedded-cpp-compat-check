// feature: deduction_guides
// macro: __cpp_deduction_guides
// standard: cpp17
// category: language
// description: Class template argument deduction (CTAD)

#include <utility>
auto main() -> int { auto p = std::pair(1, 2.0); return p.first - 1; }
