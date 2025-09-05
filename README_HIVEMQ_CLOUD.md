# Configuración HiveMQ Cloud - Sistema de Reciclaje

## ☁️ HiveMQ Cloud vs Mosquitto

### Diferencias Clave:
- **HiveMQ Cloud**: Servicio en la nube, SSL/TLS obligatorio, client_id único
- **Mosquitto**: Broker local, SSL opcional, client_id reutilizable

## 🔧 Configuraciones Específicas para HiveMQ Cloud

### 1. SSL/TLS Configurado
```python
ctx = ssl.create_default_context()
ctx.check_hostname = False  # Requerido para HiveMQ Cloud
ctx.verify_mode = ssl.CERT_NONE  # Requerido para HiveMQ Cloud
```

### 2. Client ID Único
```python
import uuid
client_id = f"raspi-recycling-{uuid.uuid4().hex[:8]}"
```

### 3. Configuraciones de Conexión
```python
keepalive = 60  # HiveMQ Cloud recomienda 60s
clean_session = True  # Limpiar sesión al desconectar
```

## 📡 Tópicos Configurados

### Materiales Detectados
- **Tópico**: `material/detectado`
- **QoS**: 1 (At least once)
- **Retain**: False
- **Formato**: JSON

### Comandos ESP32
- **Tópico**: `reciclaje/esp32/command`
- **QoS**: 1 (At least once)
- **Retain**: False
- **Formato**: JSON

### Niveles de Contenedores
- **Tópico**: `reciclaje/+/nivel`
- **QoS**: 1 (At least once)
- **Retain**: False
- **Formato**: JSON

## 🚀 Cómo Usar

### 1. Diagnóstico HiveMQ Cloud
```bash
python3 mqtt_diagnostic.py
```

**Salida esperada**:
```
✅ Conexión HiveMQ Cloud exitosa!
📡 Broker: 2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud:8883
👤 Usuario: ramsi
🆔 Client ID: raspi-recycling-a1b2c3d4
📥 Suscrito a: material/detectado
📥 Suscrito a: reciclaje/esp32/command
```

### 2. Prueba de Envío
```bash
python3 test_material_send.py
```

**Salida esperada**:
```
✅ Conectado a HiveMQ Cloud
🆔 Client ID: test-sender-e5f6g7h8
📤 Enviando material: PLÁSTICO
✅ Plástico enviado a material/detectado
📤 Enviando material: ALUMINIO
✅ Aluminio enviado a material/detectado
🎉 PRUEBA EXITOSA
```

### 3. Inicio del Sistema
```bash
python3 start_with_mqtt_check.py
```

## 🔍 Características Específicas de HiveMQ Cloud

### 1. Reconexión Automática
- **Reintentos**: Hasta 10 intentos
- **Delay**: 5 segundos entre intentos
- **Clean Session**: True (limpia sesión al reconectar)

### 2. Monitoreo de Conexión
- **Health Check**: Cada 30 segundos
- **Timeout**: 10 segundos para conexión
- **Publish Timeout**: 5 segundos

### 3. Logging Detallado
- **Conexión**: Logs de conexión/desconexión
- **Mensajes**: Logs de envío/recepción
- **Errores**: Logs detallados de errores

## 📊 Formato de Mensajes

### Material Detectado
```json
{
  "action": "move_compartment",
  "material": "plastico|aluminio",
  "points": 20|30,
  "timestamp": 1703123456,
  "source": "raspberry_pi",
  "image_path": "/path/to/image.jpg"
}
```

### Comando ESP32
```json
{
  "command": "move_plastico|move_aluminio|reset|status",
  "timestamp": 1703123456,
  "source": "raspberry_pi"
}
```

## 🐛 Solución de Problemas HiveMQ Cloud

### Error: "Client ID already in use"
**Solución**: El sistema genera automáticamente client_id únicos
```python
client_id = f"raspi-recycling-{uuid.uuid4().hex[:8]}"
```

### Error: "SSL/TLS connection failed"
**Solución**: Configuración SSL específica para HiveMQ Cloud
```python
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
```

### Error: "Connection timeout"
**Solución**: Aumentar tiempo de espera
```python
time.sleep(5)  # Más tiempo para HiveMQ Cloud
```

### Error: "Authentication failed"
**Solución**: Verificar credenciales
- Usuario: `ramsi`
- Contraseña: `Erikram2025`
- Broker: `2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud:8883`

## 🔄 Flujo de Trabajo HiveMQ Cloud

```
1. Aplicación inicia
2. Genera client_id único
3. Conecta a HiveMQ Cloud con SSL/TLS
4. Suscribe a tópicos
5. Material detectado
6. Envía a tópico material/detectado
7. ESP32 recibe y mueve compartimiento
8. Usuario pasa NFC
9. Sistema otorga puntos
```

## 📈 Monitoreo y Métricas

### Logs de Conexión
```
✅ Conectado a HiveMQ Cloud - Client ID: raspi-recycling-a1b2c3d4
📡 Broker: 2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud:8883
👤 Usuario: ramsi
```

### Logs de Envío
```
✅ Material enviado a ESP32: plastico (20 pts)
📡 Tópico: material/detectado
📦 Payload: {"action":"move_compartment","material":"plastico",...}
```

### Logs de Error
```
❌ Error conectando a HiveMQ Cloud: Authentication failed
⚠️ Desconectado inesperadamente de HiveMQ Cloud: 4
```

## 🛠️ Configuración Avanzada

### Variables de Entorno
```bash
export MQTT_BROKER="2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud"
export MQTT_PORT="8883"
export MQTT_USER="ramsi"
export MQTT_PASSWORD="Erikram2025"
export MQTT_MATERIAL_TOPIC="material/detectado"
```

### Configuración de Red
```bash
# Verificar conectividad
ping 2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud

# Verificar puerto SSL
telnet 2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud 8883
```

## 🎯 Ventajas de HiveMQ Cloud

1. **Confiabilidad**: Servicio en la nube con alta disponibilidad
2. **Escalabilidad**: Maneja múltiples conexiones simultáneas
3. **Seguridad**: SSL/TLS obligatorio
4. **Monitoreo**: Dashboard web para monitoreo
5. **Soporte**: Documentación y soporte técnico

## 📞 Soporte HiveMQ Cloud

- **Documentación**: https://www.hivemq.com/hivemq-cloud/
- **Dashboard**: https://console.hivemq.cloud/
- **Soporte**: support@hivemq.com

---

**Nota**: Esta configuración está optimizada específicamente para HiveMQ Cloud y puede requerir ajustes para otros brokers MQTT.
