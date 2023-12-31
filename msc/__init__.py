from typing import Callable
from typing import Generator
from ctypes import c_void_p
from threading import Event

from pyaudio import Stream

from .msp import msc
from .msp import MSPAssert
from .msp import MSPLogin
from .msp import MSPLogout
from .msp import MSPSetParam
from .msp import MSPGetParam
from .msp import MSPUploadData
from .msp import MSPGetVersion
from .msp import MSPStatus
from .msp import MSPAudioSampleStatus
from .msp import MSPRECStatus
from .msp import MSPEPStatus
from .msp import MSPTTSStatus
from .msp import MSPHCRDataStatus
from .msp import MSPIVWMSGStatus
from .msp import MSPDATASampleStatus
from .qisr import GrammarCallBack
from .qisr import LexiconCallBack
from .qisr import QISRSessionBegin
from .qisr import QISRAudioWrite
from .qisr import QISRGetResult
from .qisr import QISRSessionEnd
from .qisr import QISRGetParam
from .qisr import QISRBuildGrammar
from .qisr import QISRUpdateLexicon
from .qtts import QTTSSessionBegin
from .qtts import QTTSTextPut
from .qtts import QTTSAudioGet
from .qtts import QTTSSessionEnd
from .qtts import QTTSGetParam
from .qivw import msgProcCallBack
from .qivw import QIVWSessionBegin
from .qivw import QIVWSessionEnd
from .qivw import QIVWAudioWrite
from .qivw import QIVWRegisterNotify
from .qise import QISESessionBegin
from .qise import QISESessionEnd
from .qise import QISETextPut
from .qise import QISEAudioWrite
from .qise import QISEGetResult


class MSC:
    def __init__(self, params: bytes) -> None:
        MSPLogin(usr=None, pwd=None, params=params)

    @staticmethod
    def asr(
        params: bytes, stream: Stream, chunk_size: int = 2048
    ) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = QISRSessionBegin(grammarList=None, params=params)

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = QISRAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS:
                # Get Result
                result, rsltStatus = QISRGetResult(sessionID, waitTime=1000)

                if result:
                    yield result

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE:
                    # Session End
                    QISRSessionEnd(sessionID, b"Normal End.")
                    break

    @staticmethod
    def tts(params: bytes, text: bytes) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = QTTSSessionBegin(params=params)

        # Text Put
        QTTSTextPut(sessionID=sessionID, textString=text, params=None)

        while True:
            # Audio Data Get
            audioData, synthStatus = QTTSAudioGet(sessionID)

            # Yield Audio Data
            yield audioData

            if synthStatus == MSPTTSStatus.MSP_TTS_FLAG_DATA_END:
                # Session End
                QTTSSessionEnd(sessionID, b"Normal End.")
                break

    @staticmethod
    def kws(
        params: bytes,
        message_callback: Callable[[bytes, int, int, int, c_void_p, c_void_p], int],
        stream: Stream,
        chunk_size: int = 2048,
        user_data=None,
        stop_event: Event = None,
    ) -> None:
        # Session Begin
        sessionID = QIVWSessionBegin(grammarList=None, params=params)

        # Register Notify
        msgProcCb = msgProcCallBack(message_callback)
        QIVWRegisterNotify(sessionID=sessionID, msgProcCb=msgProcCb, userData=user_data)

        # Audio Write
        audioData = stream.read(chunk_size)
        QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while not stop_event.is_set():
            # Audio Write
            audioData = stream.read(chunk_size)
            QIVWAudioWrite(
                sessionID=sessionID,
                audioData=audioData,
                audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
            )

        # Audio Write
        audioData = stream.read(chunk_size)
        QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
        )

        # Session End
        QIVWSessionEnd(sessionID, b"Normal End.")

    @staticmethod
    def ase(
        params: bytes, text: bytes, stream: Stream, chunk_size: int = 2048
    ) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = QISESessionBegin(params=params, userModelId=None)

        QISETextPut(sessionID=sessionID, textString=text, params=None)

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = QISEAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS:
                # Get Result
                result, rsltStatus = QISEGetResult(sessionID)

                if result:
                    # Yield Result
                    yield result

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE:
                    # Session End
                    QISESessionEnd(sessionID, b"Normal End.")
                    break

    def __del__(self) -> None:
        MSPLogout()


__version__ = "0.1.0"

__all__ = [
    __version__,
    msc,
    MSC,
    MSPStatus,
    MSPAudioSampleStatus,
    MSPRECStatus,
    MSPEPStatus,
    MSPTTSStatus,
    MSPHCRDataStatus,
    MSPIVWMSGStatus,
    MSPDATASampleStatus,
    MSPAssert,
    MSPLogin,
    MSPLogout,
    MSPSetParam,
    MSPGetParam,
    MSPUploadData,
    MSPGetVersion,
    QISRSessionBegin,
    QISRAudioWrite,
    QISRGetResult,
    QISRSessionEnd,
    QISRGetParam,
    QISRBuildGrammar,
    QISRUpdateLexicon,
    LexiconCallBack,
    GrammarCallBack,
    QTTSSessionBegin,
    QTTSTextPut,
    QTTSAudioGet,
    QTTSSessionEnd,
    QTTSGetParam,
    msgProcCallBack,
    QIVWSessionBegin,
    QIVWSessionEnd,
    QIVWAudioWrite,
    QIVWRegisterNotify,
    QISESessionBegin,
    QISESessionEnd,
    QISETextPut,
    QISEAudioWrite,
    QISEGetResult,
]
