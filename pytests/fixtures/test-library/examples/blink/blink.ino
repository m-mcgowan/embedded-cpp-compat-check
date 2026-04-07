#include <Arduino.h>
#include <test_lib.h>

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    int val = add(1, 2);
    digitalWrite(LED_BUILTIN, val > 0 ? HIGH : LOW);
    delay(1000);
}
