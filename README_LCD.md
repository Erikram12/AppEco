# Configuración para Pantalla LCD TFT 320x480

## 📱 Pantalla LCD TFT 320x480

Este documento describe cómo configurar el Sistema de Reciclaje Inteligente para funcionar en una pantalla LCD TFT de resolución 320x480 píxeles en Raspberry Pi.

## 🎯 Características de la Interfaz LCD

### ✅ Optimizaciones Implementadas

- **Resolución**: 320x480 píxeles
- **Modo pantalla completa**: Sin bordes ni barras de título
- **Fuentes optimizadas**: Tamaños 8, 10 y 12 píxeles
- **Layout vertical**: Optimizado para pantalla pequeña
- **Información esencial**: Solo lo más importante visible
- **Sin scroll innecesario**: Interfaz compacta

### 📊 Elementos de la Interfaz

1. **Título**: "♻️ RECICLAJE INTELIGENTE"
2. **Estado del Sistema**: Mensaje principal de estado
3. **Material Pendiente**: Material detectado y puntos
4. **Estadísticas**: Contadores de plástico, aluminio y puntos totales
5. **Componentes**: Estado de NFC, cámara, MQTT y Firebase
6. **Log de Actividad**: Historial compacto de eventos

## 🚀 Instalación y Configuración

### 1. Configurar Pantalla LCD

```bash
# Ejecutar configuración completa
python3 lcd_setup.py all

# O configurar paso a paso
python3 lcd_setup.py configure  # Configurar resolución
python3 lcd_setup.py optimize   # Optimizar sistema
python3 lcd_setup.py startup    # Crear script de inicio
```

### 2. Configuración Manual (Opcional)

Si prefieres configurar manualmente:

```bash
# Configurar resolución
sudo raspi-config nonint do_resolution 320 480

# Configurar para pantalla completa
sudo raspi-config nonint do_boot_behaviour B4

# Deshabilitar cursor parpadeante
sudo sh -c 'echo "setterm -cursor off" >> /etc/rc.local'

# Optimizar memoria GPU
sudo sh -c 'echo "gpu_mem=16" >> /boot/config.txt'
```

### 3. Iniciar Aplicación

```bash
# Inicio manual
python3 app.py

# Inicio automático (después de configurar)
sudo systemctl enable appeco.service
sudo systemctl start appeco.service
```

## 🎨 Características de la Interfaz LCD

### 📱 Layout Optimizado

```
┌─────────────────────────────────┐
│ ♻️ RECICLAJE INTELIGENTE        │ ← Título
├─────────────────────────────────┤
│ 🔄 Sistema iniciado...          │ ← Estado
├─────────────────────────────────┤
│ ♻️ PLASTICO!                    │ ← Material detectado
│ 🎁 20 pts - Pase NFC            │ ← Puntos pendientes
├─────────────────────────────────┤
│ 🥤 5  🥫 3  🏆 150             │ ← Estadísticas
├─────────────────────────────────┤
│ 🎫 ✅ 📷 ✅ 📡 ✅ 🔥 ✅         │ ← Componentes
├─────────────────────────────────┤
│ 📊 ACTIVIDAD                    │ ← Log
│ [14:30] ♻️ PLASTICO (+20)       │
│ [14:29] 🥤 Plástico: 85% (Lleno)│
│ [14:28] ♻️ ALUMINIO (+30)       │
│ [14:27] 🥫 Aluminio: 60% (Medio)│
│ [14:26] 🔄 Sistema reiniciado...│
│ [14:25] ⏰ Tiempo agotado...    │
│ [14:24] ♻️ PLASTICO (+20)       │
│ [14:23] 🎫 Usuario autenticado  │
└─────────────────────────────────┘
```

### 🔧 Configuración de Fuentes

- **Título**: Arial 12px bold
- **Estado principal**: Arial 10px
- **Estadísticas**: Arial 8px bold
- **Componentes**: Arial 8px
- **Log**: Consolas 8px

### 🎨 Colores Optimizados

- **Fondo**: #2c3e50 (azul oscuro)
- **Marcos**: #34495e (gris azulado)
- **Texto**: #ecf0f1 (blanco)
- **Éxito**: #27ae60 (verde)
- **Error**: #e74c3c (rojo)
- **Advertencia**: #f39c12 (naranja)
- **Info**: #3498db (azul)

## ⚙️ Configuración Avanzada

### Rotación de Pantalla

Si necesitas rotar la pantalla:

```bash
# Rotar 90 grados
sudo sh -c 'echo "display_rotate=1" >> /boot/config.txt'

# Rotar 180 grados
sudo sh -c 'echo "display_rotate=2" >> /boot/config.txt'

# Rotar 270 grados
sudo sh -c 'echo "display_rotate=3" >> /boot/config.txt'
```

### Ajuste de Brillo

```bash
# Ajustar brillo (0-255)
echo 100 | sudo tee /sys/class/backlight/*/brightness
```

### Deshabilitar Salvapantallas

```bash
# Deshabilitar salvapantallas
sudo systemctl disable lightdm
sudo systemctl mask lightdm
```

## 🔄 Reinicio Automático

El sistema incluye reinicio automático cuando no se reclaman puntos en 10 segundos:

- **Timeout configurable**: 10 segundos (modificable en `config/config.py`)
- **Reinicio completo**: Limpia todos los estados
- **Notificación visual**: Muestra mensaje de reinicio
- **Detección continua**: Vuelve a detectar materiales

## 🐛 Solución de Problemas

### Pantalla en Blanco

```bash
# Verificar resolución
xrandr

# Forzar resolución
xrandr --output HDMI-1 --mode 320x480
```

### Fuentes Muy Pequeñas

Editar `config/config.py`:

```python
FONT_SIZE_SMALL = 10   # Aumentar de 8 a 10
FONT_SIZE_MEDIUM = 12  # Aumentar de 10 a 12
FONT_SIZE_LARGE = 14   # Aumentar de 12 a 14
```

### Interfaz No Se Ajusta

```bash
# Verificar resolución actual
xrandr --query

# Configurar resolución específica
xrandr --output HDMI-1 --mode 320x480 --rate 60
```

## 📱 Compatibilidad

### Pantallas Compatibles

- LCD TFT 320x480 (3.5")
- LCD TFT 480x320 (3.5" horizontal)
- Cualquier pantalla con resolución 320x480

### Raspberry Pi Compatibles

- Raspberry Pi 3B+
- Raspberry Pi 4B
- Raspberry Pi Zero 2W
- Raspberry Pi 5

## 🎯 Características Específicas

### Información Mostrada

1. **Estado del sistema** en tiempo real
2. **Material detectado** con puntos pendientes
3. **Contadores** de plástico, aluminio y puntos totales
4. **Estado de componentes** (NFC, cámara, MQTT, Firebase)
5. **Log de actividad** con timestamp

### Información Omitida

- Detalles de usuario (email)
- Información de sesión detallada
- Estadísticas de contenedores individuales
- Logs extensos de MQTT
- Información de debug

## 🚀 Rendimiento

### Optimizaciones

- **Pantalla completa**: Sin bordes ni decoraciones
- **Fuentes pequeñas**: Máximo contenido visible
- **Layout compacto**: Información esencial únicamente
- **Scroll mínimo**: Solo en log de actividad
- **Actualizaciones eficientes**: Solo elementos necesarios

### Uso de Memoria

- **GPU**: 16MB (configurado automáticamente)
- **RAM**: Mínimo impacto
- **CPU**: Optimizado para Raspberry Pi

## 📞 Soporte

Para problemas específicos de la pantalla LCD:

1. Verificar resolución con `xrandr`
2. Comprobar configuración en `config/config.py`
3. Revisar logs del sistema
4. Ejecutar `python3 lcd_setup.py all` para reconfigurar

---

**Nota**: Esta configuración está optimizada específicamente para pantallas LCD TFT de 320x480 píxeles y puede requerir ajustes para otras resoluciones.
