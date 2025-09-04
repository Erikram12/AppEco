"""
Servicio de Firebase para el Sistema de Reciclaje Inteligente
============================================================

Este módulo maneja todas las operaciones relacionadas con Firebase,
incluyendo la inicialización, actualización de contenedores,
búsqueda de usuarios y gestión de puntos.
"""

import time
import datetime
import firebase_admin
from firebase_admin import credentials, db
from config.config import FIREBASE_DB_URL, FIREBASE_CRED_PATH, POINTS_PLASTIC, POINTS_ALUMINUM


class FirebaseService:
    """Servicio para manejar todas las operaciones de Firebase"""

    def __init__(self, status_callback=None):
        """
        Inicializa el servicio de Firebase

        Args:
            status_callback: Función callback para actualizar el estado en la UI
        """
        self.status_callback = status_callback
        self.initialized = False
        self.init_firebase()

    def init_firebase(self):
        """Inicializa la conexión con Firebase"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_CRED_PATH)
                firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})

            self.initialized = True
            if self.status_callback:
                self.status_callback("✅ Firebase conectado", "success")

        except Exception as e:
            self.initialized = False
            if self.status_callback:
                self.status_callback(f"❌ Error Firebase: {e}", "error")
            raise e

    def update_container_status(self, target, percent, state, distance_cm, device_id, timestamp):
        """
        Actualiza el estado de un contenedor en Firebase

        Args:
            target: Tipo de contenedor (contePlastico | conteAluminio)
            percent: Porcentaje de llenado (0-100)
            state: Estado del contenedor (Vacio | Medio | Lleno)
            distance_cm: Distancia del sensor en cm
            device_id: ID del dispositivo
            timestamp: Timestamp del mensaje
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            ref = db.reference("contenedor").child(target)
            ref.update({
                "estado": state,
                "porcentaje": percent,
                "distance_cm": distance_cm,
                "deviceId": device_id,
                "timestamp": timestamp,
                "updatedAt": int(time.time() * 1000)
            })

            print(f"🔥 RTDB actualizado: {target} -> {state} ({percent}%) [CAMBIO DETECTADO]")
            return True

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error actualizando contenedor: {e}", "error")
            return False

    def buscar_usuario_por_nfc(self, nfc_id):
        """
        Busca un usuario por su ID de tarjeta NFC

        Args:
            nfc_id: ID de la tarjeta NFC

        Returns:
            tuple: (uid, email) o (None, None) si no se encuentra
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            ref_index = db.reference("nfc_index").child(nfc_id).get()
            if ref_index:
                uid = ref_index
                user_ref = db.reference("usuarios").child(uid).get()
                if user_ref:
                    return uid, user_ref.get("usuario_email", "Correo no disponible")

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error buscando usuario: {e}", "error")

        return None, None

    def actualizar_puntos(self, uid, material):
        """
        Actualiza los puntos de un usuario por reciclar material

        Args:
            uid: ID del usuario
            material: Tipo de material ("plastico" | "aluminio")
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            user_ref = db.reference("usuarios").child(uid)
            user_data = user_ref.get()

            if user_data:
                puntos_actuales = user_data.get("usuario_puntos", 0)
                puntos_a_sumar = POINTS_PLASTIC if material == "plastico" else POINTS_ALUMINUM
                puntos_nuevos = puntos_actuales + puntos_a_sumar

                if self.status_callback:
                    self.status_callback(f"💾 Actualizando puntos en Firebase...", "info")

                # Actualizar puntos totales
                user_ref.update({"usuario_puntos": puntos_nuevos})

                # Agregar registro de puntos ganados
                pts_ref = user_ref.child("puntos").push()
                pts_ref.set({
                    "punto_cantidad": puntos_a_sumar,
                    "punto_descripcion": f"Reciclaje completado ({material})",
                    "punto_fecha": int(datetime.datetime.now().timestamp() * 1000),
                    "punto_tipo": "ganado",
                    "punto_userId": uid
                })

                if self.status_callback:
                    self.status_callback(f"✅ Puntos: {puntos_actuales} ➝ {puntos_nuevos}", "success")

                return puntos_a_sumar

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error actualizando puntos: {e}", "error")
            return 0

    def get_user_data(self, uid):
        """
        Obtiene los datos de un usuario

        Args:
            uid: ID del usuario

        Returns:
            dict: Datos del usuario o None si no se encuentra
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            user_ref = db.reference("usuarios").child(uid).get()
            return user_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo datos del usuario: {e}", "error")
            return None

    def get_user_data(self, uid):
        """
        Obtiene los datos de un usuario

        Args:
            uid: ID del usuario

        Returns:
            dict: Datos del usuario o None si no se encuentra
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            user_ref = db.reference("usuarios").child(uid).get()
            return user_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo datos del usuario: {e}", "error")
            return None

    def get_user_points(self, uid):
        """
        Obtiene los puntos totales de un usuario

        Args:
            uid: ID del usuario

        Returns:
            int: Puntos totales del usuario
        """
        try:
            user_data = self.get_user_data(uid)
            if user_data:
                return user_data.get("usuario_puntos", 0)
            return 0
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo puntos del usuario: {e}", "error")
            return 0

    def get_user_achievements(self, uid):
        """
        Obtiene los logros de un usuario

        Args:
            uid: ID del usuario

        Returns:
            dict: Logros del usuario o None si no se encuentra
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            achievements_ref = db.reference("usuarios").child(uid).child("logros").get()
            return achievements_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo logros del usuario: {e}", "error")
            return None

    def get_user_history(self, uid):
        """
        Obtiene el historial de un usuario

        Args:
            uid: ID del usuario

        Returns:
            dict: Historial del usuario o None si no se encuentra
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            history_ref = db.reference("usuarios").child(uid).child("historial").get()
            return history_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo historial del usuario: {e}", "error")
            return None

    def get_container_resets(self):
        """
        Obtiene los reinicios de contadores

        Returns:
            dict: Reinicios de contadores o None si hay error
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            resets_ref = db.reference("reinicios_contadores").get()
            return resets_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo reinicios de contadores: {e}", "error")
            return None

    def get_vouchers(self, uid=None):
        """
        Obtiene los vales de un usuario o todos los vales

        Args:
            uid: ID del usuario (opcional)

        Returns:
            dict: Vales del usuario o todos los vales
        """
        try:
            if not self.initialized:
                raise Exception("Firebase no inicializado")

            if uid:
                # Obtener vales de un usuario específico
                vouchers_ref = db.reference("vales").order_by_child("vale_usuario_id").equal_to(uid).get()
            else:
                # Obtener todos los vales
                vouchers_ref = db.reference("vales").get()

            return vouchers_ref

        except Exception as e:
            if self.status_callback:
                self.status_callback(f"❌ Error obteniendo vales: {e}", "error")
            return None

    def is_initialized(self):
        """Verifica si Firebase está inicializado"""
        return self.initialized
