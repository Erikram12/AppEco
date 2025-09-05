"""
Servicio MQTT para el Sistema de Reciclaje Inteligente
=====================================================

Este módulo maneja toda la comunicación MQTT, incluyendo la conexión,
suscripción a topics y procesamiento de mensajes de los contenedores.
"""

import json
import ssl
import time
import threading
import paho.mqtt.client as mqtt
from config.config import (
    MQTT_BROKER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPIC,
    MQTT_MATERIAL_TOPIC, MQTT_ESP32_TOPIC,
    ALLOWED_TARGETS, ALLOWED_STATES
)


class MQTTService:
    """Servicio para manejar la comunicación MQTT"""

    def __init__(self, message_callback=None, status_callback=None):
        """
        Inicializa el servicio MQTT

        Args:
            message_callback: Función callback para procesar mensajes recibidos
            status_callback: Función callback para actualizar el estado en la UI
        """
        self.message_callback = message_callback
        self.status_callback = status_callback
        self.client = None
        self.connected = False
        self.thread = None

    def start(self):
        """Inicia la conexión MQTT en un hilo separado"""
        self.thread = threading.Thread(target=self._connect_and_listen, daemon=True)
        self.thread.start()

    def _connect_and_listen(self):
        """Conecta al broker MQTT y escucha mensajes"""
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="raspi-updater")
            self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

            # Configurar SSL
            ctx = ssl.create_default_context()
            self.client.tls_set_context(ctx)

            # Configurar callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message

            # Conectar
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=30)
            self.client.loop_forever()

        except Exception as e:
            self.connected = False
            if self.status_callback:
                self.status_callback(f"❌ Error MQTT: {e}", "error")

    def _on_connect(self, client, userdata, flags, reason_code, properties=None):
        """Callback cuando se conecta al broker MQTT"""
        try:
            if reason_code == 0:
                client.subscribe(MQTT_TOPIC, qos=1)
                self.connected = True
                if self.status_callback:
                    self.status_callback(f"✅ MQTT suscrito a: {MQTT_TOPIC}", "success")
            else:
                self.connected = False
                if self.status_callback:
                    self.status_callback(f"❌ Error conexión MQTT: {reason_code}", "error")
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ on_connect error: {e}", "error")

    def _on_message(self, client, userdata, msg):
        """Callback cuando se recibe un mensaje MQTT"""
        try:
            print(f"📨 Mensaje recibido en topic: {msg.topic}")
            print(f"📦 Payload: {msg.payload.decode('utf-8')}")

            # Decodificar JSON
            data = json.loads(msg.payload.decode("utf-8"))

            # Validar payload
            is_valid, error_msg = self._validate_payload(data)
            if not is_valid:
                print("⚠️ Payload rechazado:", error_msg, data)
                return

            # Extraer datos
            target = data["target"]  # contePlastico | conteAluminio
            percent = int(data["percent"])  # 0..100
            state = data["state"]  # Vacío | Medio | Lleno
            distance_cm = float(data.get("distance_cm", 0.0))
            device_id = data.get("deviceId", "unknown")
            timestamp = data.get("ts", 0)

            print(f"✅ Datos válidos: {target} -> {state} ({percent}%) - Dist: {distance_cm}cm")

            # Llamar callback con los datos procesados
            if self.message_callback:
                self.message_callback({
                    'target': target,
                    'percent': percent,
                    'state': state,
                    'distance_cm': distance_cm,
                    'device_id': device_id,
                    'timestamp': timestamp
                })

        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
            print(f"📦 Payload recibido: {msg.payload}")
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ on_message error: {e}", "error")
            print(f"❌ Error en on_message: {e}")

    def _validate_payload(self, data):
        """
        Valida que el payload del mensaje MQTT sea correcto

        Args:
            data: Diccionario con los datos del mensaje

        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Validar que sea un diccionario
            if not isinstance(data, dict):
                return False, "payload no es un diccionario"

            # Validar target
            if data.get("target") not in ALLOWED_TARGETS:
                return False, f"target invalido: {data.get('target')} (permitidos: {ALLOWED_TARGETS})"

            # Validar state
            if data.get("state") not in ALLOWED_STATES:
                return False, f"state invalido: {data.get('state')} (permitidos: {ALLOWED_STATES})"

            # Validar percent
            try:
                p = int(data.get("percent"))
                if not (0 <= p <= 100):
                    return False, f"percent fuera de rango: {p} (debe ser 0-100)"
            except (ValueError, TypeError):
                return False, f"percent invalido: {data.get('percent')}"

            # Validar campos opcionales
            if "distance_cm" in data:
                try:
                    float(data["distance_cm"])
                except (ValueError, TypeError):
                    return False, f"distance_cm invalido: {data.get('distance_cm')}"

            if "deviceId" in data and not isinstance(data["deviceId"], str):
                return False, f"deviceId debe ser string: {data.get('deviceId')}"

            if "ts" in data:
                try:
                    int(data["ts"])
                except (ValueError, TypeError):
                    return False, f"ts invalido: {data.get('ts')}"

        except Exception as e:
            return False, f"error validando payload: {e}"

        return True, "ok"

    def is_connected(self):
        """Verifica si está conectado al broker MQTT"""
        return self.connected

    def send_material_detected(self, material, points, image_path=None):
        """
        Envía un material detectado a la ESP32 para mover compartimientos
        
        Args:
            material: Tipo de material detectado (plastico, aluminio)
            points: Puntos otorgados por el material
            image_path: Ruta de la imagen capturada (opcional)
        """
        if not self.connected or not self.client:
            print("❌ MQTT no conectado - No se puede enviar material")
            return False
        
        try:
            # Crear mensaje para ESP32
            message = {
                "action": "move_compartment",
                "material": material.lower(),
                "points": points,
                "timestamp": int(time.time()),
                "source": "raspberry_pi"
            }
            
            # Agregar ruta de imagen si existe
            if image_path:
                message["image_path"] = image_path
            
            # Convertir a JSON
            payload = json.dumps(message)
            
            # Publicar en tópico de materiales detectados
            result = self.client.publish(MQTT_MATERIAL_TOPIC, payload, qos=1)
            
            if result.rc == 0:
                print(f"✅ Material enviado a ESP32: {material} ({points} pts)")
                print(f"📡 Tópico: {MQTT_MATERIAL_TOPIC}")
                print(f"📦 Payload: {payload}")
                return True
            else:
                print(f"❌ Error enviando material: {result.rc}")
                return False
                
        except Exception as e:
            print(f"❌ Error enviando material a ESP32: {e}")
            return False

    def send_esp32_command(self, command, data=None):
        """
        Envía un comando específico a la ESP32
        
        Args:
            command: Comando a enviar (move_plastico, move_aluminio, reset, status)
            data: Datos adicionales del comando (opcional)
        """
        if not self.connected or not self.client:
            print("❌ MQTT no conectado - No se puede enviar comando")
            return False
        
        try:
            # Crear mensaje de comando
            message = {
                "command": command,
                "timestamp": int(time.time()),
                "source": "raspberry_pi"
            }
            
            # Agregar datos adicionales si existen
            if data:
                message.update(data)
            
            # Convertir a JSON
            payload = json.dumps(message)
            
            # Publicar en tópico de comandos ESP32
            result = self.client.publish(MQTT_ESP32_TOPIC, payload, qos=1)
            
            if result.rc == 0:
                print(f"✅ Comando enviado a ESP32: {command}")
                print(f"📡 Tópico: {MQTT_ESP32_TOPIC}")
                print(f"📦 Payload: {payload}")
                return True
            else:
                print(f"❌ Error enviando comando: {result.rc}")
                return False
                
        except Exception as e:
            print(f"❌ Error enviando comando a ESP32: {e}")
            return False

    def disconnect(self):
        """Desconecta del broker MQTT"""
        if self.client:
            self.client.disconnect()
            self.connected = False
