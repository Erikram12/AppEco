"""
Componentes de UI para el Sistema de Reciclaje Inteligente
=========================================================

Este módulo contiene todos los componentes de interfaz de usuario,
incluyendo la creación de widgets, actualización de estados y
manejo de la interfaz gráfica.
"""

import tkinter as tk
from tkinter import ttk
import datetime
from config.config import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_BG_COLOR, FRAME_BG_COLOR, TEXT_COLOR,
    STATUS_COLORS, CONTAINER_COLORS, CONTAINER_EMOJIS
)


class UIComponents:
    """Clase para manejar todos los componentes de la interfaz de usuario"""

    def __init__(self, root):
        """
        Inicializa los componentes de UI

        Args:
            root: Ventana principal de Tkinter
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=WINDOW_BG_COLOR)

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

        # Crear todos los widgets
        self._create_widgets()

    def _create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=WINDOW_BG_COLOR)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título principal
        self._create_title(main_frame)

        # Estado del sistema
        self._create_status_section(main_frame)

        # Información del usuario
        self._create_user_section(main_frame)

        # Progreso de sesión
        self._create_session_section(main_frame)

        # Materiales detectados
        self._create_materials_section(main_frame)

        # Estadísticas en tiempo real
        self._create_stats_section(main_frame)

        # Estado de componentes
        self._create_components_section(main_frame)

    def _create_title(self, parent):
        """Crea el título principal"""
        title_label = tk.Label(
            parent, text="♻️ SISTEMA DE RECICLAJE INTELIGENTE",
            font=('Arial', 24, 'bold'), bg=WINDOW_BG_COLOR, fg=TEXT_COLOR
        )
        title_label.pack(pady=(0, 20))

    def _create_status_section(self, parent):
        """Crea la sección de estado del sistema"""
        status_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        status_frame.pack(fill='x', pady=(0, 20))

        tk.Label(status_frame, text="📊 ESTADO DEL SISTEMA",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.status_label = tk.Label(status_frame, text="🔄 Iniciando sistema...",
                                     font=('Arial', 14), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.status_label.pack(pady=10)

    def _create_user_section(self, parent):
        """Crea la sección de información del usuario"""
        self.user_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        self.user_frame.pack(fill='x', pady=(0, 20))

        tk.Label(self.user_frame, text="🎯 ESTADO DE DETECCIÓN",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.user_info_label = tk.Label(self.user_frame, text="🔄 Detectando materiales...",
                                        font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#3498db')
        self.user_info_label.pack(pady=10)

    def _create_session_section(self, parent):
        """Crea la sección de progreso de sesión"""
        self.session_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        self.session_frame.pack(fill='x', pady=(0, 20))

        tk.Label(self.session_frame, text="🎁 MATERIAL PENDIENTE",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.session_label = tk.Label(self.session_frame, text="🔄 Esperando detección...",
                                      font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#bdc3c7')
        self.session_label.pack(pady=5)

        # Mostrar puntos pendientes
        self.pending_points_label = tk.Label(self.session_frame, text="",
                                            font=('Arial', 14, 'bold'), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.pending_points_label.pack(pady=5)

    def _create_materials_section(self, parent):
        """Crea la sección de materiales detectados"""
        materials_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        materials_frame.pack(fill='x', pady=(0, 20))

        tk.Label(materials_frame, text="📊 MATERIALES DETECTADOS",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        self.materials_text = tk.Text(materials_frame, height=8, width=60,
                                      font=('Consolas', 10), bg=WINDOW_BG_COLOR, fg=TEXT_COLOR,
                                      insertbackground='white', state='disabled')
        self.materials_text.pack(pady=5, padx=10)

        scrollbar = tk.Scrollbar(materials_frame, command=self.materials_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.materials_text.config(yscrollcommand=scrollbar.set)

    def _create_stats_section(self, parent):
        """Crea la sección de estadísticas en tiempo real"""
        stats_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        stats_frame.pack(fill='x', pady=(0, 20))

        tk.Label(stats_frame, text="📈 ESTADÍSTICAS EN TIEMPO REAL",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        stats_content_frame = tk.Frame(stats_frame, bg=FRAME_BG_COLOR)
        stats_content_frame.pack(pady=10)

        self.plastic_count_label = tk.Label(stats_content_frame, text="🥤 Plástico: 0",
                                            font=('Arial', 12, 'bold'), bg=FRAME_BG_COLOR, fg='#3498db')
        self.plastic_count_label.pack(side='left', padx=20)

        self.aluminum_count_label = tk.Label(stats_content_frame, text="🥫 Aluminio: 0",
                                             font=('Arial', 12, 'bold'), bg=FRAME_BG_COLOR, fg='#95a5a6')
        self.aluminum_count_label.pack(side='left', padx=20)

        self.total_points_label = tk.Label(stats_content_frame, text="🏆 Puntos Totales: 0",
                                           font=('Arial', 12, 'bold'), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.total_points_label.pack(side='left', padx=20)

    def _create_components_section(self, parent):
        """Crea la sección de estado de componentes"""
        components_frame = tk.Frame(parent, bg=FRAME_BG_COLOR, relief='raised', bd=2)
        components_frame.pack(fill='x', pady=(0, 20))

        tk.Label(components_frame, text="🔧 ESTADO DE COMPONENTES",
                 font=('Arial', 16, 'bold'), bg=FRAME_BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        components_content_frame = tk.Frame(components_frame, bg=FRAME_BG_COLOR)
        components_content_frame.pack(pady=10)

        self.nfc_status_label = tk.Label(components_content_frame, text="🎫 NFC: ⏳ Conectando...",
                                         font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.nfc_status_label.pack(side='left', padx=20)

        self.camera_status_label = tk.Label(components_content_frame, text="📷 Cámara: ⏳ Conectando...",
                                            font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.camera_status_label.pack(side='left', padx=20)

        self.mqtt_status_label = tk.Label(components_content_frame, text="📡 MQTT: ⏳ Conectando...",
                                          font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.mqtt_status_label.pack(side='left', padx=20)

        self.firebase_status_label = tk.Label(components_content_frame, text="🔥 Firebase: ⏳ Conectando...",
                                              font=('Arial', 12), bg=FRAME_BG_COLOR, fg='#f39c12')
        self.firebase_status_label.pack(side='left', padx=20)

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
        self.user_info_label.config(text=f"👤 Usuario: {email}", fg='#27ae60')

    def clear_user_info(self):
        """Limpia la información del usuario"""
        self.current_user = None
        self.user_info_label.config(text="⏳ Esperando autenticación...", fg='#bdc3c7')

    def update_session_status(self, active=True):
        """
        Actualiza el estado de la sesión

        Args:
            active: Si la sesión está activa
        """
        if active:
            self.session_active = True
            self.session_label.config(text="🟢 Sesión activa - Detectando materiales...", fg='#27ae60')
        else:
            self.session_active = False
            self.session_label.config(text="✅ Sesión finalizada", fg='#27ae60')
            self.progress_var.set(0)

    def update_progress(self, progress):
        """
        Actualiza la barra de progreso

        Args:
            progress: Valor de progreso (0-100)
        """
        self.progress_var.set(progress)

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
            container_name = "🥤 Plástico" if target == "contePlastico" else "🥫 Aluminio"
            log_entry = f"{emoji} {container_name}: {percent}% ({state}) - {distance_cm:.1f}cm\n"

            self.materials_text.config(state='normal')
            self.materials_text.insert('end', log_entry)
            self.materials_text.see('end')
            self.materials_text.config(state='disabled')

            # Actualizar el estado en la UI principal
            if target == "contePlastico":
                self.plastic_count_label.config(text=f"🥤 Plástico: {self.plastic_count} | {state}", fg=color)
            elif target == "conteAluminio":
                self.aluminum_count_label.config(text=f"🥫 Aluminio: {self.aluminum_count} | {state}", fg=color)

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
        log_entry = f"[{ts}] ♻️ {material.upper()} detectado (+{points} puntos)\n"

        self.materials_text.config(state='normal')
        self.materials_text.insert('end', log_entry)
        self.materials_text.see('end')
        self.materials_text.config(state='disabled')

        # Actualizar contadores
        if material == "plastico":
            self.plastic_count += 1
            self.plastic_count_label.config(text=f"🥤 Plástico: {self.plastic_count}")
        elif material == "aluminio":
            self.aluminum_count += 1
            self.aluminum_count_label.config(text=f"🥫 Aluminio: {self.aluminum_count}")

        self.total_points += points
        self.total_points_label.config(text=f"🏆 Puntos Totales: {self.total_points}")

    def update_component_status(self, component, status, color):
        """
        Actualiza el estado de un componente

        Args:
            component: Nombre del componente (nfc, camera, mqtt, firebase)
            status: Estado del componente
            color: Color del estado
        """
        if component == "nfc":
            self.nfc_status_label.config(text=f"🎫 NFC: {status}", fg=color)
        elif component == "camera":
            self.camera_status_label.config(text=f"📷 Cámara: {status}", fg=color)
        elif component == "mqtt":
            self.mqtt_status_label.config(text=f"📡 MQTT: {status}", fg=color)
        elif component == "firebase":
            self.firebase_status_label.config(text=f"🔥 Firebase: {status}", fg=color)

    def append_material_log(self, label, value, extra=None):
        """
        Agrega una entrada al log de materiales

        Args:
            label: Etiqueta del log
            value: Valor a registrar
            extra: Información adicional (opcional)
        """
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] 📡 {label}: {value}"
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
        self.user_info_label.config(text=status, fg=color)

    def update_pending_material(self, material, points):
        """
        Actualiza el material pendiente y puntos

        Args:
            material: Material detectado
            points: Puntos a otorgar
        """
        if material:
            self.session_label.config(text=f"♻️ {material.upper()} detectado!", fg='#27ae60')
            self.pending_points_label.config(text=f"🎁 {points} puntos pendientes - Pase su tarjeta NFC", fg='#f39c12')
        else:
            self.session_label.config(text="🔄 Esperando detección...", fg='#bdc3c7')
            self.pending_points_label.config(text="", fg='#f39c12')

    def clear_pending_material(self):
        """Limpia el material pendiente"""
        self.session_label.config(text="🔄 Esperando detección...", fg='#bdc3c7')
        self.pending_points_label.config(text="", fg='#f39c12')
