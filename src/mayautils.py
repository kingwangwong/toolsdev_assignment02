import logging

import pymel.core as pmc
from pymel.core.system import Path

log = logging.getLogger(__name__)

def parse_name(file_name):

    full_name = file_name.split('_')
    descriptor = full_name[0]
    v_e = full_name[1].split('v')[-1].split('.')
    #v_e is version number and file extension after split
    version = int(v_e[0])
    ext = v_e[1]
    return {
        'descriptor': descriptor,
        'version': version,
        'ext': ext
    }

class SceneFile(object):
    """This class represents a DCCsoftware scene"""
    """    Attributes:
    dir (Path, optional): Directory to the scene file. Defaults to ' '.
    descriptor (str, optional): short descriptor of the scene file. Defaults to "main"
    version (int, optional): version number. Defaults to 1.
    ext (str, optional): Extension. Defaults to "ma" """


    def __init__(self, dir=pmc.system.sceneName(), descriptor='main', version=1, ext="ma"):
        self._dir = Path(dir)
        if self._dir == '':
            self.descriptor = descriptor
            self.version = version
            self.ext = ext
            self._dir = Path(pmc.system.sceneName())
        else:
            file_name = self._dir.split('/')[-1]
            attributes = parse_name(file_name)
            self.descriptor = attributes['descriptor']
            self.version = attributes['version']
            self.ext = attributes['ext']


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

        name_pattern = "{descriptor}_v{version:03d}.{ext}"
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

    def dir(self):
        current_path = Path(pmc.system.sceneName())
        self.dir = current_path.parent


    def increment_and_save(self):
        self.version += 1
        print(self.version)
        self.save()

"""     #current_path = pmc.system.sceneName()
        #print(current_path)
        path_sh = current_path.split("v")[1]
        version_num = path_sh.split(".")[0]
        print(version_num)
        vn = int(version_num)
        self.version = vn + 1
"""

