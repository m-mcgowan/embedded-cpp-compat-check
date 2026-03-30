// feature: node_extract
// macro: __cpp_lib_node_extract
// standard: cpp17
// category: library
// description: Splicing maps and sets (extract, merge)

#include <map>
auto main() -> int { std::map<int,int> a = {{1,2}}, b; auto nh = a.extract(1); b.insert(std::move(nh)); return b[1] - 2; }
