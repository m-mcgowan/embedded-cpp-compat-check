// feature: inline_variables
// macro: __cpp_inline_variables
// standard: cpp17
// category: language
// description: Inline variables

struct Config {
    static inline int max_retries = 3;
};

auto main() -> int {
    return Config::max_retries - 3;
}
