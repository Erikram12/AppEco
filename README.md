# 🚀 AppEco - Sistema de Reciclaje Inteligente

Sistema de reciclaje automatizado que utiliza inteligencia artificial para detectar materiales reciclables (plástico y aluminio) y otorgar puntos a los usuarios mediante tarjetas NFC.

## 🎯 Características Principales

- **🤖 Detección IA**: Clasificación automática de materiales con confianza ≥ 95%
- **📱 Interfaz NFC**: Sistema de puntos mediante tarjetas NFC
- **📷 Cámara Continua**: Detección en tiempo real con cámara siempre activa
- **🔥 Firebase**: Base de datos en tiempo real para usuarios y puntos
- **📡 MQTT**: Comunicación con sensores IoT
- **🔊 Audio**: Retroalimentación sonora para cada material
- **🗑️ Limpieza Automática**: Gestión automática de archivos temporales

## 🖥️ Requisitos del Sistema

### Windows (Desarrollo)
- Python 3.11.2
- Cámara web (Logitech Brio recomendada)
- Lector NFC compatible

### Raspberry Pi 4B (Producción)
- Raspberry Pi 4B (8GB RAM recomendada)
- Python 3.11.2
- Cámara USB o módulo de cámara
- Lector NFC compatible
- Sistema operativo: Raspberry Pi OS

## 📦 Instalación

### 🪟 Windows (Desarrollo)

1. **Clonar el repositorio:**
```bash
git clone <URL_DEL_REPOSITORIO>
cd AppEco
```

2. **Ejecutar instalación automática:**
```bash
install_windows.bat
```

3. **Configurar Firebase:**
   - Copiar tu archivo de credenciales de Firebase a `config/`
   - Renombrar como `resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json`

4. **Ejecutar la aplicación:**
```bash
python app.py
```

### 🍓 Raspberry Pi (Producción)

1. **Clonar el repositorio:**
```bash
git clone <URL_DEL_REPOSITORIO>
cd AppEco
```

2. **Ejecutar instalación automática:**
```bash
chmod +x install_raspberry_pi.sh
./install_raspberry_pi.sh
```

3. **Configurar Firebase:**
   - Copiar tu archivo de credenciales de Firebase a `config/`
   - Renombrar como `resiclaje-39011-firebase-adminsdk-fbsvc-433ec62b6c.json`

4. **Ejecutar la aplicación:**
```bash
python app.py
```

## 🔧 Configuración Manual

### Dependencias Principales

```bash
# Instalar dependencias base
pip install -r requirements.txt

# Para Windows (desarrollo)
pip install tensorflow==2.14.0

# Para Raspberry Pi (producción)
# TensorFlow Lite ya está incluido en requirements.txt
```

### Configuración de Cámara

El sistema detecta automáticamente cámaras disponibles. Para Logitech Brio:
- Resolución: 1920x1080
- FPS: 30
- Índices probados: 0, 1, 2

### Configuración NFC

Asegúrate de que tu lector NFC sea compatible con `pyscard`:
```bash
# Verificar lectores NFC disponibles
python -c "from smartcard.System import readers; print(readers())"
```

## 🚀 Uso del Sistema

### Flujo de Trabajo

1. **Inicio**: La cámara se activa automáticamente
2. **Detección**: El sistema detecta materiales en tiempo real
3. **Validación**: Solo materiales con confianza ≥ 95% son procesados
4. **NFC**: Usuario pasa tarjeta para recibir puntos
5. **Limpieza**: Imágenes se eliminan automáticamente

### Materiales Soportados

- **Plástico**: 20 puntos
- **Aluminio**: 30 puntos
- **Vacío**: No otorga puntos, cierra sesión después de 5 segundos

### Timeouts

- **Material Pendiente**: 30 segundos para pasar tarjeta NFC
- **Vacío Prolongado**: 5 segundos para cerrar sesión automáticamente

## 📁 Estructura del Proyecto

```
AppEco/
├── app.py                          # Aplicación principal
├── config/
│   ├── config.py                   # Configuración general
│   └── firebase-credentials.json   # Credenciales Firebase
├── modelo/
│   ├── keras_model.h5             # Modelo de IA (Windows)
│   ├── model.tflite               # Modelo de IA (Raspberry Pi)
│   └── labels.txt                 # Etiquetas del modelo
├── services/
│   ├── camera_service.py          # Servicio de cámara e IA
│   ├── firebase_service.py        # Servicio de base de datos
│   ├── mqtt_service.py            # Servicio MQTT
│   └── nfc_service.py             # Servicio NFC
├── sounds/
│   ├── plastico1.mp3              # Audio para plástico
│   └── aluminio1.mp3              # Audio para aluminio
├── ui/
│   └── ui_components.py           # Componentes de interfaz
├── requirements.txt                # Dependencias Python
├── install_windows.bat            # Instalación Windows
├── install_raspberry_pi.sh        # Instalación Raspberry Pi
└── README.md                      # Este archivo
```

## 🔍 Solución de Problemas

### Cámara No Detectada
```bash
# Verificar cámaras disponibles
python -c "import cv2; print([i for i in range(10) if cv2.VideoCapture(i).isOpened()])"
```

### Error de Modelo IA
```bash
# Verificar archivos del modelo
ls -la modelo/
# Debe contener: keras_model.h5, model.tflite, labels.txt
```

### Error de NFC
```bash
# Verificar lectores NFC
python -c "from smartcard.System import readers; print(readers())"
```

### Error de Firebase
```bash
# Verificar credenciales
ls -la config/
# Debe contener el archivo de credenciales JSON
```

## 📊 Monitoreo del Sistema

### Logs de Detección
```
🎁 Material pendiente: plastico - Esperando NFC
📷 Imagen guardada: captura_20241201_143022.jpg
✅ Usuario recibió 20 puntos! Total: 150
🗑️ Imagen eliminada: captura_20241201_143022.jpg
```

### Estadísticas de Cámara
```python
stats = camera_service.get_detection_stats()
print(f"Cámara activa: {stats['camera_continuously_active']}")
print(f"Detecciones: {stats['total_detections']}")
print(f"Materiales válidos: {stats['valid_materials']}")
```

## 🔄 Actualizaciones

Para actualizar el sistema:

```bash
# En Raspberry Pi
cd AppEco
git pull origin main
python app.py
```

## 📞 Soporte

Para reportar problemas o solicitar características:
1. Crear un issue en el repositorio
2. Incluir logs de error
3. Especificar sistema operativo y versión de Python

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

---

**Desarrollado para promover el reciclaje mediante tecnología inteligente** 🌱♻️
