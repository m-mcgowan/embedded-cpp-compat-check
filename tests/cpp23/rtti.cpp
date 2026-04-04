// feature: rtti
// macro: __cpp_rtti
// standard: cpp23
// category: language
// description: Run-time type information (typeid)

#include <typeinfo>
struct Base { virtual ~Base() {} };
struct Derived : Base {};
auto main() -> int { Derived d; Base& b = d; return typeid(b) == typeid(Derived) ? 0 : 1; }
