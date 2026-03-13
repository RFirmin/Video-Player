"""
app to look the mp4 file
"""

import importlib.metadata
import sys
from functools import partial

from PySide6 import QtWidgets, QtMultimedia, QtMultimediaWidgets, QtCore


class PyPlayer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyPlayer")
        self.show()

        self.open_icon = self.style().standardIcon(QtWidgets.QStyle.SP_DriveDVDIcon)
        self.play_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay)
        self.previous_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipBackward)
        self.pause_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause)
        self.stop_icon = self.style().standardIcon(QtWidgets.QStyle.SP_MediaStop)

        self.init_ui()

    def init_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.toolbar = QtWidgets.QToolBar()
        self.file_menu = self.menuBar().addMenu("Fichier")

        # Audio
        self.audio_output = QtMultimedia.QAudioOutput()

        # ACTIONS
        self.act_open = self.file_menu.addAction(self.open_icon, "Ouvrir")
        self.act_open.setShortcut("Ctrl+O")
        self.act_play = self.toolbar.addAction(self.play_icon, "Lire")
        self.act_previous = self.toolbar.addAction(self.previous_icon, "Revenir au debut")
        self.act_pause = self.toolbar.addAction(self.pause_icon, "Pause")
        self.act_stop = self.toolbar.addAction(self.stop_icon, "Stop")

    def create_layouts(self):
        pass

    def modify_widgets(self):
        pass

    def add_widgets_to_layouts(self):
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.video_widget)
        self.player.setVideoOutput(self.video_widget)
        self.player.setAudioOutput(self.audio_output)

    def setup_connections(self):
        self.act_open.triggered.connect(self.open)
        self.act_play.triggered.connect(self.player.play)
        self.act_pause.triggered.connect(self.player.pause)
        self.act_stop.triggered.connect(self.player.stop)
        self.act_previous.triggered.connect(partial(self.player.setPosition, 0))
        self.player.playbackStateChanged.connect(self.update_buttons)

    def open(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setMimeTypeFilters(["video/mkv"])
        move_dir = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(move_dir)
        if file_dialog.exec_() == QtWidgets.QDialog.Accepted:
            movie = file_dialog.selectedUrls()[0]
            self.player.setSource(movie)
            self.player.play()

    def update_buttons(self, state):
        self.act_play.setDisabled(state == QtMultimedia.QMediaPlayer.PlayingState)
        self.act_pause.setDisabled(state != QtMultimedia.QMediaPlayer.PlayingState)
        self.act_stop.setDisabled(state == QtMultimedia.QMediaPlayer.StoppedState)



def main():
    # Linux desktop environments use an app's .desktop file to integrate the app
    # in to their application menus. The .desktop file of this app will include
    # the StartupWMClass key, set to app's formal name. This helps associate the
    # app's windows to its menu item.
    #
    # For association to work, any windows of the app must have WMCLASS property
    # set to match the value set in app's desktop file. For PySide6, this is set
    # with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib.metadata.metadata(app_module)

    QtWidgets.QApplication.setApplicationName(metadata["Formal-Name"])

    app = QtWidgets.QApplication(sys.argv)
    main_window = PyPlayer()
    main_window.resize(1920/2, 1200/2)
    sys.exit(app.exec())
