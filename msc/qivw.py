from _ctypes import CFuncPtr
from ctypes import CDLL
from ctypes import byref
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from .msp import MSPAssert


class QIVW:
    def __init__(self, msc: CDLL) -> None:
        self.msc = msc
        self.msc.QIVWSessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
        self.msc.QIVWSessionBegin.restype = c_char_p

        self.msc.QIVWSessionEnd.argtypes = [c_char_p, c_char_p]
        self.msc.QIVWSessionEnd.restype = c_int

        self.msc.QIVWAudioWrite.argtypes = [c_char_p, c_void_p, c_uint, c_int]
        self.msc.QIVWAudioWrite.restype = c_int

        self.msgProcCallBack = CFUNCTYPE(
            c_int, c_char_p, c_int, c_int, c_int, c_void_p, c_void_p
        )
        self.msc.QIVWRegisterNotify.argtypes = [
            c_char_p,
            self.msgProcCallBack,
            c_void_p,
        ]
        self.msc.QIVWRegisterNotify.restype = c_int

    """
    const char* MSPAPI QIVWSessionBegin(const char *grammarList, const char *params, int *errorCode);
    """

    def QIVWSessionBegin(self, grammarList: bytes, params: bytes) -> bytes:
        errorCode = c_int()
        sessionID: bytes = self.msc.QIVWSessionBegin(
            grammarList, params, byref(errorCode)
        )
        MSPAssert(errorCode.value, "QIVWSessionBegin failed")
        return sessionID

    """
    int MSPAPI QIVWSessionEnd(const char *sessionID, const char *hints);
    """

    def QIVWSessionEnd(self, sessionID: bytes, hints: bytes):
        errorCode: int = self.msc.QIVWSessionEnd(sessionID, hints)
        MSPAssert(errorCode, "QIVWSessionEnd failed")

    """
    int MSPAPI QIVWAudioWrite(const char *sessionID, const void *audioData, unsigned int audioLen, int audioStatus);
    """

    def QIVWAudioWrite(self, sessionID: bytes, audioData: bytes, audioStatus: int):
        audioLen = len(audioData)
        errorCode: int = self.msc.QIVWAudioWrite(
            sessionID, audioData, audioLen, audioStatus
        )
        MSPAssert(errorCode, "QIVWAudioWrite failed")

    """
    typedef int( *ivw_ntf_handler)( const char *sessionID, int msg, int param1, int param2, const void *info, void *userData );
    int MSPAPI QIVWRegisterNotify(const char *sessionID, ivw_ntf_handler msgProcCb, void *userData);
    """

    def QIVWRegisterNotify(
        self, sessionID: bytes, msgProcCb: CFuncPtr, userData: bytes
    ):
        errorCode: int = self.msc.QIVWRegisterNotify(sessionID, msgProcCb, userData)
        MSPAssert(errorCode, "QIVWRegisterNotify failed")


__all__ = ["QIVW"]
