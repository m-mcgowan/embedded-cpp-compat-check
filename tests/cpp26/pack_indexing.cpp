// feature: pack_indexing
// macro: __cpp_pack_indexing
// standard: cpp26
// category: language
// description: Pack indexing

template<typename... Ts> using first_t = Ts...[0];
auto main() -> int { first_t<int, double> v = 42; return v - 42; }
