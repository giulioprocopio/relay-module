.PHONY: flash

PYTHON := $(shell which python3)

PIO_CORE_DIR := $(shell pio system info \
	| grep 'PlatformIO Core Directory'\
	| tr -s ' ' | cut -d ' ' -f 4)
PIO_BIN_DIR := .pio/build/esp32dev

ESPTOOL := $(PIO_CORE_DIR)/packages/tool-esptoolpy/esptool.py

BOOTLOADER_BIN := $(PIO_BIN_DIR)/bootloader.bin
PARTITIONS_BIN := $(PIO_BIN_DIR)/partitions.bin
FIRMWARE_BIN := $(PIO_BIN_DIR)/firmware.bin
BOOTAPP_BIN := $(PIO_CORE_DIR)/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin
NVS_BIN := nvs.bin

# Forward port and baud rate to `esptool.py` if provided, otherwise let it try
# to deduce them.
PORT_ARG := $(if $(PORT),--port $(PORT),)
BAUD_ARG := $(if $(BAUD),--baud $(BAUD),)

flash:
	$(PYTHON) $(ESPTOOL) --chip esp32 $(PORT_ARG) $(BAUD_ARG) \
		--before default_reset --after hard_reset \
		write_flash -z --flash_mode dio --flash_freq 40m --flash_size 4MB \
		0x1000 $(BOOTLOADER_BIN) \
		0x8000 $(PARTITIONS_BIN) \
		0x9000 $(NVS_BIN) \
		0xe000 $(BOOTAPP_BIN) \
		0x10000 $(FIRMWARE_BIN)
