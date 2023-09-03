from _ctypes import CFuncPtr
from ctypes import byref
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from .msp import msc
from .msp import MSPAssert


"""
const char* MSPAPI QIVWSessionBegin(const char *grammarList, const char *params, int *errorCode);
"""
msc.QIVWSessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
msc.QIVWSessionBegin.restype = c_char_p


def QIVWSessionBegin(grammarList: bytes, params: bytes) -> bytes:
    errorCode = c_int()
    sessionID: bytes = msc.QIVWSessionBegin(grammarList, params, byref(errorCode))
    MSPAssert(errorCode.value, "QIVWSessionBegin failed")
    return sessionID


"""
int MSPAPI QIVWSessionEnd(const char *sessionID, const char *hints);
"""
msc.QIVWSessionEnd.argtypes = [c_char_p, c_char_p]
msc.QIVWSessionEnd.restype = c_int


def QIVWSessionEnd(sessionID: bytes, hints: bytes):
    errorCode: int = msc.QIVWSessionEnd(sessionID, hints)
    MSPAssert(errorCode, "QIVWSessionEnd failed")


"""
int MSPAPI QIVWAudioWrite(const char *sessionID, const void *audioData, unsigned int audioLen, int audioStatus);
"""
msc.QIVWAudioWrite.argtypes = [c_char_p, c_void_p, c_uint, c_int]
msc.QIVWAudioWrite.restype = c_int


def QIVWAudioWrite(sessionID: bytes, audioData: bytes, audioStatus: int):
    audioLen = len(audioData)
    errorCode: int = msc.QIVWAudioWrite(sessionID, audioData, audioLen, audioStatus)
    MSPAssert(errorCode, "QIVWAudioWrite failed")


"""
typedef int( *ivw_ntf_handler)( const char *sessionID, int msg, int param1, int param2, const void *info, void *userData );
int MSPAPI QIVWRegisterNotify(const char *sessionID, ivw_ntf_handler msgProcCb, void *userData);
"""
msgProcCallBack = CFUNCTYPE(c_int, c_char_p, c_int, c_int, c_int, c_void_p, c_void_p)
msc.QIVWRegisterNotify.argtypes = [c_char_p, msgProcCallBack, c_void_p]
msc.QIVWRegisterNotify.restype = c_int


def QIVWRegisterNotify(sessionID: bytes, msgProcCb: CFuncPtr, userData: bytes):
    errorCode: int = msc.QIVWRegisterNotify(sessionID, msgProcCb, userData)
    MSPAssert(errorCode, "QIVWRegisterNotify failed")


__all__ = [
    msgProcCallBack,
    QIVWSessionBegin,
    QIVWSessionEnd,
    QIVWAudioWrite,
    QIVWRegisterNotify,
]
