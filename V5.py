import sys
import vlc

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QSlider, QLabel
)

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFontDatabase, QFont, QIcon
from PyQt6.QtMultimedia import QSoundEffect


class EzioPlayer(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Animus Media Player")
        self.setGeometry(200, 100, 1200, 700)
        self.setWindowIcon(QIcon("Assassins_creed_logo.png"))

        self.intro_played = False

        # ---------- Load Custom Font ----------
        font_id = QFontDatabase.addApplicationFont("WatatsukiTechSans-GOJxA.ttf")

        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(family, 11))

        # ---------- Button Sound ----------
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("click.wav"))
        self.click_sound.setVolume(0.5)

        # ---------- VLC ----------
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # ---------- Intro Screen ----------
        self.video_frame = QLabel()
        self.video_frame.setStyleSheet("background-color:black;")
        self.video_frame.setMinimumSize(800, 450)
        self.video_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        self.setLayout(layout)

        QTimer.singleShot(200, self.play_intro)

    # ---------- Intro ----------
    def play_intro(self):

        media = self.instance.media_new("intro.mp4")
        self.player.set_media(media)

        if sys.platform.startswith("linux"):
            self.player.set_xwindow(self.video_frame.winId())

        elif sys.platform == "win32":
            self.player.set_hwnd(self.video_frame.winId())

        elif sys.platform == "darwin":
            self.player.set_nsobject(int(self.video_frame.winId()))

        self.player.play()

        QTimer.singleShot(5000, self.build_main_ui)

    # ---------- Build UI ----------
    def build_main_ui(self):

        self.player.stop()
        self.intro_played = True

        QWidget().setLayout(self.layout())

        self.video_frame = QLabel()
        self.video_frame.setMinimumSize(800, 450)
        self.video_frame.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video_frame.setStyleSheet("""
        QLabel {
        background-image: url(wallpaper-ezio-1.jpg);
        background-position: center;
        background-repeat: no-repeat;
        border-radius: 12px;
        }
        """)

        # ---------- Buttons ----------
        self.open_btn = QPushButton("OPEN")
        self.play_btn = QPushButton("PLAY")
        self.pause_btn = QPushButton("PAUSE")
        self.stop_btn = QPushButton("STOP")
        self.rewind_btn = QPushButton("<< 10s")
        self.forward_btn = QPushButton("10s >>")
        self.fullscreen_btn = QPushButton("FULLSCREEN")

        # ---------- Timeline ----------
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.sliderMoved.connect(self.set_position)

        # ---------- Volume ----------
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # ---------- Layout ----------
        controls = QHBoxLayout()

        controls.addWidget(self.open_btn)
        controls.addWidget(self.play_btn)
        controls.addWidget(self.pause_btn)
        controls.addWidget(self.stop_btn)
        controls.addWidget(self.rewind_btn)
        controls.addWidget(self.forward_btn)
        controls.addWidget(self.fullscreen_btn)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("VOLUME"))
        volume_layout.addWidget(self.volume_slider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_frame)
        layout.addWidget(self.position_slider)
        layout.addLayout(controls)
        layout.addLayout(volume_layout)

        self.setLayout(layout)

        # ---------- Button Connections ----------
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.play)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)
        self.rewind_btn.clicked.connect(self.rewind)
        self.forward_btn.clicked.connect(self.forward)
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)

        # ---------- Timer ----------
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)

        self.apply_styles()

    # ---------- Click Sound ----------
    def click(self):
        self.click_sound.play()

    # ---------- Styling ----------
    def apply_styles(self):

        button_style = """
        QPushButton {
            background-color: rgba(0,0,0,180);
            color: white;
            border: 2px solid #aa0000;
            padding: 6px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: rgba(170,0,0,200);
        }
        """

        slider_style = """
        QSlider::groove:horizontal {
            height: 6px;
            background: #222;
        }

        QSlider::handle:horizontal {
            background: red;
            width: 14px;
        }
        """

        self.setStyleSheet(button_style + slider_style)

    # ---------- Open Media ----------
    def open_file(self):

        if not self.intro_played:
            return

        self.click()

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Media",
            "",
            "Media Files (*.mp4 *.mp3)"
        )

        if filename:

            media = self.instance.media_new(filename)
            self.player.set_media(media)

            # force scaling
            self.player.video_set_scale(0)
            self.player.video_set_aspect_ratio(None)

            if sys.platform.startswith("linux"):
                self.player.set_xwindow(self.video_frame.winId())

            elif sys.platform == "win32":
                self.player.set_hwnd(self.video_frame.winId())

            elif sys.platform == "darwin":
                self.player.set_nsobject(int(self.video_frame.winId()))

            QTimer.singleShot(100, self.play)

    # ---------- Playback ----------
    def play(self):
        self.click()
        self.player.play()
        self.timer.start()

    def pause(self):
        self.click()
        self.player.pause()

    def stop(self):
        self.click()
        self.player.stop()

    # ---------- Seek ----------
    def rewind(self):
        self.click()
        t = self.player.get_time()
        self.player.set_time(max(0, t - 10000))

    def forward(self):
        self.click()
        t = self.player.get_time()
        self.player.set_time(t + 10000)

    # ---------- Timeline ----------
    def set_position(self, position):
        self.player.set_position(position / 1000.0)

    def update_ui(self):
        pos = self.player.get_position()
        self.position_slider.setValue(int(pos * 1000))

    # ---------- Volume ----------
    def set_volume(self, volume):
        self.player.audio_set_volume(volume)

    # ---------- Fullscreen ----------
    def toggle_fullscreen(self):

        self.click()

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    # ---------- Resize Fix ----------
    def resizeEvent(self, event):
        try:
            self.player.video_set_scale(0)
        except:
            pass

    # ---------- Keyboard ----------
    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Space:
            self.pause()

        elif event.key() == Qt.Key.Key_Left:
            self.rewind()

        elif event.key() == Qt.Key.Key_Right:
            self.forward()

        elif event.key() == Qt.Key.Key_F:
            self.toggle_fullscreen()

        elif event.key() == Qt.Key.Key_Escape:
            self.showNormal()


app = QApplication(sys.argv)

app.setWindowIcon(QIcon("Assassins_creed_logo.png"))

player = EzioPlayer()
player.show()

sys.exit(app.exec())
