#include <WiFi.h>
#include <HTTPClient.h>

#define press_pin 33 //INPUTA:33 INPUTB:32
#define LED_PIN 26 //outa26 outb13

int num1;

float ain,vo,rf;

void setup(){
  // Serial Setting
  Serial.begin(115200);

  // Port Setting
  pinMode(press_pin, INPUT);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH);
}

void loop() {
  while (1)
  {
    delay(100);
    if(Serial.available() > 0)
    digitalWrite(LED_PIN, LOW);
    break;
  }

  while (1)
  {
  ain = analogRead(press_pin);
  vo = ain * 3.3 / 4096;
  rf = 10000 * vo / (3.3 - vo);
  Serial.print( rf );
  Serial.println( "g" );
  delay( 1000 );
  //break;
}}
