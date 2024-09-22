const int ledPin = 9;  // Pin PWM para el LED
int ledState = LOW;     // Estado inicial del LED
int pwmValue = 0;       // Valor inicial del PWM

void setup() {
    pinMode(ledPin, OUTPUT);
    Serial.begin(115200);
    analogWrite(ledPin, 0);  // Asegúrate de que el LED esté apagado al inicio
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        if (command == "1") {  // Encender LED
            ledState = HIGH;
            analogWrite(ledPin, pwmValue);  // Mantiene el valor de PWM actual
            Serial.println("ENCENDIDO");
        } else if (command == "0") {  // Apagar LED
            ledState = LOW;
            analogWrite(ledPin, 0);  // Apagar el LED
            Serial.println("APAGADO");
        } else {
            pwmValue = command.toInt();
            if (pwmValue >= 1 && pwmValue <= 255) {
                analogWrite(ledPin, pwmValue);  // Ajusta el PWM
                if (ledState == LOW) {
                    ledState = HIGH;  // Cambia el estado a encendido si se ajusta el brillo
                    Serial.println("ENCENDIDO");
                }
            }
        }
        delay(50);  // Evitar comandos rápidos
    }
}
