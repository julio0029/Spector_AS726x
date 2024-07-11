#include <Wire.h>
// AS7265X connects to ip2c default from Wire library:
// SDA connect to A4 
// SLC connect to A5
// Ground and 3V
#include <SparkFun_AS7265X.h>
#include "SparkFun_AS7265X.h"

// === GLOBAL VARIABLES ===
unsigned long _time;
AS7265X sensor;

int cycle = 0;// LED cycle
const int LEDS [] ={2,3,5,6,9,10};

// === SETUP ===
void setup() {
  Serial.begin(115200);
  
  // Spectro Sensor
  if(sensor.begin() == false)
  {
    Serial.println("Sensor not well connected. Check wiring and restart.");
    while(1);
  }
  sensor.disableIndicator(); //Turn off the blue status LED

// initiate LED pins
  for (int LEDpin : LEDS) {
    pinMode(LEDpin, OUTPUT);
    }
}

void loop() {

  int  startTime = millis();

  for (int LEDpin : LEDS) {

    _time = millis();
    
    // Turn LED on and take measurment
    digitalWrite(LEDpin, HIGH);
    Serial.print(cycle);
    Serial.print(",");
    Serial.print(_time);
    Serial.print(",");
    Serial.print(LEDpin);
    Serial.print(",");

    sensor.takeMeasurements();
    Serial.print(sensor.getCalibratedA());
    Serial.print(",");
    Serial.print(sensor.getCalibratedB());
    Serial.print(",");
    Serial.print(sensor.getCalibratedC());
    Serial.print(",");
    Serial.print(sensor.getCalibratedD());
    Serial.print(",");
    Serial.print(sensor.getCalibratedE());
    Serial.print(",");
    Serial.print(sensor.getCalibratedF());
    Serial.print(",");
    Serial.print(sensor.getCalibratedG());
    Serial.print(",");
    Serial.print(sensor.getCalibratedH());
    Serial.print(",");
    Serial.print(sensor.getCalibratedR());
    Serial.print(",");
    Serial.print(sensor.getCalibratedI());
    Serial.print(",");
    Serial.print(sensor.getCalibratedS());
    Serial.print(",");
    Serial.print(sensor.getCalibratedJ());
    Serial.print(",");
    Serial.print(sensor.getCalibratedT());
    Serial.print(",");
    Serial.print(sensor.getCalibratedU());
    Serial.print(",");
    Serial.print(sensor.getCalibratedV());
    Serial.print(",");
    Serial.print(sensor.getCalibratedW());
    Serial.print(",");
    Serial.print(sensor.getCalibratedK());
    Serial.print(",");
    Serial.print(sensor.getCalibratedL());
    Serial.println();

    // Turn LED off and move to next
    digitalWrite(LEDpin, LOW);
    }
  ++cycle;
  int elapsedTime=millis()-startTime;
  if (elapsedTime<2000){
    int deltaT=2000-elapsedTime;
    delay(deltaT);
  }
}
