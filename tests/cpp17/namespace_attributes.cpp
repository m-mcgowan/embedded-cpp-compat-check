// feature: namespace_attributes
// macro: __cpp_namespace_attributes
// standard: cpp17
// category: language
// description: Attributes on namespaces and enumerators

namespace [[deprecated]] old_ns { inline int x = 0; }
auto main() -> int { return 0; }
