@echo off
REM ===========================================
REM SCRIPT DE INSTALACIÓN PARA WINDOWS
REM Sistema de Reciclaje Inteligente - AppEco
REM ===========================================

echo 🚀 Iniciando instalación de AppEco en Windows...
echo 📋 Python requerido: 3.11.2
echo.

REM Verificar versión de Python
echo 🔍 Verificando versión de Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado. Por favor instala Python 3.11.2
    pause
    exit /b 1
)

REM Crear entorno virtual
echo 🐍 Creando entorno virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual
echo ⚡ Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo ⬆️ Actualizando pip...
python -m pip install --upgrade pip setuptools wheel

REM Instalar dependencias
echo 📚 Instalando dependencias de Python...

REM Instalar NumPy primero
python -m pip install numpy==1.24.3

REM Instalar OpenCV
python -m pip install opencv-python==4.8.1.78

REM Instalar TensorFlow completo para Windows
python -m pip install tensorflow==2.14.0

REM Instalar otras dependencias
python -m pip install ^
    firebase-admin==6.4.0 ^
    paho-mqtt==1.6.1 ^
    pygame==2.5.2 ^
    pyscard==2.1.1 ^
    requests==2.31.0 ^
    Pillow==10.0.1

REM Verificar instalación
echo ✅ Verificando instalación...
python -c "
import cv2
import numpy as np
import pygame
import firebase_admin
import paho.mqtt.client as mqtt
try:
    import tensorflow as tf
    print('✅ TensorFlow:', tf.__version__)
except ImportError:
    print('❌ TensorFlow: Error')

try:
    from smartcard.System import readers
    print('✅ NFC (pyscard): OK')
except ImportError:
    print('❌ NFC (pyscard): Error - Instala drivers NFC')

print('✅ OpenCV:', cv2.__version__)
print('✅ NumPy:', np.__version__)
print('✅ Pygame:', pygame.version.ver)
print('✅ Firebase Admin: OK')
print('✅ MQTT: OK')
"

REM Crear directorio para imágenes si no existe
if not exist "images" mkdir images

echo.
echo 🎉 ¡Instalación completada!
echo.
echo 📋 PRÓXIMOS PASOS:
echo 1. Asegúrate de tener el archivo de credenciales de Firebase en config/
echo 2. Conecta la cámara USB
echo 3. Conecta el lector NFC (si tienes uno)
echo 4. Ejecuta la aplicación: python app.py
echo.
echo 🔧 COMANDOS ÚTILES:
echo - Activar entorno: .venv\Scripts\activate.bat
echo - Desactivar entorno: deactivate
echo - Verificar cámara: python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
echo.
echo ⚠️ NOTAS IMPORTANTES:
echo - Asegúrate de tener Python 3.11.2 instalado
echo - Para NFC en Windows, instala los drivers del lector
echo - El archivo de credenciales de Firebase debe estar en config/
echo - Si tienes problemas con OpenCV, reinstala: pip uninstall opencv-python && pip install opencv-python==4.8.1.78
echo.
pause
