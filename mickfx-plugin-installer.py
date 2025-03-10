import sys
import os
import random
import shutil

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QMessageBox, QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QUrl, QPropertyAnimation, QRectF, QPointF, QEasingCurve
from PyQt5.QtGui import QPixmap, QPainter, QMovie, QFontDatabase, QIcon, QColor, QFont, QPainterPath, QPen, QDesktopServices
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class LogoBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._background_image = None
        self.setAttribute(Qt.WA_StyledBackground, True)

    @property
    def background_image(self):
        if self._background_image is None:
            self._background_image = QPixmap(resource_path(os.path.join("MickFX Required Sources", "MickFX Background.jpg")))
        return self._background_image

class OBSPluginInstaller(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set only critical properties immediately
        self.setWindowTitle("MickFX OBS Plugin Installer")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setStyleSheet("background-color: #662D91;")
        
        # Initialize basic variables
        self.plugin_alert_shown = False
        self.installation_in_progress = False
        self.current_popup = None
        self._success_player = None
        self._error_player = None
        self._end_player = None
        self._loading_player = None
        self._media_player = None

        # Create basic layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create and add the background containers immediately
        self.logo_background = LogoBackgroundWidget(self)
        self.logo_background.setFixedHeight(190)
        self.main_layout.addWidget(self.logo_background)
        
        self.content_background = ContentBackgroundWidget(self)
        self.main_layout.addWidget(self.content_background)
        
        # Stage the initialization
        QTimer.singleShot(0, self.init_stage1)

    def init_stage1(self):
        # Load font
        self.resource_folder = self.find_resource_folder()
        font_path = resource_path(os.path.join("MickFX Required Sources", "Tomorrow-Medium.ttf"))
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        # Start background music
        QTimer.singleShot(0, self.init_background_music)
        
        # Continue with UI setup
        QTimer.singleShot(0, self.init_stage2)

    def init_stage2(self):
        # Initialize content layout
        self.content_layout = QVBoxLayout(self.content_background)
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Continue with the rest of your UI initialization
        QTimer.singleShot(0, self.complete_initialization)

    def lazy_load_media_player(self):
        if self._media_player is None:
            self._media_player = QMediaPlayer()
            self._media_player.setMedia(QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "MickFX Song.mp3")))))
            self._media_player.setVolume(75)
        return self._media_player

    def get_success_player(self):
        if self._success_player is None:
            self._success_player = QMediaPlayer()
            self._success_player.setVolume(50)
        return self._success_player

    def play_success_sound(self):
        if not hasattr(self, '_success_sounds'):
            self._success_sounds = []
            for i in range(1, 4):
                sound = QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", f"Yoshi{i}.mp3"))))
                self._success_sounds.append(sound)
        
        player = self.get_success_player()
        player.setMedia(random.choice(self._success_sounds))
        player.play()

    def play_error_sound(self):
        if self._error_player is None:
            self._error_player = QMediaPlayer()
            self._error_player.setVolume(50)
            self._error_player.setMedia(QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi Error.mp3")))))
        self._error_player.play()

    def play_end_sound(self):
        if self._end_player is None:
            self._end_player = QMediaPlayer()
            self._end_player.setVolume(50)
            self._end_player.setMedia(QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi End.mp3")))))
        self._end_player.play()

    def play_loading_sound(self):
        if self._loading_player is None:
            self._loading_player = QMediaPlayer()
            self._loading_player.setVolume(50)
            self._loading_player.setMedia(QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi Loading.mp3")))))
        self._loading_player.play()

    def init_background_music(self):
        self._media_player = QMediaPlayer()
        self._media_player.setMedia(QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "MickFX Song.mp3")))))
        self._media_player.setVolume(75)
        self._media_player.play()

    def complete_initialization(self):
        from PyQt5.QtCore import QSize
        # Start loading the background music after UI is shown
        QTimer.singleShot(100, lambda: self.lazy_load_media_player().play())
        # Load custom font
        self.resource_folder = self.find_resource_folder()
        font_path = resource_path(os.path.join("MickFX Required Sources", "Tomorrow-Medium.ttf"))
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("Error loading custom font")
            font_family = "Arial"  # Fallback font
            
        # Sound effect setup
        self.setup_sound_effects()
        # Define colors
        purple_color = QColor(102, 45, 145)        # Main purple color
        gold_color = QColor(255, 215, 0)           # Gold color
        disabled_gold_color = QColor(204, 172, 0)  # Lighter gold for disabled state

        # Apply styles
        self.setStyleSheet(f"""
            QLabel {{
                color: white;
            }}
            QPushButton {{
                background-color: {gold_color.name()};
                color: black;
                border: 1px solid transparent;
                padding: 8px 16px;
                min-width: 10px;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {gold_color.lighter(150).name()};
            }}
            QPushButton:pressed {{
                background-color: {gold_color.darker(150).name()};
            }}
            QPushButton:disabled {{
                background-color: {disabled_gold_color.name()};
                color: #888;
            }}
            QProgressBar {{
                border: 3px solid {gold_color.name()};
                border-radius: 5px;
                background-color: #555;
                color: white;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {gold_color.name()};
                width: 10px;
            }}
            #message-signature-card {{
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                padding: 15px;
                border: 3px solid #000000;
                }}
        QMessageBox {{
            background-color: #662D91;
            border: 2px solid #4A1D6A;
            border-radius: 10px;
        }}
        QMessageBox QLabel {{
            color: {gold_color.name()};
            font-weight: bold;
            font-size: 16px;
            margin: 10px 20px;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }}
        QMessageBox QPushButton {{
            background-color: {gold_color.name()};
            color: #4A1D6A;
            border: 2px solid #4A1D6A;
            padding: 8px 20px;
            border-radius: 5px;
            font-weight: bold;
            font-size: 14px;
            min-width: 100px;
        }}
        QMessageBox QPushButton:hover {{
            background-color: {gold_color.lighter(120).name()};
            border-color: {gold_color.darker(120).name()};
        }}
        QMessageBox QPushButton:pressed {{
            background-color: {gold_color.darker(110).name()};
            border-color: {gold_color.darker(130).name()};
        }}
        QMessageBox QDialogButtonBox {{
            button-layout: center;
            margin-top: 15px;
            margin-bottom: 10px;
        }}
        QMessageBox QLabel#qt_msgboxex_icon_label {{
            padding: 10;
            margin: 14px 0 0 20px;  /* Top, Right, Bottom, Left */
            alignment: top;
        }}
        QMessageBox QTextEdit {{
            background-color: rgba(0, 0, 0, 0.1);
            border-radius: 5px;
            padding: 10px;
            margin: 10px 20px 10px 0px;  /* Top, Right, Bottom, Left */
            color: {gold_color.name()};
            font-weight: bold;
            font-size: 17px;
        }}
        """)

        # Clear any existing widgets from main layout
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Create background container for logo
        logo_background = LogoBackgroundWidget(self)
        logo_background.setFixedHeight(190)  # Adjust this value as needed
        self.main_layout.addWidget(logo_background)

        # Logo layout inside logo background
        logo_layout = QVBoxLayout(logo_background)
        logo_layout.setContentsMargins(0, 5, 20, 40)  # Adjust margins as needed
        
        self.logo_label = ScalingClickableLabel()
        self.logo_movie = QMovie(resource_path(os.path.join("MickFX Required Sources", "MickFX Logo.gif")))
        self.logo_label.setMovie(self.logo_movie)
        self.logo_movie.setSpeed(140)  # Base speed
        self.logo_movie.start()
        logo_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)

        # Content container with the second background
        content_background = ContentBackgroundWidget(self)
        self.main_layout.addWidget(content_background)

        # Separate layouts for Paragraph/Signature and Icons
        content_layout = QVBoxLayout(content_background)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Paragraph/Signature layout
        self.paragraph_signature_layout = QVBoxLayout()
        self.paragraph_signature_layout.setContentsMargins(42, 5, 42, 5)  # Adjust margins as needed

        # Message and signature card
        self.message_signature_card = QWidget()
        self.message_signature_card.setObjectName("message-signature-card")
        message_signature_layout = QVBoxLayout(self.message_signature_card)

        paragraph_text = QLabel("Welcome to the future of streaming! I hope that\nyou and your viewers enjoy my effects as\nmuch as I enjoyed making them. Stay cool.")
        paragraph_text.setWordWrap(True)
        paragraph_text.setAlignment(Qt.AlignCenter)

        paragraph_font = QFont(font_family)
        paragraph_font.setPointSize(16)  # Larger font for paragraph
        paragraph_text.setFont(paragraph_font)
        message_signature_layout.addWidget(paragraph_text)

        signature_label = QLabel("-MickYayger")
        signature_label.setAlignment(Qt.AlignCenter)

        signature_font = QFont(font_family)
        signature_font.setPointSize(14)  # Smaller font for signature
        signature_label.setFont(signature_font)

        message_signature_layout.addWidget(signature_label)
        self.paragraph_signature_layout.addWidget(self.message_signature_card)

        # Add paragraph/signature layout to content layout
        content_layout.addLayout(self.paragraph_signature_layout)

        # Icons layout
        self.icons_layout = QVBoxLayout()
        self.icons_layout.setContentsMargins(10, 0, 5, 1)  # Adjust margins as needed

        social_mute_layout = QHBoxLayout()

        # Mute button (now on the left)
        self.mute_button = QPushButton()
        self.mute_button.setIcon(QIcon(os.path.join(self.resource_folder, "Volume Icon.png")))
        self.mute_button.setIconSize(QSize(24, 24))
        self.mute_button.setFixedSize(32, 32)
        self.mute_button.setStyleSheet("""
            QPushButton {
                background-color: #FFD700;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FFC700;
            }
        """)
        self.mute_button.clicked.connect(self.toggle_mute)
        social_mute_layout.addWidget(self.mute_button)

        social_mute_layout.addSpacing(10)  # Add some space between mute button and social icons

        # Add social media icons
        social_icons = [
            ("Discord Logo.png", "https://discord.gg/m3pmBhDnts"),
            ("Youtube Logo.png", "https://www.youtube.com/@MickYayger"),
            ("X Logo.png", "https://x.com/MickFXOfficial"),
            ("Twitch Logo.png", "https://www.twitch.tv/mickyayger")
        ]

        for icon_file, url in social_icons:
            icon_button = QPushButton()
            icon_button.setIcon(QIcon(os.path.join(self.resource_folder, icon_file)))
            icon_button.setIconSize(QSize(30, 30))
            icon_button.setFixedSize(34, 34)
            icon_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                }
            """)
            icon_button.clicked.connect(lambda checked, url=url: QDesktopServices.openUrl(QUrl(url)))
            social_mute_layout.addWidget(icon_button)

        # Add spacer to push everything to the left
        social_mute_layout.addStretch(1)

        # Add link to MickFX website
        mickfx_link = QPushButton("Click here to go to MickFX!")

        # Create shadow effect for the link
        link_shadow = QGraphicsDropShadowEffect()
        link_shadow.setBlurRadius(10)
        link_shadow.setColor(QColor(0, 0, 0, 180))
        link_shadow.setOffset(2, 2)
        mickfx_link.setGraphicsEffect(link_shadow)

        mickfx_link.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #ffd700;
                border: none;
                text-decoration: underline;
                font-size: 21px;
                font-weight: bold;      
            }
            QPushButton:hover {
                color: #fae15c;
            }
        """)
        mickfx_link.setCursor(Qt.PointingHandCursor)
        mickfx_link.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.mickfx.com")))
        social_mute_layout.addWidget(mickfx_link)

        # Add the social_mute_layout to the icons layout
        self.icons_layout.addLayout(social_mute_layout)

        # Add icons layout to content layout
        content_layout.addLayout(self.icons_layout)

        # OBS selection layout (renamed from obs_sammi_layout)
        self.obs_layout = QVBoxLayout()
        self.obs_layout.setContentsMargins(10, 4, 10, 4)  # Normal margins for content

        lower_card_widget = QWidget()
        lower_card_widget.setObjectName("lower-card")
        lower_card_widget.setStyleSheet("""
            #lower-card {
                background: qlineargradient(
                    x1: 0.5, y1: 0, 
                    x2: 1, y2:0,
                    stop: 0 rgba(134, 64, 164, 1.0), 
                    stop: 1 rgba(106, 44, 153, 1.0)
                );
                border: 1px solid #000000;
                border-radius: 4px;
            }
        """)

        # Create the shadow effect
        shadow = QGraphicsDropShadowEffect(lower_card_widget)
        shadow.setBlurRadius(15)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 170))

        # Apply the shadow to the widget
        lower_card_widget.setGraphicsEffect(shadow)

        lower_card_layout = QVBoxLayout(lower_card_widget)

        # Reduce vertical spacing
        lower_card_layout.setSpacing(5)

        # Set individual padding for each side
        left_padding = 15
        top_padding = 6
        right_padding = 15
        bottom_padding = 10

        lower_card_layout.setContentsMargins(left_padding, top_padding, right_padding, bottom_padding)

        # Bold and bigger OBS selection text with updated text
        self.obs_label = QLabel("<b style='font-size: 16px;'>Select your OBS.exe</b>")
        lower_card_layout.addWidget(self.obs_label)
        
        # Path information with inline styling for shading effect
        self.path_info = QLabel("This is what you use to launch OBS with. Your OBS installation path is <span style='background-color: rgba(0, 0, 0, 0.3); border-radius: 4px; padding: 2px 6px; color: #FFD700; font-family: monospace;'>OBS-Studio -> 64bit -> obs64.exe</span>")
        self.path_info.setWordWrap(True)
        lower_card_layout.addWidget(self.path_info)

        self.obs_button = QPushButton("Select obs64.exe")
        self.obs_button.clicked.connect(self.select_obs_exe)
        lower_card_layout.addWidget(self.obs_button)

        self.plugin_layout = QVBoxLayout()
        lower_card_layout.addLayout(self.plugin_layout)
        
        from PyQt5.QtWidgets import QProgressBar
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        lower_card_layout.addWidget(self.progress_bar)

        # Add the lower card widget to the obs_layout
        self.obs_layout.addWidget(lower_card_widget)

        self.obs_layout.addSpacing(1)  # Add a spacer at the bottom

        self.link_label = QLabel('<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" style="color: #9729ff; font-size: 10px;">Click me.</a>')
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setAlignment(Qt.AlignCenter)
        self.obs_layout.addWidget(self.link_label)

        # Add obs_layout to content layout
        content_layout.addLayout(self.obs_layout)

        self.setLayout(self.main_layout)

        self.plugins = [
            {
                "name": "Source Clone",
                "description": "Allows you to clone sources.",
                "page_url": "https://obsproject.com/forum/resources/source-clone.1632/",
                "download_url": "https://obsproject.com/forum/resources/source-clone.1632/version/5627/download?file=104021",
                "file_name": "source-clone.pdb",
                "required": True
            },
            {
                "name": "Obs-shaderfilter",
                "description": "Allows you to add shaders effects to sources.",
                "page_url": "https://obsproject.com/forum/resources/obs-shaderfilter.1736/",
                "download_url": "https://github.com/exeldro/obs-shaderfilter/releases/download/2.3.2/obs-shaderfilter-2.3.2-windows.zip",
                "file_name": "obs-shaderfilter.pdb",
                "required": True
            },
            {
                "name": "Advanced Masks",
                "description": "Set up masks which you can change.",
                "page_url": "https://obsproject.com/forum/resources/advanced-masks.1856/",
                "download_url": "https://obsproject.com/forum/resources/advanced-masks.1856/version/5424/download?file=101265",
                "file_name": "obs-advanced-masks.pdb",
                "required": True
            },
            {
                "name": "Move Source",
                "description": "Move sources and change values.",
                "page_url": "https://obsproject.com/forum/resources/move.913/",
                "download_url": "https://obsproject.com/forum/resources/move.913/version/5662/download?file=104546",
                "file_name": "move-transition.pdb",
                "required": True
            },
            {
                "name": "Vintage Filter",
                "description": "Adds black & white or sepia effects to sources.",
                "page_url": "https://obsproject.com/forum/resources/vintage-filter.818/",
                "download_url": "https://github.com/cg2121/obs-vintage-filter/releases/download/1.0.0/obs-vintage-filter-1.0.0-windows-x64.zip",
                "file_name": "obs-vintage-filter.dll",
                "required": False
            }
        ]
        self.resource_folder = self.find_resource_folder()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_plugins)
        QTimer.singleShot(100, self.adjustSize)
        self.layout_updated = False
        

    def setup_sound_effects(self):
        # Create separate players for different types of sounds
        self.success_player = QMediaPlayer()
        self.error_player = QMediaPlayer()
        self.end_player = QMediaPlayer()
        self.loading_player = QMediaPlayer()
        
        # Load success sounds (Yoshi1, Yoshi2, Yoshi3)
        self.success_sounds = []
        for i in range(1, 4):  # Will load Yoshi1.mp3, Yoshi2.mp3, Yoshi3.mp3
            sound = QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", f"Yoshi{i}.mp3"))))
            self.success_sounds.append(sound)
        
        # Load error and end sounds
        self.error_sound = QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi Error.mp3"))))
        self.end_sound = QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi End.mp3"))))
        self.loading_sound = QMediaContent(QUrl.fromLocalFile(resource_path(os.path.join("MickFX Required Sources", "Yoshi Loading.mp3"))))
        
        # Set default volumes
        self.success_player.setVolume(50)
        self.error_player.setVolume(50)
        self.end_player.setVolume(50)
        self.loading_player.setVolume(50)
            
    def adjustSize(self):
        # Force layout update
        self.layout().activate()
        # Adjust window size to content
        super().adjustSize()
        # Update logo size
        if hasattr(self, 'logo_label'):
            self.logo_label.updatePixmap()

    def showEvent(self, event):
        super().showEvent(event)
        # Trigger adjust size after show event
        QTimer.singleShot(100, self.adjustSize)

    def find_resource_folder(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        resource_folder = os.path.join(current_folder, "MickFX Required Sources")
        if os.path.exists(resource_folder):
            return resource_folder
        resource_folder = os.path.join(current_folder, "..", "MickFX Required Sources")
        if os.path.exists(resource_folder):
            return resource_folder
        return ""

    def toggle_mute(self):
        if self._media_player.isMuted():
            self._media_player.setMuted(False)
            self.mute_button.setIcon(QIcon(os.path.join(self.resource_folder, "Volume Icon.png")))
        else:
            self._media_player.setMuted(True)
            self.mute_button.setIcon(QIcon(os.path.join(self.resource_folder, "Mute Icon.png")))

    def hide_paragraph_signature(self):
        if hasattr(self, 'message_signature_card'):
            self.message_signature_card.hide()

    def select_obs_exe(self):
        from PyQt5.QtWidgets import QFileDialog
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("OBS Executable (obs64.exe)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            if selected_file.endswith("obs64.exe"):
                print(f"Selected OBS executable: {selected_file}")
                self.obs_exe_path = selected_file
                self.obs_button.setText(self.obs_exe_path)
                
                # Hide the paragraph and signature
                self.hide_paragraph_signature()
                
                # Now check the plugins
                success = self.check_plugins()
                
                if not success:
                    self.play_error_sound()
                    print("Failed to check plugins")
                    QMessageBox.warning(self, "Error", "Failed to find or update plugins. Please check the OBS installation.")
                
                # Adjust margins
                self.obs_layout.setContentsMargins(10, 0, 10, 4)
                self.icons_layout.setContentsMargins(10, 0, 5, 0)
                self.paragraph_signature_layout.setContentsMargins(42, 0, 42, 0)
                
                # Force another update of the UI
                QApplication.processEvents()
                
                # Update the layout manually
                self.update_plugin_layout(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.obs_exe_path))), "obs-plugins", "64bit"))
                
            else:
                QMessageBox.warning(self, "Error", "Please select the correct obs64.exe file.")

    def check_plugins(self):
        print("Starting check_plugins method")
        if not self.obs_exe_path:
            print("OBS executable path is not set")
            return False

        plugins_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.obs_exe_path))), "obs-plugins", "64bit")
        print(f"Plugins folder: {plugins_folder}")

        if not os.path.exists(plugins_folder):
            print(f"Plugins folder not found: {plugins_folder}")
            return False

        print(f"Current plugin layout count: {self.plugin_layout.count()}")

        if self.plugin_layout.count() == 0:
            print("Creating initial plugin layout")
            self.initial_plugin_layout(plugins_folder)
        else:
            print("Updating existing plugin layout")
            self.update_plugin_layout(plugins_folder)

        print("Finished check_plugins method")
        return True

    def initial_plugin_layout(self, plugins_folder):
        if not os.path.exists(plugins_folder) or not self.obs_exe_path:
            return False

        all_required_installed = True

        # First handle required plugins
        for plugin in [p for p in self.plugins if p["required"]]:
            plugin_installed = os.path.exists(os.path.join(plugins_folder, plugin["file_name"]))
            print(f"Plugin: {plugin['name']}, Installed: {plugin_installed}")

            if not plugin_installed:
                all_required_installed = False

            # Create a new plugin layout
            plugin_layout = QVBoxLayout()
            plugin_layout.setContentsMargins(5, 5, 5, 5)
            plugin_layout.setSpacing(5)

            plugin_label = QLabel(f"<b>{plugin['name']}</b> - {plugin['description']}")
            plugin_label.setObjectName(f"label_{plugin['name']}")
            plugin_label.setWordWrap(True)
            plugin_layout.addWidget(plugin_label)

            button_layout = QHBoxLayout()

            page_button = QPushButton("Plugin Page")
            page_button.setStyleSheet("color: blue;")
            page_button.clicked.connect(lambda _, url=plugin['page_url']: QDesktopServices.openUrl(QUrl(url)))
            button_layout.addWidget(page_button, 1)

            status_frame = QFrame()
            status_frame.setFrameShape(QFrame.Box)
            status_frame.setFrameShadow(QFrame.Raised)
            status_frame_layout = QHBoxLayout(status_frame)
            status_frame_layout.setContentsMargins(0, 0, 0, 0)
            status_frame_layout.setSpacing(0)

            status_label = QLabel("Installed" if plugin_installed else "Not Installed")
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setObjectName(f"status_label_{plugin['name']}")
            status_label.setStyleSheet("font-weight: bold;" if plugin_installed else "font-weight: bold; color: red;")
            status_frame_layout.addWidget(status_label)

            if not plugin_installed:
                install_button = QPushButton("Auto-Install")
                install_button.setObjectName(f"install_button_{plugin['name']}")
                install_button.setStyleSheet("background-color: #e5f3ff; font-weight: bold;")
                install_button.clicked.connect(lambda _, p=plugin: self.install_plugin(p))
                status_frame_layout.addWidget(install_button)

            status_frame_layout.setStretch(0, 2)
            status_frame_layout.setStretch(1, 2)

            button_layout.addWidget(status_frame, 2)

            plugin_layout.addLayout(button_layout)

            # Add the plugin layout to the main plugin layout
            self.plugin_layout.addLayout(plugin_layout)
            print(f"Added plugin layout for {plugin['name']} to the layout")  # Debugging statement

        # Add separator and Optional Plugins section
        optional_plugins = [p for p in self.plugins if not p["required"]]
        
        if optional_plugins:
            # Add separator
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet("""
                QFrame {
                    color: #FFD700;
                    height: 2px;
                    margin: 10px 0px;
                }
            """)
            self.plugin_layout.addWidget(separator)

            # Add "Optional Plugins" header
            optional_header = QLabel("MickFX Wasted Optional Vintage Plugin")
            optional_header.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    margin-top: 5px;
                }
            """)
            self.plugin_layout.addWidget(optional_header)

            # Now handle optional plugins
            for plugin in optional_plugins:
                plugin_installed = os.path.exists(os.path.join(plugins_folder, plugin["file_name"]))
                print(f"Plugin: {plugin['name']}, Installed: {plugin_installed}")

                # Create a new plugin layout
                plugin_layout = QVBoxLayout()
                plugin_layout.setContentsMargins(5, 5, 5, 5)
                plugin_layout.setSpacing(5)

                plugin_label = QLabel(f"<b>{plugin['name']}</b> - {plugin['description']}")
                plugin_label.setObjectName(f"label_{plugin['name']}")
                plugin_label.setWordWrap(True)
                plugin_layout.addWidget(plugin_label)

                button_layout = QHBoxLayout()

                page_button = QPushButton("Plugin Page")
                page_button.setStyleSheet("color: blue;")
                page_button.clicked.connect(lambda _, url=plugin['page_url']: QDesktopServices.openUrl(QUrl(url)))
                button_layout.addWidget(page_button, 1)

                status_frame = QFrame()
                status_frame.setFrameShape(QFrame.Box)
                status_frame.setFrameShadow(QFrame.Raised)
                status_frame_layout = QHBoxLayout(status_frame)
                status_frame_layout.setContentsMargins(0, 0, 0, 0)
                status_frame_layout.setSpacing(0)

                status_label = QLabel("Installed" if plugin_installed else "Not Installed")
                status_label.setAlignment(Qt.AlignCenter)
                status_label.setObjectName(f"status_label_{plugin['name']}")
                status_label.setStyleSheet("font-weight: bold;" if plugin_installed else "font-weight: bold; color: red;")
                status_frame_layout.addWidget(status_label)

                if not plugin_installed:
                    install_button = QPushButton("Auto-Install")
                    install_button.setObjectName(f"install_button_{plugin['name']}")
                    install_button.setStyleSheet("background-color: #e5f3ff; font-weight: bold;")
                    install_button.clicked.connect(lambda _, p=plugin: self.install_plugin(p))
                    status_frame_layout.addWidget(install_button)

                status_frame_layout.setStretch(0, 2)
                status_frame_layout.setStretch(1, 2)

                button_layout.addWidget(status_frame, 2)

                plugin_layout.addLayout(button_layout)

                # Add the plugin layout to the main plugin layout
                self.plugin_layout.addLayout(plugin_layout)
                print(f"Added plugin layout for {plugin['name']} to the layout")  # Debugging statement

        # Start the timer if not all required plugins are installed
        if not all_required_installed:
            print("Not all required plugins are installed. Starting the timer.")
            self.timer.start(5000)
        else:
            print("All required plugins are installed. Copying SEF and showing alert.")
            success = self.copy_sef_to_downloads()
            if success:
                QTimer.singleShot(2000, lambda: self.extracting_popup.close())
                QTimer.singleShot(2250, self.install_ext_alert)

        return True

    def update_plugin_layout(self, plugins_folder):
        if not os.path.exists(plugins_folder) or not self.obs_exe_path:
            return False

        all_required_installed = True  # Change this to track only required plugins
        for i in range(self.plugin_layout.count()):
            plugin_layout = self.plugin_layout.itemAt(i).layout()
            if plugin_layout:
                status_label = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QLabel)
                if status_label:
                    plugin_name = status_label.objectName().split("_")[2]
                    plugin = next((p for p in self.plugins if p["name"] == plugin_name), None)
                    if plugin:
                        plugin_installed = os.path.exists(os.path.join(plugins_folder, plugin["file_name"]))
                        if plugin_installed:
                            status_label.setText("Installed")
                            status_label.setStyleSheet("font-weight: bold;")

                            install_button = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QPushButton, f"install_button_{plugin['name']}")
                            if install_button:
                                install_button.setVisible(False)
                        else:
                            if plugin.get("required", True):  # Only affect all_required_installed if it's a required plugin
                                all_required_installed = False
                            status_label.setText("Not Installed")
                            status_label.setStyleSheet("font-weight: bold; color: red;")

                            install_button = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QPushButton, f"install_button_{plugin['name']}")
                            if install_button:
                                install_button.setVisible(True)

        # Only show alert if it hasn't been shown yet and we're not in the middle of installing
        if not self.plugin_alert_shown and not hasattr(self, 'installation_in_progress'):
            # Check if all required plugins are installed
            all_required_installed = all(os.path.exists(os.path.join(plugins_folder, p["file_name"])) 
                                      for p in self.plugins if p.get("required", True))
            if all_required_installed:
                print("Showing initial alert")
                self.plugin_alert_shown = True
                self.install_ext_alert()
        elif not self.layout_updated:
            # Force layout update only once
            self.updateGeometry()
            self.adjustSize()
            self.layout_updated = True

        return all_required_installed

    def on_plugin_download_finished(self, zip_path, plugin):
        import zipfile
        try:
            # Get OBS root directory
            obs_root = os.path.dirname(os.path.dirname(os.path.dirname(self.obs_exe_path)))
            
            # Extract all files from the zip to the OBS root directory
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(obs_root)
                
            # Clean up temp folder
            temp_folder = os.path.dirname(zip_path)
            shutil.rmtree(temp_folder)
            
            self.progress_bar.setVisible(False)
                  
            # Store the popup reference
            self.current_popup = PopupBox("Plugin Installed", 
                f"The plugin '{plugin['name']}' has been installed successfully.", self)

            # Check if all required plugins are installed
            all_required_installed = True
            obs_plugins_folder = os.path.join(obs_root, "obs-plugins", "64bit")
            for i in range(self.plugin_layout.count()):
                plugin_layout = self.plugin_layout.itemAt(i).layout()
                if plugin_layout:
                    status_label = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QLabel)
                    if status_label:
                        plugin_name = status_label.objectName().split("_")[2]
                        current_plugin = next((p for p in self.plugins if p["name"] == plugin_name), None)
                        if current_plugin and current_plugin.get("required", True):  # Only check required plugins
                            plugin_installed = os.path.exists(os.path.join(obs_plugins_folder, current_plugin["file_name"]))
                            if not plugin_installed:
                                all_required_installed = False
                                break

            # Connect appropriate handler based on whether this is the final required plugin
            if all_required_installed and plugin.get("required", True):  # Only trigger for required plugins
                for button in self.current_popup.findChildren(QPushButton):
                    if button.text() == "OK":
                        button.clicked.disconnect()
                        button.clicked.connect(lambda: self.handle_final_plugin_ok(self.current_popup))
            else:
                for button in self.current_popup.findChildren(QPushButton):
                    if button.text() == "OK":
                        button.clicked.disconnect()
                        button.clicked.connect(lambda: self.handle_plugin_ok(self.current_popup))

            self.current_popup.show()
            self.play_success_sound()

            # Update UI states
            self.update_plugin_status(obs_plugins_folder)
            QTimer.singleShot(100, self.update_layout)

        except Exception as e:
            self.play_error_sound()
            QMessageBox.critical(self, "Error", f"An error occurred during plugin installation: {str(e)}")
            print(f"Error during plugin installation: {str(e)}")
        finally:
            if not self.timer.isActive():
                self.timer.start(5000)
            
    def handle_plugin_ok(self, popup):
        """Handler for non-final plugin installations"""
        popup.close()
        self.current_popup = None
        self.installation_in_progress = False

    def update_plugin_status(self, plugins_folder):
        """Update the UI status for all plugins"""
        for i in range(self.plugin_layout.count()):
            plugin_layout = self.plugin_layout.itemAt(i).layout()
            if plugin_layout:
                status_label = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QLabel)
                if status_label:
                    plugin_name = status_label.objectName().split("_")[2]
                    current_plugin = next((p for p in self.plugins if p["name"] == plugin_name), None)
                    if current_plugin:
                        plugin_installed = os.path.exists(os.path.join(plugins_folder, current_plugin["file_name"]))
                        if plugin_installed:
                            status_label.setText("Installed")
                            status_label.setStyleSheet("font-weight: bold;")
                            install_button = plugin_layout.itemAt(1).layout().itemAt(1).widget().findChild(QPushButton, f"install_button_{current_plugin['name']}")
                            if install_button:
                                install_button.setVisible(False)

    def update_layout(self):
        # Update the layout of this widget and all child widgets
        self.updateGeometry()
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget():
                item.widget().updateGeometry()
        
        # Force an immediate layout update
        self.layout().update()
        
        # Adjust the window size
        self.adjustSize()
        
        # Set the window size to its sizeHint
        new_size = self.sizeHint()
        self.resize(new_size)
        
        # Force a repaint
        self.repaint()

    @pyqtSlot(str)
    def on_plugin_download_error(self, error_message):
        self.play_error_sound()
        QMessageBox.critical(self, "Error", f"An error occurred during file download: {error_message}")
        print(f"Error during file download: {error_message}")
        self.progress_bar.setVisible(False)
        self.timer.start(5000)  # Restart the timer

    @pyqtSlot(dict)
    def install_plugin(self, plugin):
        if not hasattr(self, 'requests'):
            import requests
            self.requests = requests  # Import once and store as instance variable
            
        if hasattr(self, 'installation_in_progress') and self.installation_in_progress:
            print("Installation already in progress")
            return

        self.installation_in_progress = True
        try:
            # Stop the timer
            if self.timer.isActive():
                print("Stopping the timer for plugin installation.")
                self.timer.stop()

            temp_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
            os.makedirs(temp_folder, exist_ok=True)

            zip_path = os.path.join(temp_folder, f"{plugin['name']}.zip")
            signals = DownloadSignals()
            worker = DownloadWorker(plugin['download_url'], zip_path, signals)
            
            signals.finished.connect(lambda path: self.on_plugin_download_finished(path, plugin))
            signals.error.connect(self.on_plugin_download_error)
            signals.progress.connect(self.update_progress_bar)

            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.update_layout()
            
            QThreadPool.globalInstance().start(worker)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during plugin installation: {str(e)}")
            print(f"Error during plugin installation: {str(e)}")
            
            # Update the label to "Installed"
            plugin_frame = self.plugin_layout.itemAt(self.plugins.index(plugin)).widget()
            status_label = plugin_frame.findChild(QLabel, "status_label")
            if status_label:
                status_label.setText("Installed")
                status_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Remove the "Auto-Install" button
            install_button = plugin_frame.findChild(QPushButton, "install_button")
            if install_button:
                install_button.setParent(None)
            
            self.check_plugins()
            
            # Start the timer if not all plugins are installed
            if not self.update_plugin_layout(os.path.dirname(self.obs_exe_path)):
                print("Not all plugins are installed. Restarting the timer.")
                self.timer.start(5000)

    def handle_final_plugin_ok(self, popup):
            popup.close()
            self.installation_in_progress = False
            self.plugin_alert_shown = True
            success = self.copy_sef_to_downloads()
            if success:
                QTimer.singleShot(2000, lambda: self.extracting_popup.close())
                QTimer.singleShot(2250, self.install_ext_alert)
            
    def install_ext_alert(self):
        popup1 = DetailedPopupBox("SEF File Downloaded", 
            "MickFX Base.sef has been copied to your Downloads folder.\n\n"
            "To install in SAMMI:\n"
            "1. Open SAMMI\n"
            "2. Select SAMMI Bridge on left\n"
            "3. Click 'Import Extension'\n"
            "4. Select 'MickFX Base.sef' from your Downloads folder\n\n"
            "Feel free to download any optional plugins before closing.", self)
        # Modify the OK button behavior
        for button in popup1.findChildren(QPushButton):
            if button.text() == "OK":
                button.clicked.disconnect()
                button.clicked.connect(lambda: self.on_first_popup_ok(popup1))
        popup1.show()

    def on_first_popup_ok(self, popup):
        popup.close()
        
        # Set plugin_alert_shown and continue showing the UI
        self.plugin_alert_shown = True
        
        # Still allow the user to see and install optional plugins
        popup2 = PopupBox("Installation Complete", 
            "Required plugins installed!\nFeel free to install optional plugins.", self)
        popup2.show()
        self.play_end_sound()

    @pyqtSlot(int, int)
    def update_progress_bar(self, current, total):
        if total > 0:
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)

    def copy_sef_to_downloads(self):
        try:
            self.extracting_popup = PopupBox("Please Wait", "Extracting MickFX Base...", self)
            for button in self.extracting_popup.findChildren(QPushButton):
                if button.text() == "OK":
                    button.hide()
            self.extracting_popup.show()
            self.play_loading_sound()
            
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            
            # Updated path to look in the Required Sources directory
            if getattr(sys, 'frozen', False):
                # If running as compiled executable
                base_path = sys._MEIPASS
            else:
                # If running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
                
            source_sef = os.path.join(base_path, 'MickFX Required Sources', 'MickFX Base.sef')
            destination_sef = os.path.join(downloads_path, 'MickFX Base.sef')
            
            shutil.copy2(source_sef, destination_sef)
            return True
        except Exception as e:
            self.play_error_sound()
            print(f"Error copying SEF file: {str(e)}")
            error_popup = PopupBox("Error", f"Failed to copy SEF file to Downloads: {str(e)}", self)
            error_popup.show()
            return False

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class DarkOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Setup opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)
        
        # Setup animation
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0)
        self.animation.setEndValue(0.5)
        self.animation.finished.connect(self.on_animation_finished)
        
        # Make sure overlay covers the entire parent widget
        if parent:
            self.resize(parent.size())
            self.original_parent_resize = parent.resizeEvent
            parent.resizeEvent = self.parent_resize_event
    
    def on_animation_finished(self):
        # Ensure opacity stays at final value
        self.opacity_effect.setOpacity(0.5)
    
    def parent_resize_event(self, event):
        try:
            if not self.isHidden() and not self.isDeleted():
                self.resize(event.size())
            if hasattr(self, 'original_parent_resize'):
                self.original_parent_resize(event)
        except RuntimeError:
            if self.parent():
                self.parent().resizeEvent = self.original_parent_resize
        event.accept()

    def isDeleted(self):
        try:
            return not bool(self.parent())
        except RuntimeError:
            return True
        
    def cleanup(self):
        if self.parent():
            self.parent().resizeEvent = self.original_parent_resize
        
    def closeEvent(self, event):
        self.cleanup()
        super().closeEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 127))  # Semi-transparent black

class PopupBox(QWidget):
    finished = pyqtSignal()
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setObjectName("PopupBox")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setupUI(title, message)
        self.setupAnimations()

    def setupUI(self, title, message):
        # Define colors
        purple_color = QColor(102, 45, 145)  # Main purple color
        gold_color = QColor(255, 215, 0)     # Gold color
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)

        # OK Button
        ok_button = QPushButton("OK")
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {gold_color.name()};
                color: black;
                border: 1px solid transparent;
                padding: 8px 60px;
                min-width: 100px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {gold_color.lighter(150).name()};
            }}
            QPushButton:pressed {{
                background-color: {gold_color.darker(150).name()};
            }}
        """)
        ok_button.clicked.connect(self.close)

        # Title bar with dark background
        title_bar = QWidget()
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 10, 5, 10)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        close_button = QPushButton("✕")
        close_button.setFixedSize(30, 30)  # Set a fixed size for the button
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {gold_color.name()};
                font-size: 30px;
                font-weight: bold;
                border: none;
                padding: 0px;
            }}
            QPushButton:hover {{
                color: {gold_color.lighter(150).name()};
            }}
        """)
        close_button.clicked.connect(ok_button.click)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)

        # Message
        message_label = QLabel(message)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            margin: 6px 15px 6px 15px;
        """)

        layout.addWidget(title_bar)
        layout.addWidget(message_label)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def on_close(self):
        self.finished.emit()
        self.close()

    def setupAnimations(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def paintEvent(self, event):
        purple_color = QColor(102, 45, 145)  # Main purple color
        border_color = purple_color.darker(300)  # Much darker purple for the border
        title_bar_color = purple_color.darker(150)  # Color for the title bar

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create rounded rectangle for main shape
        path = QPainterPath()
        rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)  # Adjust for border width
        path.addRoundedRect(rect, 10, 10)

        # Set clipping path to ensure nothing is drawn outside the rounded rectangle
        painter.setClipPath(path)

        # Draw main background
        painter.setBrush(purple_color)
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        # Draw title bar
        title_bar_height = 50  # Adjust this value based on your title bar height
        title_bar_rect = QRectF(rect.x(), rect.y(), rect.width(), title_bar_height)
        painter.setBrush(title_bar_color)
        painter.drawRect(title_bar_rect)

        # Draw border between title bar and message label
        painter.setPen(QPen(border_color, 2))  # Use the same color as the outer border
        painter.drawLine(QPointF(rect.left(), rect.top() + title_bar_height),
                         QPointF(rect.right(), rect.top() + title_bar_height))

        # Remove clipping to draw the outer border
        painter.setClipping(False)

        # Draw much darker purple border
        pen = QPen(border_color, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

    def showEvent(self, event):
        super().showEvent(event)
        self.animation.start()
        if self.parent():
            parent_rect = self.parent().rect()
            size_hint = self.sizeHint()
            min_width = 300  # Previous minimum width
            
            # Use the larger of sizeHint width and min_width
            width = max(min_width, size_hint.width())   
            
            # Calculate the vertical position
            vertical_offset = parent_rect.height() // 7  # Adjust this value to change how low the popup appears
            
            self.setGeometry(
                parent_rect.width() // 2 - width // 2,
                parent_rect.height() // 2 - size_hint.height() // 2 + vertical_offset,
                width,
                size_hint.height()
            )

    def show(self):
        if self.parent():
            # Create and show overlay
            self.overlay = DarkOverlay(self.parent())
            self.overlay.resize(self.parent().size())
            self.overlay.show()
            self.overlay.animation.start()
            
            # Connect close events
            self.finished.connect(self.cleanup_overlay)
        
        super().show()
        self.raise_()
        self.activateWindow()

    def cleanup_overlay(self):
        if hasattr(self, 'overlay'):
            self.overlay.cleanup()  # Call cleanup before deleting
            self.overlay.deleteLater()

    def closeEvent(self, event):
        self.cleanup_overlay()
        super().closeEvent(event)

class DetailedPopupBox(QWidget):
    finished = pyqtSignal()
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setObjectName("DetailedPopupBox")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setupUI(title, message)
        self.setupAnimations()

    def setupUI(self, title, message):
        # Define colors
        purple_color = QColor(102, 45, 145)
        gold_color = QColor(255, 215, 0)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 25)
        layout.setSpacing(20)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {gold_color.name()};
                color: black;
                border: none;
                border-radius: 20px;
                padding: 12px 90px;
                min-width: 140px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {gold_color.lighter(150).name()};
            }}
            QPushButton:pressed {{
                background-color: {gold_color.darker(150).name()};
            }}
        """)
        ok_button.clicked.connect(self.close)
        
        # Title bar with dark background
        title_bar = QWidget()
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(25, 20, 15, 20)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
        """)
        
        close_button = QPushButton("✕")
        close_button.setFixedSize(32, 32)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {gold_color.name()};
                font-size: 28px;
                font-weight: bold;
                border: none;
                padding: 0px;
            }}
            QPushButton:hover {{
                color: {gold_color.lighter(150).name()};
            }}
        """)
        close_button.clicked.connect(ok_button.click)
        
        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(close_button)

        # Content widget to ensure proper centering
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(25, 0, 25, 0)
        content_layout.setSpacing(0)  # Reduced overall spacing

        # Split message into parts
        if "\n\nTo install in SAMMI:" in message:
            main_message, install_instructions = message.split("\n\nTo install in SAMMI:")
            steps = install_instructions.split("\n", 1)  # Split after first newline
            
            # First part with larger font
            main_message_label = QLabel(main_message)
            main_message_label.setAlignment(Qt.AlignLeft)
            main_message_label.setWordWrap(True)
            main_message_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 22px;
                    line-height: 150%;
                    padding: 0px;
                }
            """)
            content_layout.addWidget(main_message_label)
            content_layout.addSpacing(15)  # Space before separator

            # Separator line
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet("""
                QFrame {
                    background-color: rgba(32, 4, 53, 0.8);
                    border: none;
                    height: 1px;
                }
            """)
            content_layout.addWidget(separator)
            content_layout.addSpacing(15)  # Space after separator

            # "To install in SAMMI:" header
            install_header = QLabel("To install in SAMMI:")
            install_header.setAlignment(Qt.AlignLeft)
            install_header.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 20px;
                    font-weight: bold;
                    padding: 0px;
                }
            """)
            content_layout.addWidget(install_header)
            content_layout.addSpacing(3)  # Reduced space between header and list

            # Installation steps with normal font
            steps_label = QLabel(steps[1])  # steps[1] contains the numbered list
            steps_label.setAlignment(Qt.AlignLeft)
            steps_label.setWordWrap(True)
            steps_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    line-height: 150%;
                    padding: 0px;
                }
            """)
            content_layout.addWidget(steps_label)
        else:
            # For other messages, use a single label
            message_label = QLabel(message)
            message_label.setAlignment(Qt.AlignLeft)
            message_label.setWordWrap(True)
            message_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    line-height: 150%;
                    padding: 0px;
                }
            """)
            content_layout.addWidget(message_label)

        content_layout.addStretch()
        
        # Add widgets to main layout
        layout.addWidget(title_bar)
        layout.addWidget(content_widget)

        layout.addWidget(ok_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.setMinimumWidth(450)
        self.setMaximumWidth(550)

    def on_close(self):
        self.finished.emit()
        self.close()

    def setupAnimations(self):
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(250)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

    def paintEvent(self, event):
        purple_color = QColor(102, 45, 145)
        border_color = purple_color.darker(300)
        title_bar_color = purple_color.darker(150)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        path = QPainterPath()
        rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        path.addRoundedRect(rect, 12, 12)

        painter.setClipPath(path)

        painter.setBrush(purple_color)
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        title_bar_height = 65  # Increased height
        title_bar_rect = QRectF(rect.x(), rect.y(), rect.width(), title_bar_height)
        painter.setBrush(title_bar_color)
        painter.drawRect(title_bar_rect)

        painter.setPen(QPen(border_color, 2))
        painter.drawLine(QPointF(rect.left(), rect.top() + title_bar_height),
                         QPointF(rect.right(), rect.top() + title_bar_height))

        painter.setClipping(False)

        pen = QPen(border_color, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

    def showEvent(self, event):
        super().showEvent(event)
        self.animation.start()
        if self.parent():
            parent_rect = self.parent().rect()
            size_hint = self.sizeHint()
            width = max(450, size_hint.width())   
            
            vertical_offset = parent_rect.height() // 12
            
            self.setGeometry(
                parent_rect.width() // 2 - width // 2,
                parent_rect.height() // 2 - size_hint.height() // 2 + vertical_offset,
                width,
                size_hint.height()
            )

    def show(self):
        if self.parent():
            # Create and show overlay
            self.overlay = DarkOverlay(self.parent())
            self.overlay.resize(self.parent().size())
            self.overlay.show()
            self.overlay.animation.start()
            
            # Connect close events
            self.finished.connect(self.cleanup_overlay)
        
        super().show()
        self.raise_()
        self.activateWindow()

    def cleanup_overlay(self):
        if hasattr(self, 'overlay'):
            self.overlay.cleanup()  # Call cleanup before deleting
            self.overlay.deleteLater()

    def closeEvent(self, event):
        self.cleanup_overlay()
        super().closeEvent(event)

class ScalingClickableLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        self._pixmap = None
        self._scaled_pixmap = None
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the widget background transparent
        self.setStyleSheet("background-color: transparent;")  # Ensure transparent background

    def setMovie(self, movie):
        self.movie = movie
        self.movie.frameChanged.connect(self.onFrameChanged)
        super().setMovie(self.movie)

    def onFrameChanged(self):
        self._pixmap = self.movie.currentPixmap()
        self.updatePixmap()

    def updatePixmap(self):
        if self._pixmap:
            parent_width = self.parent().width() if self.parent() else self.width()
            target_width = int(parent_width * 0.8)
            scaled_size = self._pixmap.size()
            scaled_size.scale(target_width, self._pixmap.height(), Qt.KeepAspectRatio)
            self._scaled_pixmap = self._pixmap.scaled(
                scaled_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setFixedSize(self._scaled_pixmap.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updatePixmap()

    def paintEvent(self, event):
        if self._scaled_pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self._scaled_pixmap)
        else:
            super().paintEvent(event)

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl("https://www.mickfx.com"))
        
        
class LogoBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap(resource_path(os.path.join("MickFX Required Sources", "MickFX Background.jpg")))
        self.setAttribute(Qt.WA_StyledBackground, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_image = self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(self.rect(), scaled_image)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

class ContentBackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap(resource_path(os.path.join("MickFX Required Sources", "MickFX Background2.jpg")))
        self.setAttribute(Qt.WA_StyledBackground, True)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_image = self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(self.rect(), scaled_image)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

class DownloadWorker(QRunnable):
    def __init__(self, url, output_path, signals):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.signals = signals

    def run(self):
        from tqdm import tqdm
        import requests
        try:
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(self.output_path, 'wb') as file:
                downloaded_size = 0
                for data in response.iter_content(chunk_size=8192):
                    size = file.write(data)
                    downloaded_size += size
                    self.signals.progress.emit(downloaded_size, total_size)

            self.signals.finished.emit(self.output_path)
        except Exception as e:
            self.signals.error.emit(str(e))

class DownloadSignals(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Create and show splash screen with webp logo
    splash_label = QLabel()
    splash_pixmap = QPixmap(resource_path(os.path.join("MickFX Required Sources", "MickFX Logo.webp")))
    # Scale the pixmap to fit nicely in the splash screen
    scaled_pixmap = splash_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    splash_label.setPixmap(scaled_pixmap)
    splash_label.setStyleSheet("""
        QLabel {
            background-color: #662D91;
            qproperty-alignment: AlignCenter;
        }
    """)
    splash_label.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    splash_label.resize(600, 400)
    
    # Center splash screen
    screen = app.primaryScreen().geometry()
    splash_label.move(screen.center() - splash_label.rect().center())
    splash_label.show()
    
    # Pre-initialize heavy components
    installer = OBSPluginInstaller()
    installer.move(screen.center() - installer.rect().center())
    
    def show_main():
        installer.show()
        splash_label.close()
    
    # Can reduce delay since static image loads faster than GIF
    QTimer.singleShot(300, show_main)
    
    sys.exit(app.exec_())