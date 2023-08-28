from typing import TypedDict, Literal, Optional, Union


class MSPLoginParams(TypedDict):
    appid: str
    engine_start: Literal["ivw", "asr"]
    ivw_res_path: Optional[str]
    asr_res_path: Optional[str]


class MSPUploadDataParams(TypedDict):
    sub: Literal["uup"]
    dtt: Literal["userword", "contact"]


class QISRSessionBeginParams(TypedDict):
    engine_type: Literal["cloud", "local"]
    sub: Literal["iat", "asr"]
    language: Literal["zh_cn", "en_us"]
    sample_rate: Literal[8000, 16000]
    asr_threshold: int
    asr_denoise: Literal[0, 1]
    asr_res_path: str
    grm_build_path: str
    result_type: Literal["plain", "json"]
    text_encoding: str
    result_encoding: str
    local_grammar: int
    aue: Literal[
        "raw",
        "ico",
        "speex;0",
        "speex;1",
        "speex;2",
        "speex;3",
        "speex;4",
        "speex;5",
        "speex;6",
        "speex;7",
        "speex;8",
        "speex;9",
        "speex;10",
        "speex-wb;0",
        "speex-wb;1",
        "speex-wb;2",
        "speex-wb;3",
        "speex-wb;4",
        "speex-wb;5",
        "speex-wb;6",
        "speex-wb;7",
        "speex-wb;8",
        "speex-wb;9",
        "speex-wb;10",
    ]
    accent: Union[Literal["mandarin"], str]
    vad_enable: [0, 1]
    vad_bos: int
    vad_eos: int
    ptt: Literal[0, 1]
    dwa: Literal["wpgs"]
    nbest: Literal[1, 2, 3, 4, 5]
    wbest: Literal[1, 2, 3, 4, 5]
    rlang: Literal["zh-cn", "zh-hk"]
    domain: Literal["iat", "medical"]
    pd: Literal["game", "health", "shopping", "trip"]

