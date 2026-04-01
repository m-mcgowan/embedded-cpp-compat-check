// feature: enumerator_attributes
// macro: __cpp_enumerator_attributes
// standard: cpp17
// category: language
// description: Attributes on enumerators (e.g. [[deprecated]])

enum class E { A, B [[deprecated]] };
auto main() -> int { return static_cast<int>(E::A); }
