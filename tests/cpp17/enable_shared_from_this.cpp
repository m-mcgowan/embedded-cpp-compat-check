// feature: enable_shared_from_this
// macro: __cpp_lib_enable_shared_from_this
// standard: cpp17
// category: library
// description: std::enable_shared_from_this::weak_from_this

#include <memory>
struct S : std::enable_shared_from_this<S> {};
auto main() -> int { auto sp = std::make_shared<S>(); auto wp = sp->weak_from_this(); return wp.expired() ? 1 : 0; }
