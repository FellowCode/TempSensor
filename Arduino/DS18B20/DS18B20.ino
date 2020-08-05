// библиотека для работы с протоколом 1-Wire
#include <OneWire.h>
// библиотека для работы с датчиком DS18B20
#include <DallasTemperature.h>
 
// сигнальный провод датчика
#define ONE_WIRE_BUS 11
#define ONE_WIRE2_BUS 12
 
// создаём объект для работы с библиотекой OneWire
OneWire oneWire(ONE_WIRE_BUS);
OneWire oneWire2(ONE_WIRE2_BUS);
// создадим объект для работы с библиотекой DallasTemperature
DallasTemperature sensors(&oneWire);
DallasTemperature sensors2(&oneWire2);

DeviceAddress *sensorsUnique;
DeviceAddress *sensorsUnique2;
// создаём указатель массив для хранения адресов датчиков
// количество датчиков на шине
int countSensors, countSensors2;
 
// функция вывода адреса датчи

void printAddress(DeviceAddress address){
    for (int i=0; i<8; i++){
      if (address[i] < 16)
        Serial.print(0);
      Serial.print(address[i], HEX);
    }
}
 
void setup(){
  // инициализируем работу Serial-порта
  Serial.begin(115200);
  Serial.println("start");
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);
  // ожидаем открытия Serial-порта
  while(!Serial);
  // начинаем работу с датчиком
  sensors.begin();
  sensors2.begin();
  // выполняем поиск устройств на шине
  countSensors = sensors.getDeviceCount();
  countSensors2 = sensors2.getDeviceCount();
  
  Serial.print("Found sensors: ");
  Serial.println(countSensors + countSensors2);
  // выделяем память в динамическом массиве под количество обнаруженных сенсоров
  sensorsUnique = new DeviceAddress[countSensors];
  sensorsUnique2 = new DeviceAddress[countSensors2];
  // определяем в каком режиме питания подключены сенсоры
  /*if (sensors.isParasitePowerMode()) {
    Serial.println("Mode power is Parasite");
  } else {
    Serial.println("Mode power is Normal");
  }*/
 
  // делаем запрос на получение адресов датчиков
  for (int i = 0; i < countSensors; i++) {
    sensors.getAddress(sensorsUnique[i], i);
  }
  for (int i = 0; i < countSensors2; i++) {
    sensors2.getAddress(sensorsUnique2[i], i);
  }
  // выводим полученные адреса
  for (int i = 0; i < countSensors + countSensors2; i++) {
    Serial.print("Device ");
    Serial.print(i);
    Serial.print(" Address: ");
    if (i<countSensors)
      printAddress(sensorsUnique[i]);
    else
      printAddress(sensorsUnique2[i - countSensors]);
    Serial.println();
  }
  Serial.println();
  
  // устанавливаем разрешение всех датчиков в 12 бит
  for (int i = 0; i < countSensors; i++) {
    sensors.setResolution(sensorsUnique[i], 12);
  }
  // устанавливаем разрешение всех датчиков в 12 бит
  for (int i = 0; i < countSensors2; i++) {
    sensors2.setResolution(sensorsUnique2[i], 12);
  }
}
 
void loop(){
  // переменная для хранения температуры
  float temperature[countSensors + countSensors2];
  // отправляем запрос на измерение температуры всех сенсоров
  sensors.requestTemperatures();
  sensors2.requestTemperatures();
  // считываем данные из регистра каждого датчика по очереди
  for (int i = 0; i < countSensors; i++) {
    temperature[i] = sensors.getTempCByIndex(i);
  }
  for (int i = 0; i < countSensors2; i++) {
    temperature[i + countSensors] = sensors2.getTempCByIndex(i);
  }
  // выводим температуру в Serial-порт по каждому датчику
  for (int i = 0; i < countSensors + countSensors2; i++) {
    Serial.print("Device:");
    Serial.print(i);
    Serial.print(";Address:");
    if (i<countSensors)
      printAddress(sensorsUnique[i]);
    else
      printAddress(sensorsUnique2[i-countSensors]);
    Serial.print(";TempC:");
    Serial.print(temperature[i]);
    Serial.println();
  }
  Serial.println();
  // ждём одну секунду
  delay(1000);
}
