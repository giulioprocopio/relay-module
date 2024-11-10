#include <iostream>

#include <driver/gpio.h>
#include <esp_log.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <nvs_flash.h>

#include "hardware.h"

#define gpio_pad_select_gpio esp_rom_gpio_pad_select_gpio

static const char *tag = "main";

void init_nvs() {
  esp_err_t ret = nvs_flash_init();
  if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
      ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
    ESP_ERROR_CHECK(nvs_flash_erase());
    ret = nvs_flash_init();
  }
  ESP_ERROR_CHECK(ret);
}

extern "C" void app_main(void) {
  init_nvs();

  gpio_pad_select_gpio(RELAY_GPIO);
  gpio_set_direction(RELAY_GPIO, GPIO_MODE_OUTPUT);

  while (true) {
    gpio_set_level(RELAY_GPIO, 1);
    vTaskDelay(1000 / portTICK_PERIOD_MS);

    gpio_set_level(RELAY_GPIO, 0);
    vTaskDelay(1000 / portTICK_PERIOD_MS);

    ESP_LOGI(tag, "Tick");
  }
}
