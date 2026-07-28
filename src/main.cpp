//--INITIAILZE--
#include <Arduino.h>
int directionPin = 13;
int pwmPin = 11;
int brakePin = 8;
float frequency_currrent; 
int led_brightness;

const int SIZE = 256;
    double items[SIZE];
   uint8_t * items_pointer = reinterpret_cast<uint8_t*>(items);
   const uint8_t * items_pointer_beginning = items_pointer;
const int buffer_size = 32;

//note: at 15 volts ONLY
const float minimum_pwm = 90.00;


float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
  Serial.begin(115200);
  //initialize LED digital pin as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(directionPin, OUTPUT);
    pinMode(brakePin, OUTPUT);
}


void loop() { 
  digitalWrite(LED_BUILTIN, LOW);
  if (items_pointer-items_pointer_beginning == SIZE * __SIZEOF_DOUBLE__){
    //We have now loaded all the data
    //turn on main led
    digitalWrite(LED_BUILTIN, HIGH);
    // Change direction. High = clockwise LOW= counterclockwise
    digitalWrite(directionPin, HIGH);
    digitalWrite(brakePin, LOW);
    for (int index = 0; index < SIZE; index++){
      led_brightness = round(mapFloat(items[index], 0.00,1.00,minimum_pwm,255.00));
      analogWrite(pwmPin, led_brightness );
      Serial.println(led_brightness);
      delay(100);}
  }
  else {
  if (Serial.available() >= buffer_size){
    // Serial.readBytes(reinterpret_cast<uint8_t*>(items), buffer_size);
    Serial.readBytes(items_pointer, buffer_size);
    items_pointer += buffer_size;
  }
}
}