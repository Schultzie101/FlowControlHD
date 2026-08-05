//--INITIAILZE--
#include <Arduino.h>
#include <TimerOne.h>

int directionPin = 13;
int pwmPin = 11;
int brakePin = 8;
float frequency_currrent; 
int led_brightness;



//--FLOW SENSOR VARIABLES--
float lastTime = 0;
int sensorPin = 2;
volatile double volume = 0.0;
volatile double flowrate = 0.0;
int time_milli = 500; //millis
float flow_average = 0;
const double TIME_INTERVAL = 0.1; // seconds
bool timer_started = false; 

//--BUTTON VARIABLES 
int buttonPin = 7;
int value = 0;

//Note: Larger "array_size" means more points for the "frequency_array" to calculate. 
//This leads to a smoother live graph...
const int array_size = 20;
float flow_array[array_size] = {0}; 
int flow_index = 0;

const int SIZE = 256;
    double items[SIZE];
   uint8_t * items_pointer = reinterpret_cast<uint8_t*>(items);
   const uint8_t * items_pointer_beginning = items_pointer;
const int buffer_size = 32;

//note: at 15 volts ONLY
const float minimum_pwm = 90.00;

//--Pulse for flow sensor--
void pulse()   //measure the quantity of square wave
{ // Do not use serial.print or delay() in this function.
  volume += 1.0 * 1000 / 540.0; // 1L=540 pulses
}

//calculations for the live graph
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




// This function runs automatically every TIME_INTERVAL
void calculate_slope() {
  static double previous_volume = 0; // Remembers value between interrupts (only sets to 0 the first time it's run)

  double current_volume = volume;

  // slope = rise / run = change in Y / change in X
  flowrate = (current_volume - previous_volume) / TIME_INTERVAL;
  previous_volume = current_volume;
  flowrate = volume * 60;
}


float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {

  Serial.begin(115200);
  //--BUTTON SETUP--
  pinMode(buttonPin, INPUT_PULLUP);

  //initialize LED digital pin as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(directionPin, OUTPUT);
    pinMode(brakePin, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(sensorPin), pulse, RISING);  //DIGITAL Pin 3: Interrupt 0
  

  Timer1.initialize((int) TIME_INTERVAL * 1000000); // takes in us (microseconds)
  Timer1.attachInterrupt(calculate_slope);
  Timer1.stop();
}


void loop() { 
    double flowrate_copy;
  digitalWrite(LED_BUILTIN, LOW);
  if (items_pointer-items_pointer_beginning == SIZE * __SIZEOF_DOUBLE__){
    if(!timer_started){
      Timer1.start();
      timer_started = true;
    } 
    //We have now loaded all the data
    //turn on main led
    digitalWrite(LED_BUILTIN, HIGH);
    // Change direction. High = clockwise LOW= counterclockwise
    // BUTTON DIRECTION
    value = digitalRead(buttonPin);
    digitalWrite(brakePin, LOW);
    if(value == 1){
      digitalWrite(directionPin, HIGH);
    }
    if(value == 0){
      digitalWrite(directionPin, LOW);
    }


    for (int index = 0; index < SIZE; index++){
      led_brightness = round(mapFloat(items[index], 0.00,1.00,minimum_pwm,255.00));
      analogWrite(pwmPin, led_brightness );
      noInterrupts();
      flowrate_copy = flowrate;
      interrupts();

      flow_array[flow_index] = flowrate_copy;
      flow_index = flow_index + 1;
      flow_average = array_average(flow_array, array_size);
      if (flow_index >= array_size) {
      flow_index = 0;
      }
      
      //Line which will be sent back for the graph in the python program. However, this can also be previewed with the serial monitor. 
      //DO NOT open the serial monitor with the GUI.py open. this will result in a crash or unexpected behavior. 
      Serial.println(flowrate);
      delay(200);
    }
  }
  else {
  if (Serial.available() >= buffer_size){
    Serial.readBytes(items_pointer, buffer_size);
    items_pointer += buffer_size;
  }
}
}