# iFLYTEK-MSC-Python-SDK
A third-party Python SDK for a iFLYTEK MSC. Using for ASR, TSS, KWS.

# Quick Start
* Install MSC SDK

    ```bash
    $ pip install git+https://github.com/jm12138/iFLYTEK-MSC-Python-SDK
    ```

* Import MSC SDK

    ```python
    import msc
    ```

* Login MSC SDK

    ```python
    # Set the APP ID
    app_id = '' 

    # Login MSC SDK
    msc.MSPLogin(
        usr=None,
        pwd=None,
        params="appid={}".format(app_id)
    )
    ```

* [Offical Documents](https://www.xfyun.cn/doc/mscapi/Windows&Linux/wlapi.html)