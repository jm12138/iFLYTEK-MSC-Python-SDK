# iFLYTEK-MSC-Python-SDK
A third-party Python SDK for a iFLYTEK MSC. Using for ASR, TSS, KWS.

# Quick Start
* Install MSC SDK

    ```bash
    $ pip install git+https://github.com/jm12138/iFLYTEK-MSC-Python-SDK
    ```

* Voice Wakeup (KWS)

    ```python
    import msc
    import pyaudio
    from ctypes import string_at, c_void_p
    from threading import Event

    # Audio Stream
    p = pyaudio.PyAudio()
    input_stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=2048
    )

    # Set APP ID
    appid = '' 

    # Set MSC Client
    client = msc.MSC(params=f"appid={appid}".encode('UTF-8'))

    # Stop Event
    stop_event = Event()

    # KSW Callback Function
    def message_callback(
            sessionID: bytes,
            msg: int,
            param1: int,
            param2: int,
            info: c_void_p,
            userData: c_void_p
    ):
        # Print Result
        print('sessionID: ', sessionID.decode('UTF-8'))
        print('msg: ', msg)
        print('param1: ', param1)
        print('param2: ', param2)
        print('info: ', string_at(info, param2).decode('UTF-8'))
        print('userData: ', userData)

        # Stop
        stop_event.set()

        return 0

    # Set IVW Res Path
    ivw_res_path = ''

    # Start KWS
    client.kws(
        params=f'ivw_res_path=fo|{ivw_res_path}'.encode('UTF-8'),
        message_callback=message_callback,
        stream=input_stream,
        chunk_size=2048,
        user_data=None,
        stop_event=stop_event
    )
    ```

        pIvwParam = {
            "rlt": [
                {
                    "sid": "undefine",
                    "istart": 33,
                    "iresid": 119,
                    "iresIndex": 2,
                    "iduration": 189,
                    "nfillerscore": 0,
                    "nkeywordscore": 142754,
                    "ncm": 1525,
                    "keyword": "ding1 dong1 ding1 dong1  "
                }
            ]
        }
        data->rlt = {
            "rlt": [
                {
                    "sid": "undefine",
                    "istart": 33,
                    "iresid": 119,
                    "iresIndex": 2,
                    "iduration": 189,
                    "nfillerscore": 0,
                    "nkeywordscore": 142754,
                    "ncm": 1525,
                    "keyword": "ding1 dong1 ding1 dong1  "
                }
            ]
        }
        data->datalen=76864
        sessionID:  civw1PdHHBHvGQRgCahtaaBJvtTw1WLl5L
        msg: 1
        param1: 0
        param2: 98
        info: {
            "sst": "wakeup",
            "id": 2,
            "score": 1525,
            "bos": 330,
            "eos": 2220,
            "keyword": "lao3-zhang1-lao3-zhang1"
        }
        userData:  None
        wakeup : ivw param = {
            "rlt": [
                {
                    "sid": "undefine",
                    "istart": 33,
                    "iresid": 119,
                    "iresIndex": 2,
                    "iduration": 189,
                    "nfillerscore": 0,
                    "nkeywordscore": 142754,
                    "ncm": 1525,
                    "keyword": "ding1 dong1 ding1 dong1  "
                }
            ]
        }

* [Offical Documents](https://www.xfyun.cn/doc/mscapi/Windows&Linux/wlapi.html)