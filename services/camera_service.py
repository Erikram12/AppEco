"""
Servicio de Cámara para el Sistema de Reciclaje Inteligente
==========================================================

Este módulo maneja la captura de imágenes y la clasificación de materiales
usando la cámara del sistema y un modelo de IA entrenado.
"""
import cv2
import numpy as np
import os
import time
import pygame
from datetime import datetime

# Imports compatibles con Python 3.11.2 y TensorFlow Lite
try:
    # Intentar importar TensorFlow Lite primero (para Raspberry Pi)
    import tflite_runtime.interpreter as tflite
    TFLITE_AVAILABLE = True
    print("✅ TensorFlow Lite disponible")
except ImportError:
    TFLITE_AVAILABLE = False
    print("⚠️ TensorFlow Lite no disponible, intentando TensorFlow completo...")
    try:
        from tensorflow.keras.models import load_model
        import tensorflow as tf
        TF_AVAILABLE = True
        print("✅ TensorFlow completo disponible")
    except ImportError:
        TF_AVAILABLE = False
        print("❌ Ni TensorFlow Lite ni TensorFlow completo están disponibles")

# Configurar numpy para evitar notación científica
np.set_printoptions(suppress=True)


class CameraService:
    """Servicio para manejar la cámara y clasificación de materiales con IA"""

    def __init__(self, status_callback=None):
        """
        Inicializa el servicio de cámara

        Args:
            status_callback: Función callback para actualizar el estado en la UI
        """
        self.status_callback = status_callback
        self.camera_available = False
        self.model_loaded = False
        self.model = None
        self.interpreter = None  # Para TensorFlow Lite
        self.class_names = []
        self.model_type = None  # 'tflite' o 'keras'

        # Variables para control de audio y tiempo
        self.last_prediction = ""
        self.last_audio_time = 0
        self.audio_cooldown = 6  # 6 segundos de espera entre audios
        
        # Variables para control de vacío prolongado
        self.empty_start_time = None
        self.empty_timeout = 5  # 5 segundos de vacío para cerrar sesión
        self.session_end_callback = None  # Callback para cerrar sesión
        
        # Variables para detección de cambios
        self.last_detected_material = None
        self.last_detection_time = 0
        self.detection_cooldown = 3  # 3 segundos entre detecciones del mismo material
        
        # Variables para cámara continua
        self.camera_cap = None  # Objeto de cámara que se mantiene abierto
        self.camera_continuously_active = False

        # Inicializar pygame mixer para audio
        try:
            pygame.mixer.init()
            self.audio_available = True
        except Exception as e:
            self.audio_available = False
            print(f"⚠️ Audio no disponible: {e}")

        # Verificar disponibilidad de cámara y modelo
        self._check_camera_availability()
        self._load_ai_model()
        
        # Iniciar cámara continua
        self._start_continuous_camera()

    def _check_camera_availability(self):
        """Verifica si la cámara está disponible"""
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    self.camera_available = True
                    print("✅ Cámara disponible")
                else:
                    self.camera_available = False
                    print("⚠️ Cámara no responde correctamente")
                cap.release()
            else:
                self.camera_available = False
                print("❌ No se puede abrir la cámara")
        except Exception as e:
            self.camera_available = False
            print(f"❌ Error verificando cámara: {e}")

    def _load_ai_model(self):
        """Carga el modelo de IA y las etiquetas - Compatible con Python 3.11.2"""
        try:
            # Verificar si existen los archivos del modelo
            if not os.path.exists("modelo/labels.txt"):
                self.model_loaded = False
                print("⚠️ Archivo modelo/labels.txt no encontrado")
                if self.status_callback:
                    self.status_callback("⚠️ Archivo modelo/labels.txt no encontrado", "warning")
                return

            # Cargar etiquetas
            self.class_names = open("modelo/labels.txt", "r").readlines()
            print(f"✅ Etiquetas cargadas: {len(self.class_names)} clases")

            # Intentar cargar modelo TensorFlow Lite primero (recomendado para Raspberry Pi)
            if TFLITE_AVAILABLE and os.path.exists("modelo/model.tflite"):
                try:
                    self.interpreter = tflite.Interpreter(model_path="modelo/model.tflite")
                    self.interpreter.allocate_tensors()
                    self.model_type = 'tflite'
                    self.model_loaded = True
                    print("✅ Modelo TensorFlow Lite cargado correctamente")
                    if self.status_callback:
                        self.status_callback("🤖 Modelo TensorFlow Lite cargado", "success")
                    return
                except Exception as e:
                    print(f"⚠️ Error cargando TensorFlow Lite: {e}")

            # Intentar cargar modelo Keras si TensorFlow Lite no está disponible
            if TF_AVAILABLE and os.path.exists("modelo/keras_model.h5"):
                try:
                    # Intentar cargar con configuración estándar
                    self.model = load_model("modelo/keras_model.h5", compile=False)
                    self.model_type = 'keras'
                    self.model_loaded = True
                    print("✅ Modelo Keras cargado correctamente")
                    if self.status_callback:
                        self.status_callback("🤖 Modelo Keras cargado", "success")
                    return
                except Exception as e1:
                    print(f"⚠️ Error cargando modelo Keras estándar: {e1}")
                    try:
                        # Intentar con custom_objects para compatibilidad
                        from tensorflow.keras.layers import DepthwiseConv2D, Dense, GlobalAveragePooling2D
                        from tensorflow.keras.models import Model
                        from tensorflow.keras.applications import MobileNetV2

                        # Custom objects para manejar incompatibilidades
                        def custom_depthwise_conv2d(*args, **kwargs):
                            kwargs.pop('groups', None)
                            kwargs.pop('bias_constraint', None)
                            kwargs.pop('depthwise_constraint', None)
                            kwargs.pop('activity_regularizer', None)
                            kwargs.pop('bias_regularizer', None)
                            kwargs.pop('depthwise_regularizer', None)
                            return DepthwiseConv2D(*args, **kwargs)

                        def custom_dense(*args, **kwargs):
                            kwargs.pop('input_shape', None)
                            kwargs.pop('input_dim', None)
                            return Dense(*args, **kwargs)

                        custom_objects = {
                            'DepthwiseConv2D': custom_depthwise_conv2d,
                            'Dense': custom_dense
                        }

                        self.model = load_model("modelo/keras_model.h5", compile=False, custom_objects=custom_objects)
                        self.model_type = 'keras'
                        self.model_loaded = True
                        print("✅ Modelo Keras cargado con custom_objects")
                        if self.status_callback:
                            self.status_callback("🤖 Modelo Keras cargado (compatibilidad)", "success")
                        return
                    except Exception as e2:
                        print(f"❌ Error cargando modelo Keras con custom_objects: {e2}")

            # Si no se pudo cargar ningún modelo
            self.model_loaded = False
            print("❌ No se pudo cargar ningún modelo de IA")
            if self.status_callback:
                self.status_callback("❌ Error cargando modelo de IA", "error")

        except Exception as e:
            self.model_loaded = False
            print(f"❌ Error cargando modelo de IA: {e}")
            if self.status_callback:
                self.status_callback(f"❌ Error cargando IA: {e}", "error")

    def capture_image(self, save_path=None):
        """
        Captura una imagen de la cámara continua

        Args:
            save_path: Ruta donde guardar la imagen (opcional)

        Returns:
            str: Ruta de la imagen capturada o None si falla
        """
        try:
            if not self.camera_continuously_active or self.camera_cap is None:
                if self.status_callback:
                    self.status_callback("❌ Cámara continua no disponible", "error")
                return None

            # Capturar frame de la cámara continua
            ret, frame = self.camera_cap.read()

            if not ret or frame is None:
                if self.status_callback:
                    self.status_callback("❌ Error capturando frame", "error")
                return None

            # Generar nombre de archivo si no se proporciona
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = f"captura_{timestamp}.jpg"

            # Guardar imagen
            success = cv2.imwrite(save_path, frame)

            if success:
                return save_path
            else:
                if self.status_callback:
                    self.status_callback("❌ Error guardando imagen", "error")
                return None

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error capturando imagen: {e}", "error")
            return None

    def classify_material(self, image_path):
        """
        Clasifica el material en la imagen usando IA - Compatible con Python 3.11.2

        Args:
            image_path: Ruta de la imagen a clasificar

        Returns:
            str: Tipo de material ("plastico" | "aluminio" | "vacio")
        """
        try:
            if not self.model_loaded:
                if self.status_callback:
                    self.status_callback("❌ Modelo de IA no disponible", "error")
                raise Exception("Modelo de IA no está cargado")

            if self.status_callback:
                self.status_callback("🤖 Clasificando material con IA...", "info")

            # Cargar y procesar la imagen
            image = cv2.imread(image_path)
            if image is None:
                raise Exception("No se pudo cargar la imagen")

            # Redimensionar la imagen a 224x224 píxeles
            image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

            # Convertir a array numpy y reestructurar para el modelo
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

            # Normalizar la imagen
            image = (image / 127.5) - 1

            # Realizar predicción según el tipo de modelo
            if self.model_type == 'tflite':
                # Usar TensorFlow Lite
                input_details = self.interpreter.get_input_details()
                output_details = self.interpreter.get_output_details()
                
                # Configurar entrada
                self.interpreter.set_tensor(input_details[0]['index'], image)
                
                # Ejecutar inferencia
                self.interpreter.invoke()
                
                # Obtener resultado
                prediction = self.interpreter.get_tensor(output_details[0]['index'])
                index = np.argmax(prediction[0])
                confidence_score = prediction[0][index]
                
            elif self.model_type == 'keras':
                # Usar Keras/TensorFlow
                prediction = self.model.predict(image, verbose=0)
                index = np.argmax(prediction)
                confidence_score = prediction[0][index]
            else:
                raise Exception("Tipo de modelo no reconocido")

            # Obtener nombre de clase
            if index < len(self.class_names):
                class_name = self.class_names[index]
                # Limpiar el nombre de la clase
                clean_class_name = class_name[2:].strip().lower()
            else:
                raise Exception(f"Índice de clase fuera de rango: {index} (máximo: {len(self.class_names)-1})")

            # Verificar nivel de confianza mínimo (95%)
            confidence_percent = np.round(confidence_score * 100)
            if confidence_percent < 95:
                if self.status_callback:
                    self.status_callback(f"⚠️ Confianza insuficiente: {confidence_percent}% (mínimo 95%)", "warning")
                print(f"⚠️ Confianza insuficiente: {confidence_percent}% (mínimo 95%)")
                raise Exception(f"Confianza insuficiente: {confidence_percent}% (mínimo 95%)")

            # Mapear a los tipos de material del sistema
            material = self._map_class_to_material(clean_class_name)

            if self.status_callback:
                self.status_callback(f"✅ Material: {material} (Confianza: {confidence_percent}%)", "success")

            print(f"🤖 Clasificación IA: {clean_class_name} -> {material} (Confianza: {confidence_percent}%)")

            return material

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error clasificando material: {e}", "error")
            print(f"❌ Error en clasificación IA: {e}")
            raise e

    def _map_class_to_material(self, class_name):
        """
        Mapea el nombre de clase de la IA a los tipos de material del sistema

        Args:
            class_name: Nombre de la clase detectada por la IA

        Returns:
            str: Tipo de material mapeado
        """
        class_name = class_name.lower()

        if "plastico" in class_name or "plastic" in class_name:
            return "plastico"
        elif "aluminio" in class_name or "aluminum" in class_name:
            return "aluminio"
        elif "vacio" in class_name or "empty" in class_name:
            return "vacio"
        else:
            # Si no se reconoce la clase, lanzar error
            raise Exception(f"Clase de material no reconocida: {class_name}")

    def process_material_detection(self):
        """
        Proceso completo de detección de material:
        1. Captura imagen
        2. Clasifica material
        3. Reproduce audio si es necesario

        Returns:
            tuple: (material_type, image_path) o (None, None) si falla
        """
        try:
            # Capturar imagen
            image_path = self.capture_image()
            if not image_path:
                return None, None

            # Clasificar material
            material = self.classify_material(image_path)

            # Verificar si es un cambio significativo
            if not self.is_significant_change(material):
                # No es un cambio significativo, no procesar
                return None, None

            # Actualizar estado de detección
            self.update_detection_state(material)

            # Verificar vacío prolongado para cerrar sesión
            self._check_empty_timeout(material)

            # Reproducir audio si es necesario
            self._play_audio_for_material(material)

            return material, image_path

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error en detección de material: {e}", "error")
            return None, None

    def _play_audio_for_material(self, material):
        """
        Reproduce audio para el material detectado con control de tiempo

        Args:
            material: Tipo de material detectado
        """
        if not self.audio_available:
            return

        current_time = time.time()
        clean_material = material.strip().lower()

        # Condiciones para reproducir audio:
        # 1. Si cambió el material (inmediato)
        # 2. Si es el mismo material pero han pasado 6 segundos
        should_play = False

        if clean_material != self.last_prediction:
            # Cambió el material -> reproducir inmediatamente
            should_play = True
            print(f"📱 Cambio detectado: {self.last_prediction} → {clean_material}")
        elif clean_material == self.last_prediction and (current_time - self.last_audio_time >= self.audio_cooldown):
            # Mismo material pero ya pasaron 6 segundos
            should_play = True
            print(f"⏰ 6 segundos pasados para: {clean_material}")

        if should_play:
            audio_file = None

            if "plastico" in clean_material:
                audio_file = "sounds/plastico1.mp3"
            elif "aluminio" in clean_material:
                audio_file = "sounds/aluminio1.mp3"
            elif "vacio" in clean_material:
                # Para vacío, actualizar pero no reproducir audio
                self.last_prediction = clean_material
                self.last_audio_time = current_time
                print(f"🔇 Vacío detectado - sin audio")
                return

            # Reproducir el audio si hay archivo definido
            if audio_file:
                if os.path.exists(audio_file):
                    try:
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play()
                        self.last_audio_time = current_time
                        self.last_prediction = clean_material
                        print(f"🔊 Reproduciendo: {audio_file}")
                    except Exception as e:
                        print(f"❌ Error reproduciendo {audio_file}: {e}")
                else:
                    print(f"❌ No se encuentra el archivo: {audio_file}")
                    self.last_prediction = clean_material
                    self.last_audio_time = current_time
        else:
            # No reproducir, solo actualizar la predicción actual
            if clean_material == self.last_prediction:
                remaining_time = self.audio_cooldown - (current_time - self.last_audio_time)
                if remaining_time > 0:
                    print(f"⏳ Esperando {remaining_time:.1f}s más para {clean_material}")

            # Actualizar last_prediction incluso si no reproduce audio
            self.last_prediction = clean_material

    def cleanup_old_images(self, max_age_hours=24):
        """
        Limpia imágenes antiguas para liberar espacio

        Args:
            max_age_hours: Edad máxima de las imágenes en horas
        """
        try:
            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600

            # Buscar archivos de imagen
            for filename in os.listdir("."):
                if filename.startswith("captura_") and filename.endswith(".jpg"):
                    file_path = os.path.join(".", filename)
                    file_age = current_time - os.path.getmtime(file_path)

                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        print(f"🗑️ Imagen antigua eliminada: {filename}")

        except Exception as e:
            print(f"❌ Error limpiando imágenes: {e}")

    def is_camera_available(self):
        """Verifica si la cámara está disponible"""
        return self.camera_available

    def is_ai_model_loaded(self):
        """Verifica si el modelo de IA está cargado"""
        return self.model_loaded

    def is_audio_available(self):
        """Verifica si el audio está disponible"""
        return self.audio_available

    def get_camera_info(self):
        """
        Obtiene información sobre la cámara

        Returns:
            dict: Información de la cámara
        """
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                cap.release()

                return {
                    "available": True,
                    "width": width,
                    "height": height,
                    "fps": fps
                }
            else:
                return {"available": False}

        except Exception as e:
            return {"available": False, "error": str(e)}

    def get_ai_model_info(self):
        """
        Obtiene información sobre el modelo de IA

        Returns:
            dict: Información del modelo de IA
        """
        return {
            "loaded": self.model_loaded,
            "model_type": self.model_type,
            "classes": len(self.class_names) if self.class_names else 0,
            "class_names": [name.strip() for name in self.class_names] if self.class_names else [],
            "tflite_available": TFLITE_AVAILABLE,
            "tf_available": TF_AVAILABLE
        }

    def get_audio_info(self):
        """
        Obtiene información sobre el sistema de audio

        Returns:
            dict: Información del audio
        """
        return {
            "available": self.audio_available,
            "cooldown": self.audio_cooldown,
            "last_prediction": self.last_prediction
        }

    def set_session_end_callback(self, callback):
        """
        Configura el callback para cerrar la sesión cuando se detecta vacío prolongado

        Args:
            callback: Función a llamar para cerrar la sesión
        """
        self.session_end_callback = callback

    def _check_empty_timeout(self, material):
        """
        Verifica si se ha detectado vacío por más de 5 segundos

        Args:
            material: Material detectado
        """
        current_time = time.time()
        
        if "vacio" in material.lower():
            # Si es vacío, iniciar o continuar el contador
            if self.empty_start_time is None:
                self.empty_start_time = current_time
                print(f"🕐 Iniciando contador de vacío...")
            else:
                # Verificar si ya pasaron 5 segundos
                empty_duration = current_time - self.empty_start_time
                if empty_duration >= self.empty_timeout:
                    if self.status_callback:
                        self.status_callback(f"⏰ Vacío detectado por {empty_duration:.1f}s - Cerrando sesión", "warning")
                    print(f"⏰ Vacío detectado por {empty_duration:.1f}s - Cerrando sesión")
                    
                    # Llamar callback para cerrar sesión
                    if self.session_end_callback:
                        self.session_end_callback()
                    
                    # Resetear contador
                    self.empty_start_time = None
        else:
            # Si no es vacío, resetear el contador
            if self.empty_start_time is not None:
                print(f"✅ Material detectado - Reseteando contador de vacío")
                self.empty_start_time = None

    def is_valid_material_for_points(self, material):
        """
        Verifica si el material detectado es válido para otorgar puntos

        Args:
            material: Material detectado

        Returns:
            bool: True si el material es válido para puntos
        """
        material_lower = material.lower()
        return "plastico" in material_lower or "aluminio" in material_lower

    def is_significant_change(self, material):
        """
        Verifica si hay un cambio significativo en la detección

        Args:
            material: Material detectado

        Returns:
            bool: True si es un cambio significativo
        """
        current_time = time.time()
        
        # Si es el primer material detectado
        if self.last_detected_material is None:
            return True
        
        # Si cambió el material
        if self.last_detected_material != material:
            return True
        
        # Si es el mismo material pero ya pasó el cooldown
        if (current_time - self.last_detection_time) >= self.detection_cooldown:
            return True
        
        return False

    def update_detection_state(self, material):
        """
        Actualiza el estado de la última detección

        Args:
            material: Material detectado
        """
        self.last_detected_material = material
        self.last_detection_time = time.time()

    def get_detection_stats(self):
        """
        Obtiene estadísticas de detección

        Returns:
            dict: Estadísticas de detección
        """
        current_time = time.time()
        time_since_last = current_time - self.last_detection_time if self.last_detection_time > 0 else 0
        
        return {
            "last_material": self.last_detected_material,
            "time_since_last": time_since_last,
            "detection_cooldown": self.detection_cooldown,
            "camera_active": self.camera_available,
            "camera_continuously_active": self.camera_continuously_active,
            "model_loaded": self.model_loaded
        }

    def is_camera_continuously_active(self):
        """Verifica si la cámara está activa continuamente"""
        return self.camera_continuously_active and self.camera_cap is not None and self.camera_cap.isOpened()

    def _start_continuous_camera(self):
        """Inicia la cámara en modo continuo"""
        try:
            if self.camera_available and not self.camera_continuously_active:
                # Intentar con diferentes índices de cámara para Logitech Brio
                camera_indices = [0, 1, 2]  # Probar diferentes índices
                
                for camera_index in camera_indices:
                    self.camera_cap = cv2.VideoCapture(camera_index)
                    if self.camera_cap.isOpened():
                        # Configurar resolución para Logitech Brio
                        self.camera_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                        self.camera_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                        self.camera_cap.set(cv2.CAP_PROP_FPS, 30)
                        
                        # Verificar que realmente funciona
                        ret, frame = self.camera_cap.read()
                        if ret and frame is not None:
                            self.camera_continuously_active = True
                            print(f"✅ Cámara continua iniciada en índice {camera_index}")
                            if self.status_callback:
                                self.status_callback(f"📷 Cámara continua activa (índice {camera_index})", "success")
                            return
                        else:
                            self.camera_cap.release()
                            self.camera_cap = None
                
                # Si no se pudo abrir ninguna cámara
                self.camera_continuously_active = False
                print("❌ No se pudo iniciar cámara continua")
                if self.status_callback:
                    self.status_callback("❌ Error iniciando cámara continua", "error")
                    
        except Exception as e:
            self.camera_continuously_active = False
            print(f"❌ Error iniciando cámara continua: {e}")
            if self.status_callback:
                self.status_callback(f"❌ Error cámara continua: {e}", "error")

    def _stop_continuous_camera(self):
        """Detiene la cámara continua"""
        try:
            if self.camera_cap is not None:
                self.camera_cap.release()
                self.camera_cap = None
                self.camera_continuously_active = False
                print("📷 Cámara continua detenida")
                if self.status_callback:
                    self.status_callback("📷 Cámara detenida", "info")
        except Exception as e:
            print(f"❌ Error deteniendo cámara: {e}")

    def pause_continuous_camera(self):
        """Pausa la cámara continua (mantiene abierta pero no captura)"""
        self.camera_continuously_active = False
        print("⏸️ Cámara pausada")
        if self.status_callback:
            self.status_callback("⏸️ Cámara pausada", "info")

    def resume_continuous_camera(self):
        """Reanuda la cámara continua"""
        if self.camera_cap is not None and self.camera_cap.isOpened():
            self.camera_continuously_active = True
            print("▶️ Cámara reanudada")
            if self.status_callback:
                self.status_callback("▶️ Cámara reanudada", "success")
        else:
            # Reiniciar cámara si se cerró
            self._start_continuous_camera()

    def delete_image(self, image_path):
        """
        Elimina una imagen específica del sistema de archivos

        Args:
            image_path: Ruta de la imagen a eliminar
        """
        try:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
                print(f"🗑️ Imagen eliminada: {image_path}")
                return True
            else:
                print(f"⚠️ Imagen no encontrada: {image_path}")
                return False
        except Exception as e:
            print(f"❌ Error eliminando imagen {image_path}: {e}")
            return False

    def cleanup_old_images(self, max_age_hours=1):
        """
        Limpia imágenes antiguas para liberar espacio

        Args:
            max_age_hours: Edad máxima de las imágenes en horas
        """
        try:
            current_time = datetime.now().timestamp()
            max_age_seconds = max_age_hours * 3600

            # Buscar archivos de imagen
            for filename in os.listdir("."):
                if filename.startswith("captura_") and filename.endswith(".jpg"):
                    file_path = os.path.join(".", filename)
                    file_age = current_time - os.path.getmtime(file_path)

                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        print(f"🗑️ Imagen antigua eliminada: {filename}")

        except Exception as e:
            print(f"❌ Error limpiando imágenes: {e}")

    def cleanup(self):
        """Limpia recursos al cerrar la aplicación"""
        try:
            self._stop_continuous_camera()
            # Limpiar todas las imágenes al cerrar
            self.cleanup_old_images(0)  # Eliminar todas las imágenes
            print("🧹 Recursos de cámara limpiados")
        except Exception as e:
            print(f"❌ Error limpiando recursos: {e}")
