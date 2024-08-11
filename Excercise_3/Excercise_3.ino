const int led1Pin = 18;
const int freq = 5000;
const int ledChannel = 0;  
const int resolution = 8;  

volatile char type;
volatile int pwm_percentile;
int PWM;
bool suspend = false;
TaskHandle_t hwcontrolTask;  



void setup() {
  Serial.begin(115200);
  xTaskCreatePinnedToCore(serialget, "get serial data", 1000, NULL, 0, NULL, 0);
  xTaskCreatePinnedToCore(hwcontrol, "HW control", 1000, NULL, 0, &hwcontrolTask, 0);
  ledcAttach(led1Pin, freq,resolution);  // กำหนดขา led ที่ต้องการควบคุม
  //ledcAttachChannel(led1Pin, freq,resolution,ledChannel);
}

void serialget(void *pvParameters) {
  while (1) {
    if (Serial.available() > 0) {
      String command = Serial.readString();
      type = command.substring(0, 1).charAt(0);
      pwm_percentile = command.substring(1).toInt();
    }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void hwcontrol(void *pvParameters) {
  while (1) {
    PWM = (pwm_percentile * 100.0) / 255;
    if (type == 'L') {
      ledcWrite(ledChannel, PWM);
    } else if (type == 'C') {
      count_down(); 
    } else {
      if (!suspend) {
        vTaskSuspend(hwcontrolTask);
        suspend = true;
      } else {
        vTaskResume(hwcontrolTask);
        suspend = false;
      }
    }
    vTaskDelay(pdMS_TO_TICKS(10)); 
  }
}

void count_down() {
  while (1) {
    ledcWriteChannel(ledChannel, PWM); 
    delay(1000);
    PWM -= (10 * 100.0) / 255;  
    if (PWM <= 0) {             
      break;                   
    }
  }
}

void loop() {
  Serial.println(PWM / 255 * 5);
}
