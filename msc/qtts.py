from ctypes import POINTER
from ctypes import byref, string_at
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msp import msc
from .msp import MSPAssert


"""
/** 
 * @fn		QTTSSessionBegin
 * @brief	Begin a TTS Session
 * 
 *  Create a tts session to synthesize data.
 * 
 * @return	const char* - Return the new session id in success, otherwise return NULL, error code.
 * @param	const char* params			- [in] parameters when the session created.
 * @param	const char** sessionID		- [out] return a string to this session.
 * @see		
 */
const char* MSPAPI QTTSSessionBegin(const char* params, int* errorCode);
"""
msc.QTTSSessionBegin.argtypes = [c_char_p, POINTER(c_int)]
msc.QTTSSessionBegin.restype = c_char_p


def QTTSSessionBegin(params: bytes) -> bytes:
    errorCode = c_int()
    sessionID: bytes = msc.QTTSSessionBegin(params, byref(errorCode))
    MSPAssert(errorCode.value, "QTTSSessionBegin failed")
    return sessionID


"""
/** 
 * @fn		QTTSTextPut
 * @brief	Put Text Buffer to TTS Session
 * 
 *  Writing text string to synthesizer.
 * 
 * @return	int MSPAPI	- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by sesson begin
 * @param	const char* textString	- [in] text buffer
 * @param	unsigned int textLen	- [in] text size in bytes
 * @see		
 */
int MSPAPI QTTSTextPut(const char* sessionID, const char* textString, unsigned int textLen, const char* params);
"""
msc.QTTSTextPut.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]
msc.QTTSTextPut.restype = c_int


def QTTSTextPut(sessionID: bytes, textString: bytes, params: bytes):
    textLen = len(textString)
    errorCode: int = msc.QTTSTextPut(sessionID, textString, textLen, params)
    MSPAssert(errorCode, "QTTSTextPut failed")


"""
/** 
 * @fn		QTTSAudioGet
 * @brief	Synthesize text to audio
 * 
 *  Synthesize text to audio, and return audio information.
 * 
 * @return	const void*	- Return current synthesized audio data buffer, size returned by QTTSTextSynth.
 * @param	const char* sessionID	- [in] session id returned by session begin
 * @param	unsigned int* audioLen 	- [out] synthesized audio size in bytes
 * @param	int* synthStatus	- [out] synthesizing status
 * @param	int* errorCode	- [out] error code if failed, 0 to success.
 * @see		
 */
const void* MSPAPI QTTSAudioGet(const char* sessionID, unsigned int* audioLen, int* synthStatus, int* errorCode);
"""
msc.QTTSAudioGet.argtypes = [c_char_p, POINTER(c_uint), POINTER(c_int), POINTER(c_int)]
msc.QTTSAudioGet.restype = c_void_p


def QTTSAudioGet(sessionID: bytes) -> Tuple[bytes, int]:
    audioLen = c_uint()
    synthStatus = c_int()
    errorCode = c_int()
    audioData: c_void_p = msc.QTTSAudioGet(
        sessionID, byref(audioLen), byref(synthStatus), byref(errorCode)
    )
    MSPAssert(errorCode.value, "QTTSAudioGet failed")
    return string_at(audioData, audioLen.value), synthStatus.value


"""
/** 
 * @fn		QTTSSessionEnd
 * @brief	End a Recognizer Session
 * 
 *  End the recognizer session, release all resource.
 * 
 * @return	int MSPAPI	- Return 0 in success, otherwise return error code.
 * @param	const char* session_id	- [in] session id string to end
 * @param	const char* hints	- [in] user hints to end session, hints will be logged to CallLog
 * @see		
 */
int MSPAPI QTTSSessionEnd(const char* sessionID, const char* hints);
"""
msc.QTTSSessionEnd.argtypes = [c_char_p, c_char_p]
msc.QTTSSessionEnd.restype = c_int


def QTTSSessionEnd(sessionID: bytes, hints: bytes):
    errorCode: int = msc.QTTSSessionEnd(sessionID, hints)
    MSPAssert(errorCode, "QTTSSessionEnd failed")


"""
/** 
 * @fn		QTTSGetParam
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
int MSPAPI QTTSGetParam(const char* sessionID, const char* paramName, char* paramValue, unsigned int* valueLen);
"""
msc.QTTSGetParam.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_uint)]
msc.QTTSGetParam.restype = c_int


def QTTSGetParam(sessionID: bytes, paramName: bytes, paramValue: bytes) -> bytes:
    valueLen = c_uint(len(paramValue))
    errorCode: int = msc.QTTSGetParam(sessionID, paramName, paramValue, byref(valueLen))
    MSPAssert(errorCode, "QTTSGetParam failed")
    return string_at(paramValue, valueLen.value)


__all__ = [
    QTTSSessionBegin,
    QTTSTextPut,
    QTTSAudioGet,
    QTTSSessionEnd,
    QTTSGetParam,
]
