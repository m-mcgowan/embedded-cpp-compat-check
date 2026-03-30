// feature: range_based_for
// macro: __cpp_range_based_for
// standard: cpp11
// category: language
// description: Range-based for loop

auto main() -> int { int a[] = {1,2,3}; int s=0; for(auto x:a) s+=x; return s-6; }
