// feature: shared_ptr_weak_type
// macro: __cpp_lib_shared_ptr_weak_type
// standard: cpp17
// category: library
// description: std::shared_ptr<T>::weak_type

#include <memory>
auto main() -> int { using W = std::shared_ptr<int>::weak_type; auto sp = std::make_shared<int>(42); W wp = sp; return wp.expired() ? 1 : 0; }
