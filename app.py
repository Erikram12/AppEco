"""
Sistema de Reciclaje Inteligente - Aplicación Principal
======================================================

Esta es la aplicación principal que coordina todos los servicios del sistema
de reciclaje inteligente, incluyendo MQTT, Firebase, NFC, cámara y UI.
"""
import time
import threading
import tkinter as tk

# Importar servicios
from services.firebase_service import FirebaseService
from services.mqtt_service import MQTTService
from services.nfc_service import NFCService
from services.camera_service import CameraService
from ui.ui_components import UIComponents
from config.config import SESSION_DURATION, POINTS_CLAIM_TIMEOUT


class ReciclajeApp:
    """Aplicación principal del Sistema de Reciclaje Inteligente"""

    def __init__(self, root):
        """
        Inicializa la aplicación principal

        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.is_running = True
        self.current_user = None
        self.session_active = False
        
        # Nuevas variables para el flujo de detección continua
        self.detection_active = True
        self.pending_material = None  # Material detectado esperando NFC
        self.pending_points = 0  # Puntos pendientes de otorgar
        self.pending_material_time = 0  # Timestamp del material pendiente
        self.pending_image_path = None  # Ruta de la imagen del material pendiente
        self.pending_timeout = POINTS_CLAIM_TIMEOUT  # Timeout para reclamar puntos antes del reinicio
        self.detection_thread = None

        # Inicializar componentes de UI
        self.ui = UIComponents(root)
        
        # Configurar cierre de aplicación
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # Inicializar servicios
        self.firebase_service = FirebaseService(self.ui.update_status)
        self.mqtt_service = MQTTService(self._on_mqtt_message, self.ui.update_status)
        self.nfc_service = NFCService(self._on_nfc_card, self.ui.update_status)
        self.camera_service = CameraService(self.ui.update_status)
        
        # Configurar callback para cierre de sesión por vacío prolongado
        self.camera_service.set_session_end_callback(self._end_session_by_empty)

        # Iniciar servicios
        self._start_services()

        # Sistema listo
        self._start_system()

    def _start_services(self):
        """Inicia todos los servicios del sistema"""
        # Actualizar estado de componentes
        if self.firebase_service.is_initialized():
            self.ui.update_component_status("firebase", "✅ Conectado", "#27ae60")
        else:
            self.ui.update_component_status("firebase", "❌ Error", "#e74c3c")

        if self.nfc_service.is_reader_available():
            self.ui.update_component_status("nfc", "✅ Disponible", "#27ae60")
        else:
            self.ui.update_component_status("nfc", "❌ No disponible", "#e74c3c")

        if self.camera_service.is_camera_available():
            camera_status = "✅ Disponible"
            if self.camera_service.is_ai_model_loaded():
                camera_status += " + IA"
            self.ui.update_component_status("camera", camera_status, "#27ae60")
        else:
            self.ui.update_component_status("camera", "❌ No disponible", "#e74c3c")

        # Iniciar servicios
        self.mqtt_service.start()
        self.nfc_service.start_monitoring()

    def _start_system(self):
        """Inicia el sistema principal"""
        self.is_running = True
        self.ui.update_status(f"🟢 Sistema iniciado - Cámara siempre activa, detección con confianza ≥ 95% - Timeout: {POINTS_CLAIM_TIMEOUT}s", "success")
        
        # Iniciar detección continua de materiales
        self._start_continuous_detection()

    def _start_continuous_detection(self):
        """Inicia la detección continua de materiales en un hilo separado"""
        if self.detection_thread is None or not self.detection_thread.is_alive():
            self.detection_thread = threading.Thread(target=self._continuous_detection_loop, daemon=True)
            self.detection_thread.start()

    def _continuous_detection_loop(self):
        """Loop continuo de detección de materiales - Cámara siempre activa en tiempo real"""
        while self.is_running:
            try:
                # Solo detectar si no hay material pendiente
                if self.pending_material is None and self.detection_active:
                    material, image_path = self.camera_service.process_material_detection()
                    
                    if material and self.camera_service.is_valid_material_for_points(material):
                        # Material válido detectado con confianza ≥ 95% - solicitar NFC
                        self._handle_material_detected(material, image_path)
                    elif material and "vacio" in material.lower():
                        # Vacío detectado - solo mostrar, no procesar
                        self.ui.update_status(f"🔍 Detectado: {material}", "info")
                    # Si material es None, significa que no hubo cambio significativo
                    # (No mostrar mensaje para evitar spam en la UI)
                elif self.pending_material is not None:
                    # Hay material pendiente, verificar timeout
                    current_time = time.time()
                    if (current_time - self.pending_material_time) > self.pending_timeout:
                        # Timeout alcanzado, reiniciar sistema
                        print(f"⏰ Timeout de puntos no reclamados: {self.pending_material} - Reiniciando sistema")
                        self.ui.update_status(f"⏰ Tiempo agotado para reclamar {self.pending_material} - Reiniciando sistema...", "warning")
                        
                        # Reiniciar sistema completo
                        self._restart_system()
                
                # Pausa muy corta para detección en tiempo real
                time.sleep(0.1)  # 100ms para detección en tiempo real
                
            except Exception as e:
                print(f"❌ Error en detección continua: {e}")
                time.sleep(0.2)  # Pausa corta en caso de error

    def _handle_material_detected(self, material, image_path=None):
        """
        Maneja cuando se detecta un material válido
        
        Args:
            material: Material detectado (plastico o aluminio)
            image_path: Ruta de la imagen capturada
        """
        # Calcular puntos según el material
        if "plastico" in material.lower():
            points = 20  # POINTS_PLASTIC
        elif "aluminio" in material.lower():
            points = 30  # POINTS_ALUMINUM
        else:
            return
        
        # Guardar material, puntos e imagen pendientes
        self.pending_material = material
        self.pending_points = points
        self.pending_material_time = time.time()
        self.pending_image_path = image_path
        
        # Actualizar UI
        self.ui.update_status(f"♻️ {material.upper()} detectado! Pase su tarjeta NFC para recibir {points} puntos (Tiempo límite: {POINTS_CLAIM_TIMEOUT}s)", "success")
        self.ui.update_pending_material(material, points)
        self.ui.log_material(material, points)
        
        # Marcar material pendiente (la cámara sigue activa)
        print(f"🎁 Material pendiente: {material} - Esperando NFC")
        if image_path:
            print(f"📷 Imagen guardada: {image_path}")

    def _on_mqtt_message(self, data):
        """
        Callback para procesar mensajes MQTT

        Args:
            data: Diccionario con los datos del mensaje
        """
        target = data['target']
        percent = data['percent']
        state = data['state']
        distance_cm = data['distance_cm']
        device_id = data['device_id']
        timestamp = data['timestamp']

        # Verificar si hay cambios significativos
        if not self.ui.has_significant_change(target, percent, state):
            print(f"⏭️ {target}: Sin cambios significativos ({percent}% {state}) - Omitiendo actualización Firebase")
            self.ui.update_container_status(target, percent, state, distance_cm)
            return

        # Actualizar Firebase
        success = self.firebase_service.update_container_status(
            target, percent, state, distance_cm, device_id, timestamp
        )

        if success:
            # Actualizar estado anterior
            self.ui.update_last_state(target, percent, state)

            # Actualizar contadores si el contenedor está lleno
            if state == "Lleno" and percent >= 90:
                if target == "contePlastico":
                    self.ui.plastic_count += 1
                elif target == "conteAluminio":
                    self.ui.aluminum_count += 1

        # Actualizar UI
        self.ui.update_container_status(target, percent, state, distance_cm)

    def _on_nfc_card(self, nfc_id):
        """
        Callback para procesar tarjetas NFC detectadas

        Args:
            nfc_id: ID de la tarjeta NFC
        """
        # Verificar si hay material pendiente
        if self.pending_material is not None:
            self._process_pending_material(nfc_id)
        else:
            # No hay material pendiente - mostrar mensaje
            self.ui.update_status("⚠️ No hay material detectado. Coloque un material primero.", "warning")

    def _process_pending_material(self, nfc_id):
        """
        Procesa el material pendiente con la tarjeta NFC
        
        Args:
            nfc_id: ID de la tarjeta NFC
        """
        # Buscar usuario en Firebase
        uid, email = self.firebase_service.buscar_usuario_por_nfc(nfc_id)

        if uid:
            # Usuario válido - otorgar puntos
            self.ui.update_status(f"🔓 Usuario autenticado: {email}", "success")
            
            # Actualizar puntos en Firebase
            points_awarded = self.firebase_service.actualizar_puntos(uid, self.pending_material)
            
            if points_awarded > 0:
                # Obtener información del usuario
                user_data = self.firebase_service.get_user_data(uid)
                if user_data:
                    user_points = user_data.get("usuario_puntos", 0)
                    user_name = user_data.get("usuario_nombre", "Usuario")
                    self.ui.update_status(f"✅ {user_name} recibió {points_awarded} puntos! Total: {user_points}", "success")
                
                # Eliminar imagen del material procesado
                if self.pending_image_path:
                    self.camera_service.delete_image(self.pending_image_path)
                
                # Limpiar material pendiente
                self.pending_material = None
                self.pending_points = 0
                self.pending_image_path = None
                self.ui.clear_pending_material()
                
                # La cámara ya está activa, solo actualizar UI
                self.ui.update_status("🔄 Cámara activa - Detectando cambios...", "info")
                self.ui.update_detection_status("🔄 Cámara activa - Detectando cambios...", "#3498db")
            else:
                self.ui.update_status("❌ Error otorgando puntos", "error")
        else:
            self.ui.update_status("❌ Usuario no válido", "error")
            time.sleep(1.5)
            self.ui.update_status(f"♻️ {self.pending_material.upper()} detectado! Pase su tarjeta NFC para recibir {self.pending_points} puntos (Tiempo límite: {POINTS_CLAIM_TIMEOUT}s)", "success")

    def _restart_system(self):
        """
        Reinicia el sistema completo limpiando todos los estados
        """
        print("🔄 Reiniciando sistema...")
        
        # Limpiar material pendiente si existe
        if self.pending_material is not None:
            # Eliminar imagen pendiente
            if self.pending_image_path:
                self.camera_service.delete_image(self.pending_image_path)
            
            self.pending_material = None
            self.pending_points = 0
            self.pending_material_time = 0
            self.pending_image_path = None
            self.ui.clear_pending_material()
        
        # Limpiar sesión activa
        self.session_active = False
        self.current_user = None
        
        # Reiniciar detección
        self.detection_active = True
        
        # Actualizar UI
        self.ui.update_status("🔄 Sistema reiniciado - Cámara activa, detectando cambios...", "info")
        self.ui.update_detection_status("🔄 Cámara activa - Detectando cambios...", "#3498db")
        
        print("✅ Sistema reiniciado exitosamente")

    def _end_session_by_empty(self):
        """
        Callback para cerrar la sesión cuando se detecta vacío prolongado
        """
        # Limpiar material pendiente si existe
        if self.pending_material is not None:
            # Eliminar imagen pendiente
            if self.pending_image_path:
                self.camera_service.delete_image(self.pending_image_path)
            
            self.pending_material = None
            self.pending_points = 0
            self.pending_image_path = None
            self.ui.clear_pending_material()
        
        # La cámara ya está activa, solo actualizar UI
        self.ui.update_status("🔄 Cámara activa - Detectando cambios...", "info")
        self.ui.update_detection_status("🔄 Cámara activa - Detectando cambios...", "#3498db")

    def _on_closing(self):
        """Maneja el cierre de la aplicación"""
        try:
            print("🔄 Cerrando aplicación...")
            self.is_running = False
            
            # Limpiar recursos de cámara
            if hasattr(self, 'camera_service'):
                self.camera_service.cleanup()
            
            # Cerrar ventana
            self.root.destroy()
        except Exception as e:
            print(f"❌ Error cerrando aplicación: {e}")
            self.root.destroy()


def main():
    root = tk.Tk()
    app = ReciclajeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()