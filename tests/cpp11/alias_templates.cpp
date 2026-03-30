// feature: alias_templates
// macro: __cpp_alias_templates
// standard: cpp11
// category: language
// description: Alias templates

template<typename T> using Ptr = T*;
auto main() -> int { Ptr<int> p = nullptr; return p == nullptr ? 0 : 1; }
