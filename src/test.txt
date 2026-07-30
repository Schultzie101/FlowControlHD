#include <Arduino.h>
//setup variables 
int led_pin = 11;
int brightness = 1;
int fadeAmount = 10;
float time;
//time in milliseconds
float time_millis;

//calculations for the array
float array_average(float array [], int size4array){
float element_sum = 0;
float average; 
for (int index = 0; index < size4array; index++){
  element_sum = element_sum + array[index];
}
average = element_sum/size4array;
//return the average so it can be accsessed later. 
return average;
}


//Arrays
//Note: Larger "array_size" means more points for the "frequency_array" to calculate. 
//This leads to a smoother "brightness graph."
const int array_size = 150;
float frequency_array[array_size] = {0};
int index = 0;
float frequency_current;

float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
// put your setup code here, to run once:
Serial.begin(74880);
Serial.print(">voltage:");
Serial.println(0);
Serial.print(">voltage:");
Serial.println(5);
pinMode(led_pin, OUTPUT);
}

void loop() {
// put your main code here, to run repeatedly:

// Analog --> Digital value(s)
int analog_value =  analogRead(A2);
float voltage = 5.00 * (analog_value / 1023.00);

// Higher votage = higher wave frequency
frequency_current =  mapFloat(voltage, 0.00, 5.00, 0.25, 4.00);
  Serial.print(">frequency_current:");
Serial.println(frequency_current);
frequency_array[index] = frequency_current;
index = index + 1;
if (index >= array_size) {
index = 0;
}

  time_millis = (float)millis();
  time = time_millis/1000;

//Calcualte the array's average for "frequency_average"
float frequency_average = array_average(frequency_array, array_size);
  Serial.print(">frequency_average:");
  Serial.println(frequency_average);

//Plot calculation for brightness graph
  float velocity = 127.5 * sin(2*3.141*frequency_average*time)+127.5;
  brightness = int round(velocity);
  brightness = constrain(brightness, 0, 255);
  analogWrite(led_pin, brightness);
  Serial.print(">brightness:");
  Serial.println(brightness);


  delay(10);
}

