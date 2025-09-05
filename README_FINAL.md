# Sistema de Reciclaje Inteligente - Estado Final

## ✅ Sistema Completamente Funcional

### 🎯 Características Implementadas

1. **Detección de Materiales con IA**:
   - Clasificación de plástico y aluminio
   - Confianza mínima del 95%
   - Detección de vacío para reinicio automático

2. **Comunicación MQTT con HiveMQ Cloud**:
   - Envío automático de materiales detectados a ESP32
   - Tópico: `material/detectado`
   - Formato JSON estructurado

3. **Interfaz LCD Optimizada**:
   - Resolución 320x480 píxeles
   - Modo pantalla completa
   - Información esencial únicamente

4. **Sistema de Puntos**:
   - Plástico: 20 puntos
   - Aluminio: 30 puntos
   - Integración con Firebase

5. **Reinicio Automático**:
   - Timeout de 10 segundos para reclamar puntos
   - Limpieza automática de estados

## 🚀 Cómo Usar

### Instalación
```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar sistema
python app.py
```

### Configuración MQTT
- **Broker**: HiveMQ Cloud
- **Tópico Materiales**: `material/detectado`
- **Tópico Comandos**: `reciclaje/esp32/command`
- **Tópico Niveles**: `reciclaje/+/nivel`

## 📡 Formato de Mensajes MQTT

### Material Detectado
```json
{
  "action": "move_compartment",
  "material": "plastico|aluminio",
  "points": 20|30,
  "timestamp": 1757091145,
  "source": "raspberry_pi",
  "image_path": "captura_20250905_105225.jpg"
}
```

### Comando ESP32
```json
{
  "command": "move_plastico|move_aluminio|reset|status",
  "timestamp": 1757091145,
  "source": "raspberry_pi"
}
```

## 🔄 Flujo de Trabajo

1. **Detección**: Cámara detecta material con IA
2. **Envío MQTT**: Material enviado a ESP32 automáticamente
3. **Movimiento**: ESP32 mueve compartimiento correspondiente
4. **NFC**: Usuario pasa tarjeta para recibir puntos
5. **Puntos**: Sistema otorga puntos y registra en Firebase
6. **Reinicio**: Timeout de 10s si no se reclaman puntos

## 📊 Logs del Sistema

### Conexión MQTT
```
✅ Conectado a HiveMQ Cloud - Client ID: raspi-recycling-8d05b8be
```

### Detección de Material
```
🤖 Clasificación IA: aluminio -> aluminio (Confianza: 96.0%)
✅ Material detectado - Reseteando contador de vacío
```

### Envío a ESP32
```
✅ Material enviado a ESP32: aluminio (30 pts)
📡 Tópico: material/detectado
📦 Payload: {"action": "move_compartment", "material": "aluminio", ...}
```

## 🎯 Estado del Sistema

- ✅ **MQTT**: Conectado a HiveMQ Cloud
- ✅ **IA**: TensorFlow funcionando correctamente
- ✅ **Cámara**: Detección continua activa
- ✅ **ESP32**: Comunicación establecida
- ✅ **Firebase**: Integración lista
- ✅ **UI**: Pantalla LCD optimizada

## 📋 Archivos Principales

- `app.py`: Aplicación principal
- `services/mqtt_service.py`: Comunicación MQTT
- `services/camera_service.py`: Detección con IA
- `services/firebase_service.py`: Base de datos
- `ui/ui_components.py`: Interfaz LCD
- `config/config.py`: Configuraciones

## 🔧 Configuración para Raspberry Pi

### Pantalla LCD
- Resolución: 320x480 píxeles
- Modo: Pantalla completa
- Fuentes: Optimizadas para pantalla pequeña

### MQTT
- Broker: HiveMQ Cloud
- SSL/TLS: Habilitado
- QoS: 1 (At least once)

### IA
- Modelo: TensorFlow Lite
- Confianza mínima: 95%
- Clases: plástico, aluminio, vacío

## 🎉 Resultado Final

El sistema está completamente funcional y listo para producción:

1. **Detección automática** de materiales con IA
2. **Comunicación MQTT** con ESP32 para mover compartimientos
3. **Interfaz LCD** optimizada para pantalla pequeña
4. **Sistema de puntos** integrado con Firebase
5. **Reinicio automático** por timeout
6. **Logging completo** para monitoreo

---

**Sistema probado y funcionando correctamente** ✅
