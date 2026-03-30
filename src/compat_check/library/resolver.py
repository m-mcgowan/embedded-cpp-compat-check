"""Map library platform declarations to our curated platform definitions."""
from compat_check.platform.models import Platform

_ARCH_ALIASES = {
    "avr": ["atmelavr"],
    "esp32": ["espressif32"],
    "esp8266": ["espressif8266"],
    "stm32": ["ststm32"],
    "rp2040": ["raspberrypi"],
    "samd": ["atmelsam"],
    "nrf52": ["nordicnrf52"],
}

def resolve_platforms(declared: list[str], available: list[Platform]) -> list[Platform]:
    if "*" in declared:
        return list(available)
    matched = []
    for platform in available:
        pio_platform = platform.platformio.get("platform", "")
        for decl in declared:
            if decl in pio_platform:
                matched.append(platform)
                break
            if decl == platform.architecture:
                matched.append(platform)
                break
            aliases = _ARCH_ALIASES.get(decl, [])
            if any(alias in pio_platform for alias in aliases):
                matched.append(platform)
                break
    return matched
