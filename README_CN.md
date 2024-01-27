# iFLYTEK-MSC-Python-SDK

## 简介

* 中文 | [English](./README.md)

* 一个讯飞智能语音平台 MSC 的第三方 Python SDK，支持语音唤醒、语音识别、语音合成、语音评测等功能。

## 快速开始
* 安装 MSC Python SDK

    ```bash
    $ pip install git+https://github.com/jm12138/iFLYTEK-MSC-Python-SDK
    ```

* 下载 MSC SDK

    * [SDK 下载](https://www.xfyun.cn/sdk/dispatcher)

* 语音唤醒

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

    # Set MSC SDK DLL/SO File Path
    # X86: SDK_DIR/bin/msc.dll
    # X64: SDK_DIR/bin/msc_x64.dll
    sdk_path = ''

    # Set MSC Client
    client = msc.MSC(sdk_path=sdk_path, params=f"appid={appid}".encode('UTF-8'))

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
    # SDK_DIR/bin/msc/res/ivw/wakeupresource.jet
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

* 语音识别

    ```python
    import msc
    import pyaudio

    # Audio Stream
    p = pyaudio.PyAudio()
    input_stream = p.open(
        format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048
    )

    # Set APP ID
    appid = '' 

    # Set MSC SDK DLL/SO File Path
    # X86: SDK_DIR/bin/msc.dll
    # X64: SDK_DIR/bin/msc_x64.dll
    sdk_path = ''

    # Set MSC Client
    client = msc.MSC(sdk_path=sdk_path, params=f"appid={appid}".encode('UTF-8'))

    # Set Domain
    domain = "iat"

    # Start ASR
    for item in client.asr(
        params=f"domain={domain}".encode("UTF-8"),
        stream=input_stream,
        chunk_size=2048,
    ):
        print(item.decode("UTF-8"))
    ```

        {"sn":1,"ls":false,"bg":0,"ed":0,"ws":[{"bg":64,"cw":[{"sc":0.0,"w":"今天"}]},{"bg":132,"cw":[{"sc":0.0,"w":"天气"}]},{"bg":164,"cw":[{"sc":0.0,"w":"怎么样"}]}]}
        {"sn":2,"ls":true,"bg":0,"ed":0,"ws":[{"bg":235,"cw":[{"sc":0.0,"w":"？"}]}]}

* 语音合成

    ```python
    import msc
    import pyaudio

    # Audio Stream
    p = pyaudio.PyAudio()
    output_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)

    # Set APP ID
    appid = '' 

    # Set MSC SDK DLL/SO File Path
    # X86: SDK_DIR/bin/msc.dll
    # X64: SDK_DIR/bin/msc_x64.dll
    sdk_path = ''

    # Set MSC Client
    client = msc.MSC(sdk_path=sdk_path, params=f"appid={appid}".encode('UTF-8'))

    # Set Text Encoding
    text_encoding = "UTF8"

    # Start TTS
    for item in client.tts(
        params=f"text_encoding={text_encoding}".encode("UTF-8"),
        text="你好，我是您的语音助手，有什么需要帮助的吗？".encode("UTF-8"),
    ):
        output_stream.write(item)
    ```

## 文档

* [官方文档](https://www.xfyun.cn/doc/mscapi/Windows&Linux/wlapi.html)
