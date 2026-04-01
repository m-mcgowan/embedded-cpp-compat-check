// feature: is_aggregate
// macro: __cpp_lib_is_aggregate
// standard: cpp17
// category: library
// description: std::is_aggregate_v<SomeStruct>

#include <type_traits>
struct Agg { int x; int y; };
struct NonAgg { NonAgg() {} int x; };
auto main() -> int { return std::is_aggregate_v<Agg> && !std::is_aggregate_v<NonAgg> ? 0 : 1; }
