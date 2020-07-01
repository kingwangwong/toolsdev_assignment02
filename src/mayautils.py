import logging

import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)

class SceneFile(object):
    """This class represents a DCCsoftware scene"""
    """    Attributes:
    dir (Path, optional): Directory to the scene file. Defaults to ' '.
    descriptor (str, optional): short descriptor of the scene file. Defaults to "main"
    version (int, optional): version number. Defaults to 1.
    ext (str, optional): Extension. Defaults to "ma" """


    def __init__(self, dir='', descriptor='main', version=1, ext="ma"):
        self._dir = Path(dir)
        self.descriptor = descriptor
        self.version = version
        self.ext = ext

    @property
    def dir(self):
        print("getting")
        return Path(self._dir)

    @dir.setter
    def dir(self, val):
        print("setting")
        self._dir = Path(val)

    def basename(self):
        #returns the DCC scene file name, ship_001.ma

        name_pattern = "{descriptor}_{version:03d}.{ext}"
        name = name_pattern.format(descriptor=self.descriptor,
                                   version=self.version,
                                   ext=self.ext)
        return name

    def path(self):
        #This function returns a path to scene file, includes drive letter and directory path
        return Path(self.dir) / self.basename()

    def save(self):
        #Saves scene file
        try:
            pmc.system.saveAs(self.path())
        except RuntimeError:
            log.warning("Missing directories. Creating directories.")
            self.dir.makedirs_p()
            pmc.system.saveAs(self.path())

    def increment_and_save(self):
        self.ext + 1
