# 🚀 Guía de Instalación - AppEco Sistema de Reciclaje Inteligente

## 📋 Requisitos del Sistema

### Python
- **Versión requerida**: Python 3.11.2
- **Ambos entornos**: Windows (desarrollo) y Raspberry Pi 4B (producción)

### Hardware Mínimo
- **Raspberry Pi 4B**: 8GB RAM recomendado
- **Cámara USB**: Compatible con OpenCV
- **Lector NFC**: Compatible con pyscard
- **Conexión a Internet**: Para Firebase y MQTT

---

## 🖥️ Instalación en Windows (Desarrollo)

### Método 1: Script Automático
```bash
# Ejecutar el script de instalación
install_windows.bat
```

### Método 2: Instalación Manual
```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
.venv\Scripts\activate.bat

# 3. Actualizar pip
python -m pip install --upgrade pip setuptools wheel

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Para desarrollo con TensorFlow completo
pip install tensorflow==2.14.0
```

### Verificación en Windows
```bash
# Activar entorno virtual
.venv\Scripts\activate.bat

# Verificar instalación
python -c "
import cv2, numpy, pygame, firebase_admin, paho.mqtt.client as mqtt
import tensorflow as tf
print('✅ Todas las dependencias instaladas correctamente')
print('TensorFlow:', tf.__version__)
print('OpenCV:', cv2.__version__)
"
```

---

## 🍓 Instalación en Raspberry Pi 4B (Producción)

### Método 1: Script Automático
```bash
# Hacer ejecutable el script
chmod +x install_raspberry_pi.sh

# Ejecutar instalación
./install_raspberry_pi.sh
```

### Método 2: Instalación Manual
```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias del sistema
sudo apt install -y python3-pip python3-venv python3-dev \
    libopencv-dev python3-opencv libasound2-dev portaudio19-dev \
    pcscd libpcsclite-dev libpcsclite1 swig libssl-dev libffi-dev \
    build-essential cmake pkg-config

# 3. Configurar servicio NFC
sudo systemctl enable pcscd
sudo systemctl start pcscd

# 4. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 5. Instalar dependencias Python
pip install -r requirements.txt
```

### Verificación en Raspberry Pi
```bash
# Activar entorno virtual
source .venv/bin/activate

# Verificar instalación
python3 -c "
import cv2, numpy, pygame, firebase_admin, paho.mqtt.client as mqtt
import tflite_runtime.interpreter as tflite
print('✅ Todas las dependencias instaladas correctamente')
print('OpenCV:', cv2.__version__)
print('TensorFlow Lite: OK')
"
```

---

## 📦 Dependencias Principales

### Versiones Específicas para Python 3.11.2

| Librería | Versión | Propósito |
|----------|---------|-----------|
| `firebase-admin` | 6.4.0 | Conexión con Firebase |
| `paho-mqtt` | 1.6.1 | Comunicación MQTT |
| `opencv-python` | 4.8.1.78 | Procesamiento de imágenes |
| `numpy` | 1.24.3 | Operaciones matemáticas |
| `pygame` | 2.5.2 | Reproducción de audio |
| `pyscard` | 2.1.1 | Lectura de tarjetas NFC |
| `tflite-runtime` | 2.14.0 | IA optimizada para RPi |
| `tensorflow` | 2.14.0 | IA completa (solo Windows) |
| `requests` | 2.31.0 | Peticiones HTTP |
| `Pillow` | 10.0.1 | Procesamiento de imágenes |

---

## 🔧 Configuración Post-Instalación

### 1. Archivos de Configuración
```bash
# Verificar que existan estos archivos:
config/resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json
modelo/keras_model.h5  # o model.tflite
modelo/labels.txt
sounds/plastico1.mp3
sounds/aluminio1.mp3
```

### 2. Permisos en Raspberry Pi
```bash
# Agregar usuario al grupo video para cámara
sudo usermod -a -G video $USER

# Verificar permisos NFC
sudo systemctl status pcscd
```

### 3. Variables de Entorno (Opcional)
```bash
# Crear archivo .env
MQTT_BROKER=tu_broker_mqtt
MQTT_USER=tu_usuario
MQTT_PASSWORD=tu_password
FIREBASE_DB_URL=tu_url_firebase
```

---

## 🚀 Ejecución del Sistema

### Windows
```bash
# Activar entorno virtual
.venv\Scripts\activate.bat

# Ejecutar aplicación
python app.py
```

### Raspberry Pi
```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar aplicación
python3 app.py
```

---

## 🔍 Solución de Problemas

### Error: "No module named 'cv2'"
```bash
# Reinstalar OpenCV
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

### Error: "NFC no disponible"
```bash
# En Raspberry Pi
sudo systemctl restart pcscd
pcsc_scan  # Verificar lectores NFC

# En Windows: Instalar drivers del lector NFC
```

### Error: "TensorFlow Lite no disponible"
```bash
# En Raspberry Pi
pip install tflite-runtime==2.14.0

# En Windows (para desarrollo)
pip install tensorflow==2.14.0
```

### Error: "Cámara no disponible"
```bash
# Verificar cámara
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# En Raspberry Pi: Verificar permisos
sudo usermod -a -G video $USER
```

---

## 📊 Verificación del Sistema

### Comandos de Diagnóstico
```bash
# Verificar Python
python --version  # Debe ser 3.11.2

# Verificar dependencias
python -c "import cv2, numpy, pygame, firebase_admin, paho.mqtt.client as mqtt; print('✅ OK')"

# Verificar cámara
python -c "import cv2; cap = cv2.VideoCapture(0); print('Cámara:', cap.isOpened()); cap.release()"

# Verificar NFC (Raspberry Pi)
pcsc_scan

# Verificar TensorFlow Lite
python -c "import tflite_runtime.interpreter as tflite; print('✅ TensorFlow Lite OK')"
```

---

## 🔄 Actualización del Sistema

### Actualizar Dependencias
```bash
# Activar entorno virtual
source .venv/bin/activate  # Linux
# o
.venv\Scripts\activate.bat  # Windows

# Actualizar pip
pip install --upgrade pip

# Actualizar dependencias
pip install --upgrade -r requirements.txt
```

### Actualizar Código
```bash
# Desde el repositorio Git
git pull origin main

# Reiniciar aplicación
python app.py  # o python3 app.py en RPi
```

---

## 📝 Notas Importantes

1. **Python 3.11.2**: Es crucial usar exactamente esta versión para compatibilidad
2. **TensorFlow Lite**: Optimizado para Raspberry Pi, más ligero que TensorFlow completo
3. **OpenCV 4.8.1.78**: Versión estable y compatible con RPi 4B
4. **NFC**: Requiere servicio pcscd activo en Raspberry Pi
5. **Cámara**: Verificar permisos y conectividad USB
6. **Firebase**: Archivo de credenciales debe estar en `config/`

---

## 🆘 Soporte

Si encuentras problemas:
1. Verifica la versión de Python: `python --version`
2. Revisa los logs de error en la consola
3. Verifica que todos los archivos de configuración estén presentes
4. Ejecuta los comandos de diagnóstico
5. Consulta la sección de solución de problemas

¡Tu sistema AppEco está listo para funcionar! 🎉
