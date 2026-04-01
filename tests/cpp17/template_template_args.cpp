// feature: template_template_args
// macro: __cpp_template_template_args
// standard: cpp17
// category: language
// description: Matching of template template-arguments

template<template<typename> class C, typename T> struct Wrap { C<T> c; };
#include <vector>
auto main() -> int { Wrap<std::vector, int> w; w.c.push_back(42); return w.c[0] - 42; }
