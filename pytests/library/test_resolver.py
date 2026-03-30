from compat_check.library.resolver import resolve_platforms
from compat_check.platform.models import Platform

def _make_platform(slug, architecture, pio_platform):
    return Platform(
        name=slug, slug=slug, version="1.0.0",
        architecture=architecture, mcu="test",
        build_system="platformio", standards=["c++17"],
        framework="arduino",
        platformio={"platform": pio_platform, "board": "test", "framework": "arduino"},
    )

ALL_PLATFORMS = [
    _make_platform("avr-uno", "avr", "atmelavr"),
    _make_platform("esp32s3", "xtensa", "https://github.com/pioarduino/platform-espressif32/releases/download/55.03.36/platform-espressif32.zip"),
    _make_platform("stm32-f411", "arm", "ststm32"),
    _make_platform("rp2040-pico", "arm", "raspberrypi"),
]

def test_resolve_star():
    result = resolve_platforms(["*"], ALL_PLATFORMS)
    assert len(result) == 4

def test_resolve_pio_platform_name():
    result = resolve_platforms(["atmelavr"], ALL_PLATFORMS)
    assert len(result) == 1
    assert result[0].slug == "avr-uno"

def test_resolve_pio_platform_name_in_url():
    result = resolve_platforms(["espressif32"], ALL_PLATFORMS)
    assert len(result) == 1
    assert result[0].slug == "esp32s3"

def test_resolve_arduino_architecture():
    result = resolve_platforms(["avr"], ALL_PLATFORMS)
    assert len(result) == 1
    assert result[0].slug == "avr-uno"

def test_resolve_arduino_esp32_alias():
    result = resolve_platforms(["esp32"], ALL_PLATFORMS)
    assert len(result) == 1
    assert result[0].slug == "esp32s3"

def test_resolve_multiple():
    result = resolve_platforms(["atmelavr", "ststm32"], ALL_PLATFORMS)
    assert len(result) == 2
    slugs = {p.slug for p in result}
    assert slugs == {"avr-uno", "stm32-f411"}

def test_resolve_no_match():
    result = resolve_platforms(["teensy"], ALL_PLATFORMS)
    assert result == []
