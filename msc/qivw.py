from _ctypes import CFuncPtr
from ctypes import byref
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msc import msc
from .msp import MSPAssert

__all__ = [
    "ivw_ntf_handler",
    "QIVWSessionBegin",
    "QIVWSessionEnd",
    "QIVWAudioWrite",
    "QIVWRegisterNotify",
    "QIVWGetResInfo",
]


"""
#ifndef __QIVW_H__
#define __QIVW_H__

#ifdef __cplusplus
extern "C" {
#endif /* C++ */

#include "msp_types.h"

typedef int( *ivw_ntf_handler)( const char *sessionID, int msg, int param1, int param2, const void *info, void *userData );

const char* MSPAPI QIVWSessionBegin(const char *grammarList, const char *params, int *errorCode);
typedef const char* (MSPAPI *Proc_QIVWSessionBegin)(const char *grammarList, const char *params, int *errorCode);

int MSPAPI QIVWSessionEnd(const char *sessionID, const char *hints);
typedef int (MSPAPI *Proc_QIVWSessionEnd)(const char *sessionID, const char *hints);

int MSPAPI QIVWAudioWrite(const char *sessionID, const void *audioData, unsigned int audioLen, int audioStatus);
typedef int (MSPAPI *Proc_QIVWAudioWrite)(const char *sessionID, const void *audioData, unsigned int audioLen, int audioStatus);

int MSPAPI QIVWRegisterNotify(const char *sessionID, ivw_ntf_handler msgProcCb, void *userData);
typedef int (MSPAPI *Proc_QIVWRegisterNotify)(const char *sessionID, ivw_ntf_handler msgProcCb, void *userData);

int MSPAPI QIVWGetResInfo(const char *resPath, char *resInfo, unsigned int *infoLen, const char *params);
typedef int (MSPAPI *Proc_QIVWGetResInfo)(const char *resPath, char *resInfo, unsigned int *infoLen, const char *params);



#ifdef __cplusplus
} /* extern "C" */	
#endif /* C++ */

#endif /* __QIVW_H__ */
"""


msc.QIVWSessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
msc.QIVWSessionBegin.restype = c_char_p

msc.QIVWSessionEnd.argtypes = [c_char_p, c_char_p]
msc.QIVWSessionEnd.restype = c_int

msc.QIVWAudioWrite.argtypes = [c_char_p, c_void_p, c_uint, c_int]
msc.QIVWAudioWrite.restype = c_int

ivw_ntf_handler = CFUNCTYPE(c_int, c_char_p, c_int, c_int, c_void_p, c_void_p)
msc.QIVWRegisterNotify.argtypes = [c_char_p, ivw_ntf_handler, c_void_p]
msc.QIVWRegisterNotify.restype = c_int

msc.QIVWGetResInfo.argtypes = [c_char_p, c_char_p, POINTER(c_uint), c_char_p]
msc.QIVWGetResInfo.restype = c_int


def QIVWSessionBegin(grammarList: str, params: str) -> str:
    grammarList = grammarList.encode("UTF-8") if grammarList else None
    params = params.encode("UTF-8") if params else None
    errorCode = c_int()
    sessionID: bytes = msc.QIVWSessionBegin(grammarList, params, byref(errorCode))
    MSPAssert(errorCode.value)
    return sessionID.decode("UTF-8") if sessionID else None


def QIVWSessionEnd(sessionID: str, hints: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    hints = hints.encode("UTF-8") if hints else None
    errorCode: int = msc.QIVWSessionEnd(sessionID, hints)
    MSPAssert(errorCode)


def QIVWAudioWrite(sessionID: str, audioData: bytes, audioStatus: int):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    errorCode: int = msc.QIVWAudioWrite(
        sessionID, audioData, len(audioData), audioStatus
    )
    MSPAssert(errorCode)


def QIVWRegisterNotify(sessionID: str, msgProcCb: CFuncPtr, userData: bytes):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    errorCode: int = msc.QIVWRegisterNotify(sessionID, msgProcCb, userData)
    MSPAssert(errorCode)


def QIVWGetResInfo(resPath: str, params: str) -> Tuple[str, int]:
    resPath = resPath.encode("UTF-8") if resPath else None
    params = params.encode("UTF-8") if params else None
    infoLen = c_uint()
    resInfo = c_char_p()
    errorCode: int = msc.QIVWGetResInfo(resPath, resInfo, byref(infoLen), params)
    MSPAssert(errorCode)
    return resInfo.value.decode("UTF-8"), infoLen.value
