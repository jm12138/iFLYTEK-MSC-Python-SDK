from ctypes import POINTER
from ctypes import byref, string_at
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msp import msc
from .msp import MSPAssert


'''
/** 
 * @fn		QISESessionBegin
 * @brief	Begin a Evaluation Session
 * 
 *  Create a evaluation session to evaluate audio data
 * 
 * @return	const char* MSPAPI		- Return the new session id in success, otherwise return NULL.
 * @param	const char* params		- [in] Parameters to create session.
 * @param	const char* userModelId	- [in] user model id.
 * @param	int *errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const char* MSPAPI QISESessionBegin(const char* params, const char* userModelId, int* errorCode);
'''
msc.QISESessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
msc.QISESessionBegin.restype = c_char_p


def QISESessionBegin(params: bytes, userModelId: bytes) -> bytes:
    errorCode = c_int()
    sessionID: bytes = msc.QISESessionBegin(
        params, userModelId, byref(errorCode))
    MSPAssert(errorCode.value, "QISESessionBegin failed")
    return sessionID


'''
/** 
 * @fn		QISETextPut
 * @brief	Put Text
 * 
 *  Writing text string to evaluator.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by QISESessionBegin.
 * @param	const char* textString	- [in] Text buffer.
 * @param	unsigned int textLen	- [in] Text length in bytes.
 * @param	const char* params		- [in] Parameters describing the text.
 * @see		
 */
int MSPAPI QISETextPut(const char* sessionID, const char* textString, unsigned int textLen, const char* params);
'''
msc.QISETextPut.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]
msc.QISETextPut.restype = c_int


def QISETextPut(sessionID: bytes, textString: bytes, params: bytes):
    textLen = len(textString)
    errorCode: int = msc.QISETextPut(sessionID, textString, textLen, params)
    MSPAssert(errorCode, "QISETextPut failed")


'''
/** 
 * @fn		QISEAudioWrite
 * @brief	Write Audio
 * 
 *  Writing binary audio data to evaluator.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by QISESessionBegin.
 * @param	const void* waveData	- [in] Audio data to write.
 * @param	unsigned int waveLen	- [in] Audio length in bytes.
 * @param	int audioStatus			- [in] Audio status. 
 * @param	int *epStatus			- [out] EP or vad status.
 * @param	int *evlStatus			- [out] Status of evaluation result, 0: success, 1: no match, 2: incomplete, 5:speech complete.
 * @see		
 */
int MSPAPI QISEAudioWrite(const char* sessionID, const void* waveData, unsigned int waveLen, int audioStatus, int *epStatus, int *Status);
'''
msc.QISEAudioWrite.argtypes = [
    c_char_p,
    c_void_p,
    c_uint,
    c_int,
    POINTER(c_int),
    POINTER(c_int),
]
msc.QISEAudioWrite.restype = c_int


def QISEAudioWrite(
    sessionID: bytes, waveData: bytes, audioStatus: int
) -> Tuple[int, int]:
    waveLen = len(waveData)
    epStatus = c_int()
    recogStatus = c_int()
    errorCode: int = msc.QISEAudioWrite(
        sessionID, waveData, waveLen, audioStatus, byref(
            epStatus), byref(recogStatus)
    )
    MSPAssert(errorCode, "QISEAudioWrite failed")
    return epStatus.value, recogStatus.value


'''
/** 
 * @fn		QISEGetResult
 * @brief	Get Evaluation Result
 * 
 *  Get evaluation result.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by QISESessionBegin.
 * @param	int* rsltLen			- [out] Length of result returned.
 * @param	int* rsltStatus			- [out] Status of evaluation result returned.
 * @param	int* errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const char * MSPAPI QISEGetResult(const char* sessionID, unsigned int* rsltLen, int* rsltStatus, int *errorCode);
'''
msc.QISEGetResult.argtypes = [c_char_p, POINTER(
    c_uint), POINTER(c_int), POINTER(c_int)]
msc.QISEGetResult.restype = c_char_p


def QISEGetResult(sessionID: bytes) -> Tuple[bytes, int]:
    rsltLen = c_uint()
    rsltStatus = c_int()
    errorCode = c_int()
    result: bytes = msc.QISEGetResult(
        sessionID, byref(rsltLen), byref(rsltStatus), byref(errorCode)
    )
    MSPAssert(errorCode.value, "QISEGetResult failed")
    # return result, rsltStatus.value
    return string_at(result, rsltLen), rsltStatus.value


'''
/** 
 * @fn		QISESessionEnd
 * @brief	End a ISR Session
 * 
 *  End a evaluation session, release all resource.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] The session id returned by QISESessionBegin.
 * @param	const char* hints		- [in] Reason to end current session.
 * @see		
 */
int MSPAPI QISESessionEnd(const char* sessionID, const char* hints);
'''
msc.QISESessionEnd.argtypes = [c_char_p, c_char_p]
msc.QISESessionEnd.restype = c_int


def QISESessionEnd(sessionID: bytes, hints: bytes):
    errorCode: int = msc.QISESessionEnd(sessionID, hints)
    MSPAssert(errorCode, "QISESessionEnd failed")


__all__ = [
    QISESessionBegin,
    QISESessionEnd,
    QISETextPut,
    QISEAudioWrite,
    QISEGetResult,
]
