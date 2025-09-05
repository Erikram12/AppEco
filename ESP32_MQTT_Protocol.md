# Protocolo MQTT para Comunicación con ESP32

## 📡 Tópicos MQTT

### 1. Material Detectado
**Tópico**: `reciclaje/material/detected`  
**Dirección**: Raspberry Pi → ESP32  
**Propósito**: Enviar material detectado para mover compartimientos

#### Formato del Mensaje:
```json
{
  "action": "move_compartment",
  "material": "plastico|aluminio",
  "points": 20|30,
  "timestamp": 1234567890,
  "source": "raspberry_pi",
  "image_path": "/path/to/image.jpg"  // Opcional
}
```

#### Ejemplo:
```json
{
  "action": "move_compartment",
  "material": "plastico",
  "points": 20,
  "timestamp": 1703123456,
  "source": "raspberry_pi",
  "image_path": "/tmp/material_20231221_143456.jpg"
}
```

### 2. Comandos ESP32
**Tópico**: `reciclaje/esp32/command`  
**Dirección**: Raspberry Pi → ESP32  
**Propósito**: Enviar comandos específicos a la ESP32

#### Comandos Disponibles:

##### Mover Compartimiento de Plástico
```json
{
  "command": "move_plastico",
  "timestamp": 1234567890,
  "source": "raspberry_pi"
}
```

##### Mover Compartimiento de Aluminio
```json
{
  "command": "move_aluminio",
  "timestamp": 1234567890,
  "source": "raspberry_pi"
}
```

##### Reset del Sistema
```json
{
  "command": "reset",
  "timestamp": 1234567890,
  "source": "raspberry_pi"
}
```

##### Solicitar Estado
```json
{
  "command": "status",
  "timestamp": 1234567890,
  "source": "raspberry_pi"
}
```

## 🔄 Flujo de Comunicación

### 1. Detección de Material
```
Raspberry Pi detecta material → Envía a ESP32 → ESP32 mueve compartimiento
```

### 2. Secuencia Completa
```
1. Cámara detecta material (plástico/aluminio)
2. Raspberry Pi envía mensaje a tópico "reciclaje/material/detected"
3. ESP32 recibe mensaje y mueve compartimiento correspondiente
4. ESP32 confirma movimiento (opcional)
5. Usuario pasa tarjeta NFC
6. Sistema otorga puntos
```

## 📋 Código ESP32 de Ejemplo

### Suscripción a Tópicos
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "TU_WIFI";
const char* password = "TU_PASSWORD";
const char* mqtt_server = "2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  // Configurar MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  // Suscribirse a tópicos
  client.subscribe("reciclaje/material/detected");
  client.subscribe("reciclaje/esp32/command");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  if (String(topic) == "reciclaje/material/detected") {
    handleMaterialDetected(message);
  } else if (String(topic) == "reciclaje/esp32/command") {
    handleCommand(message);
  }
}

void handleMaterialDetected(String message) {
  // Parsear JSON (usar ArduinoJson library)
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, message);
  
  String material = doc["material"];
  int points = doc["points"];
  
  Serial.println("Material detectado: " + material);
  Serial.println("Puntos: " + String(points));
  
  // Mover compartimiento según material
  if (material == "plastico") {
    movePlasticoCompartment();
  } else if (material == "aluminio") {
    moveAluminioCompartment();
  }
}

void handleCommand(String message) {
  DynamicJsonDocument doc(512);
  deserializeJson(doc, message);
  
  String command = doc["command"];
  
  if (command == "move_plastico") {
    movePlasticoCompartment();
  } else if (command == "move_aluminio") {
    moveAluminioCompartment();
  } else if (command == "reset") {
    resetSystem();
  } else if (command == "status") {
    sendStatus();
  }
}

void movePlasticoCompartment() {
  Serial.println("Moviendo compartimiento de plástico...");
  // Código para mover servo/motor del compartimiento de plástico
  // Ejemplo: servo1.write(90); delay(1000); servo1.write(0);
}

void moveAluminioCompartment() {
  Serial.println("Moviendo compartimiento de aluminio...");
  // Código para mover servo/motor del compartimiento de aluminio
  // Ejemplo: servo2.write(90); delay(1000); servo2.write(0);
}

void resetSystem() {
  Serial.println("Reseteando sistema...");
  // Código para resetear posiciones de compartimientos
}

void sendStatus() {
  // Enviar estado actual de la ESP32
  String status = "{\"status\":\"ok\",\"compartimientos\":\"ready\"}";
  client.publish("reciclaje/esp32/status", status.c_str());
}
```

## 🔧 Configuración MQTT

### Credenciales
- **Broker**: `2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud`
- **Puerto**: `8883` (SSL/TLS)
- **Usuario**: `ramsi`
- **Contraseña**: `Erikram2025`

### QoS
- **Nivel**: 1 (At least once)
- **Propósito**: Garantizar entrega de mensajes

## 📊 Monitoreo

### Logs en Raspberry Pi
```
✅ Material enviado a ESP32: plastico (20 pts)
📡 Tópico: reciclaje/material/detected
📦 Payload: {"action":"move_compartment","material":"plastico","points":20,"timestamp":1703123456,"source":"raspberry_pi"}
```

### Logs en ESP32
```
Material detectado: plastico
Puntos: 20
Moviendo compartimiento de plástico...
```

## 🚨 Manejo de Errores

### Errores Comunes
1. **MQTT desconectado**: Verificar conexión WiFi y broker
2. **Mensaje no recibido**: Verificar tópico y QoS
3. **JSON inválido**: Verificar formato del mensaje
4. **Compartimiento no se mueve**: Verificar hardware y código

### Códigos de Error
- `0`: Éxito
- `1`: Error de conexión
- `2`: Error de suscripción
- `3`: Error de publicación

## 🔄 Flujo de Datos Completo

```
┌─────────────────┐    MQTT     ┌──────────────┐    Hardware    ┌─────────────┐
│  Raspberry Pi   │ ──────────► │    ESP32     │ ──────────────► │ Compartimientos │
│                 │             │              │                 │             │
│ 1. Detecta      │             │ 2. Recibe    │                 │ 3. Mueve    │
│    material     │             │    mensaje   │                 │    compart.  │
│                 │             │              │                 │             │
│ 4. Envía a      │             │ 5. Confirma  │                 │ 6. Posición │
│    Firebase     │             │    movimiento│                 │    final    │
└─────────────────┘             └──────────────┘                 └─────────────┘
```

## 📝 Notas Importantes

1. **Seguridad**: Usar SSL/TLS para conexión MQTT
2. **Reintentos**: Implementar lógica de reintento en ESP32
3. **Validación**: Validar JSON antes de procesar
4. **Logging**: Registrar todos los movimientos para debugging
5. **Timeouts**: Implementar timeouts para movimientos de compartimientos

## 🛠️ Librerías Requeridas

### Arduino IDE
- `WiFi` (incluida)
- `PubSubClient` (instalar desde Library Manager)
- `ArduinoJson` (instalar desde Library Manager)

### Instalación
```
Tools → Manage Libraries → Search:
- PubSubClient by Nick O'Leary
- ArduinoJson by Benoit Blanchon
```

## 📞 Soporte

Para problemas con la comunicación MQTT:

1. Verificar logs en Raspberry Pi
2. Verificar logs en ESP32
3. Probar conexión MQTT con cliente externo
4. Verificar configuración de red
5. Revisar formato de mensajes JSON
