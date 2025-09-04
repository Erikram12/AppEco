#!/bin/bash

# Script de instalación mejorado para Raspberry Pi
# AppEco - Sistema de Reciclaje Inteligente

set -e  # Salir si hay algún error

echo "🚀 Instalando AppEco en Raspberry Pi..."
echo "📅 $(date)"
echo "🖥️ Sistema: $(uname -a)"
echo "🐍 Python: $(python3 --version)"

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encontró app.py. Ejecuta este script desde el directorio del proyecto."
    exit 1
fi

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
    pcscd \
    libpcsclite-dev \
    swig \
    libusb-1.0-0-dev \
    libssl-dev \
    libffi-dev \
    build-essential \
    git \
    pcsc-tools

# Verificar cámara
echo "📷 Verificando cámara..."
if ls /dev/video* 1> /dev/null 2>&1; then
    echo "✅ Cámara detectada: $(ls /dev/video*)"
else
    echo "⚠️ No se detectó cámara. Asegúrate de conectar una cámara USB."
fi

# Verificar lectores NFC
echo "📱 Verificando lectores NFC..."
if command -v pcsc_scan &> /dev/null; then
    echo "✅ PC/SC disponible"
else
    echo "⚠️ Instalando herramientas PC/SC..."
    sudo apt install -y pcsc-tools
fi

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "🔄 Entorno virtual existente detectado. Eliminando..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

# Actualizar pip
echo "📚 Actualizando pip..."
pip install --upgrade pip setuptools wheel

# Instalar dependencias Python
echo "📚 Instalando dependencias Python..."
pip install -r requirements.txt

# Verificar instalación
echo "🔍 Verificando instalación..."
python -c "import cv2; print(f'✅ OpenCV: {cv2.__version__}')"
python -c "import numpy; print(f'✅ NumPy: {numpy.__version__}')"
python -c "import pygame; print(f'✅ Pygame: {pygame.version.ver}')"
python -c "import firebase_admin; print('✅ Firebase Admin')"
python -c "import paho.mqtt.client; print('✅ MQTT')"

# Verificar modelo de IA
echo "🤖 Verificando modelo de IA..."
if [ -f "modelo/model.tflite" ]; then
    echo "✅ Modelo TensorFlow Lite encontrado"
else
    echo "⚠️ Modelo TensorFlow Lite no encontrado. Asegúrate de tener model.tflite en modelo/"
fi

if [ -f "modelo/labels.txt" ]; then
    echo "✅ Etiquetas del modelo encontradas"
else
    echo "⚠️ Archivo labels.txt no encontrado en modelo/"
fi

# Verificar archivos de audio
echo "🔊 Verificando archivos de audio..."
if [ -f "sounds/plastico1.mp3" ] && [ -f "sounds/aluminio1.mp3" ]; then
    echo "✅ Archivos de audio encontrados"
else
    echo "⚠️ Archivos de audio no encontrados en sounds/"
fi

# Configurar permisos
echo "🔐 Configurando permisos..."
chmod +x app.py
chmod +x install_raspberry_pi_improved.sh

# Crear directorio de logs
mkdir -p logs

# Configurar auto-inicio (opcional)
echo ""
read -p "¿Deseas configurar auto-inicio? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "⚙️ Configurando auto-inicio..."
    
    # Obtener directorio actual
    CURRENT_DIR=$(pwd)
    USER=$(whoami)
    
    # Crear servicio systemd
    sudo tee /etc/systemd/system/appeco.service > /dev/null <<EOF
[Unit]
Description=AppEco Sistema de Reciclaje Inteligente
After=network.target graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$CURRENT_DIR/venv/bin
Environment=DISPLAY=:0
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/app.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    sudo systemctl enable appeco.service
    
    echo "✅ Auto-inicio configurado"
    echo "📝 Comandos útiles:"
    echo "   - Iniciar: sudo systemctl start appeco"
    echo "   - Detener: sudo systemctl stop appeco"
    echo "   - Estado: sudo systemctl status appeco"
    echo "   - Logs: sudo journalctl -u appeco -f"
fi

# Crear script de inicio manual
echo "📝 Creando script de inicio manual..."
cat > start_appeco.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "🚀 Iniciando AppEco..."
python app.py
EOF
chmod +x start_appeco.sh

echo ""
echo "🎉 ¡Instalación completada exitosamente!"
echo ""
echo "📋 Resumen de la instalación:"
echo "   ✅ Sistema actualizado"
echo "   ✅ Dependencias instaladas"
echo "   ✅ Entorno virtual creado"
echo "   ✅ Dependencias Python instaladas"
echo "   ✅ Permisos configurados"
echo ""
echo "🚀 Para ejecutar la aplicación:"
echo "   Opción 1: ./start_appeco.sh"
echo "   Opción 2: source venv/bin/activate && python app.py"
echo ""
echo "⚠️ IMPORTANTE:"
echo "   1. Asegúrate de tener el archivo de credenciales de Firebase en config/"
echo "   2. Conecta tu cámara USB"
echo "   3. Conecta tu lector NFC"
echo "   4. Verifica que los archivos del modelo estén en modelo/"
echo ""
echo "🔧 Para verificar el sistema:"
echo "   - Cámara: ls /dev/video*"
echo "   - NFC: pcsc_scan"
echo "   - Python: source venv/bin/activate && python --version"
echo ""
echo "📞 Si tienes problemas, revisa los logs o contacta al desarrollador."
