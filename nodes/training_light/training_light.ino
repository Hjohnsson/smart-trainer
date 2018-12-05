//Correct file

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>

#define _ESPLOGLEVEL_ 0

//const char* ssid = "ASUS";
//const char* password =  "hermanebest123!";
//const char* mqttServer = "192.168.1.200";

const char* ssid = "SmartTrainer";
const char* password =  "runforestrun";
const char* mqttServer = "192.168.1.20";

//IPAddress mqttServer(192,168,4,1);
const int mqttPort = 1883;
const char* mqttUser = "guest";
const char* mqttPassword = "guest";
char message_buff[100];
String state = "";
String node = "NODE-3";

String node_on = node + "-ON";
String node_off = node + "-OFF";
String node_standby = node + "-STANDBY";

#define echoPin D3 // Echo Pin
#define trigPin D4 // Trigger Pin

#define NUM_PIXELS 24

long duration, distance; // Duration used to calculate distance
int max_time = 500;
int loops = 0;
int distance_limit = 20;
int ind1;
String message;

 
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

void setColor(uint32_t color) {
  for (int i = 0; i < NUM_PIXELS; i++) {
    pixels.setPixelColor(i, color);
    pixels.show();
    //delay(5);
  }
}


void measure_distance(int distance_limit) {
  distance = 100;
  while (distance > distance_limit)
  {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    //Calculate the distance (in cm) based on the speed of sound.
    distance = duration/58.2;
    Serial.println(distance);
    delay(10);
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
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("Training-NODE-3")) {
 
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
 
    }
  }
 
  client.subscribe("wemos");
 
}
 
void loop() {
  client.loop();
}
