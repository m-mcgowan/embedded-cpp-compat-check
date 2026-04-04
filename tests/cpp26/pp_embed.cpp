// feature: pp_embed
// macro: __cpp_pp_embed
// standard: cpp26
// category: language
// description: #embed preprocessor directive

auto main() -> int {
#ifdef __cpp_pp_embed
  return 0;
#else
  return 0;
#endif
}
