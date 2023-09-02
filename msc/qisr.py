from _ctypes import CFuncPtr
from ctypes import byref, string_at
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msp import msc
from .msp import MSPAssert


'''
/** 
 * @fn		QISRSessionBegin
 * @brief	Begin a Recognizer Session
 * 
 *  Create a recognizer session to recognize audio data
 * 
 * @return	return sessionID of current session, NULL is failed.
 * @param	const char* grammarList		- [in] grammars list, inline grammar support only one.
 * @param	const char* params			- [in] parameters when the session created.
 * @param	int *errorCode				- [out] return 0 on success, otherwise return error code.
 * @see		
 */
const char* MSPAPI QISRSessionBegin(const char* grammarList, const char* params, int* errorCode);
'''
msc.QISRSessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
msc.QISRSessionBegin.restype = c_char_p


def QISRSessionBegin(grammarList: bytes, params: bytes) -> bytes:
    errorCode = c_int()
    sessionID: bytes = msc.QISRSessionBegin(
        grammarList, params, byref(errorCode))
    MSPAssert(errorCode.value, "QISRSessionBegin failed")
    return sessionID


'''
/** 
 * @fn		QISRAudioWrite
 * @brief	Write Audio Data to Recognizer Session
 * 
 *  Writing binary audio data to recognizer.
 * 
 * @return	int MSPAPI	- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by recog_begin
 * @param	const void* waveData	- [in] Binary data of waveform
 * @param	unsigned int waveLen	- [in] Waveform data size in bytes
 * @param	int audioStatus			- [in] Audio status, can be 
 * @param	int *epStatus			- [out] ISRepState
 * @param	int *recogStatus		- [out] ISRrecRecognizerStatus, see isr_rec.h
 * @see		
 */
int MSPAPI QISRAudioWrite(const char* sessionID, const void* waveData, unsigned int waveLen, int audioStatus, int *epStatus, int *recogStatus);
'''
msc.QISRAudioWrite.argtypes = [
    c_char_p,
    c_void_p,
    c_uint,
    c_int,
    POINTER(c_int),
    POINTER(c_int),
]
msc.QISRAudioWrite.restype = c_int


def QISRAudioWrite(
    sessionID: bytes, waveData: bytes, audioStatus: int
) -> Tuple[int, int]:
    waveLen = len(waveData)
    epStatus = c_int()
    recogStatus = c_int()
    errorCode: int = msc.QISRAudioWrite(
        sessionID, waveData, waveLen, audioStatus, byref(
            epStatus), byref(recogStatus)
    )
    MSPAssert(errorCode, "QISRAudioWrite failed")
    return epStatus.value, recogStatus.value


'''
/** 
 * @fn		QISRGetResult
 * @brief	Get Recognize Result in Specified Format
 * 
 *  Get recognize result in Specified format.
 * 
 * @return	int MSPAPI	- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] session id returned by session begin
 * @param	int* rsltStatus			- [out] status of recognition result, 0: success, 1: no match, 2: incomplete, 5:speech complete
 * @param	int *errorCode			- [out] return 0 on success, otherwise return error code.
 * @see		
 */
const char * MSPAPI QISRGetResult(const char* sessionID, int* rsltStatus, int waitTime, int *errorCode);
'''
msc.QISRGetResult.argtypes = [c_char_p, POINTER(c_int), c_int, POINTER(c_int)]
msc.QISRGetResult.restype = c_char_p


def QISRGetResult(sessionID: bytes, waitTime: int) -> Tuple[bytes, int]:
    rsltStatus = c_int()
    errorCode = c_int()
    result: bytes = msc.QISRGetResult(
        sessionID, byref(rsltStatus), waitTime, byref(errorCode)
    )
    MSPAssert(errorCode.value, "QISRGetResult failed")
    return result, rsltStatus.value


'''
/** 
 * @fn		QISRSessionEnd
 * @brief	End a Recognizer Session
 * 
 *  End the recognizer session, release all resource.
 * 
 * @return	int MSPAPI	- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] session id string to end
 * @param	const char* hints	- [in] user hints to end session, hints will be logged to CallLog
 * @see		
 */
int MSPAPI QISRSessionEnd(const char* sessionID, const char* hints);
'''
msc.QISRSessionEnd.argtypes = [c_char_p, c_char_p]
msc.QISRSessionEnd.restype = c_int


def QISRSessionEnd(sessionID: bytes, hints: bytes):
    errorCode: int = msc.QISRSessionEnd(sessionID, hints)
    MSPAssert(errorCode, "QISRSessionEnd failed")


'''
/** 
 * @fn		QISRGetParam
 * @brief	get params related with msc
 * 
 *  the params could be local or server param, we only support netflow params "upflow" & "downflow" now
 * 
 * @return	int	- Return 0 if success, otherwise return errcode.
 * @param	const char* sessionID	- [in] session id of related param, set NULL to got global param
 * @param	const char* paramName	- [in] param name,could pass more than one param split by ','';'or'\n'
 * @param	const char* paramValue	- [in] param value buffer, malloced by user
 * @param	int *valueLen			- [in, out] pass in length of value buffer, and return length of value string
 * @see		
 */
int MSPAPI QISRGetParam(const char* sessionID, const char* paramName, char* paramValue, unsigned int* valueLen);
'''
msc.QISRGetParam.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_uint)]
msc.QISRGetParam.restype = c_int


def QISRGetParam(sessionID: bytes, paramName: bytes, paramValue: bytes) -> bytes:
    valueLen = c_uint(len(paramValue))
    errorCode = c_int()
    errorCode: int = msc.QISRGetParam(
        sessionID, paramName, paramValue, byref(valueLen)
    )
    MSPAssert(errorCode.value, "QISRGetParam failed")
    return string_at(paramValue, valueLen.value)


'''
typedef int ( *GrammarCallBack)( int, const char*, void*);
int MSPAPI QISRBuildGrammar(const char *grammarType, const char *grammarContent, unsigned int grammarLength, const char *params, GrammarCallBack callback, void *userData);
'''
GrammarCallBack = CFUNCTYPE(c_int, c_int, c_char_p, c_void_p)
msc.QISRBuildGrammar.argtypes = [
    c_char_p,
    c_char_p,
    c_uint,
    c_char_p,
    GrammarCallBack,
    c_void_p,
]
msc.QISRBuildGrammar.restype = c_int


def QISRBuildGrammar(
    grammarType: bytes,
    grammarContent: bytes,
    params: bytes,
    callback: CFuncPtr,
    userData: bytes,
):
    grammarLength = len(grammarContent)
    errorCode: int = msc.QISRBuildGrammar(
        grammarType, grammarContent, grammarLength, params, callback, userData
    )
    MSPAssert(errorCode, "QISRBuildGrammar failed")


'''
typedef int ( *LexiconCallBack)( int, const char*, void*);
int MSPAPI QISRUpdateLexicon(const char *lexiconName, const char *lexiconContent, unsigned int lexiconLength, const char *params, LexiconCallBack callback, void *userData);
'''
LexiconCallBack = CFUNCTYPE(c_int, c_int, c_char_p, c_void_p)
msc.QISRUpdateLexicon.argtypes = [
    c_char_p,
    c_char_p,
    c_uint,
    c_char_p,
    LexiconCallBack,
    c_void_p,
]
msc.QISRUpdateLexicon.restype = c_int


def QISRUpdateLexicon(
    lexiconName: bytes,
    lexiconContent: bytes,
    lexiconLength: int,
    params: bytes,
    callback: CFuncPtr,
    userData: bytes,
):
    errorCode: int = msc.QISRUpdateLexicon(
        lexiconName, lexiconContent, lexiconLength, params, callback, userData
    )
    MSPAssert(errorCode, "QISRUpdateLexicon failed")


__all__ = [
    QISRSessionBegin,
    QISRAudioWrite,
    QISRGetResult,
    QISRSessionEnd,
    QISRGetParam,
    QISRBuildGrammar,
    QISRUpdateLexicon,
    LexiconCallBack,
    GrammarCallBack,
]
