#ifndef CONFIG_H
#define CONFIG_H

// Enforce using the Soft AP method instead of BLE.
#ifndef FORCE_SOFT_AP
#define FORCE_SOFT_AP 0
#endif

// Automatically delete previously provisioned data on boot.
#ifndef RESET_PROVISIONED_ON_BOOT
#define RESET_PROVISIONED_ON_BOOT 0
#endif

// Serial communication baud rate.
#ifndef SERIAL_BAUD_RATE
#define SERIAL_BAUD_RATE 115200
#endif

#endif
