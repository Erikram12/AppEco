"""
Configuración para Pantalla LCD TFT 320x480
==========================================

Script para configurar la pantalla LCD TFT en Raspberry Pi
y optimizar la visualización para el sistema de reciclaje.
"""

import os
import subprocess
import sys

def configure_lcd_display():
    """
    Configura la pantalla LCD TFT para el sistema de reciclaje
    """
    print("🖥️ Configurando pantalla LCD TFT 320x480...")
    
    try:
        # Configurar resolución de pantalla
        os.system("sudo raspi-config nonint do_resolution 320 480")
        
        # Configurar para pantalla completa
        os.system("sudo raspi-config nonint do_boot_behaviour B4")
        
        # Deshabilitar cursor parpadeante
        os.system("sudo sh -c 'echo \"setterm -cursor off\" >> /etc/rc.local'")
        
        # Configurar rotación de pantalla si es necesario
        # os.system("sudo sh -c 'echo \"display_rotate=1\" >> /boot/config.txt'")
        
        print("✅ Configuración de pantalla completada")
        print("📝 Reinicia el sistema para aplicar los cambios")
        
    except Exception as e:
        print(f"❌ Error configurando pantalla: {e}")

def optimize_for_lcd():
    """
    Optimiza el sistema para pantalla LCD
    """
    print("⚙️ Optimizando sistema para LCD...")
    
    try:
        # Deshabilitar salvapantallas
        os.system("sudo systemctl disable lightdm")
        
        # Configurar para iniciar automáticamente
        os.system("sudo systemctl enable appeco.service")
        
        # Optimizar memoria para pantalla pequeña
        os.system("sudo sh -c 'echo \"gpu_mem=16\" >> /boot/config.txt'")
        
        print("✅ Optimización completada")
        
    except Exception as e:
        print(f"❌ Error optimizando sistema: {e}")

def create_startup_script():
    """
    Crea script de inicio para la aplicación
    """
    print("📝 Creando script de inicio...")
    
    startup_script = """#!/bin/bash
# Script de inicio para Sistema de Reciclaje Inteligente

# Configurar pantalla
export DISPLAY=:0
xset s off
xset -dpms
xset s noblank

# Iniciar aplicación
cd /home/pi/AppEco
python3 app.py
"""
    
    try:
        with open("/home/pi/start_recycling.sh", "w") as f:
            f.write(startup_script)
        
        os.system("chmod +x /home/pi/start_recycling.sh")
        
        # Crear servicio systemd
        service_content = """[Unit]
Description=Sistema de Reciclaje Inteligente
After=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/AppEco
ExecStart=/home/pi/start_recycling.sh
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
"""
        
        with open("/etc/systemd/system/appeco.service", "w") as f:
            f.write(service_content)
        
        print("✅ Script de inicio creado")
        
    except Exception as e:
        print(f"❌ Error creando script de inicio: {e}")

if __name__ == "__main__":
    print("🖥️ Configurador de Pantalla LCD para Sistema de Reciclaje")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "configure":
            configure_lcd_display()
        elif sys.argv[1] == "optimize":
            optimize_for_lcd()
        elif sys.argv[1] == "startup":
            create_startup_script()
        elif sys.argv[1] == "all":
            configure_lcd_display()
            optimize_for_lcd()
            create_startup_script()
        else:
            print("Uso: python3 lcd_setup.py [configure|optimize|startup|all]")
    else:
        print("Uso: python3 lcd_setup.py [configure|optimize|startup|all]")
        print("\nOpciones:")
        print("  configure - Configura la resolución de pantalla")
        print("  optimize  - Optimiza el sistema para LCD")
        print("  startup   - Crea script de inicio automático")
        print("  all       - Ejecuta todas las configuraciones")
