from ctypes import cdll
from ctypes import c_void_p
from typing import Callable
from typing import Generator
from threading import Event

from pyaudio import Stream

from .msp import MSPAssert

from .msp import MSP
from .msp import MSPStatus
from .msp import MSPAudioSampleStatus
from .msp import MSPRECStatus
from .msp import MSPEPStatus
from .msp import MSPTTSStatus
from .msp import MSPHCRDataStatus
from .msp import MSPIVWMSGStatus
from .msp import MSPDATASampleStatus

from .qise import QISE
from .qisr import QISR
from .qivw import QIVW
from .qtts import QTTS


class MSC(MSP, QISR, QTTS, QIVW, QISE):
    def __init__(self, sdk_path: str, params: bytes) -> None:
        self.msc = cdll.LoadLibrary(sdk_path)
        MSP.__init__(self, self.msc)
        QISR.__init__(self, self.msc)
        QTTS.__init__(self, self.msc)
        QIVW.__init__(self, self.msc)
        QISE.__init__(self, self.msc)

        self.MSPLogin(usr=b"", pwd=b"", params=params)

    def asr(
        self, params: bytes, stream: Stream, chunk_size: int = 2048
    ) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = self.QISRSessionBegin(grammarList=b"", params=params)

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = self.QISRAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = self.QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = self.QISRAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS:
                # Get Result
                result, rsltStatus = self.QISRGetResult(sessionID, waitTime=1000)

                if result:
                    yield result

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE:
                    # Session End
                    self.QISRSessionEnd(sessionID, b"Normal End.")
                    break

    def tts(self, params: bytes, text: bytes) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = self.QTTSSessionBegin(params=params)

        # Text Put
        self.QTTSTextPut(sessionID=sessionID, textString=text, params=b"")

        while True:
            # Audio Data Get
            audioData, synthStatus = self.QTTSAudioGet(sessionID)

            # Yield Audio Data
            yield audioData

            if synthStatus == MSPTTSStatus.MSP_TTS_FLAG_DATA_END:
                # Session End
                self.QTTSSessionEnd(sessionID, b"Normal End.")
                break

    def kws(
        self,
        params: bytes,
        message_callback: Callable[[bytes, int, int, int, c_void_p, c_void_p], int],
        stream: Stream,
        chunk_size: int = 2048,
        user_data=b"",
        stop_event: Event = Event(),
    ) -> None:
        # Session Begin
        sessionID = self.QIVWSessionBegin(grammarList=b"", params=params)

        # Register Notify
        msgProcCb = self.msgProcCallBack(message_callback)
        self.QIVWRegisterNotify(
            sessionID=sessionID, msgProcCb=msgProcCb, userData=user_data
        )

        # Audio Write
        audioData = stream.read(chunk_size)
        self.QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while not stop_event.is_set():
            # Audio Write
            audioData = stream.read(chunk_size)
            self.QIVWAudioWrite(
                sessionID=sessionID,
                audioData=audioData,
                audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
            )

        # Audio Write
        audioData = stream.read(chunk_size)
        self.QIVWAudioWrite(
            sessionID=sessionID,
            audioData=audioData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
        )

        # Session End
        self.QIVWSessionEnd(sessionID, b"Normal End.")

    def ase(
        self, params: bytes, text: bytes, stream: Stream, chunk_size: int = 2048
    ) -> Generator[bytes, None, None]:
        # Session Begin
        sessionID = self.QISESessionBegin(params=params, userModelId=b"")

        self.QISETextPut(sessionID=sessionID, textString=text, params=b"")

        # Audio Write
        waveData = stream.read(chunk_size)
        epStatus, recogStatus = self.QISEAudioWrite(
            sessionID=sessionID,
            waveData=waveData,
            audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_FIRST,
        )

        while True:
            if epStatus != MSPEPStatus.MSP_EP_AFTER_SPEECH:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = self.QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_CONTINUE,
                )
            else:
                # Audio Write
                waveData = stream.read(chunk_size)
                epStatus, recogStatus = self.QISEAudioWrite(
                    sessionID=sessionID,
                    waveData=waveData,
                    audioStatus=MSPAudioSampleStatus.MSP_AUDIO_SAMPLE_LAST,
                )
            if recogStatus == MSPRECStatus.MSP_REC_STATUS_SUCCESS:
                # Get Result
                result, rsltStatus = self.QISEGetResult(sessionID)

                if result:
                    # Yield Result
                    yield result

                if rsltStatus == MSPRECStatus.MSP_REC_STATUS_COMPLETE:
                    # Session End
                    self.QISESessionEnd(sessionID, b"Normal End.")
                    break

    def __del__(self) -> None:
        self.MSPLogout()


__version__ = "0.2.0"

__all__ = [
    "__version__",
    "MSC",
    "MSPStatus",
    "MSPAudioSampleStatus",
    "MSPRECStatus",
    "MSPEPStatus",
    "MSPTTSStatus",
    "MSPHCRDataStatus",
    "MSPIVWMSGStatus",
    "MSPDATASampleStatus",
    "MSPAssert",
    "QISE",
    "QISR",
    "QIVW",
    "QTTS",
    "MSP",
]
