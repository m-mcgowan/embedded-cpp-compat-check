// feature: deducing_this
// macro: __cpp_explicit_this_parameter
// standard: cpp23
// category: language
// description: Deducing this (explicit object parameter)

struct Widget {
    int value = 0;
    auto get_value(this const Widget& self) -> int { return self.value; }
};

auto main() -> int {
    Widget w{42};
    return w.get_value() - 42;
}
