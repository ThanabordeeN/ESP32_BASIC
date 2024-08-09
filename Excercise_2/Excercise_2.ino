volatile char command;
const int led1Pin = 2;
const int led2Pin = 15;
const int led3Pin = 4;
TaskHandle_t taskserial;
TaskHandle_t hardwarect;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(10);
  pinMode(LED1, OUTPUT);

  void setup() {
    Serial.begin(115200);
    Serial.setTimeout(10);
    pinMode(LED1, OUTPUT);
    xTaskCreatePinnedToCore(serialget, "get serial data", 1000, NULL, 0, NULL, 0);
    xTaskCreatePinnedToCore(hwcontrol, "HW control", 1000, NULL, 0, NULL, 0);
  }
  void serialget(void *pvParameters) {
    while (1) {
      if (Serial.available() > 0) {
        command = Serial.read();
      }
      vTaskDelay(pdMS_TO_TICKS(10));
    }
  }
  void hwcontrol(void *pvParameters) {
    while (1) {
      switch (command) {
        case '1':                                        // LED1 Control
          digitalWrite(led1Pin, !digitalRead(led1Pin));  // Toggle LED1
          break;
        case '2':                                        // LED2 Control
          digitalWrite(led2Pin, !digitalRead(led2Pin));  // Toggle LED2
          break;
        case '3':                                        // LED3 Control
          digitalWrite(led1Pin, HIGH);                   // Turn off LED1
          digitalWrite(led2Pin, HIGH);                   // Turn off LED2
          digitalWrite(led3Pin, !digitalRead(led3Pin));  // Toggle LED3
          break;
        default:

          break;
      }
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}
void loop() {
  vTaskDelete(NULL);
}
