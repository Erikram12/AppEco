#!/bin/bash
# ===========================================
# SCRIPT DE INSTALACIÓN PARA RASPBERRY PI 4B
# Sistema de Reciclaje Inteligente - AppEco
# ===========================================

echo "🚀 Iniciando instalación de AppEco en Raspberry Pi 4B..."
echo "📋 Python requerido: 3.11.2"
echo ""

# Verificar versión de Python
echo "🔍 Verificando versión de Python..."
python3 --version

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    libopencv-dev \
    python3-opencv \
    libasound2-dev \
    portaudio19-dev \
    pcscd \
    libpcsclite-dev \
    libpcsclite1 \
    swig \
    libssl-dev \
    libffi-dev \
    build-essential \
    cmake \
    pkg-config \
    libjpeg-dev \
    libtiff5-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran

# Habilitar y iniciar servicio PC/SC para NFC
echo "🎫 Configurando servicio NFC..."
sudo systemctl enable pcscd
sudo systemctl start pcscd

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias específicas para ARM64
echo "📚 Instalando dependencias de Python..."

# Instalar NumPy primero (requerido por OpenCV)
pip install numpy==1.24.3

# Instalar OpenCV
pip install opencv-python==4.8.1.78

# Instalar TensorFlow Lite Runtime para ARM64
pip install tflite-runtime==2.14.0

# Instalar otras dependencias
pip install \
    firebase-admin==6.4.0 \
    paho-mqtt==1.6.1 \
    pygame==2.5.2 \
    pyscard==2.1.1 \
    requests==2.31.0 \
    Pillow==10.0.1

# Verificar instalación
echo "✅ Verificando instalación..."
python3 -c "
import cv2
import numpy as np
import pygame
import firebase_admin
import paho.mqtt.client as mqtt
try:
    import tflite_runtime.interpreter as tflite
    print('✅ TensorFlow Lite: OK')
except ImportError:
    print('❌ TensorFlow Lite: Error')

try:
    from smartcard.System import readers
    print('✅ NFC (pyscard): OK')
except ImportError:
    print('❌ NFC (pyscard): Error')

print('✅ OpenCV:', cv2.__version__)
print('✅ NumPy:', np.__version__)
print('✅ Pygame:', pygame.version.ver)
print('✅ Firebase Admin: OK')
print('✅ MQTT: OK')
"

# Configurar permisos para cámara
echo "📷 Configurando permisos para cámara..."
sudo usermod -a -G video $USER

# Crear directorio para imágenes si no existe
mkdir -p images

# Configurar auto-inicio (opcional)
echo "🤔 ¿Deseas configurar auto-inicio del sistema? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "⚙️ Configurando auto-inicio..."
    
    # Crear script de inicio
    cat > start_appeco.sh << 'EOF'
#!/bin/bash
cd /home/pi/AppEco
source .venv/bin/activate
python3 app.py
EOF
    
    chmod +x start_appeco.sh
    
    # Agregar al crontab para auto-inicio
    (crontab -l 2>/dev/null; echo "@reboot /home/pi/AppEco/start_appeco.sh") | crontab -
    
    echo "✅ Auto-inicio configurado"
fi

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Reinicia la Raspberry Pi: sudo reboot"
echo "2. Clona tu repositorio en /home/pi/AppEco"
echo "3. Activa el entorno virtual: source .venv/bin/activate"
echo "4. Ejecuta la aplicación: python3 app.py"
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "- Activar entorno: source .venv/bin/activate"
echo "- Verificar NFC: pcsc_scan"
echo "- Verificar cámara: python3 -c 'import cv2; print(cv2.VideoCapture(0).isOpened())'"
echo "- Ver logs del sistema: journalctl -u pcscd"
echo ""
echo "⚠️ NOTAS IMPORTANTES:"
echo "- Asegúrate de tener Python 3.11.2 instalado"
echo "- Verifica que la cámara esté conectada"
echo "- Verifica que el lector NFC esté conectado"
echo "- El archivo de credenciales de Firebase debe estar en config/"
