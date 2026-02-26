#include "main.h"
#include "stm32g4xx_hal.h"
#include <stdio.h>
#include "usb_device.h"
#include "usbd_customhid.h"
#include "tim.h"
#include "nkro.hpp"

extern USBD_HandleTypeDef hUsbDeviceFS;
extern ADC_HandleTypeDef hadc1;
extern ADC_HandleTypeDef hadc2;
RapidTriggerKeyboard keyboard;

// LED明るさ制御 (TIM6割り込みで減光)
// 知覚的な明るさレベル (0-255)。PWMへはガンマ補正(²)で変換する
volatile uint32_t led_brightness = 0;

// USB経由の設定変更リクエスト
volatile bool config_update_request = false;
volatile uint8_t config_target = 0;
volatile uint32_t config_val = 0;

// USBデバッグ変数
volatile uint8_t last_received_cmd = 0;
volatile uint16_t last_received_len = 0;
volatile uint32_t usb_rx_cnt = 0;
volatile uint8_t usb_rx_err = 0;
volatile uint8_t last_payload[4] = {0};

// USB設定パケット処理
extern "C" void ProcessConfigPacket(uint8_t* data, uint16_t len) {
    last_received_len = len;
    usb_rx_cnt++;
    if (len > 0) last_received_cmd = data[0];
    if (len >= 4) {
        last_payload[0] = data[0];
        last_payload[1] = data[1];
        last_payload[2] = data[2];
        last_payload[3] = data[3];
    }

    if (len < 1) return;

    uint8_t cmd = data[0];
    uint8_t idx_target = 1;
    uint8_t idx_val = 2;

    // HIDのReport ID(0x00)が先頭に付く場合のオフセット対応
    if (cmd == 0x00 && len > 1) {
        cmd = data[1];
        idx_target = 2;
        idx_val = 3;
    }

    if (cmd == 0x01) { // Set Sensitivity
        config_target = data[idx_target];
        config_val = data[idx_val];
        config_update_request = true;
    }
}

extern "C" void setup()
{
    keyboard.init();

    printf("=== Rapid Trigger Keyboard ===\r\n");
    printf("Sensitivity(K0): %lu\r\n", keyboard.getSensitivity(0));

    // ADCキャリブレーション
    if (HAL_ADCEx_Calibration_Start(&hadc1, ADC_SINGLE_ENDED) != HAL_OK) {
        printf("[ERR] ADC1 Calibration Failed\r\n");
    }
    if (HAL_ADCEx_Calibration_Start(&hadc2, ADC_SINGLE_ENDED) != HAL_OK) {
        printf("[ERR] ADC2 Calibration Failed\r\n");
    }

    // LED PWM開始 (TIM3 CH2)
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);

    // TIM6割り込み開始 (LED減光用)
    HAL_TIM_Base_Start_IT(&htim6);

    printf("Setup complete.\r\n");
    printf("------------------------------\r\n");
}

// MUX切り替え (PB4-PB7: S0-S3)
void selectMuxChannel(int channel) {
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_4, (channel & 0x01) ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_5, (channel & 0x02) ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_6, (channel & 0x04) ? GPIO_PIN_SET : GPIO_PIN_RESET);
    HAL_GPIO_WritePin(GPIOB, GPIO_PIN_7, (channel & 0x08) ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

uint32_t debug_adc1[16];  // MUX1(ADC1) 各チャンネルのADC値
uint32_t debug_adc2[16];  // MUX2(ADC2) 各チャンネルのADC値

extern "C" void loop()
{
    // USB経由の設定変更
    if (config_update_request) {
        config_update_request = false;
        keyboard.setSensitivity((int)config_target, config_val);
        printf("[CFG] Key:%d Sens:%d\r\n", config_target, (int)config_val);
    }

    // キー押下検出 → LED最大輝度
    {
        KeyboardReport* rpt = keyboard.getReport();
        bool any_key = (rpt->MODIFIER != 0);
        if (!any_key) {
            for (int i = 0; i < 15; i++) {
                if (rpt->KEYS[i] != 0) { any_key = true; break; }
            }
        }
        if (any_key) {
            led_brightness = 255;
        }
    }

    // ADCスキャン (全MUXチャンネル)
    for (int ch = 0; ch < RapidTriggerKeyboard::MUX_CH_COUNT; ch++) {
        selectMuxChannel(ch);

        // 信号安定待ち
        for (volatile int w = 0; w < 200; w++);

        // ADC1 (MUX1)
        __HAL_ADC_CLEAR_FLAG(&hadc1, ADC_FLAG_OVR);
        uint32_t ret1 = HAL_ADC_Start(&hadc1);
        if (ret1 == HAL_OK) {
            if (HAL_ADC_PollForConversion(&hadc1, 10) == HAL_OK) {
                uint32_t val1 = HAL_ADC_GetValue(&hadc1);
                keyboard.updateKeyByMux(ch, 0, val1);
                debug_adc1[ch] = val1;
            } else {
                HAL_ADC_Stop(&hadc1);
                debug_adc1[ch] = 8888; // Timeout
            }
        } else {
            HAL_ADC_Stop(&hadc1);
            debug_adc1[ch] = 9000 + ret1; // Error
        }

        // ADC2 (MUX2)
        __HAL_ADC_CLEAR_FLAG(&hadc2, ADC_FLAG_OVR);
        uint32_t ret2 = HAL_ADC_Start(&hadc2);
        if (ret2 == HAL_OK) {
            if (HAL_ADC_PollForConversion(&hadc2, 10) == HAL_OK) {
                uint32_t val2 = HAL_ADC_GetValue(&hadc2);
                keyboard.updateKeyByMux(ch, 1, val2);
                debug_adc2[ch] = val2;
            } else {
                HAL_ADC_Stop(&hadc2);
                debug_adc2[ch] = 8888;
            }
        } else {
            HAL_ADC_Stop(&hadc2);
            debug_adc2[ch] = 9000 + ret2;
        }
    }

    // USBレポート送信
    KeyboardReport* report = keyboard.getReport();
    if (hUsbDeviceFS.dev_state == USBD_STATE_CONFIGURED) {
        USBD_CUSTOM_HID_SendReport(&hUsbDeviceFS, (uint8_t*)report, sizeof(KeyboardReport));

        // デバッグ出力 (200msに1回)
        static uint32_t last_print = 0;
        if (HAL_GetTick() - last_print > 200) {
            last_print = HAL_GetTick();

            // ステータス行
            printf("Sens:%lu LED:%lu | USB[Cmd:%02X Cnt:%lu]\r\n",
                   keyboard.getSensitivity(0), (uint32_t)led_brightness,
                   last_received_cmd, usb_rx_cnt);

            // MUX1(ADC1): キー名とADC値 (nkro.cppのマッピング順)
            printf(" KP0:%4lu KP.:%4lu Ent:%4lu KP3:%4lu KP2:%4lu KP1:%4lu KP6:%4lu KP5:%4lu KP4:%4lu\r\n",
                   debug_adc1[0],  debug_adc1[15], debug_adc1[14],
                   debug_adc1[13], debug_adc1[12], debug_adc1[11],
                   debug_adc1[10], debug_adc1[9],  debug_adc1[8]);

            // MUX2(ADC2): キー名とADC値
            printf(" KP+:%4lu KP9:%4lu KP8:%4lu KP7:%4lu KP-:%4lu KP*:%4lu KP/:%4lu Num:%4lu\r\n",
                   debug_adc2[15], debug_adc2[14], debug_adc2[13],
                   debug_adc2[12], debug_adc2[11], debug_adc2[10],
                   debug_adc2[9],  debug_adc2[8]);
        }
    }
}

// TIM6 割り込みコールバック: LED減光処理 (知覚リニア)
extern "C" void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM6) {
        // TIM6: Prescaler=0, Period=65535 @ 170MHz → 約386µs周期 (≒2593Hz)
        // サブカウンタで10分周 → 約3.86msごとに1段階減少
        // 255段階 × 3.86ms ≈ 984ms ≈ 1秒で完全消灯
        static uint32_t sub_counter = 0;
        sub_counter++;
        if (sub_counter >= 10) {
            sub_counter = 0;
            if (led_brightness > 0) {
                led_brightness--;
            }
        }
        // ガンマ2.0補正: PWM = brightness² (0-65025)
        uint32_t pwm_val = (uint32_t)led_brightness * led_brightness;
        __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_2, pwm_val);
    }
}