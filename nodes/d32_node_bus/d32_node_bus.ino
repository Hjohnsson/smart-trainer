//Correct file

#include <WiFi.h>
#include <PubSubClient.h>
#include <NeoPixelBus.h>
#include <SharpDistSensor.h>
#define _ESPLOGLEVEL_ 0

//SSID of your network 
const char* ssid     = "ASUS";
const char* password = "hermanebest123!";
const char* mqttServer = "192.168.1.200";

//const char* ssid = "SmartTrainer";
//const char* password =  "runforestrun";
//const char* mqttServer = "192.168.1.20";  // used when cable are connected
//const char* mqttServer = "192.168.4.1";   // used when no cable are connected

//IPAddress mqttServer(192,168,4,1);
const int mqttPort = 1883;
const char* mqttUser = "guest";
const char* mqttPassword = "guest";
char message_buff[100];
String state = "";
String node = "NODE-6";

String node_online = node + "-ONLINE";
String node_on = node + "-ON";
String node_off = node + "-OFF";
String node_standby = node + "-STANDBY";
String node_id = node + "-ID";
String node_bat = "";

const uint16_t PixelCount = 24; // this example assumes 4 pixels, making it smaller will cause a failure
const uint8_t PixelPin = 23;  // make sure to set this to the correct pin, ignored for Esp8266

#define colorSaturation 128

RgbColor red(colorSaturation, 0, 0);
RgbColor green(0, colorSaturation, 0);
RgbColor blue(0, 0, colorSaturation);
RgbColor white(colorSaturation);
RgbColor black(0);

HslColor hslRed(red);
HslColor hslGreen(green);
HslColor hslBlue(blue);
HslColor hslWhite(white);
HslColor hslBlack(black);

//#define ledringPin 21
#define buzzer 4 // buzzer Pin
#define NUM_PIXELS 24

long duration; // Duration used to calculate distance
unsigned int distance;
int max_time = 1500;
int loops = 0;
int distance_limit = 100;
int ind1;
String message;

// Analog pin to which the sensor is connected
const byte sensorPin = A6;
// Window size of the median filter (odd number, 1 = no filtering)
const byte medianFilterWindowSize = 1;

// Battery 
// Voltage divider 
// Input voltage = 4.2
// R1 = 500
// R2 = 500
// input for vBatPin = max 2.1 volt 
// 2.1 volt of max 3.3 = 2400 input value
int vBatPin = A4;    // Read battery voltage, max 4096
float vBat = 0;  // 
float maxVBat = 2400; // 2.1 volt
float percentBat = 0; //
int battery = 0;
int returnbat = 0;

// Create an object instance of the SharpDistSensor class
SharpDistSensor sensor(sensorPin, medianFilterWindowSize);
 
WiFiClient Wclient;
PubSubClient client(Wclient);
NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod> strip(PixelCount, PixelPin);
//Adafruit_NeoPixel pixels(NUM_PIXELS, ledringPin, NEO_GRB | NEO_KHZ800);

void start_sq() {
  for (int x=0; x <= 5; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, green);
      strip.Show();
      delay(20);
    }
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, black);
      strip.Show();
      delay(20);
    }
  }
  for (int i = 0; i < NUM_PIXELS; i++) {
    strip.SetPixelColor(i, blue);
    strip.Show();
    //delay(20);
  }
  
}

void finish_sq() {
  for (int x=0; x <= 10; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, green);
      strip.Show();
      //delay(1);
    }
    delay(150);
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, black);
      strip.Show();
      //delay(1);
    }
    delay(150);
  }
//  for (int i = 0; i < NUM_PIXELS; i++) {
//    strip.SetPixelColor(i, 0, 0, 100);
//    strip.Show();
//    //delay(20);
//  }
}

void connected_sq() {
  for (int x=0; x <= 1; x++) {  
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, green);
      //strip.Show();
      //delay(1);
    }
    strip.Show();
    delay(150);
    for (int i = 0; i < NUM_PIXELS; i++) {
      strip.SetPixelColor(i, black);
      //strip.Show();
      //delay(1);
    }
    strip.Show();
    delay(150);
  }
}

void disconnected_sq() {
  strip.SetPixelColor(0, red);
  strip.SetPixelColor(8, red);
  strip.SetPixelColor(16, red);
  strip.Show();
}

void id_sq(int id) {
  for (int i = 0; i < id*2; i++) {
    strip.SetPixelColor(i, red);
    strip.Show();
    i++;
  }
  delay(10000);
  for (int i = 0; i < id*2; i++) {
    strip.SetPixelColor(i, black);
    strip.Show();
    i++;
  }
}

void setColor(RgbColor color) {
  for (int i = 0; i < NUM_PIXELS; i++) {
    strip.SetPixelColor(i, color);
    //delay(1);
    strip.Show();
  }
}

int battery_level() {
  // read the value from the sensor:
  vBat = analogRead(vBatPin);
  percentBat = vBat / maxVBat;
  Serial.println(percentBat * 100);
  battery = percentBat * 100;
  if ( battery > 100) {
    battery = 100;
  }
  //client.publish("wemos", (char*) String(battery).c_str(), false);
  return battery;
  //client.publish("wemos", (char*) node_off.c_str(), false);
}

void measure_distance(unsigned int distance_limit) {
  distance = sensor.getDist();
  delay(3);
  distance = sensor.getDist();
  delay(3);
  distance = 2000;
  while (distance > distance_limit)
  {
    uint32_t t1 = micros();
    distance = sensor.getDist();
    distance = distance;
    Serial.println(distance);
    delay(1);
    uint32_t t2 = micros();
    //Serial.println(t2-t1);
    loops = loops + 1;
    if ( max_time < loops) {
      loops = 0;
      Serial.println("Max time reached, breaking");
      //digitalWrite(LED_BUILTIN,HIGH);
      setColor(black);
      break;
    }
  }
  //digitalWrite(LED_BUILTIN,HIGH);
  loops = 0;
  setColor(black);
  digitalWrite(buzzer,HIGH);
  delay(10);
  digitalWrite(buzzer,LOW);
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
    setColor(red);
    //state = msgString;
    measure_distance(distance_limit);
    
    //battery = 100;
    

    client.publish("wemos", (char*) node_off.c_str(), false);
    
  } else if (message=="OFF") {
    setColor(black);
    
  } else if (message==node_off) {
    setColor(black);
    
  } else if (message==node_standby) {
    Serial.println("standby");
    setColor(blue);
    
  } else if (message=="START") {
    start_sq();
    
  } else if (message=="FINISHED") {
    finish_sq();
    
  } else if (message==node_id) {
    id_sq(distance_limit);
    
  } else if (message==node+"-BAT") {
    returnbat = battery_level();
    node_bat = node +"-VBAT;" + (String(returnbat));
    client.publish("wemos", (char*) node_bat.c_str(), false);
  }
}

void connect() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    disconnected_sq();
    Serial.println(WiFi.status());
    delay(1000);
    Serial.println("Connecting to WiFi..");
    setColor(black);
    delay(1000);
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("Training-NODE-6","wemos",2,0,"NODE-6-OFFLINE")) {
 
      Serial.println("Connected to mqtt server");
      connected_sq();
      client.publish("wemos", "NODE-6-ONLINE", false);  
 
    } else {
      setColor(black);
      Serial.print("failed with state ");
      Serial.println(client.state());
      disconnected_sq();
      delay(2000);
    }
  }
  client.subscribe("wemos");
  
}


void setup() {

  Serial.begin(9600);
  analogReadResolution(10);
  pinMode(buzzer, OUTPUT);
  
  strip.Begin();
  strip.Show();

  connect();
}
 
void loop() {
  if (!client.connected()) {
    connect();
  }
  client.loop();
}
