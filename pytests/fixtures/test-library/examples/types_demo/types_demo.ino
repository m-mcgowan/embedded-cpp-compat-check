#include <Arduino.h>
#include <test_lib.h>

void setup() {
    auto result = add(10, 20);
    Serial.begin(115200);
    Serial.println(result);
}

void loop() {}
