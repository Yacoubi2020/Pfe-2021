#include "CO2Sensor.h"
#include <OneWire.h>             //bibliothèque capteur Dalas
#include <DallasTemperature.h>  //bibliothèque capteur Dalas
#include <DHT.h>                //bibliothèque capteur DHT22       
#include <TroykaMQ.h>          // bibliothèque de capteur gaz MQ2
//les dux bibliothèque qui gérer la communication via bluetooth entre esp32 et raspberry pi 
#include <Arduino.h>           
#include "BluetoothSerial.h"  
// les deux bibliothèque pour l'afficheur oled 
#include <Adafruit_GFX.h> 
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // Largeur de l'écran OLED en pixels
#define SCREEN_HEIGHT 64 //Hauteur de l'écran OLED en pixels
//initialisation d'un objet de class Adafruit_SSD1306 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define PIN_MQ2  26   // nom de broche pour connecter MQ2
#define PIN_DHT22 15
#define PIN_DALAS 4
#define Flamme_PIN 5
#define MQ7_PIN 32
#define PIN_PLUIE 23
#define PIN_CO2 25
CO2Sensor co2Sensor(PIN_CO2, 0.99, 100);  //coefficient d'inertie

BluetoothSerial SerialBT;
String name = "hci0";
String MACadd = "B8:27:EB:9E:93:CA";  //Adress mac de raspberry pi
uint8_t address[6]  = {0xB8, 0x27, 0xEB, 0x9E, 0x93, 0xCA};  //crée adress dans un tableau en hexadecimal
bool connected;



  MQ2 mq2(PIN_MQ2); // crée un objet pour travailler avec le capteur mq2   //12
  DHT dht22(PIN_DHT22,DHT22); // crée un objet pour travailler avec le capteur DHT
 //declaration des variable de type float
 float lpg, co, smoke, Hydrogen;    
 float tem1,tem2;
 float d;  //Fahrenheit.
 float hum1,hum2;
 float flame;   //valeur de flamme
 
OneWire oneWire(PIN_DALAS);
DallasTemperature sensors(&oneWire);

void setup() {
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { //  Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
   Serial.begin(115200);  //Moniteur série
   mq2.calibrate();
   co2Sensor.calibrate();
   Serial.println("Ro = " + String(mq2.getRo()));

  dht22.begin();    //Démarrage de l'objet 
  sensors.begin();  //Démarrage de l'objet

  display.clearDisplay(); //Effacer le tampon
  SerialBT.begin("pfe_bluetooth"); //Nom de l'appareil Bluetooth
  Serial.println("L'appareil a démarré");
  connected = SerialBT.connect(address);  //connect avec raspberry pi 
  }
  void loop(){

  int val = co2Sensor.read();
  Serial.print("CO2 value: ");
    Serial.println(val);
    delay(2000);
  //capteur DALAS
   sensors.requestTemperatures();
   float tc=sensors.getTempCByIndex(0); //°C
   //capteur DHT22
   tem1=dht22.readTemperature(); // temperateur  capteur DHT22 AM2302
   
   
   hum1=dht22.readHumidity();   //humidity capteur DHT22 AM2302
   
   Serial.println("LPG: " + String(mq2.readLPG()) + " ppm");
   Serial.println("Methane: " + String(mq2.readMethane()) + " ppm");
   Serial.println("Smoke: " + String(mq2.readSmoke()) + " ppm");
   Serial.println("Hydrogen: " + String(mq2.readHydrogen()) + " ppm");
   lpg=mq2.readLPG();
   co=mq2.readMethane();
   smoke=mq2.readSmoke();
   Hydrogen=mq2.readHydrogen();
  //capteur Flamme
  int c=digitalRead(Flamme_PIN);
Serial.println(c);
  //capteur MQ7 
  int mQ7 =analogRead(MQ7_PIN); 
  int mq7=map(mQ7,0,4096,20,2000);    //  convertir la valeur analogique à une valeur de gaz en ppm   
  //capteur de pluie
  int pluies1=digitalRead(PIN_PLUIE);

  //capteur MG811
    
    //afficher la valeur de co2 sur moniteur serie
   
   String gpsString=String(tc);    //convertir la valeur de températeur de capteur DALAS  à String par exemple si TEMP=18>>TEMP="18"

   String gp=String(tem1); //convertir la valeur de températeur de DHT22 AM2302 à String par exemple 19="19"
   String pg=String(tem2); //convertir la valeur de températeur de DHT22 AM2302 à String par exemple 20="20"
   String humidite1=String(hum1);
   String flamme=String(c);
   String mq7final=String(mq7);
   String pluie=String(pluies1);
   String mg811=String(val);
   String lpgg=String(lpg);
   String cog=String(co);
   String smokeg=String(smoke);
     
     SerialBT.print(gpsString+":"+gp+":"+humidite1+":"+flamme+":"+mq7final+":"+pluie+":"+mg811+":"+lpgg+":"+cog+":"+smokeg);
    // delay(10000);  //Send a request every 10 

 //oled 
 //choisit la taille de contenue qui va afficher sur oled
  display.setTextSize(1);  
  //choisit le couleur  de contenue qui va afficher sur oled
  display.setTextColor(WHITE); 
  //placer le premier  élemntent de contunue sur la valeur de pixel (0,5) 
   display.setCursor(0,5);
  // Display static text
  display.print("_____________________");
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(3,5);
  // Display static text
  display.print("____________________");
  display.display();
  
  display.setTextSize(1);
  display.setTextColor(WHITE);
   
  display.setCursor(10,20);

  // afficher sur oled 
  display.print("temperature: ");
  //afficher la valeur de  température
  display.print( gp);
  //faire défiler le texte de gauche à droite  
  display.display();
  //choisit la taille de contenue qui va afficher sur oled
  display.setTextSize(1);
 //choisit le couleur  de contenue qui va afficher sur oled
  display.setTextColor(WHITE);
  //placer le premier  élemntent de contunue sur la valeur de pixel (10,30)
  display.setCursor(10,30);
  // Display static text
  display.print("humidite: ");
  display.print(humidite1);

  display.display(); 
  delay(5000);
  //effacer la contenue 
   display.clearDisplay();
    //choisit la taille de nouvelle  contenue qui va afficher sur oled
  display.setTextSize(1);
  //choisit le couleur  de nouvelle contenue qui va afficher sur oled
  display.setTextColor(WHITE);
   //placer le premier  élemntent de  la nouvelle contunue sur la valeur de pixel (10,30)
  display.setCursor(0,5);
  // Display static text
  display.print("_____________________");
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(3,5);
  // Display static text
  display.print("____________________");
  display.display();
  display.setTextSize(1);
  display.setTextColor(WHITE);
   
  display.setCursor(10,20);

  // Display static text
  display.print("co ");
  //afficher la valeur de co de capteur MQ7
  display.print(mq7final);
  //faire défiler le texte de gauche à droite
  display.display();
 
  
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(10,30);
   //Display static text
   display.print("co2: ");
   //afficher la valeur de co2 de capteur mg811
    display.print(mg811);
   //faire défiler le texte de gauche à droite
   display.display(); 
   delay(2000);
   display.clearDisplay();
 }
