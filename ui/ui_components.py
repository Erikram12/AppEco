"""
Componentes de UI para el Sistema de Reciclaje Inteligente - Versión LCD
========================================================================

Este módulo contiene todos los componentes de interfaz de usuario optimizados
para pantalla LCD TFT de 320x480 píxeles, mostrando solo información esencial.
"""

import tkinter as tk
from tkinter import ttk
import datetime
from config.config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG_COLOR, FRAME_BG_COLOR, TEXT_COLOR,
    STATUS_COLORS, CONTAINER_COLORS, CONTAINER_EMOJIS, COMPACT_MODE,
    FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE
)


class UIComponents:
    """Clase para manejar todos los componentes de la interfaz de usuario optimizada para LCD"""

    def __init__(self, root):
        """
        Inicializa los componentes de UI para pantalla LCD

        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG_COLOR)
        
        # Configurar para pantalla completa en LCD
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)

        # Variables de estado
        self.plastic_count = 0
        self.aluminum_count = 0
        self.total_points = 0
        self.current_user = None
        self.session_active = False

        # Estado anterior para evitar spam de actualizaciones
        self.last_state_plastico = None
        self.last_state_aluminio = None
        self.last_percent_plastico = None
        self.last_percent_aluminio = None

        # Crear todos los widgets optimizados para LCD
        self._create_compact_widgets()

    def _create_compact_widgets(self):
        """Crea widgets optimizados para pantalla LCD de 320x480"""
        # Frame principal con padding mínimo
        main_frame = tk.Frame(self.root, bg=WINDOW_BG_COLOR)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # 1. Título compacto (línea 1)
        self._create_compact_title(main_frame)

        # 2. Estado del sistema (línea 2)
        self._create_compact_status(main_frame)

        # 3. Material pendiente (línea 3-4)
        self._create_compact_pending(main_frame)

        # 4. Estadísticas compactas (línea 5)
        self._create_compact_stats(main_frame)

        # 5. Estado de componentes (línea 6)
        self._create_compact_components(main_frame)

        # 6. Log compacto (línea 7-8)
        self._create_compact_log(main_frame)

    def _create_compact_title(self, parent):
        """Crea título compacto"""
        title_label = tk.Label(
            parent, text="♻️ RECICLAJE INTELIGENTE",
            font=('Arial', FONT_SIZE_LARGE, 'bold'), 
            bg=WINDOW_BG_COLOR, fg=TEXT_COLOR
        )
        title_label.pack(pady=2)

    def _create_compact_status(self, parent):
        """Crea estado del sistema compacto"""
        status_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=1)
        status_frame.pack(fill='x', pady=2)

        self.status_label = tk.Label(
            status_frame, text="🔄 Iniciando...",
            font=('Arial', FONT_SIZE_MEDIUM), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.status_label.pack(pady=3)

    def _create_compact_pending(self, parent):
        """Crea sección de material pendiente compacta"""
        pending_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=1)
        pending_frame.pack(fill='x', pady=2)

        # Material detectado
        self.pending_material_label = tk.Label(
            pending_frame, text="🔄 Esperando detección...",
            font=('Arial', FONT_SIZE_MEDIUM, 'bold'), 
            bg=FRAME_BG_COLOR, fg='#bdc3c7'
        )
        self.pending_material_label.pack(pady=2)

        # Puntos pendientes
        self.pending_points_label = tk.Label(
            pending_frame, text="",
            font=('Arial', FONT_SIZE_SMALL), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.pending_points_label.pack(pady=1)

    def _create_compact_stats(self, parent):
        """Crea estadísticas compactas en una sola línea"""
        stats_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=1)
        stats_frame.pack(fill='x', pady=2)

        # Frame horizontal para estadísticas
        stats_content = tk.Frame(stats_frame, bg=FRAME_BG_COLOR)
        stats_content.pack(pady=2)

        # Plástico
        self.plastic_count_label = tk.Label(
            stats_content, text="🥤 0",
            font=('Arial', FONT_SIZE_SMALL, 'bold'), 
            bg=FRAME_BG_COLOR, fg='#3498db'
        )
        self.plastic_count_label.pack(side='left', padx=5)

        # Aluminio
        self.aluminum_count_label = tk.Label(
            stats_content, text="🥫 0",
            font=('Arial', FONT_SIZE_SMALL, 'bold'), 
            bg=FRAME_BG_COLOR, fg='#95a5a6'
        )
        self.aluminum_count_label.pack(side='left', padx=5)

        # Puntos totales
        self.total_points_label = tk.Label(
            stats_content, text="🏆 0",
            font=('Arial', FONT_SIZE_SMALL, 'bold'), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.total_points_label.pack(side='left', padx=5)

    def _create_compact_components(self, parent):
        """Crea estado de componentes compacto"""
        components_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=1)
        components_frame.pack(fill='x', pady=2)

        # Frame horizontal para componentes
        comp_content = tk.Frame(components_frame, bg=FRAME_BG_COLOR)
        comp_content.pack(pady=2)

        # NFC
        self.nfc_status_label = tk.Label(
            comp_content, text="🎫 ⏳",
            font=('Arial', FONT_SIZE_SMALL), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.nfc_status_label.pack(side='left', padx=3)

        # Cámara
        self.camera_status_label = tk.Label(
            comp_content, text="📷 ⏳",
            font=('Arial', FONT_SIZE_SMALL), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.camera_status_label.pack(side='left', padx=3)

        # MQTT
        self.mqtt_status_label = tk.Label(
            comp_content, text="📡 ⏳",
            font=('Arial', FONT_SIZE_SMALL), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.mqtt_status_label.pack(side='left', padx=3)

        # Firebase
        self.firebase_status_label = tk.Label(
            comp_content, text="🔥 ⏳",
            font=('Arial', FONT_SIZE_SMALL), 
            bg=FRAME_BG_COLOR, fg='#f39c12'
        )
        self.firebase_status_label.pack(side='left', padx=3)

    def _create_compact_log(self, parent):
        """Crea log compacto con scroll"""
        log_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=1)
        log_frame.pack(fill='both', expand=True, pady=2)

        # Título del log
        tk.Label(
            log_frame, text="📊 ACTIVIDAD",
            font=('Arial', FONT_SIZE_SMALL, 'bold'), 
            bg=FRAME_BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=1)

        # Text widget compacto
        self.materials_text = tk.Text(
            log_frame, height=8, width=35,
            font=('Consolas', FONT_SIZE_SMALL), 
            bg=WINDOW_BG_COLOR, fg=TEXT_COLOR,
            insertbackground='white', state='disabled',
            wrap='word'
        )
        self.materials_text.pack(pady=2, padx=2, fill='both', expand=True)

        # Scrollbar compacta
        scrollbar = tk.Scrollbar(log_frame, command=self.materials_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.materials_text.config(yscrollcommand=scrollbar.set)

    def update_status(self, message, status_type="info"):
        """
        Actualiza el mensaje de estado del sistema

        Args:
            message: Mensaje a mostrar
            status_type: Tipo de estado (success, error, warning, info)
        """
        color = STATUS_COLORS.get(status_type, "#3498db")
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def update_user_info(self, email):
        """
        Actualiza la información del usuario

        Args:
            email: Email del usuario autenticado
        """
        self.current_user = email
        # No mostramos email en modo compacto para ahorrar espacio

    def clear_user_info(self):
        """Limpia la información del usuario"""
        self.current_user = None

    def update_session_status(self, active=True):
        """
        Actualiza el estado de la sesión

        Args:
            active: Si la sesión está activa
        """
        if active:
            self.session_active = True
        else:
            self.session_active = False

    def update_progress(self, progress):
        """
        Actualiza la barra de progreso (no usado en modo compacto)

        Args:
            progress: Valor de progreso (0-100)
        """
        pass

    def update_container_status(self, target, percent, state, distance_cm):
        """
        Actualiza el estado visual de los contenedores

        Args:
            target: Tipo de contenedor (contePlastico | conteAluminio)
            percent: Porcentaje de llenado
            state: Estado del contenedor
            distance_cm: Distancia del sensor
        """
        try:
            # Determinar color y emoji basado en el estado
            color = CONTAINER_COLORS.get(state, "#27ae60")
            emoji = CONTAINER_EMOJIS.get(state, "🟢")

            # Actualizar el log con información visual
            container_name = "🥤" if target == "contePlastico" else "🥫"
            log_entry = f"{emoji} {container_name}: {percent}% ({state})\n"

            self.materials_text.config(state='normal')
            self.materials_text.insert('end', log_entry)
            self.materials_text.see('end')
            self.materials_text.config(state='disabled')

            # Actualizar contadores en estadísticas
            if target == "contePlastico":
                self.plastic_count_label.config(text=f"🥤 {self.plastic_count}", fg=color)
            elif target == "conteAluminio":
                self.aluminum_count_label.config(text=f"🥫 {self.aluminum_count}", fg=color)

        except Exception as e:
            print(f"❌ Error actualizando estado del contenedor: {e}")

    def log_material(self, material, points):
        """
        Registra un material detectado en el log

        Args:
            material: Tipo de material
            points: Puntos otorgados
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{ts}] ♻️ {material.upper()} (+{points})\n"

        self.materials_text.config(state='normal')
        self.materials_text.insert('end', log_entry)
        self.materials_text.see('end')
        self.materials_text.config(state='disabled')

        # Actualizar contadores
        if material == "plastico":
            self.plastic_count += 1
            self.plastic_count_label.config(text=f"🥤 {self.plastic_count}")
        elif material == "aluminio":
            self.aluminum_count += 1
            self.aluminum_count_label.config(text=f"🥫 {self.aluminum_count}")

        self.total_points += points
        self.total_points_label.config(text=f"🏆 {self.total_points}")

    def update_component_status(self, component, status, color):
        """
        Actualiza el estado de un componente

        Args:
            component: Nombre del componente (nfc, camera, mqtt, firebase)
            status: Estado del componente
            color: Color del estado
        """
        # Simplificar estados para pantalla pequeña
        if "✅" in status or "Conectado" in status or "Disponible" in status:
            status_icon = "✅"
        elif "❌" in status or "Error" in status or "No disponible" in status:
            status_icon = "❌"
        else:
            status_icon = "⏳"

        if component == "nfc":
            self.nfc_status_label.config(text=f"🎫 {status_icon}", fg=color)
        elif component == "camera":
            self.camera_status_label.config(text=f"📷 {status_icon}", fg=color)
        elif component == "mqtt":
            self.mqtt_status_label.config(text=f"📡 {status_icon}", fg=color)
        elif component == "firebase":
            self.firebase_status_label.config(text=f"🔥 {status_icon}", fg=color)

    def append_material_log(self, label, value, extra=None):
        """
        Agrega una entrada al log de materiales

        Args:
            label: Etiqueta del log
            value: Valor a registrar
            extra: Información adicional (opcional)
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {label}: {value}"
        if extra is not None:
            line += f" ({extra})"
        line += "\n"

        self.materials_text.config(state='normal')
        self.materials_text.insert('end', line)
        self.materials_text.see('end')
        self.materials_text.config(state='disabled')

    def has_significant_change(self, target, percent, state):
        """
        Verifica si hay cambios significativos que justifiquen actualizar Firebase

        Args:
            target: Tipo de contenedor
            percent: Porcentaje de llenado
            state: Estado del contenedor

        Returns:
            bool: True si hay cambios significativos
        """
        if target == "contePlastico":
            # Verificar cambio de estado
            if state != self.last_state_plastico:
                return True
            # Verificar cambio de porcentaje significativo (5% o más)
            if (self.last_percent_plastico is None or
                    abs(percent - self.last_percent_plastico) >= 5):
                return True
        elif target == "conteAluminio":
            # Verificar cambio de estado
            if state != self.last_state_aluminio:
                return True
            # Verificar cambio de porcentaje significativo (5% o más)
            if (self.last_percent_aluminio is None or
                    abs(percent - self.last_percent_aluminio) >= 5):
                return True
        return False

    def update_last_state(self, target, percent, state):
        """
        Actualiza el estado anterior después de una actualización exitosa

        Args:
            target: Tipo de contenedor
            percent: Porcentaje de llenado
            state: Estado del contenedor
        """
        if target == "contePlastico":
            self.last_state_plastico = state
            self.last_percent_plastico = percent
        elif target == "conteAluminio":
            self.last_state_aluminio = state
            self.last_percent_aluminio = percent

    def update_detection_status(self, status, color="#3498db"):
        """
        Actualiza el estado de detección

        Args:
            status: Estado de la detección
            color: Color del estado
        """
        # Simplificar mensaje para pantalla pequeña
        if "Cámara activa" in status:
            short_status = "🔄 Detectando..."
        elif "detectado" in status.lower():
            short_status = "♻️ Material detectado!"
        else:
            short_status = status[:20] + "..." if len(status) > 20 else status
            
        self.pending_material_label.config(text=short_status, fg=color)

    def update_pending_material(self, material, points):
        """
        Actualiza el material pendiente y puntos

        Args:
            material: Material detectado
            points: Puntos a otorgar
        """
        if material:
            self.pending_material_label.config(
                text=f"♻️ {material.upper()}!", 
                fg='#27ae60'
            )
            self.pending_points_label.config(
                text=f"🎁 {points} pts - Pase NFC", 
                fg='#f39c12'
            )
        else:
            self.pending_material_label.config(
                text="🔄 Esperando...", 
                fg='#bdc3c7'
            )
            self.pending_points_label.config(text="", fg='#f39c12')

    def clear_pending_material(self):
        """Limpia el material pendiente"""
        self.pending_material_label.config(text="🔄 Esperando...", fg='#bdc3c7')
        self.pending_points_label.config(text="", fg='#f39c12')

    def log_esp32_command(self, material, success=True):
        """
        Registra el envío de comando a ESP32
        
        Args:
            material: Material enviado
            success: Si el envío fue exitoso
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        status_icon = "✅" if success else "❌"
        log_entry = f"[{ts}] {status_icon} ESP32: {material.upper()}\n"

        self.materials_text.config(state='normal')
        self.materials_text.insert('end', log_entry)
        self.materials_text.see('end')
        self.materials_text.config(state='disabled')