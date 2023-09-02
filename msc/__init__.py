import json

from typing import Callable
from ctypes import c_void_p
from threading import Event

from pyaudio import Stream

from .msc import msc

from .msp import MSPStatus, MSPAudioSampleStatus
from .msp import MSPRECStatus, MSPEPStatus
from .msp import MSPTTSFlags, MSPHCRDataFlags
from .msp import MSPIVWMSGFlags, MSPDATASampleFlags
from .msp import MSPLogin, MSPLogout
from .msp import MSPSetParam, MSPGetParam
from .msp import MSPUploadData, MSPDownloadData
from .msp import MSPSearch, MSPNlpSearch
from .msp import MSPNlpSchCancel, MSPRegisterNotify
from .msp import MSPGetVersion, MSPAssert

from .qisr import recog_result_ntf_handler
from .qisr import recog_status_ntf_handler
from .qisr import recog_error_ntf_handler
from .qisr import GrammarCallBack, LexiconCallBack
from .qisr import QISRSessionBegin, QISRSessionEnd
from .qisr import QISRAudioWrite, QISRGetResult, QISRGetBinaryResult
from .qisr import QISRGetParam, QISRSetParam, QISRRegisterNotify
from .qisr import QISRBuildGrammar, QISRUpdateLexicon

from .qise import QISESessionBegin, QISESessionEnd
from .qise import QISETextPut, QISEAudioWrite, QISEGetResult
from .qise import QISEResultInfo, QISEGetParam

from .qivw import ivw_ntf_handler
from .qivw import QIVWSessionBegin, QIVWSessionEnd
from .qivw import QIVWAudioWrite, QIVWRegisterNotify
from .qivw import QIVWGetResInfo

from .qtts import tts_result_ntf_handler
from .qtts import tts_status_ntf_handler
from .qtts import tts_error_ntf_handler
from .qtts import QTTSSessionBegin, QTTSSessionEnd
from .qtts import QTTSTextPut, QTTSAudioGet, QTTSAudioInfo
from .qtts import QTTSGetParam, QTTSSetParam, QTTSRegisterNotify


__all__ = [
    "__version__",
    "MSC",
    "msc",
    "MSPStatus",
    "MSPAudioSampleStatus",
    "MSPRECStatus",
    "MSPEPStatus",
    "MSPTTSFlags",
    "MSPHCRDataFlags",
    "MSPIVWMSGFlags",
    "MSPDATASampleFlags",
    "MSPAssert",
    "MSPLogin",
    "MSPLogout",
    "MSPSetParam",
    "MSPGetParam",
    "MSPUploadData",
    "MSPDownloadData",
    "MSPSearch",
    "MSPNlpSearch",
    "MSPNlpSchCancel",
    "MSPRegisterNotify",
    "MSPGetVersion",
    "recog_result_ntf_handler",
    "recog_status_ntf_handler",
    "recog_error_ntf_handler",
    "GrammarCallBack",
    "LexiconCallBack",
    "QISRSessionBegin",
    "QISRAudioWrite",
    "QISRGetResult",
    "QISRGetBinaryResult",
    "QISRSessionEnd",
    "QISRGetParam",
    "QISRSetParam",
    "QISRRegisterNotify",
    "QISRBuildGrammar",
    "QISRUpdateLexicon",
    "QISESessionBegin",
    "QISETextPut",
    "QISEAudioWrite",
    "QISEGetResult",
    "QISEResultInfo",
    "QISESessionEnd",
    "QISEGetParam",
    "ivw_ntf_handler",
    "QIVWSessionBegin",
    "QIVWSessionEnd",
    "QIVWAudioWrite",
    "QIVWRegisterNotify",
    "QIVWGetResInfo",
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


class MSC:
    def __init__(self, params: str) -> None:
        MSPLogin(usr=None, pwd=None, params=params)

    @staticmethod
    def asr(params: str, stream: Stream, chunk_size: int = 2048):
        # Session Begin
        sessionID = QISRSessionBegin(grammarList=None, params=params)

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = QISRAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST.value,
        )

        results = []
        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH.value:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE.value,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST.value,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS.value:
                # Get Result
                result, rsltStatus = QISRGetResult(sessionID, waitTime=1000)

                if result:
                    result = json.loads(result)

                    if result["pgs"] == "apd":
                        # Append
                        text = ""
                        for item in result["ws"]:
                            text += item["cw"][0]["w"]
                        results.append(text)
                    else:
                        # Replace
                        text = ""
                        for item in result["ws"]:
                            text += item["cw"][0]["w"]
                        start, end = result["rg"]
                        start -= 1
                        end -= 1
                        results[start] = text
                        results.append("")
                        for i in range(start + 1, end + 1):
                            results[i] = ""

                    # Yield Result
                    yield "".join(results)

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE.value:
                    # Session End
                    QISRSessionEnd(sessionID, "Normal End.")
                    break

    @staticmethod
    def tts(params: str, text: str):
        # Session Begin
        sessionID = QTTSSessionBegin(params=params)

        # Text Put
        QTTSTextPut(sessionID=sessionID, textString=text, params=None)

        while True:
            # Audio Data Get
            audioData, synthStatus = QTTSAudioGet(sessionID)

            # Yield Audio Data
            yield audioData

            if synthStatus == MSPTTSFlags.MSP_TTS_FLAG_DATA_END.value:
                # Session End
                QTTSSessionEnd(sessionID, "Normal End.")
                break

    @staticmethod
    def kws(
        params: str,
        message_callback: Callable[[bytes, int, int, int, c_void_p, c_void_p], int],
        stream: Stream,
        chunk_size: int = 2048,
        user_data=None,
        stop_event: Event = None
    ):
        # Session Begin
        sessionID = QIVWSessionBegin(grammarList=None, params=params)

        # Register Notify
        msgProcCb = ivw_ntf_handler(message_callback)
        QIVWRegisterNotify(sessionID=sessionID,
                           msgProcCb=msgProcCb, userData=user_data)

        # Audio Write
        audioData = stream.read(chunk_size)
        QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST.value,
        )

        while not stop_event.is_set():
            # Audio Write
            audioData = stream.read(chunk_size)
            QIVWAudioWrite(
                sessionID=sessionID,
                audioData=audioData,
                audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE.value,
            )

        # Audio Write
        audioData = stream.read(chunk_size)
        QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST.value,
        )

    @staticmethod
    def ase(params: str, text: str, stream: Stream, chunk_size: int = 2048):
        # Session Begin
        sessionID = QISESessionBegin(params=params, userModelId=None)

        QISETextPut(
            sessionID=sessionID,
            textString=text,
            params=None
        )

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = QISEAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST.value,
        )

        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH.value:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE.value,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST.value,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS.value:
                # Get Result
                result, rsltStatus = QISEGetResult(sessionID)

                if result:
                    # Yield Result
                    yield result

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE.value:
                    # Session End
                    QISESessionEnd(sessionID, "Normal End.")
                    break

    def __del__(self) -> None:
        MSPLogout()


__version__ = "0.1.0"
