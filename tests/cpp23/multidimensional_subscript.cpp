// feature: multidimensional_subscript
// macro: __cpp_multidimensional_subscript
// standard: cpp23
// category: language
// description: Multidimensional subscript operator

struct Matrix {
    int data[4] = {0, 1, 2, 3};
    int operator[](int r, int c) { return data[r * 2 + c]; }
};

auto main() -> int {
    Matrix m;
    return m[1, 1] - 3;
}
