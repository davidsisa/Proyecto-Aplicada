int sensorPin = A0; 
int lecturaRaw = 0;
float humedadPercent = 0.0;
String estado;

void setup() {
  Serial.begin(9600);  
}

void loop() {
  lecturaRaw = analogRead(sensorPin); 
  humedadPercent = 100.0 - ((lecturaRaw / 1023.0) * 100.0);
  
  if (humedadPercent < 0) humedadPercent = 0;
  if (humedadPercent > 100) humedadPercent = 100;
  
  if (humedadPercent < 30) {
    estado = "Bajo";
  } else {
    estado = "Normal";
  }
  
  Serial.print("Humedad: ");
  Serial.print(humedadPercent, 2);
  Serial.print("%, Estado: ");
  Serial.println(estado);
  
  delay(2000);
}

