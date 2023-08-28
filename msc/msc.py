import os
import platform

from ctypes import cdll
from ctypes import CDLL

__all__ = [
    "msc",
]


def LoadLibrary(
    file_name: str, base_dir: str = os.path.dirname(os.path.abspath(__file__))
) -> CDLL:
    try:
        file_path = os.path.join(base_dir, "bin", file_name)
        msc = cdll.LoadLibrary(file_path)
    except Exception as e:
        raise Exception("Failed to load library: %s" % e)
    return msc


def LoadMSC() -> CDLL:
    system = platform.system()
    arch = platform.architecture()[0]

    if system == "Windows":
        if arch == "64bit":
            msc = LoadLibrary("msc_x64.dll")
        else:
            msc = LoadLibrary("msc_x86.dll")
    elif system == "Linux":
        if arch == "64bit":
            msc = LoadLibrary("msc_x64.so")
        else:
            msc = LoadLibrary("msc_x86.so")
    else:
        raise Exception("Unsupported system: %s" % system)
    return msc


msc = LoadMSC()
