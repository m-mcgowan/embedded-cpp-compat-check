# Library Compatibility Report: note-cpp v0.1.0

Generated: 2026-03-30

## Summary

| Platform | Min Standard | Examples |
|----------|-------------|----------|
| avr-uno | — | 0/11 |
| esp32s3-arduino-v3 | — | 2/11 |
| rp2040-pico | — | 1/11 |
| stm32-nucleo-f411re | — | 5/11 |

## Detail

| Example | avr-uno c++11 | avr-uno c++14 | avr-uno c++17 | esp32s3-arduino-v3 c++11 | esp32s3-arduino-v3 c++14 | esp32s3-arduino-v3 c++17 | esp32s3-arduino-v3 c++20 | esp32s3-arduino-v3 c++23 | esp32s3-arduino-v3 c++26 | rp2040-pico c++11 | rp2040-pico c++14 | rp2040-pico c++17 | rp2040-pico c++20 | rp2040-pico c++23 | stm32-nucleo-f411re c++11 | stm32-nucleo-f411re c++14 | stm32-nucleo-f411re c++17 | stm32-nucleo-f411re c++20 |
|---------|---------------|---------------|---------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|--------------------------|-------------------|-------------------|-------------------|-------------------|-------------------|---------------------------|---------------------------|---------------------------|---------------------------|
| arduino/i2c_basic | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| arduino/serial_basic | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| attention_pin | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| getting_started | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| hub-configuration | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| location_tracking | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| migration_notec | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS | PASS | FAIL | FAIL | FAIL | FAIL |
| sending-notes | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| smoke | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |
| target_filtering | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| zero_alloc | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | PASS | PASS | PASS | PASS |

## Failures

### avr-uno c++11: arduino/i2c_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: arduino/serial_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: attention_pin
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: getting_started
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: hub-configuration
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: location_tracking
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: migration_notec
```
src/migration_notec.cpp:9:10: fatal error: cstdio: No such file or directory
```

### avr-uno c++11: sending-notes
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: smoke
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: target_filtering
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++11: zero_alloc
```
lib/note-cpp/include/note/types.hpp:3:10: fatal error: cstdint: No such file or directory
```

### avr-uno c++14: arduino/i2c_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: arduino/serial_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: attention_pin
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: getting_started
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: hub-configuration
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: location_tracking
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: migration_notec
```
src/migration_notec.cpp:9:10: fatal error: cstdio: No such file or directory
```

### avr-uno c++14: sending-notes
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: smoke
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: target_filtering
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++14: zero_alloc
```
lib/note-cpp/include/note/types.hpp:3:10: fatal error: cstdint: No such file or directory
```

### avr-uno c++17: arduino/i2c_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: arduino/serial_basic
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: attention_pin
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: getting_started
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: hub-configuration
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: location_tracking
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: migration_notec
```
src/migration_notec.cpp:9:10: fatal error: cstdio: No such file or directory
```

### avr-uno c++17: sending-notes
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: smoke
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: target_filtering
```
lib/note-cpp/include/note/arena.hpp:14:10: fatal error: cstddef: No such file or directory
```

### avr-uno c++17: zero_alloc
```
lib/note-cpp/include/note/types.hpp:3:10: fatal error: cstdint: No such file or directory
```

### esp32s3-arduino-v3 c++11: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++11: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++11: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++11: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++11: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++11: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++11: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++11: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++11: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++14: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++14: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++14: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++14: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++14: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++14: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++14: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++14: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++14: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++17: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++17: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++17: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++17: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++17: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++17: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++17: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++17: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++17: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++20: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++20: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++20: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++20: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++20: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++20: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++20: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++20: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++20: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++23: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++23: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++23: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++23: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++23: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++23: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++23: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++23: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++23: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++26: attention_pin
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++26: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++26: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++26: location_tracking
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++26: migration_notec
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++26: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++26: smoke
```
collect2: error: ld returned 1 exit status
```

### esp32s3-arduino-v3 c++26: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### esp32s3-arduino-v3 c++26: zero_alloc
```
collect2: error: ld returned 1 exit status
```

### rp2040-pico c++11: arduino/i2c_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++11: arduino/serial_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++11: attention_pin
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++11: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++11: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++11: location_tracking
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++11: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++11: smoke
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++11: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++11: zero_alloc
```
lib/note-cpp/include/note/error.hpp:58:10: error: 'string_view' in namespace 'std' does not name a type
```

### rp2040-pico c++14: arduino/i2c_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++14: arduino/serial_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++14: attention_pin
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++14: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++14: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++14: location_tracking
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++14: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++14: smoke
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++14: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++14: zero_alloc
```
lib/note-cpp/include/note/error.hpp:58:10: error: 'string_view' in namespace 'std' does not name a type
```

### rp2040-pico c++17: arduino/i2c_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++17: arduino/serial_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++17: attention_pin
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++17: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++17: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++17: location_tracking
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++17: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++17: smoke
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++17: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++17: zero_alloc
```
lib/note-cpp/include/note/error.hpp:58:10: error: 'string_view' in namespace 'std' does not name a type
```

### rp2040-pico c++20: arduino/i2c_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++20: arduino/serial_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++20: attention_pin
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++20: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++20: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++20: location_tracking
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++20: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++20: smoke
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++20: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++20: zero_alloc
```
lib/note-cpp/include/note/error.hpp:58:10: error: 'string_view' in namespace 'std' does not name a type
```

### rp2040-pico c++23: arduino/i2c_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++23: arduino/serial_basic
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++23: attention_pin
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++23: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++23: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++23: location_tracking
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++23: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### rp2040-pico c++23: smoke
```
lib/note-cpp/include/note/allocator.hpp:60:37: error: 'std::pmr' has not been declared
```

### rp2040-pico c++23: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### rp2040-pico c++23: zero_alloc
```
lib/note-cpp/include/note/error.hpp:58:10: error: 'string_view' in namespace 'std' does not name a type
```

### stm32-nucleo-f411re c++11: arduino/serial_basic
```
collect2: error: ld returned 1 exit status
```

### stm32-nucleo-f411re c++11: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++11: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++11: migration_notec
```
src/migration_notec.cpp:84:5: error: 'int16_t' does not name a type
```

### stm32-nucleo-f411re c++11: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++11: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++14: arduino/serial_basic
```
collect2: error: ld returned 1 exit status
```

### stm32-nucleo-f411re c++14: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++14: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++14: migration_notec
```
src/migration_notec.cpp:84:5: error: 'int16_t' does not name a type
```

### stm32-nucleo-f411re c++14: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++14: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++17: arduino/serial_basic
```
collect2: error: ld returned 1 exit status
```

### stm32-nucleo-f411re c++17: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++17: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++17: migration_notec
```
src/migration_notec.cpp:84:5: error: 'int16_t' does not name a type
```

### stm32-nucleo-f411re c++17: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++17: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++20: arduino/serial_basic
```
collect2: error: ld returned 1 exit status
```

### stm32-nucleo-f411re c++20: getting_started
```
src/getting_started.cpp:27:10: fatal error: mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++20: hub-configuration
```
src/main.cpp:21:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++20: migration_notec
```
src/migration_notec.cpp:84:5: error: 'int16_t' does not name a type
```

### stm32-nucleo-f411re c++20: sending-notes
```
src/main.cpp:27:10: fatal error: ../mock_backend.hpp: No such file or directory
```

### stm32-nucleo-f411re c++20: target_filtering
```
src/target_filtering.cpp:18:10: fatal error: mock_backend.hpp: No such file or directory
```

