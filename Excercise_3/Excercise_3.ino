volatile String command;
const int led1Pin = 18;
const int freq = 5000;
const int ledChannel = 0;  // ช่อง 0-15
const int resolution = 8;  // ความละเอียด 0-16 bit
volatile char type;
volatile int pwm_percentile;
int PWM;


void setup() {
  Serial.begin(115200);
  xTaskCreatePinnedToCore(serialget, "get serial data", 1000, NULL, 0, NULL, 0);
  xTaskCreatePinnedToCore(hwcontrol, "HW control", 1000, NULL, 0, NULL, 0);
  ledcSetup(ledChannel, freq, resolution);  // ตั้งค่า LED PWM ช่อง 0 ความถี่ 5000mhz ความละเอียด 8bit หรือค่า 0-255
  ledcAttachPin(led1Pin, ledChannel);        // กำหนดขา led ที่ต้องการควบคุม
}
void serialget(void *pvParameters) {
  while (1) {
    if (Serial.available() > 0) {
      command = Serial.readString();
      type = command.substring(0, 1);
      pwm_percentile = command.substring(1).toFloat();
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}
void hwcontrol(void *pvParameters) {
  while (1) {
    PWM = pwm_percentile * 100.0 / 255;

    if (type == 'L') {
      ledcWrite(ledChannel, PWM);
    } else if (type == 'P') {
      count_down();  // Call count_down once
    } else {
      PWM = 0;
    }

    vTaskDelay(pdMS_TO_TICKS(10));  // Delay inside the loop
  }
}
void count_down() {
  while (true) {
    ledcWrite(ledChannel, PWM);  // Correct `ledcWrite` call
    delay(1000);
    PWM -= (10 * 100.0) / 255;  // Ensure floating-point division
    if (PWM <= 0) {             // Simplified condition
      break;                    // Semicolon added
    }
  }
}


void loop() {
}
