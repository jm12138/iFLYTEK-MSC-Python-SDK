from _ctypes import CFuncPtr
from ctypes import byref, string_at
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_uint, c_void_p, c_char_p

from typing import Tuple

from .msc import msc
from .msp import MSPAssert

__all__ = [
    "tts_result_ntf_handler",
    "tts_status_ntf_handler",
    "tts_error_ntf_handler",
    "QTTSSessionBegin",
    "QTTSTextPut",
    "QTTSAudioGet",
    "QTTSAudioInfo",
    "QTTSSessionEnd",
    "QTTSGetParam",
    "QTTSSetParam",
    "QTTSRegisterNotify",
]

"""
/** 
 * @file	qtts.h
 * @brief   iFLY Speech Synthesizer Header File
 * 
 *  This file contains the quick application programming interface (API) declarations 
 *  of TTS. Developer can include this file in your project to build applications.
 *  For more information, please read the developer guide.
 
 *  Use of this software is subject to certain restrictions and limitations set
 *  forth in a license agreement entered into between iFLYTEK, Co,LTD.
 *  and the licensee of this software.  Please refer to the license
 *  agreement for license use rights and restrictions.
 *
 *  Copyright (C)    1999 - 2009 by ANHUI USTC iFLYTEK, Co,LTD.
 *                   All rights reserved.
 * 
 * @author	Speech Dept.
 * @version	1.0
 * @date	2009/11/26
 * 
 * @see		
 * 
 * <b>History:</b><br>
 * <table>
 *  <tr> <th>Version	<th>Date		<th>Author	<th>Notes</tr>
 *  <tr> <td>1.0		<td>2009/11/26	<td>Speech	<td>Create this file</tr>
 * </table>
 * 
 */
#ifndef __QTTS_H__
#define __QTTS_H__

#if !defined(MSPAPI)
#if defined(WIN32)
	#define MSPAPI __stdcall
#else
	#define MSPAPI
#endif /* WIN32 */
#endif /* MSPAPI */

#ifdef __cplusplus
extern "C" {
#endif /* C++ */

#include "msp_types.h"

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
typedef const char* (MSPAPI *Proc_QTTSSessionBegin)(const char* params, int* errorCode);
#ifdef MSP_WCHAR_SUPPORT
const wchar_t* MSPAPI QTTSSessionBeginW(const wchar_t* params, int* errorCode);
typedef const wchar_t* (MSPAPI *Proc_QTTSSessionBeginW)(const wchar_t* params, int* errorCode);
#endif

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
typedef int (MSPAPI *Proc_QTTSTextPut)(const char* sessionID, const char* textString, unsigned int textLen, const char* params);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QTTSTextPutW(const wchar_t* sessionID, const wchar_t* textString, unsigned int textLen, const wchar_t* params);
typedef int (MSPAPI *Proc_QTTSTextPutW)(const wchar_t* sessionID, const wchar_t* textString, unsigned int textLen, const wchar_t* params);
#endif

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
typedef const void* (MSPAPI *Proc_QTTSAudioGet)(const char* sessionID, unsigned int* audioLen, int* synthStatus, int* errorCode);
#ifdef MSP_WCHAR_SUPPORT
const void* MSPAPI QTTSAudioGetW(const wchar_t* sessionID, unsigned int* audioLen, int* synthStatus, int* errorCode);
typedef const void* (MSPAPI *Proc_QTTSAudioGetW)(const wchar_t* sessionID, unsigned int* audioLen, int* synthStatus, int* errorCode);
#endif

/** 
 * @fn		QTTSAudioInfo
 * @brief	Get Synthesized Audio information
 * 
 *  Get synthesized audio data information.
 * 
 * @return	const char * - Return audio info string.
 * @param	const char* sessionID	- [in] session id returned by session begin
 * @see		
 */
const char* MSPAPI QTTSAudioInfo(const char* sessionID);
typedef const char* (MSPAPI *Proc_QTTSAudioInfo)(const char* sessionID);
#ifdef MSP_WCHAR_SUPPORT
const wchar_t* MSPAPI QTTSAudioInfoW(const wchar_t* sessionID);
typedef const wchar_t* (MSPAPI *Proc_QTTSAudioInfoW)(const wchar_t* sessionID);
#endif

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
typedef int (MSPAPI *Proc_QTTSSessionEnd)(const char* sessionID, const char* hints);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QTTSSessionEndW(const wchar_t* sessionID, const wchar_t* hints);
typedef int (MSPAPI *Proc_QTTSSessionEndW)(const wchar_t* sessionID, const wchar_t* hints);
#endif

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
typedef int (MSPAPI *Proc_QTTSGetParam)(const char* sessionID, const char* paramName, char* paramValue, unsigned int* valueLen);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QTTSGetParamW(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue, unsigned int* valueLen);
typedef int (MSPAPI *Proc_QTTSGetParamW)(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue, unsigned int* valueLen);
#endif

/** 
 * @fn		QTTSSetParam
 * @brief	set params related with msc
 * 
 *  the params could be local or server param, we only support netflow params "upflow" & "downflow" now
 * 
 * @return	int	- Return 0 if success, otherwise return errcode.
 * @param	const char* sessionID	- [in] session id of related param, set NULL to got global param
 * @param	const char* paramName	- [in] param name,could pass more than one param split by ','';'or'\n'
 * @param	const char* paramValue	- [in] param value buffer, malloced by user
 * @see		
 */
int MSPAPI QTTSSetParam(const char *sessionID, const char *paramName, const char *paramValue);
typedef int (MSPAPI *Proc_QTTSSetParam)(const char* sessionID, const char* paramName, char* paramValue);
#ifdef MSP_WCHAR_SUPPORT
int MSPAPI QTTSSetParamW(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue);
typedef int (MSPAPI *Proc_QTTSSetParamW)(const wchar_t* sessionID, const wchar_t* paramName, wchar_t* paramValue);
#endif

typedef void ( *tts_result_ntf_handler)( const char *sessionID, const char *audio, int audioLen, int synthStatus, int ced, const char *audioInfo, int audioInfoLen, void *userData ); 
typedef void ( *tts_status_ntf_handler)( const char *sessionID, int type, int status, int param1, const void *param2, void *userData);
typedef void ( *tts_error_ntf_handler)(const char *sessionID, int errorCode,	const char *detail, void *userData);
int MSPAPI QTTSRegisterNotify(const char *sessionID, tts_result_ntf_handler rsltCb, tts_status_ntf_handler statusCb, tts_error_ntf_handler errCb, void *userData);

#ifdef __cplusplus
} /* extern "C" */
#endif /* C++ */

#endif /* __QTTS_H__ */
"""

msc.QTTSSessionBegin.argtypes = [c_char_p, POINTER(c_int)]
msc.QTTSSessionBegin.restype = c_char_p

msc.QTTSTextPut.argtypes = [c_char_p, c_char_p, c_uint, c_char_p]
msc.QTTSTextPut.restype = c_int

msc.QTTSAudioGet.argtypes = [c_char_p, POINTER(c_uint), POINTER(c_int), POINTER(c_int)]
msc.QTTSAudioGet.restype = c_void_p

msc.QTTSAudioInfo.argtypes = [c_char_p]
msc.QTTSAudioInfo.restype = c_char_p

msc.QTTSSessionEnd.argtypes = [c_char_p, c_char_p]
msc.QTTSSessionEnd.restype = c_int

msc.QTTSGetParam.argtypes = [c_char_p, c_char_p, c_char_p, POINTER(c_uint)]
msc.QTTSGetParam.restype = c_int

msc.QTTSSetParam.argtypes = [c_char_p, c_char_p, c_char_p]
msc.QTTSSetParam.restype = c_int

tts_result_ntf_handler = CFUNCTYPE(
    None, c_char_p, c_char_p, c_int, c_int, c_int, c_char_p, c_int, c_void_p
)
tts_status_ntf_handler = CFUNCTYPE(
    None, c_char_p, c_int, c_int, c_int, c_void_p, c_void_p
)
tts_error_ntf_handler = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_void_p)
msc.QTTSRegisterNotify.argtypes = [
    c_char_p,
    tts_result_ntf_handler,
    tts_status_ntf_handler,
    tts_error_ntf_handler,
    c_void_p,
]
msc.QTTSRegisterNotify.restype = c_int


def QTTSSessionBegin(params: str) -> str:
    params = params.encode("UTF-8") if params else None
    errorCode = c_int()
    sessionID: bytes = msc.QTTSSessionBegin(params, byref(errorCode))
    MSPAssert(errorCode.value)
    return sessionID.decode("UTF-8") if sessionID else None


def QTTSTextPut(sessionID: str, textString: str, params: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    textString = textString.encode("UTF-8") if textString else None
    params = params.encode("UTF-8") if params else None
    textLen = len(textString)
    errorCode: int = msc.QTTSTextPut(sessionID, textString, textLen, params)
    MSPAssert(errorCode)


def QTTSAudioGet(sessionID: str) -> Tuple[bytes, int]:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    audioLen = c_uint()
    synthStatus = c_int()
    errorCode = c_int()
    audioData: c_void_p = msc.QTTSAudioGet(
        sessionID, byref(audioLen), byref(synthStatus), byref(errorCode)
    )
    MSPAssert(errorCode.value)
    return string_at(audioData, audioLen.value), synthStatus.value


def QTTSAudioInfo(sessionID: str) -> str:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    audioInfo: bytes = msc.QTTSAudioInfo(sessionID)
    return audioInfo.decode("UTF-8") if audioInfo else None


def QTTSSessionEnd(sessionID: str, hints: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    hints = hints.encode("UTF-8") if hints else None
    errorCode: int = msc.QTTSSessionEnd(sessionID, hints)
    MSPAssert(errorCode)


def QTTSGetParam(sessionID: str, paramName: str) -> Tuple[str, int]:
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    paramName = paramName.encode("UTF-8") if paramName else None
    valueLen = c_uint()
    paramValue = c_char_p()
    errorCode: int = msc.QTTSGetParam(sessionID, paramName, paramValue, byref(valueLen))
    MSPAssert(errorCode)
    return paramValue.value.decode("UTF-8"), valueLen.value


def QTTSSetParam(sessionID: str, paramName: str, paramValue: str):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    paramName = paramName.encode("UTF-8") if paramName else None
    paramValue = paramValue.encode("UTF-8") if paramValue else None
    errorCode: int = msc.QTTSSetParam(sessionID, paramName, paramValue)
    MSPAssert(errorCode)


def QTTSRegisterNotify(
    sessionID: str,
    rsltCb: CFuncPtr,
    statusCb: CFuncPtr,
    errCb: CFuncPtr,
    userData: bytes,
):
    sessionID = sessionID.encode("UTF-8") if sessionID else None
    errorCode: int = msc.QTTSRegisterNotify(
        sessionID, rsltCb, statusCb, errCb, userData
    )
    MSPAssert(errorCode)
