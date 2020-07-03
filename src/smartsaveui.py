import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import os

import mayautils

def maya_main_window():
    """Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)

class SmartSaveUI(QtWidgets.QDialog):
    """Simple UI Class"""

    def __init__(self):
        """Constructor"""

        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.scene = mayautils.SceneFile()
        self.setWindowTitle("Smart Save")
        self.resize(500, 200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create Widgets for our UI"""
        self.title_lbl = QtWidgets.QLabel("Smart Save")
        self.title_lbl.setStyleSheet("font: bold 40px")
        self.dir_lbl = QtWidgets.QLabel("Directory")
        self.dir_le = QtWidgets.QLineEdit(self.scene.dir())
        self.dir_le.setText(self.scene.dir)
        self.browse_btn = QtWidgets.QPushButton("Browse")
        self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
        self.descriptor_le = QtWidgets.QLineEdit()
        self.descriptor_le.setText(self.scene.descriptor)
        self.version_lbl = QtWidgets.QLabel("Version")
        self.version_spinbox = QtWidgets.QSpinBox()
        self.version_spinbox.setValue(self.scene.version)
        self.ext_lbl = QtWidgets.QLabel("Extension")
        self.ext_le = QtWidgets.QLineEdit()
        self.ext_le.setText(self.scene.ext)
        self.save_btn = QtWidgets.QPushButton("Save")
        self.increment_save_btn = QtWidgets.QPushButton("Increment and Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        """Layout our widgets in the UI"""

        self.directory_lay = QtWidgets.QHBoxLayout()
        self.directory_lay.addWidget(self.dir_lbl)
        self.directory_lay.addWidget(self.dir_le)
        self.directory_lay.addWidget(self.browse_btn)

        self.descriptor_lay = QtWidgets.QHBoxLayout()
        self.descriptor_lay.addWidget(self.descriptor_lbl)
        self.descriptor_lay.addWidget(self.descriptor_le)

        self.version_lay = QtWidgets.QHBoxLayout()
        self.version_lay.addWidget(self.version_lbl)
        self.version_lay.addWidget(self.version_spinbox)

        self.ext_lay = QtWidgets.QHBoxLayout()
        self.ext_lay.addWidget(self.ext_lbl)
        self.ext_lay.addWidget(self.ext_le)

        self.bottom_btn_lay = QtWidgets.QHBoxLayout()
        self.bottom_btn_lay.addWidget(self.increment_save_btn)
        self.bottom_btn_lay.addWidget(self.save_btn)
        self.bottom_btn_lay.addWidget(self.cancel_btn)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_lbl)
        self.main_layout.addLayout(self.directory_lay)
        self.main_layout.addLayout(self.descriptor_lay)
        self.main_layout.addLayout(self.version_lay)
        self.main_layout.addLayout(self.ext_lay)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_btn_lay)
        self.setLayout(self.main_layout)

    def create_connections(self):
        """Connect out widget signals to slots"""
        self.cancel_btn.clicked.connect(self.cancel)
        self.save_btn.clicked.connect(self.save)
        self.increment_save_btn.clicked.connect(self.increment_save)
        self.browse_btn.clicked.connect(self.browse)

    def _populate_scenefile_properties(self):
        """Populates the SceneFile object properties from the UI"""
        self.scene.dir = self.dir_le.text()
        self.scene.descriptor = self.descriptor_le.text()
        self.scene.version = self.version_spinbox.value()
        self.scene.ext = self.ext_le.text()

    @QtCore.Slot()
    def save(self):
        """Saves the scene file"""
        self._populate_scenefile_properties()
        self.scene.save()
        self.dir_le.setText(self.scene.dir)

    @QtCore.Slot()
    def browse(self):
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory",
                                               self.scene.dir,
                                               QtWidgets.QFileDialog.ShowDirsOnly
                                               | QtWidgets.QFileDialog.DontResolveSymlinks)
        self.scene.dir = dir
        self.dir_le.setText(self.scene.dir)



    @QtCore.Slot()
    def increment_save(self):
        """Automatically finds the next available version on disk and saves up"""
        self._populate_scenefile_properties()
        path = self.scene.dir
        file_names = []
        for dir_file in os.listdir(path):
            if '.ma' in dir_file and self.scene.descriptor in dir_file:
                file_names.append(dir_file)
        max_version = max([mayautils.parse_name(file)['version'] for file in file_names])
        self.scene.version = max_version
        self.scene.increment_and_save()
        self.version_spinbox.setValue(self.scene.version)
        self.dir_le.setText(self.scene.dir)





    @QtCore.Slot()
    def cancel(self):
        """Quits the dialog"""
        self.close()