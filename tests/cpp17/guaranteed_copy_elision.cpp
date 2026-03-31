// feature: guaranteed_copy_elision
// macro: __cpp_guaranteed_copy_elision
// standard: cpp17
// category: language
// description: Guaranteed copy elision (prvalue materialization)

struct NoCopy { NoCopy() = default; NoCopy(const NoCopy&) = delete; NoCopy(NoCopy&&) = delete; };
NoCopy make() { return NoCopy{}; }
auto main() -> int { NoCopy x = make(); (void)x; return 0; }
