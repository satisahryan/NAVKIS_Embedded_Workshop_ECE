// Lab 6 (Deep dive) - Real-time multitasking with FreeRTOS
// Three independent tasks share one CPU, like tasks in a real-time OS:
//   blinkTask  - toggles the LED on GPIO 26 every 250 ms
//   sensorTask - reads the potentiometer (GPIO 34) and sends values to a QUEUE
//   printTask  - waits on the queue and prints whatever arrives
// Potentiometer wiper -> GPIO 34, LED -> GPIO 26 (same wiring as Lab 3).

const int LED_PIN = 26;
const int POT_PIN = 34;

QueueHandle_t potQueue;               // FIFO between sensorTask and printTask

void blinkTask(void* param) {
  pinMode(LED_PIN, OUTPUT);
  while (true) {
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    vTaskDelay(pdMS_TO_TICKS(250));   // sleep this task; others keep running
  }
}

void sensorTask(void* param) {
  while (true) {
    int value = analogRead(POT_PIN);
    xQueueSend(potQueue, &value, 0);  // drop the sample if the queue is full
    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void printTask(void* param) {
  int value;
  while (true) {
    if (xQueueReceive(potQueue, &value, portMAX_DELAY)) {  // block until data
      Serial.printf("[core %d] pot = %d\n", xPortGetCoreID(), value);
    }
  }
}

void setup() {
  Serial.begin(115200);
  potQueue = xQueueCreate(10, sizeof(int));   // holds up to 10 ints

  //                       function    name      stack  param prio handle
  xTaskCreate(blinkTask,  "blink",   2048,  NULL, 1,   NULL);
  xTaskCreate(sensorTask, "sensor",  2048,  NULL, 2,   NULL);
  xTaskCreate(printTask,  "print",   4096,  NULL, 1,   NULL);
}

void loop() {
  vTaskDelay(pdMS_TO_TICKS(1000));    // loop() is itself just another task
}
