"""
Servicio NFC para el Sistema de Reciclaje Inteligente
===================================================

Este módulo maneja la lectura de tarjetas NFC, incluyendo la detección
de tarjetas, extracción del UID y monitoreo continuo.
"""

import time
import threading
try:
    from smartcard.System import readers
    from smartcard.util import toHexString
    SMARTCARD_AVAILABLE = True
except ImportError:
    SMARTCARD_AVAILABLE = False
    print("⚠️ smartcard no disponible - NFC deshabilitado")


class NFCService:
    """Servicio para manejar la lectura de tarjetas NFC"""

    def __init__(self, card_callback=None, status_callback=None):
        """
        Inicializa el servicio NFC

        Args:
            card_callback: Función callback cuando se detecta una tarjeta
            status_callback: Función callback para actualizar el estado en la UI
        """
        self.card_callback = card_callback
        self.status_callback = status_callback
        self.is_running = False
        self.monitor_thread = None
        self.reader_available = False
        self._check_reader_availability()

    def _check_reader_availability(self):
        """Verifica si hay lectores NFC disponibles"""
        try:
            if not SMARTCARD_AVAILABLE:
                self.reader_available = False
                print("⚠️ smartcard no disponible - NFC deshabilitado")
                return
                
            available_readers = readers()
            self.reader_available = len(available_readers) > 0
            if self.reader_available:
                print(f"✅ Lector NFC encontrado: {available_readers[0]}")
            else:
                print("⚠️ No se encontraron lectores NFC")
        except Exception as e:
            self.reader_available = False
            print(f"❌ Error verificando lectores NFC: {e}")

    def start_monitoring(self):
        """Inicia el monitoreo de tarjetas NFC en un hilo separado"""
        if not self.reader_available:
            if self.status_callback:
                self.status_callback("❌ No hay lectores NFC disponibles", "error")
            return

        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_cards, daemon=True)
        self.monitor_thread.start()

        if self.status_callback:
            self.status_callback("🎫 NFC: ✅ Activo", "success")

    def stop_monitoring(self):
        """Detiene el monitoreo de tarjetas NFC"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)

    def _monitor_cards(self):
        """Monitorea continuamente la presencia de tarjetas NFC"""
        while self.is_running:
            try:
                if not self.reader_available or not SMARTCARD_AVAILABLE:
                    time.sleep(1)
                    continue

                # Obtener lectores disponibles
                available_readers = readers()
                if not available_readers:
                    time.sleep(1)
                    continue

                reader = available_readers[0]
                connection = reader.createConnection()

                # Comando para obtener UID
                GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

                # Intentar conectar y leer UID
                connection.connect()
                data, sw1, sw2 = connection.transmit(GET_UID)
                connection.disconnect()

                # Verificar si la operación fue exitosa
                if sw1 == 0x90:
                    uid = ''.join(toHexString(data).split()).upper()

                    if self.status_callback:
                        self.status_callback(f"🎫 Tarjeta NFC detectada: {uid[:8]}...", "info")

                    # Llamar callback con el UID de la tarjeta
                    if self.card_callback:
                        self.card_callback(uid)

                    # Esperar a que se retire la tarjeta
                    self._wait_for_card_removal(reader)

            except Exception as e:
                # Error silencioso para evitar spam en consola
                # Los errores son normales cuando no hay tarjeta presente
                pass

            time.sleep(0.2)  # Pequeña pausa para no sobrecargar el CPU

    def _wait_for_card_removal(self, reader):
        """
        Espera a que se retire la tarjeta del lector

        Args:
            reader: Instancia del lector NFC
        """
        while self.is_running:
            try:
                # Intentar conectar - si falla, la tarjeta fue retirada
                connection = reader.createConnection()
                connection.connect()
                connection.disconnect()
            except Exception:
                # La tarjeta fue retirada
                break
            time.sleep(0.2)

    def read_card_uid(self):
        """
        Lee el UID de una tarjeta NFC (método síncrono)

        Returns:
            str: UID de la tarjeta o None si no se puede leer
        """
        try:
            if not self.reader_available or not SMARTCARD_AVAILABLE:
                return None

            available_readers = readers()
            if not available_readers:
                return None

            reader = available_readers[0]
            connection = reader.createConnection()
            GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

            connection.connect()
            data, sw1, sw2 = connection.transmit(GET_UID)
            connection.disconnect()

            if sw1 == 0x90:
                uid = ''.join(toHexString(data).split()).upper()
                return uid

        except Exception as e:
            print(f"❌ Error leyendo tarjeta NFC: {e}")

        return None

    def is_reader_available(self):
        """Verifica si hay lectores NFC disponibles"""
        return self.reader_available

    def is_monitoring(self):
        """Verifica si el monitoreo está activo"""
        return self.is_running
