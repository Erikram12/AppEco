# 📚 Guía Completa para Subir AppEco a Git y Clonar en Raspberry Pi

## 🚀 Paso 1: Preparar el Repositorio Local

### 1.1 Inicializar Git (si no está inicializado)
```bash
# En tu directorio AppEco
git init
```

### 1.2 Agregar archivos al repositorio
```bash
# Agregar todos los archivos
git add .

# Verificar qué archivos se van a subir
git status
```

### 1.3 Hacer el primer commit
```bash
git commit -m "🚀 Versión inicial de AppEco - Sistema de Reciclaje Inteligente

- Detección IA con confianza ≥ 95%
- Cámara continua en tiempo real
- Sistema NFC para puntos
- Integración Firebase
- Limpieza automática de imágenes
- Compatible Windows y Raspberry Pi"
```

---

## 🌐 Paso 2: Crear Repositorio en GitHub/GitLab

### 2.1 Crear repositorio en GitHub
1. Ve a [GitHub.com](https://github.com)
2. Haz clic en "New repository"
3. Nombre: `AppEco` o `Sistema-Reciclaje-Inteligente`
4. Descripción: `Sistema de reciclaje automatizado con IA para detectar materiales y otorgar puntos via NFC`
5. **NO** marques "Initialize with README" (ya tienes uno)
6. Haz clic en "Create repository"

### 2.2 Conectar repositorio local con remoto
```bash
# Reemplaza TU_USUARIO con tu nombre de usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/AppEco.git

# Verificar conexión
git remote -v
```

### 2.3 Subir código a GitHub
```bash
# Subir código (primera vez)
git push -u origin main

# Si tienes problemas con la rama, usa:
git branch -M main
git push -u origin main
```

---

## 🍓 Paso 3: Clonar en Raspberry Pi

### 3.1 Conectar a Raspberry Pi
```bash
# Por SSH (recomendado)
ssh pi@IP_DE_TU_RASPBERRY_PI

# O directamente en la Raspberry Pi
```

### 3.2 Clonar el repositorio
```bash
# Navegar al directorio home
cd /home/pi

# Clonar el repositorio
git clone https://github.com/TU_USUARIO/AppEco.git

# Entrar al directorio
cd AppEco
```

### 3.3 Verificar archivos clonados
```bash
# Ver estructura del proyecto
ls -la

# Verificar archivos importantes
ls -la modelo/
ls -la config/
ls -la sounds/
```

---

## ⚙️ Paso 4: Instalación en Raspberry Pi

### 4.1 Ejecutar script de instalación
```bash
# Hacer ejecutable el script
chmod +x install_raspberry_pi_improved.sh

# Ejecutar instalación
./install_raspberry_pi_improved.sh
```

### 4.2 Configurar archivos faltantes
```bash
# Crear directorio config si no existe
mkdir -p config

# Copiar archivo de credenciales de Firebase
# (Debes copiarlo manualmente desde tu computadora)
scp config/resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json pi@IP_RASPBERRY_PI:/home/pi/AppEco/config/
```

### 4.3 Verificar instalación
```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar dependencias
python -c "import cv2, numpy, pygame, firebase_admin; print('✅ Todas las dependencias OK')"

# Verificar cámara
python -c "import cv2; cap = cv2.VideoCapture(0); print('✅ Cámara:', cap.isOpened()); cap.release()"

# Verificar NFC
pcsc_scan
```

---

## 🚀 Paso 5: Ejecutar la Aplicación

### 5.1 Inicio manual
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar aplicación
python app.py
```

### 5.2 Inicio automático (si configuraste auto-inicio)
```bash
# Iniciar servicio
sudo systemctl start appeco

# Ver estado
sudo systemctl status appeco

# Ver logs en tiempo real
sudo journalctl -u appeco -f
```

---

## 🔄 Paso 6: Actualizaciones Futuras

### 6.1 Actualizar desde tu computadora
```bash
# Hacer cambios en tu código
# ...

# Commit cambios
git add .
git commit -m "✨ Nueva funcionalidad: [descripción]"

# Subir cambios
git push origin main
```

### 6.2 Actualizar en Raspberry Pi
```bash
# En la Raspberry Pi
cd /home/pi/AppEco

# Detener aplicación si está corriendo
sudo systemctl stop appeco

# Actualizar código
git pull origin main

# Reiniciar aplicación
sudo systemctl start appeco
```

---

## 🛠️ Comandos Útiles

### Verificar estado del sistema
```bash
# Estado del servicio
sudo systemctl status appeco

# Logs de la aplicación
sudo journalctl -u appeco -f

# Verificar cámara
ls /dev/video*

# Verificar NFC
pcsc_scan

# Verificar Python
source venv/bin/activate && python --version
```

### Solución de problemas
```bash
# Reiniciar servicio
sudo systemctl restart appeco

# Ver logs de errores
sudo journalctl -u appeco --since "1 hour ago"

# Verificar permisos
ls -la /dev/video*
sudo usermod -a -G video pi
```

---

## 📋 Checklist de Verificación

### ✅ Antes de subir a Git:
- [ ] Archivo `.gitignore` configurado
- [ ] `README.md` actualizado
- [ ] Scripts de instalación funcionando
- [ ] Archivos sensibles excluidos (credenciales Firebase)
- [ ] Código probado en Windows

### ✅ En Raspberry Pi:
- [ ] Repositorio clonado correctamente
- [ ] Script de instalación ejecutado
- [ ] Credenciales Firebase copiadas
- [ ] Cámara detectada
- [ ] NFC funcionando
- [ ] Aplicación ejecutándose

### ✅ Funcionalidades:
- [ ] Detección IA funcionando
- [ ] Cámara continua activa
- [ ] NFC leyendo tarjetas
- [ ] Puntos otorgándose
- [ ] Audio reproduciéndose
- [ ] Limpieza de imágenes automática

---

## 🆘 Solución de Problemas Comunes

### Error: "No se puede conectar a GitHub"
```bash
# Configurar credenciales Git
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Usar token de acceso personal en lugar de contraseña
```

### Error: "Cámara no detectada"
```bash
# Verificar conexión USB
lsusb

# Verificar permisos
sudo usermod -a -G video pi
sudo chmod 666 /dev/video0
```

### Error: "NFC no funciona"
```bash
# Reiniciar servicio PC/SC
sudo systemctl restart pcscd

# Verificar lectores
pcsc_scan
```

### Error: "Firebase no conecta"
```bash
# Verificar archivo de credenciales
ls -la config/
cat config/resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json
```

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `sudo journalctl -u appeco -f`
2. Verifica la configuración: `./start_appeco.sh`
3. Consulta el README.md
4. Crea un issue en GitHub

---

**¡Tu sistema AppEco está listo para funcionar en Raspberry Pi!** 🎉
