from ctypes import byref
from ctypes import POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msc import msc
from .msp import MSPAssert

__all__ = [
    "QISESessionBegin",
    "QISETextPut",
    "QISEAudioWrite",
    "QISEGetResult",
    "QISEResultInfo",
    "QISESessionEnd",
    "QISEGetParam",
]

"""
/**
 * @file    qise.h
 * @brief   iFLY Speech Evaluation Header File
 * 
 *  This file contains the quick application programming interface (API) declarations 
 *  of evaluation. Developer can include this file in your project to build applications.
 *  For more information, please read the developer guide.
 
 *  Use of this software is subject to certain restrictions and limitations set
 *  forth in a license agreement entered into between iFLYTEK, Co,LTD.
 *  and the licensee of this software.  Please refer to the license
 *  agreement for license use rights and restrictions.
 *
 *  Copyright (C)    1999 - 2012 by ANHUI USTC iFLYTEK, Co,LTD.
 *                   All rights reserved.
 * 
 * @author  Speech Dept. iFLYTEK.
 * @version 1.0
 * @date    2012/4/16
 * 
 * @see        
 * 
 * <b>History:</b><br>
 * <table>
 *  <tr> <th>Version	<th>Date		<th>Author	<th>Notes</tr>
 *  <tr> <td>1.0		<td>2012/4/16	<td>MSP40	<td>Create this file</tr>
 * </table>
 * 
 */

#ifndef __MSP_ISE_H__
#define __MSP_ISE_H__

#ifdef __cplusplus
extern "C" {
#endif /* C++ */

#include "msp_types.h"

/** 
 * @fn		QISEInit
 * @brief	Initialize API
 * 
 *  Load API module with specified configurations.
 * 
 * @return	int MSPAPI			- Return 0 in success, otherwise return error code.
 * @param	const char* configs	- [in] Configurations to initialize.
 * @see		
 */
/*int MSPAPI QISEInit(const char* configs);
typedef int (MSPAPI *Proc_QISEInit)(const char* configs);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QISEInitW(const wchar_t* configs);
typedef int (MSPAPI *Proc_QISEInitW)(const wchar_t* configs);
#endif*/

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
typedef const char* (MSPAPI *Proc_QISESessionBegin)(const char* params, const char* userModelID, int *errorCode);
#ifdef MSP_WCHAR_SUPPORT
const wchar_t* MSPAPI QISESessionBeginW(const wchar_t* params, const wchar_t* userModelID, int *errorCode);
typedef const wchar_t* (MSPAPI *Proc_QISESessionBeginW)(const wchar_t* params, const wchar_t* userModelID, int *errorCode);
#endif

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
typedef int (MSPAPI *Proc_QISETextPut)(const char* sessionID, const char* textString, unsigned int textLen, const char* params);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QISETextPutW(const wchar_t* sessionID, const wchar_t* textString, unsigned int textLen, const wchar_t* params);
typedef int (MSPAPI *Proc_QISETextPutW)(const wchar_t* sessionID, const wchar_t* textString, unsigned int textLen, const wchar_t* params);
#endif

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
typedef int (MSPAPI *Proc_QISEAudioWrite)(const char* sessionID, const void* waveData, unsigned int waveLen, int audioStatus, int *epStatus, int *recogStatus);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QISEAudioWriteW(const wchar_t* sessionID, const void* waveData, unsigned int waveLen, int audioStatus, int *epStatus, int *evlStatus);
typedef int (MSPAPI *Proc_QISEAudioWriteW)(const wchar_t* sessionID, const void* waveData, unsigned int waveLen, int audioStatus, int *epStatus, int *evlStatus);
#endif

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
typedef const char * (MSPAPI *Proc_QISEGetResult)(const char* sessionID, unsigned int* rsltLen, int* rsltStatus, int *errorCode);
#ifdef MSP_WCHAR_SUPPORT
const wchar_t* MSPAPI QISEGetResultW(const wchar_t* sessionID, int* rsltLen, unsigned int* rsltStatus, int *errorCode);
typedef const wchar_t* (MSPAPI *Proc_QISEGetResultW)(const wchar_t* sessionID, unsigned int* rsltLen, int* rsltStatus, int *errorCode);
#endif

/** 
 * @fn		QISEResultInfo
 * @brief	Get Result Info
 * 
 *  Get info of evaluation result.
 * 
 * @return	const char *			- The session id returned by QISESessionBegin.
 * @param	const char* sessionID	- [in] session id returned by QISESessionBegin.
 * @see		
 */
const char* MSPAPI QISEResultInfo(const char* sessionID, int *errorCode);
typedef const char* (MSPAPI *Proc_QISEResultInfo)(const char* sessionID, int *errorCode);
#ifdef MSP_WCHAR_SUPPORT
const wchar_t* MSPAPI QISEResultInfoW(const wchar_t* sessionID, int *errorCode);
typedef const wchar_t* (MSPAPI *Proc_QISEResultInfoW)(const wchar_t* sessionID, int *errorCode);
#endif

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
typedef int (MSPAPI *Proc_QISESessionEnd)(const char* sessionID, const char* hints);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QISESessionEndW(const wchar_t* sessionID, const wchar_t* hints);
typedef int (MSPAPI *Proc_QISESessionEndW)(const wchar_t* sessionID, const wchar_t* hints);
#endif

/** 
 * @fn		QISEGetParam
 * @brief	get params related with msc
 * 
 *  the params could be local or server param, we only support netflow params "upflow" & "downflow" now
 * 
 * @return	int	MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* sessionID	- [in] session id of related param, set NULL to got global param
 * @param	const char* paramName	- [in] param name,could pass more than one param splited by ',' ';' or '\n'.
 * @param	const char* paramValue	- [in] param value buffer, malloced by user.
 * @param	int *valueLen			- [in, out] in: length of value buffer, out: length of value string.
 * @see		
 */
int MSPAPI QISEGetParam(const char* sessionID, const char* paramName, char* paramValue, unsigned int* valueLen);
typedef int (MSPAPI *Proc_QISEGetParam)(const char* sessionID, const char* paramName, char* paramValue, unsigned int* valueLen);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QISEGetParamW(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue, unsigned int* valueLen);
typedef int (MSPAPI *Proc_QISEGetParamW)(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue, unsigned int* valueLen);
#endif

/*
// 
// typedef void ( MSPAPI *recog_result_ntf_handler)( const char *sessionID, const char *result, int resultLen, int resultStatus, void *userData ); 
// typedef void ( MSPAPI *status_ntf_handler)( const char *sessionID, int type, int status, const void *param1, const void *param2, void *userData);
// typedef void ( MSPAPI *error_ntf_handler)(const char *sessionID, int errorCode,	const char *detail, void *userData);
// int MSPAPI QISERegisterNotify(const char *sessionID, recog_result_ntf_handler rsltCb, status_ntf_handler statusCb, error_ntf_handler errCb, void *userData);
*/


#ifdef __cplusplus
} /* extern "C" */	
#endif /* C++ */

#endif /* __MSP_ISE_H__ */
"""

msc.QISESessionBegin.argtypes = [c_char_p, c_char_p, POINTER(c_int)]
msc.QISESessionBegin.restype = c_char_p

msc.QISETextPut.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]
msc.QISETextPut.restype = c_int

msc.QISEAudioWrite.argtypes = [
    c_char_p,
    c_void_p,
    c_uint,
    c_int,
    POINTER(c_int),
    POINTER(c_int),
]
msc.QISEAudioWrite.restype = c_int

msc.QISEGetResult.argtypes = [c_char_p, POINTER(c_uint), POINTER(c_int), POINTER(c_int)]
msc.QISEGetResult.restype = c_char_p

msc.QISEResultInfo.argtypes = [c_char_p, POINTER(c_int)]
msc.QISEResultInfo.restype = c_char_p

msc.QISESessionEnd.argtypes = [c_char_p, c_char_p]
msc.QISESessionEnd.restype = c_int

msc.QISEGetParam.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_uint)]
msc.QISEGetParam.restype = c_int


def QISESessionBegin(params: str, userModelId: str) -> str:
    params = params.encode("UTF-8") if params else None
    userModelId = userModelId.encode("UTF-8") if userModelId else None
    errorCode = c_int()
    sessionID: bytes = msc.QISESessionBegin(params, userModelId, byref(errorCode))
    MSPAssert(errorCode.value, "QISESessionBegin failed")
    return sessionID.decode("UTF-8") if sessionID else None


def QISETextPut(sessionID: str, textString: str, textLen: int, params: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    textString = textString.encode("UTF-8") if textString else None
    params = params.encode("UTF-8") if params else None
    errorCode: int = msc.QISETextPut(sessionID, textString, textLen, params)
    MSPAssert(errorCode, "QISETextPut failed")


def QISEAudioWrite(
    sessionID: str, waveData: bytes, waveLen: int, audioStatus: int
) -> Tuple[int, int]:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    waveData = waveData if waveData else None
    epStatus = c_int()
    recogStatus = c_int()
    errorCode: int = msc.QISEAudioWrite(
        sessionID, waveData, waveLen, audioStatus, byref(epStatus), byref(recogStatus)
    )
    MSPAssert(errorCode, "QISEAudioWrite failed")
    return epStatus.value, recogStatus.value


def QISEGetResult(sessionID: str) -> Tuple[str, int, int]:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    rsltLen = c_uint()
    rsltStatus = c_int()
    errorCode = c_int()
    result: bytes = msc.QISEGetResult(
        sessionID, byref(rsltLen), byref(rsltStatus), byref(errorCode)
    )
    MSPAssert(errorCode.value, "QISEGetResult failed")
    return result.decode("UTF-8") if result else None, rsltLen.value, rsltStatus.value


def QISEResultInfo(sessionID: str) -> str:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    errorCode = c_int()
    resultInfo: bytes = msc.QISEResultInfo(sessionID, byref(errorCode))
    MSPAssert(errorCode.value, "QISEResultInfo failed")
    return resultInfo.decode("UTF-8") if resultInfo else None


def QISESessionEnd(sessionID: str, hints: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    hints = hints.encode("UTF-8") if hints else None
    errorCode: int = msc.QISESessionEnd(sessionID, hints)
    MSPAssert(errorCode, "QISESessionEnd failed")


def QISEGetParam(sessionID: str, paramName: str) -> Tuple[str, int]:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    paramName = paramName.encode("UTF-8") if paramName else None
    valueLen = c_uint()
    paramValue = c_char_p()
    errorCode: int = msc.QISEGetParam(sessionID, paramName, paramValue, byref(valueLen))
    MSPAssert(errorCode, "QISEGetParam failed")
    return paramValue.value.decode("UTF-8") if paramValue else None, valueLen.value
