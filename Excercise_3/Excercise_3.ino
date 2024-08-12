const int led1Pin = 18;
const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

volatile char type;
volatile int pwm_percentile;
float PWM = 0;
volatile int suspend = 0;

// TaskHandle_t

void setup() {
  Serial.begin(115200);
  xTaskCreatePinnedToCore(serialget, "get serial data", 1000, NULL, 0, NULL, 0);
  xTaskCreatePinnedToCore(hwcontrol, "HW control", 1000, NULL, 0, NULL, 0);

  ledcAttach(led1Pin, freq, resolution);  // กำหนดขา led ที่ต้องการควบคุม
  //ledcAttachChannel(led1Pin, freq,resolution,ledChannel);
}

void serialget(void *pvParameters) {
  while (1) {
    if (Serial.available() > 0) {
      String command = Serial.readString();
      type = command.substring(0, 1).charAt(0);
      pwm_percentile = command.substring(1).toInt();

      // Serial.println(command);
      // Serial.println(type);
      // Serial.println(pwm_percentile);
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void hwcontrol(void *pvParameters) {
  while (1) {
    if (pwm_percentile > 255) {
      pwm_percentile = 255;
    }
    PWM = (pwm_percentile * 255.00) / 100.0;
    if (type == 'L') {
      ledcWriteChannel(ledChannel, PWM);
      type = 0;
    } else if (type == 'C') {
      count_down();
      type = 0;
    } else if (type == 'S') {
      PWM = 0;

      ledcWriteChannel(ledChannel, PWM);
      type = 0;
      pwm_percentile = 0;
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}


void count_down() {
  while (1) {
    ledcWriteChannel(ledChannel, PWM);
    delay(200);
    if (type == 'S') {
      PWM = 0;
      ledcWriteChannel(ledChannel, PWM);
      type = 0;

      break;
    }
    PWM -= (10 * 100.0) / 255;

    if (PWM <= 0) {
      PWM = 0;
      pwm_percentile = 0;
      break;
    }
  }
}

void loop() {
  float volt = PWM / 255 * 3.3;
  Serial.println(volt);
  delay(1000);
}
