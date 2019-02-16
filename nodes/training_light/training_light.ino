//Correct file

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#include <SharpDistSensor.h>
#define _ESPLOGLEVEL_ 0

const char* ssid = "ASUS";
const char* password =  "hermanebest123!";
const char* mqttServer = "192.168.1.200";

//const char* ssid = "SmartTrainer";
//const char* password =  "runforestrun";
//const char* mqttServer = "192.168.1.20";
//const char* mqttServer = "192.168.4.1";

//IPAddress mqttServer(192,168,4,1);
const int mqttPort = 1883;
const char* mqttUser = "guest";
const char* mqttPassword = "guest";
char message_buff[100];
String state = "";
String node = "NODE-1";

String node_online = node + "-ONLINE";
String node_on = node + "-ON";
String node_off = node + "-OFF";
String node_standby = node + "-STANDBY";

#define echoPin D3 // Echo Pin
#define trigPin D4 // Trigger Pin

#define NUM_PIXELS 24

long duration, distance; // Duration used to calculate distance
int max_time = 1500;
int loops = 0;
int distance_limit = 100;
int ind1;
String message;

// Analog pin to which the sensor is connected
const byte sensorPin = A0;

// Window size of the median filter (odd number, 1 = no filtering)
const byte medianFilterWindowSize = 3;

// Create an object instance of the SharpDistSensor class
SharpDistSensor sensor(sensorPin, medianFilterWindowSize);
 
WiFiClient espClient;
PubSubClient client(espClient);
Adafruit_NeoPixel pixels(NUM_PIXELS, D1, NEO_GRB | NEO_KHZ800);

void start_sq() {
  for (int x=0; x <= 5; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 100, 0);
      pixels.show();
      delay(20);
    }
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 0, 0);
      pixels.show();
      delay(20);
    }
  }
  for (int i = 0; i < NUM_PIXELS; i++) {
    pixels.setPixelColor(i, 0, 0, 100);
    pixels.show();
    //delay(20);
  }
}

void finish_sq() {
  for (int x=0; x <= 10; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 200, 0);
      pixels.show();
      //delay(1);
    }
    delay(150);
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 0, 0);
      pixels.show();
      //delay(1);
    }
    delay(150);
  }
//  for (int i = 0; i < NUM_PIXELS; i++) {
//    pixels.setPixelColor(i, 0, 0, 100);
//    pixels.show();
//    //delay(20);
//  }
}

void connected_sq() {
  for (int x=0; x <= 1; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 200, 0);
      pixels.show();
      //delay(1);
    }
    delay(150);
    for (int i = 0; i < NUM_PIXELS; i++) {
      pixels.setPixelColor(i, 0, 0, 0);
      pixels.show();
      //delay(1);
    }
    delay(150);
  }
}

void disconnected_sq() {
  pixels.setPixelColor(0, 100, 0, 0);
  pixels.setPixelColor(8, 100, 0, 0);
  pixels.setPixelColor(16, 100, 0, 0);
  pixels.show();
}


void setColor(uint32_t color) {
  for (int i = 0; i < NUM_PIXELS; i++) {
    pixels.setPixelColor(i, color);
    pixels.show();
    //delay(5);
  }
}


void measure_distance(int distance_limit) {
  distance = sensor.getDist();
  distance = 1000;
  while (distance > distance_limit)
  {
    uint32_t t1 = micros();
    distance = sensor.getDist();
    Serial.println(distance);
    delay(1);
    uint32_t t2 = micros();
    //Serial.println(t2-t1);
    loops = loops + 1;
    if ( max_time < loops) {
      loops = 0;
      Serial.println("Max time reached, breaking");
      //digitalWrite(LED_BUILTIN,HIGH);
      setColor(pixels.Color(0, 0, 0));
      break;
    }
  }
  //digitalWrite(LED_BUILTIN,HIGH);
  loops = 0;
  setColor(pixels.Color(0, 0, 0));
}
// handles message arrived on subscribed topic(s)
void callback(char* topic, byte* payload, unsigned int length) {

  int i = 0;
  
  // create character buffer with ending null terminator (string)
  for(i=0; i<length; i++) {
    message_buff[i] = payload[i];
  }
  message_buff[i] = '\0';
  String msgString = String(message_buff);
  Serial.println(msgString);

  // find message and distance
  ind1 = msgString.indexOf(';');  //finds location of first ,
  message = msgString.substring(0, ind1);   //captures first data String
  distance_limit = msgString.substring(ind1+1).toInt();   //captures first data String

  if (message==node_on) {
    setColor(pixels.Color(100, 0, 0));
    //state = msgString;
    measure_distance(distance_limit);
    client.publish(topic, (char*) node_off.c_str(), false);
    
  } else if (message=="OFF") {
    setColor(pixels.Color(0, 0, 0));
    
  } else if (message==node_off) {
    setColor(pixels.Color(0, 0, 0));
    
  } else if (message==node_standby) {
    Serial.println("standby");
    setColor(pixels.Color(255, 255, 0));
    
  } else if (message=="START") {
    start_sq();
    
  } else if (message=="FINISHED") {
    finish_sq();
  }
  //Serial.println("Payload: " + msgString);
}
 
void setup() {
  //pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  //digitalWrite(LED_BUILTIN,HIGH);
  pixels.begin();
  Serial.begin(9600);
  setColor(pixels.Color(0, 0, 0));
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    disconnected_sq();
    delay(1000);
    Serial.println("Connecting to WiFi..");
    setColor(pixels.Color(0, 0, 0));
    delay(1000);
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("Training-NODE-1","wemos",2,0,"NODE-1-OFFLINE")) {
 
      Serial.println("connected");
      connected_sq();
      client.publish("wemos", "NODE-1-ONLINE", false);  
 
    } else {
      setColor(pixels.Color(0, 0, 0));
      Serial.print("failed with state ");
      Serial.println(client.state());
      disconnected_sq();
      delay(2000);
 
    }
  }
 
  client.subscribe("wemos");
 
}
 
void loop() {
  client.loop();
}
