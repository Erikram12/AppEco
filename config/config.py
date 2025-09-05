"""
Configuración del Sistema de Reciclaje Inteligente
==================================================

Este módulo contiene todas las configuraciones, constantes y variables de entorno
utilizadas en el sistema de reciclaje.
"""

import os
import warnings

# =========================
# Configuración MQTT
# =========================
MQTT_BROKER = os.getenv("MQTT_BROKER", "2e139bb9a6c5438b89c85c91b8cbd53f.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USER", "ramsi")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "Erikram2025")  # ⚠️ cambia o usa env
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "reciclaje/+/nivel")  # + = cualquier deviceId

# =========================
# Configuración Firebase
# =========================
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL", "https://resiclaje-39011-default-rtdb.firebaseio.com/")
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH", "config/resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json")

# =========================
# Constantes del Sistema
# =========================
ALLOWED_STATES = {"Vacío", "Medio", "Lleno"}
ALLOWED_TARGETS = {"contePlastico", "conteAluminio"}

# =========================
# Configuración de Puntos
# =========================
POINTS_PLASTIC = 20
POINTS_ALUMINUM = 30

# =========================
# Configuración de Sesión
# =========================
SESSION_DURATION = 20  # segundos

# =========================
# Configuración de Timeout de Puntos
# =========================
POINTS_CLAIM_TIMEOUT = 10  # segundos para reclamar puntos antes del reinicio

# =========================
# Configuración de UI
# =========================
WINDOW_TITLE = "Sistema de Reciclaje Inteligente - Panel de Visualización"
WINDOW_SIZE = "900x700"
WINDOW_BG_COLOR = '#2c3e50'
FRAME_BG_COLOR = '#34495e'
TEXT_COLOR = '#ecf0f1'

# Colores para estados
STATUS_COLORS = {
    "success": "#27ae60",
    "error": "#e74c3c",
    "warning": "#f39c12",
    "info": "#3498db"
}

# Colores para contenedores
CONTAINER_COLORS = {
    "Lleno": "#e74c3c",    # Rojo
    "Medio": "#f39c12",    # Naranja
    "Vacío": "#27ae60"     # Verde
}

# Emojis para contenedores
CONTAINER_EMOJIS = {
    "Lleno": "🔴",
    "Medio": "🟡",
    "Vacío": "🟢"
}

# =========================
# Configuración de Logging
# =========================
warnings.filterwarnings("ignore", category=DeprecationWarning)
