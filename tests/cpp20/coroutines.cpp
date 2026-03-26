// feature: coroutines
// macro: __cpp_impl_coroutine
// standard: cpp20
// category: language
// description: Coroutines

#include <coroutine>

struct Task {
    struct promise_type {
        Task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };
};

Task simple() { co_return; }

auto main() -> int {
    simple();
    return 0;
}
