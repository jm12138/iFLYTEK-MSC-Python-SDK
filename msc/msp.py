from ctypes import _FuncPointer
from ctypes import byref, string_at
from ctypes import CFUNCTYPE, POINTER
from ctypes import c_int, c_long, c_uint, c_void_p, c_char_p

from enum import Enum

from .msc import msc

__all__ = [
    'MSPStatus',
    'MSPAssert',
    'MSPLogin',
    'MSPLogout',
    'MSPUpload',
    'MSPDownload',
    'MSPAppendData',
    'MSPGetResult',
    'MSPSetParam',
    'MSPGetParam',
    'MSPUploadData',
    'MSPDownloadData',
    'MSPSearch',
    'MSPNlpSearch',
    'MSPNlpSchCancel',
    'MSPRegisterNotify',
    'MSPGetVersion',
]


class MSPStatus(Enum):
    MSP_SUCCESS = 0,
    MSP_ERROR_FAIL = -1,
    MSP_ERROR_EXCEPTION = -2,

    """ General errors 10100(0x2774) """

    MSP_ERROR_GENERAL = 10100, 	""" 0x2774 """
    MSP_ERROR_OUT_OF_MEMORY = 10101, 	""" 0x2775 """
    MSP_ERROR_FILE_NOT_FOUND = 10102, 	""" 0x2776 """
    MSP_ERROR_NOT_SUPPORT = 10103, 	""" 0x2777 """
    MSP_ERROR_NOT_IMPLEMENT = 10104, 	""" 0x2778 """
    MSP_ERROR_ACCESS = 10105, 	""" 0x2779 """
    MSP_ERROR_INVALID_PARA = 10106, 	""" 0x277A """  """ 缺少参数 """
    MSP_ERROR_INVALID_PARA_VALUE = 10107, 	""" 0x277B """  """ 无效参数值 """
    MSP_ERROR_INVALID_HANDLE = 10108, 	""" 0x277C """
    MSP_ERROR_INVALID_DATA = 10109, 	""" 0x277D """
    MSP_ERROR_NO_LICENSE = 10110, 	""" 0x277E """  """ 引擎授权不足 """
    MSP_ERROR_NOT_INIT = 10111, 	""" 0x277F """  """ 引擎未初始化,可能是引擎崩溃 """
    MSP_ERROR_NULL_HANDLE = 10112, 	""" 0x2780 """
    MSP_ERROR_OVERFLOW = 10113, 	""" 0x2781 """  """ 单用户下模型数超上限(10个),只出现在测试时对一个用户进行并发注册 """
    MSP_ERROR_TIME_OUT = 10114, 	""" 0x2782 """  """ 超时 """
    MSP_ERROR_OPEN_FILE = 10115, 	""" 0x2783 """
    MSP_ERROR_NOT_FOUND = 10116, 	""" 0x2784 """  """ 数据库中模型不存在 """
    MSP_ERROR_NO_ENOUGH_BUFFER = 10117, 	""" 0x2785 """
    MSP_ERROR_NO_DATA = 10118, 	""" 0x2786 """  """ 从客户端读音频或从引擎段获取结果时无数据 """
    MSP_ERROR_NO_MORE_DATA = 10119, 	""" 0x2787 """
    MSP_ERROR_NO_RESPONSE_DATA = 10120, 	""" 0x2788 """
    MSP_ERROR_ALREADY_EXIST = 10121, 	""" 0x2789 """  """ 数据库中模型已存在 """
    MSP_ERROR_LOAD_MODULE = 10122, 	""" 0x278A """
    MSP_ERROR_BUSY = 10123, 	""" 0x278B """
    MSP_ERROR_INVALID_CONFIG = 10124, 	""" 0x278C """
    MSP_ERROR_VERSION_CHECK = 10125, 	""" 0x278D """
    MSP_ERROR_CANCELED = 10126, 	""" 0x278E """
    MSP_ERROR_INVALID_MEDIA_TYPE = 10127, 	""" 0x278F """
    MSP_ERROR_CONFIG_INITIALIZE = 10128, 	""" 0x2790 """
    MSP_ERROR_CREATE_HANDLE = 10129, 	""" 0x2791 """
    MSP_ERROR_CODING_LIB_NOT_LOAD = 10130, 	""" 0x2792 """
    MSP_ERROR_USER_CANCELLED = 10131, 	""" 0x2793 """
    MSP_ERROR_INVALID_OPERATION = 10132, 	""" 0x2794 """
    MSP_ERROR_MESSAGE_NOT_COMPLETE = 10133,	""" 0x2795 """   """ flash """
    MSP_ERROR_NO_EID = 10134,	""" 0x2795 """
    MSP_ERROE_OVER_REQ = 10135,    """ 0x2797 """   """ client Redundancy request """
    MSP_ERROR_USER_ACTIVE_ABORT = 10136,    """ 0x2798 """   """ user abort """
    MSP_ERROR_BUSY_GRMBUILDING = 10137,    """ 0x2799 """
    MSP_ERROR_BUSY_LEXUPDATING = 10138,    """ 0x279A """
    MSP_ERROR_SESSION_RESET = 10139,    """ 0x279B """   """ msc主动终止会话,准备重传 """
    MSP_ERROR_BOS_TIMEOUT = 10140,    """ 0x279C """   """ VAD前端点超时 """
    MSP_ERROR_STREAM_FILTER = 10141,	""" 0X279D """   """ AIUI当前Stream被过滤 """
    MSP_ERROR_STREAM_CLEAR = 10142,    """ 0X279E """   """ AIUI当前Stream被清理 """

    """ Error codes of network 10200(0x27D8)"""
    MSP_ERROR_NET_GENERAL = 10200, 	""" 0x27D8 """
    MSP_ERROR_NET_OPENSOCK = 10201, 	""" 0x27D9 """   """ Open socket """
    MSP_ERROR_NET_CONNECTSOCK = 10202, 	""" 0x27DA """   """ Connect socket """
    MSP_ERROR_NET_ACCEPTSOCK = 10203, 	""" 0x27DB """   """ Accept socket """
    MSP_ERROR_NET_SENDSOCK = 10204, 	""" 0x27DC """   """ Send socket data """
    MSP_ERROR_NET_RECVSOCK = 10205, 	""" 0x27DD """   """ Recv socket data """
    MSP_ERROR_NET_INVALIDSOCK = 10206, 	""" 0x27DE """   """ Invalid socket handle """
    MSP_ERROR_NET_BADADDRESS = 10207, 	""" 0x27EF """   """ Bad network address """
    MSP_ERROR_NET_BINDSEQUENCE = 10208, 	""" 0x27E0 """   """ Bind after listen/connect """
    MSP_ERROR_NET_NOTOPENSOCK = 10209, 	""" 0x27E1 """   """ Socket is not opened """
    MSP_ERROR_NET_NOTBIND = 10210, 	""" 0x27E2 """   """ Socket is not bind to an address """
    MSP_ERROR_NET_NOTLISTEN = 10211, 	""" 0x27E3 """   """ Socket is not listening """
    MSP_ERROR_NET_CONNECTCLOSE = 10212, 	""" 0x27E4 """   """ The other side of connection is closed """
    MSP_ERROR_NET_NOTDGRAMSOCK = 10213, 	""" 0x27E5 """   """ The socket is not datagram type """
    MSP_ERROR_NET_DNS = 10214, 	""" 0x27E6 """   """ domain name is invalid or dns server does not function well """
    MSP_ERROR_NET_INIT = 10215, 	""" 0x27E7 """   """ ssl ctx create failed """

    """nfl error"""
    MSP_ERROR_NFL_INNER_ERROR = 10216,    """ NFL inner error """
    MSP_ERROR_MSS_TIME_OUT = 10217,    """ MSS TIMEOUT """
    MSP_ERROT_CLIENT_TIME_OUT = 10218,    """ CLIENT TIMEOUT """
    MSP_ERROR_CLIENT_CLOSE = 10219,    """ CLIENT CLOSED CONNECTION """

    MSP_ERROR_CLIENT_AREA_CHANGE = 10220,
    MSP_ERROR_NET_SSL_HANDSHAKE = 10221,
    MSP_ERROR_NET_INVALID_ROOT_CERT = 10222,
    MSP_ERROR_NET_INVALID_CLIENT_CERT = 10223,
    MSP_ERROR_NET_INVALID_SERVER_CERT = 10224,
    MSP_ERROR_NET_INVALID_KEY = 10225,
    MSP_ERROR_NET_CERT_VERIFY_FAILED = 10226,
    MSP_ERROR_NET_WOULDBLOCK = 10227,
    MSP_ERROR_NET_NOTBLOCK = 10228,

    """ Error codes of mssp message 10300(0x283C) """
    MSP_ERROR_MSG_GENERAL = 10300, 	""" 0x283C """
    MSP_ERROR_MSG_PARSE_ERROR = 10301, 	""" 0x283D """
    MSP_ERROR_MSG_BUILD_ERROR = 10302, 	""" 0x283E """
    MSP_ERROR_MSG_PARAM_ERROR = 10303, 	""" 0x283F """
    MSP_ERROR_MSG_CONTENT_EMPTY = 10304, 	""" 0x2840 """
    MSP_ERROR_MSG_INVALID_CONTENT_TYPE = 10305, 	""" 0x2841 """
    MSP_ERROR_MSG_INVALID_CONTENT_LENGTH = 10306, 	""" 0x2842 """
    MSP_ERROR_MSG_INVALID_CONTENT_ENCODE = 10307, 	""" 0x2843 """
    MSP_ERROR_MSG_INVALID_KEY = 10308, 	""" 0x2844 """
    MSP_ERROR_MSG_KEY_EMPTY = 10309, 	""" 0x2845 """
    MSP_ERROR_MSG_SESSION_ID_EMPTY = 10310, 	""" 0x2846 """   """ 会话ID为空 """
    MSP_ERROR_MSG_LOGIN_ID_EMPTY = 10311, 	""" 0x2847 """   """ 音频序列ID为空 """
    MSP_ERROR_MSG_SYNC_ID_EMPTY = 10312, 	""" 0x2848 """
    MSP_ERROR_MSG_APP_ID_EMPTY = 10313, 	""" 0x2849 """
    MSP_ERROR_MSG_EXTERN_ID_EMPTY = 10314, 	""" 0x284A """
    MSP_ERROR_MSG_INVALID_CMD = 10315, 	""" 0x284B """
    MSP_ERROR_MSG_INVALID_SUBJECT = 10316, 	""" 0x284C """
    MSP_ERROR_MSG_INVALID_VERSION = 10317, 	""" 0x284D """
    MSP_ERROR_MSG_NO_CMD = 10318, 	""" 0x284E """
    MSP_ERROR_MSG_NO_SUBJECT = 10319, 	""" 0x284F """
    MSP_ERROR_MSG_NO_VERSION = 10320, 	""" 0x2850 """
    MSP_ERROR_MSG_MSSP_EMPTY = 10321, 	""" 0x2851 """
    MSP_ERROR_MSG_NEW_RESPONSE = 10322, 	""" 0x2852 """
    MSP_ERROR_MSG_NEW_CONTENT = 10323, 	""" 0x2853 """
    MSP_ERROR_MSG_INVALID_SESSION_ID = 10324, 	""" 0x2854 """   """ 无效的会话ID(sid) """
    MSP_ERROR_MSG_INVALID_CONTENT = 10325, 	""" 0x2855 """

    """ Error codes of DataBase 10400(0x28A0)"""
    MSP_ERROR_DB_GENERAL = 10400, 	""" 0x28A0 """   """ 数据库异常 """
    MSP_ERROR_DB_EXCEPTION = 10401, 	""" 0x28A1 """
    MSP_ERROR_DB_NO_RESULT = 10402, 	""" 0x28A2 """   """ redis中没有找到会话ID(sid) """
    MSP_ERROR_DB_INVALID_USER = 10403, 	""" 0x28A3 """
    MSP_ERROR_DB_INVALID_PWD = 10404, 	""" 0x28A4 """
    MSP_ERROR_DB_CONNECT = 10405, 	""" 0x28A5 """
    MSP_ERROR_DB_INVALID_SQL = 10406, 	""" 0x28A6 """
    MSP_ERROR_DB_INVALID_APPID = 10407,	""" 0x28A7 """
    MSP_ERROR_DB_NO_UID = 10408,

    """ Error codes of Resource 10500(0x2904)"""
    MSP_ERROR_RES_GENERAL = 10500, 	""" 0x2904 """
    MSP_ERROR_RES_LOAD = 10501, 	""" 0x2905 """   """ Load resource """
    MSP_ERROR_RES_FREE = 10502, 	""" 0x2906 """   """ Free resource """
    MSP_ERROR_RES_MISSING = 10503, 	""" 0x2907 """   """ Resource File Missing """
    MSP_ERROR_RES_INVALID_NAME = 10504, 	""" 0x2908 """   """ Invalid resource file name """
    MSP_ERROR_RES_INVALID_ID = 10505, 	""" 0x2909 """   """ Invalid resource ID """
    MSP_ERROR_RES_INVALID_IMG = 10506, 	""" 0x290A """   """ Invalid resource image pointer """
    MSP_ERROR_RES_WRITE = 10507, 	""" 0x290B """   """ Write read-only resource """
    MSP_ERROR_RES_LEAK = 10508, 	""" 0x290C """   """ Resource leak out """
    MSP_ERROR_RES_HEAD = 10509, 	""" 0x290D """   """ Resource head currupt """
    MSP_ERROR_RES_DATA = 10510, 	""" 0x290E """   """ Resource data currupt """
    MSP_ERROR_RES_SKIP = 10511, 	""" 0x290F """   """ Resource file skipped """

    """ Error codes of TTS 10600(0x2968)"""
    MSP_ERROR_TTS_GENERAL = 10600, 	""" 0x2968 """
    MSP_ERROR_TTS_TEXTEND = 10601, 	""" 0x2969 """  """ Meet text end """
    MSP_ERROR_TTS_TEXT_EMPTY = 10602, 	""" 0x296A """  """ no synth text """
    MSP_ERROR_TTS_LTTS_ERROR = 10603, 	""" 0x296B """

    """ Error codes of Recognizer 10700(0x29CC) """
    MSP_ERROR_REC_GENERAL = 10700, 	""" 0x29CC """  """ 引擎异常 """
    MSP_ERROR_REC_INACTIVE = 10701, 	""" 0x29CD """
    MSP_ERROR_REC_GRAMMAR_ERROR = 10702, 	""" 0x29CE """
    MSP_ERROR_REC_NO_ACTIVE_GRAMMARS = 10703, 	""" 0x29CF """
    MSP_ERROR_REC_DUPLICATE_GRAMMAR = 10704, 	""" 0x29D0 """
    MSP_ERROR_REC_INVALID_MEDIA_TYPE = 10705, 	""" 0x29D1 """
    MSP_ERROR_REC_INVALID_LANGUAGE = 10706, 	""" 0x29D2 """
    MSP_ERROR_REC_URI_NOT_FOUND = 10707, 	""" 0x29D3 """
    MSP_ERROR_REC_URI_TIMEOUT = 10708, 	""" 0x29D4 """
    MSP_ERROR_REC_URI_FETCH_ERROR = 10709, 	""" 0x29D5 """
    MSP_ERROR_REC_PROC_MOD = 10710,	""" 0x29D6 """

    """ Error codes of Speech Detector 10800(0x2A30) """
    MSP_ERROR_EP_GENERAL = 10800, 	""" 0x2A30 """
    MSP_ERROR_EP_NO_SESSION_NAME = 10801, 	""" 0x2A31 """
    MSP_ERROR_EP_INACTIVE = 10802, 	""" 0x2A32 """
    MSP_ERROR_EP_INITIALIZED = 10803, 	""" 0x2A33 """

    """ Error codes of TUV """
    MSP_ERROR_TUV_GENERAL = 10900, 	""" 0x2A94 """
    MSP_ERROR_TUV_GETHIDPARAM = 10901, 	""" 0x2A95 """   """ Get Busin Param huanid"""
    MSP_ERROR_TUV_TOKEN = 10902, 	""" 0x2A96 """   """ Get Token """
    MSP_ERROR_TUV_CFGFILE = 10903, 	""" 0x2A97 """   """ Open cfg file """
    MSP_ERROR_TUV_RECV_CONTENT = 10904, 	""" 0x2A98 """   """ received content is error """
    MSP_ERROR_TUV_VERFAIL = 10905, 	""" 0x2A99 """   """ Verify failure """

    """ Error codes of IMTV """
    MSP_ERROR_LOGIN_SUCCESS = 11000, 	""" 0x2AF8 """   """ 成功 """
    MSP_ERROR_LOGIN_NO_LICENSE = 11001, 	""" 0x2AF9 """   """ 试用次数结束,用户需要付费 """
    MSP_ERROR_LOGIN_SESSIONID_INVALID = 11002, 	""" 0x2AFA """   """ SessionId失效,需要重新登录通行证 """
    MSP_ERROR_LOGIN_SESSIONID_ERROR = 11003, 	""" 0x2AFB """   """ SessionId为空,或者非法 """
    MSP_ERROR_LOGIN_UNLOGIN = 11004, 	""" 0x2AFC """   """ 未登录通行证 """
    MSP_ERROR_LOGIN_INVALID_USER = 11005, 	""" 0x2AFD """   """ 用户ID无效 """
    MSP_ERROR_LOGIN_INVALID_PWD = 11006, 	""" 0x2AFE """   """ 用户密码无效 """
    MSP_ERROR_LOGIN_SYSTEM_ERROR = 11099, 	""" 0x2B5B """   """ 系统错误 """

    """ Error codes of HCR """
    MSP_ERROR_HCR_GENERAL = 11100,
    MSP_ERROR_HCR_RESOURCE_NOT_EXIST = 11101,
    MSP_ERROR_HCR_CREATE = 11102,
    MSP_ERROR_HCR_DESTROY = 11103,
    MSP_ERROR_HCR_START = 11104,
    MSP_ERROR_HCR_APPEND_STROKES = 11105,
    MSP_ERROR_HCR_INIT = 11106,
    MSP_ERROR_HCR_POINT_DECODE = 11107,
    MSP_ERROR_HCR_DISPATCH = 11108,
    MSP_ERROR_HCR_GETRESULT = 11109,
    MSP_ERROR_HCR_RESOURCE = 11110,

    """ Error Codes using in local engine """
    MSP_ERROR_AUTH_NO_LICENSE = 11200,	""" 0x2BC0 """   """ 无授权 """
    MSP_ERROR_AUTH_NO_ENOUGH_LICENSE = 11201,	""" 0x2BC1 """   """ 授权不足 """
    MSP_ERROR_AUTH_INVALID_LICENSE = 11202,	""" 0x2BC2 """   """ 无效的授权 """
    MSP_ERROR_AUTH_LICENSE_EXPIRED = 11203,	""" 0x2BC3 """   """ 授权过期 """
    MSP_ERROR_AUTH_NEED_MORE_DATA = 11204,    """ 0x2BC4 """   """ 无设备信息 """
    MSP_ERROR_AUTH_LICENSE_TO_BE_EXPIRED = 11205,	""" 0x2BC5 """   """ 授权即将过期,警告性错误码 """
    MSP_ERROR_AUTH_INVALID_MACHINE_ID = 11206,    """ 0x2BC6 """   """ 无效的机器码 """
    MSP_ERROR_AUTH_LOCAL_ASR_FORBIDDEN = 11207,    """ 0x2BC7 """   """ 禁止使用本地识别引擎 """
    MSP_ERROR_AUTH_LOCAL_TTS_FORBIDDEN = 11208,    """ 0x2BC8 """   """ 禁止使用本地合成引擎 """
    MSP_ERROR_AUTH_LOCAL_IVW_FORBIDDEN = 11209,    """ 0x2BC9 """   """ 禁止使用本地唤醒引擎 """
    MSP_ERROR_AUTH_APPID_NOT_MATCH = 11210,	""" 0x2BCA """   """ 资源appid和应用appid不匹配 """
    MSP_ERROR_AUTH_UID_NOT_MATCH = 11211,	""" 0x2BCB """   """ 资源uid和登录用户uid不匹配 """
    MSP_ERROR_AUTH_TRIAL_EXPIRED = 11212,	""" 0x2BCC """   """ 试用资源过期 """
    MSP_ERROR_AUTH_LOCAL_IFD_FORBIDDEN = 11213,    """ 0x2BC9 """   """ 禁止使用本地人脸引擎 """

    MSP_ERROR_AIUI_NO_ENOUGH_LICENSE = 11216,	""" 0x2BD0 """   """ AIUI授权不足 """
    """Error Codes of Authorization"""
    MSP_ERROR_AUTH_DVC_NO_LICENSE = 11300,
    MSP_ERROR_AUTH_DVC_NO_ENOUGH_LICENSE = 11301,
    MSP_ERROR_AUTH_DVC_INVALID_LICENSE = 11302,
    MSP_ERROR_AUTH_DVC_LICENSE_EXPIRED = 11303,
    MSP_ERROR_AUTH_DVC_NEED_MORE_DATA = 11304,
    MSP_ERROR_AUTH_DVC_LICENSE_TO_BE_EXPIRED = 11305,
    MSP_ERROR_AUTH_DVC_EXCEED_LICENSE = 11306,

    """ Error codes of Ise """

    MSP_ERROR_ASE_EXCEP_SILENCE = 11401,
    MSP_ERROR_ASE_EXCEP_SNRATIO = 11402,
    MSP_ERROR_ASE_EXCEP_PAPERDATA = 11403,
    MSP_ERROR_ASE_EXCEP_PAPERCONTENTS = 11404,
    MSP_ERROR_ASE_EXCEP_NOTMONO = 11405,
    MSP_ERROR_ASE_EXCEP_OTHERS = 11406,
    MSP_ERROR_ASE_EXCEP_PAPERFMT = 11407,
    MSP_ERROR_ASE_EXCEP_ULISTWORD = 11408,

    """ Error codes of Iot """
    MSP_ERROR_IOT_BASE = 11500,
    MSP_ERROR_IOT_PARAM_ERROR = 11501,		# param error
    MSP_ERROR_IOT_INVALID_SERVICE = 11502,		# invalid service for iot ProTranServer
    MSP_ERROR_IOT_INVALID_PRODUCTID = 11503,		# invalid productid for ProTranServer
    # invalid attr value for one product in ProTranServer
    MSP_EEROR_IOT_INVALID_ATTR = 11504,
    MSP_ERROR_IOT_INVALID_PLATFORM = 11505,		# invalid platform for ProTranServer
    MSP_ERROR_IOT_DID_NOT_FOUND = 11506,		# not found device id in semantic

    """ Error codes of IVP """
    MSP_ERROR_IVP_GENERAL = 11600,  # 内核异常
    MSP_ERROR_IVP_EXTRA_RGN_SOPPORT = 11601,  # 注册时向引擎所写音频条数超过上限(9次)
    MSP_ERROR_IVP_TRUNCATED = 11602,  # 音频截幅(因信号波形的幅度太大,而超出系统的线性范围),如记录尖叫声的音频
    MSP_ERROR_IVP_MUCH_NOISE = 11603,  # 音频信噪比过低
    MSP_ERROR_IVP_TOO_LOW = 11604,  # 音频能量过低
    MSP_ERROR_IVP_ZERO_AUDIO = 11605,  # 无音频
    MSP_ERROR_IVP_UTTER_TOO_SHORT = 11606,  # 音频太短
    MSP_ERROR_IVP_TEXT_NOT_MATCH = 11607,  # 1.音频和文本不匹配,常见原因1.抢读(在按下录音键之前读)
    #  2.录音机的启动电流被录入表现在音频上是在音频首有冲击电流 3.确实不匹配"
    MSP_ERROR_IVP_NO_ENOUGH_AUDIO = 11608,  # 音频不够,注册自由说,而写入的音频又不够长时会报,告诉调用者继续传音频
    MSP_ERROR_IVP_MODEL_NOT_FOUND_IN_HBASE = 11610,  # 模型在hbase中没找到

    """ Error codes of Face """

    MSP_ERROR_IFR_NOT_FACE_IMAGE = 11700,  # 【无人脸,对应的引擎错误码是20200 】
    MSP_ERROR_FACE_IMAGE_FULL_LEFT = 11701,  # 【人脸向左,对应的引擎错误码是20201】
    MSP_ERROR_FACE_IMAGE_FULL_RIGHT = 11702,  # 【人脸向右,对应的引擎错误码是20202】
    MSP_ERROR_IMAGE_CLOCKWISE_WHIRL = 11703,  # 【顺时针旋转,对应的引擎错误码是20203】
    MSP_ERROR_IMAGE_COUNTET_CLOCKWISE_WHIRL = 11704,  # 【逆时针旋转,对应的引擎错误码是20204】
    MSP_ERROR_VALID_IMAGE_SIZE = 11705,  # 【图片大小异常 ,对应的引擎错误码是20205】
    MSP_ERROR_ILLUMINATION = 11706,  # 【光照异常,对应的引擎错误码是20206】
    MSP_ERROR_FACE_OCCULTATION = 11707,  # 【人脸被遮挡,对应的引擎错误码是20207】
    MSP_ERROR_FACE_INVALID_MODEL = 11708,  # 【非法模型数据,对应的引擎错误码是20208】
    MSP_ERROR_FUSION_INVALID_INPUT_TYPE = 11709,  # 【输入数据类型非法,对应的引擎错误码是20300】
    MSP_ERROR_FUSION_NO_ENOUGH_DATA = 11710,  # 【输入的数据不完整,对应的引擎错误码是20301】
    MSP_ERROR_FUSION_ENOUGH_DATA = 11711,  # 【输入的数据过多,对应的引擎错误码是20302】

    """Error Codes of AIUI"""
    MSP_ERROR_AIUI_CID_EXPIRED = 11800,

    """Error Codes of Encoder"""
    MSP_ERROR_ICT_ENCODER = 11900,

    """ Error codes of http 12000(0x2EE0) """
    MSP_ERROR_HTTP_BASE = 12000,	""" 0x2EE0 """
    MSP_ERROR_HTTP_400 = 12400,
    MSP_ERROR_HTTP_401 = 12401,
    MSP_ERROR_HTTP_402 = 12402,
    MSP_ERROR_HTTP_403 = 12403,
    MSP_ERROR_HTTP_404 = 12404,
    MSP_ERROR_HTTP_405 = 12405,
    MSP_ERROR_HTTP_406 = 12406,
    MSP_ERROR_HTTP_407 = 12407,
    MSP_ERROR_HTTP_408 = 12408,
    MSP_ERROR_HTTP_409 = 12409,
    MSP_ERROR_HTTP_410 = 12410,
    MSP_ERROR_HTTP_411 = 12411,
    MSP_ERROR_HTTP_412 = 12412,
    MSP_ERROR_HTTP_413 = 12413,
    MSP_ERROR_HTTP_414 = 12414,
    MSP_ERROR_HTTP_415 = 12415,
    MSP_ERROR_HTTP_416 = 12416,
    MSP_ERROR_HTTP_417 = 12417,
    MSP_ERROR_HTTP_500 = 12500,
    MSP_ERROR_HTTP_501 = 12501,
    MSP_ERROR_HTTP_502 = 12502,
    MSP_ERROR_HTTP_503 = 12503,
    MSP_ERROR_HTTP_504 = 12504,
    MSP_ERROR_HTTP_505 = 12505,
    """Error codes of ISV """
    MSP_ERROR_ISV_NO_USER = 13000,	""" 32C8 """    """ the user doesn't exist """

    """ Error codes of Lua scripts """
    MSP_ERROR_LUA_BASE = 14000,    """ 0x36B0 """
    MSP_ERROR_LUA_YIELD = 14001,	""" 0x36B1 """
    MSP_ERROR_LUA_ERRRUN = 14002,	""" 0x36B2 """
    MSP_ERROR_LUA_ERRSYNTAX = 14003,	""" 0x36B3 """
    MSP_ERROR_LUA_ERRMEM = 14004,	""" 0x36B4 """
    MSP_ERROR_LUA_ERRERR = 14005,	""" 0x36B5 """
    MSP_ERROR_LUA_INVALID_PARAM = 14006,	""" 0x36B6 """

    """ Error codes of MMP """
    MSP_ERROR_MMP_BASE = 15000,    """ 0x3A98 """
    MSP_ERROR_MMP_MYSQL_INITFAIL = 15001,	""" 0x3A99 """
    MSP_ERROR_MMP_REDIS_INITFAIL = 15002,	""" 0x3A9A """
    MSP_ERROR_MMP_NETDSS_INITFAIL = 15003,	""" 0x3A9B """
    MSP_ERROR_MMP_TAIR_INITFAIL = 15004,	""" 0x3A9C """
    MSP_ERROR_MMP_MAIL_SESSION_FAIL = 15006,	""" 0x3A9E """	""" 邮件登陆服务器时,会话错误。"""
    MSP_ERROR_MMP_MAIL_LOGON_FAIL = 15007,	""" 0x3A9F """	""" 邮件登陆服务器时,拒绝登陆。"""
    MSP_ERROR_MMP_MAIL_USER_ILLEGAL = 15008,	""" 0x3AA0 """	""" 邮件登陆服务器时,用户名非法。"""
    MSP_ERROR_MMP_MAIL_PWD_ERR = 15009,	""" 0x3AA1 """	""" 邮件登陆服务器时,密码错误。"""
    MSP_ERROR_MMP_MAIL_SOCKET_ERR = 15010,	""" 0x3AA2 """	""" 邮件发送过程中套接字错误"""
    MSP_ERROR_MMP_MAIL_INIT_FAIL = 15011,	""" 0x3AA3 """	""" 邮件初始化错误"""
    MSP_ERROR_MMP_STORE_MNR_NO_INIT = 15012,	""" 0x3AA4 """	""" store_manager未初始化,或初始化失败"""
    MSP_ERROR_MMP_STORE_MNR_POOL_FULL = 15013,	""" 0x3AA5 """	""" store_manager的连接池满了"""
    MSP_ERROR_MMP_STRATGY_PARAM_ILLEGAL = 15014,	""" 0x3AA6 """	""" 报警策略表达式非法"""
    MSP_ERROR_MMP_STRATGY_PARAM_TOOLOOG = 15015,	""" 0x3AA7 """	""" 报警策略表达式太长"""
    MSP_ERROR_MMP_PARAM_NULL = 15016,	""" 0x3AA8 """	""" 函数参数为空"""
    MSP_ERROR_MMP_ERR_MORE_TOTAL = 15017,	""" 0x3AA9 """	""" pms插入数据库中错误汇总表的数据,错误次数 > 总次数。"""
    MSP_ERROR_MMP_PROC_THRESHOLD = 15018,	""" 0x3AAA """	""" 进程监控阀值设置错误"""
    MSP_ERROR_MMP_SERVER_THRESHOLD = 15019,	""" 0x3AAB """	""" 服务器监控阀值设置错误"""
    MSP_ERROR_MMP_PYTHON_NO_EXIST = 15020,    """ 0x3AAC """	""" python脚本文件不存在 """
    MSP_ERROR_MMP_PYTHON_IMPORT_FAILED = 15021,	""" 0x3AAD """	""" python脚本导入出错 """
    MSP_ERROR_MMP_PYTHON_BAD_FUNC = 15022,	""" 0x3AAE """	""" python脚本函数格式错误 """
    MSP_ERROR_MMP_DB_DATA_ILLEGAL = 15023,	""" 0x3AAF """	""" 插入数据库中的数据格式有误 """
    MSP_ERROR_MMP_REDIS_NOT_CONN = 15024,	""" 0x3AB0 """	""" redis没有连接到服务端 """
    MSP_ERROR_MMP_PMA_NOT_FOUND_STRATEGY = 15025,	""" 0x3AB1 """	""" 没有找到报警策略 """
    MSP_ERROR_MMP_TAIR_CONNECT = 15026,	""" 0x3AB2 """	""" 连接tair集群失败 """
    MSP_ERROR_MMP_PMC_SERVINFO_INVALID = 15027,	""" Ox3AB3 """	""" 此pmc的服务器信息已经无效 """
    MSP_ERROR_MMP_ALARM_GROUP_NULL = 15028,	""" Ox3AB4 """	""" 服务器报警的短信报警组与邮件报警组均为空 """
    MSP_ERROR_MMP_ALARM_CONTXT_NULL = 15029,	""" Ox3AB5 """	""" 服务器报警的报警内容为空 """

    """ Error codes of MSC(lmod loader) """
    MSP_ERROR_LMOD_BASE = 16000,	""" 0x3E80 """
    MSP_ERROR_LMOD_NOT_FOUND = 16001,	""" 0x3E81 """	""" 没找到lmod文件 """
    MSP_ERROR_LMOD_UNEXPECTED_BIN = 16002,	""" 0x3E82 """	""" 无效的lmod """
    MSP_ERROR_LMOD_LOADCODE = 16003,	""" 0x3E83 """	""" 加载lmod指令失败 """
    MSP_ERROR_LMOD_PRECALL = 16004,	""" 0x3E84 """	""" 初始化lmod失败 """
    MSP_ERROR_LMOD_RUNTIME_EXCEPTION = 16005,	""" 0x3E85 """	""" lmod运行时异常 """
    MSP_ERROR_LMOD_ALREADY_LOADED = 16006,	""" 0x3E86 """	""" lmod重复加载 """

    # Error code of Third Business
    MSP_ERROR_BIZ_BASE = 17000,	""" 0x4268 """	""" 三方业务错误码 """

    # Error of Nginx errlog file increase exception
    MSP_ERROR_NGX_LOG_MORE_TOTEL_SIZE = 18000,				    """nginx错误日志大小异常"""

    # Error of Flash client when network checking
    MSP_ERROR_FLASH_NETWORK_CONNECT_FIALED = 19000,					"""flash服务端网络连接失败"""
    MSP_ERROR_FLASH_NETWORK_CHECK_FIALED = 19001,					"""flash服务端响应了异常消息"""
    MSP_ERROR_FLASH_NETWORK_CHECK_TIMEOUT = 19002,				    """flash服务端网络超时"""
    MSP_ERROR_FLASH_NETWORK_CLOSED_EXCEPTION = 19003,                   """flash服务端网络异常关闭"""

    """Error Code Of Speech plus"""

    SPEECH_ERROR_NO_NETWORK = 20001, """ 无有效的网络连接"""
    SPEECH_ERROR_NETWORK_TIMEOUT = 20002, """ 网络连接超时"""
    SPEECH_ERROR_NET_EXPECTION = 20003, """ 网络异常"""
    SPEECH_ERROR_INVALID_RESULT = 20004, """ 无有效的结果"""
    SPEECH_ERROR_NO_MATCH = 20005, """ 无匹配结果 """
    SPEECH_ERROR_AUDIO_RECORD = 20006, """ 录音失败 """
    SPEECH_ERROR_NO_SPPECH = 20007, """ 未检测到语音"""

    SPEECH_ERROR_SPEECH_TIMEOUT = 20008, """ 音频输入超时"""
    SPEECH_ERROR_EMPTY_UTTERANCE = 20009, """ 无效的文本输入 """
    SPEECH_ERROR_FILE_ACCESS = 20010, """ 文件读写失败 """
    SPEECH_ERROR_PLAY_MEDIA = 20011, """ 音频播放失败 """

    SPEECH_ERROR_INVALID_PARAM = 20012, """ 无效的参数"""
    SPEECH_ERROR_TEXT_OVERFLOW = 20013, """ 文本溢出 """
    SPEECH_ERROR_INVALID_DATA = 20014, """ 无效数据 """
    SPEECH_ERROR_LOGIN = 20015, """ 用户未登陆"""
    SPEECH_ERROR_PERMISSION_DENIED = 20016, """ 无效授权 """
    SPEECH_ERROR_INTERRUPT = 20017, """ 被异常打断 """

    SPEECH_ERROR_VERSION_LOWER = 20018, """ 版本过低 """
    SPEECH_CLIENT_ERROR_ISUSING = 20019, """ 录音机被占用(iOS平台) """
    SPEECH_ERROR_SYSTEM_PREINSTALL = 20020, """ 系统预置版本 """
    SPEECH_ERROR_UNSATISFIED_LINK = 20021, """ 未实现的Native函数引用 """
    SPEECH_ERROR_UNKNOWN = 20999, """ 未知错误 """

    SPEECH_ERROR_COMPONENT_NOT_INSTALLED = 21001, """ 没有安装语音组件 """
    SPEECH_ERROR_ENGINE_NOT_SUPPORTED = 21002, """ 引擎不支持 """
    SPEECH_ERROR_ENGINE_INIT_FAIL = 21003, """ 初始化失败 """
    SPEECH_ERROR_ENGINE_CALL_FAIL = 21004, """ 调用失败 """
    SPEECH_ERROR_ENGINE_BUSY = 21005, """ 引擎繁忙 """

    SPEECH_ERROR_LOCAL_NO_INIT = 22001, """ 本地引擎未初始化 """
    SPEECH_ERROR_LOCAL_RESOURCE = 22002, """ 本地引擎无资源 """
    SPEECH_ERROR_LOCAL_ENGINE = 22003, """ 本地引擎内部错误 """
    SPEECH_ERROR_IVW_INTERRUPT = 22004, """ 本地唤醒引擎被异常打断 """

    """Error Code Of Local iflytek Engines"""

    """Error Code Of AiTalk"""

    """Error Code Of AiTalk Operation"""
    SPEECH_SUCCESS = 0,  # ivErr_OK                  = 0 """成功状态"""

    SPEECH_ERROR_ASR_CLIENT = 23000, """客户端应用程序错误"""  # ?????????
    SPEECH_ERROR_ASR_INVALID_PARA = 23001, """无效的参数"""
    SPEECH_ERROR_ASR_INVALID_PARA_VALUE = 23002, """无效的参数值"""
    SPEECH_ERROR_ASR_OUT_OF_MEMORY = 23003, """内存耗尽"""
    SPEECH_ERROR_ASR_CREATE_HANDLE_FAILED = 23004, """创建句柄失败"""
    SPEECH_ERROR_ASR_ENGINE_INIT_FAILED = 23005, """引擎初始化失败"""
    SPEECH_ERROR_ASR_ENGINE_STARTED = 23006, """引擎已经启动"""
    SPEECH_ERROR_ASR_ENGINE_UNINIT = 23007, """引擎未初始化"""
    SPEECH_ERROR_ASR_SPEECH_TIMEOUT = 23008, """识别超时(VAD没开启或没有检测到后端点)"""
    SPEECH_ERROR_ASR_NO_RECOGNIZED_RESULT = 23009, """无识别结果"""
    SPEECH_ERROR_ASR_INVALID_HANDLE = 23010, """无效的句柄"""
    SPEECH_ERROR_ASR_FILE_ACCESS = 23011, """打开文件失败"""

    """Error Code Of AiTalk Engine"""
    SPEECH_ERROR_AITALK_FALSE = 23100,  # ivErr_FALSE               = 1

    """ For license check """
    SPEECH_ERROR_AITALK_PERMISSION_DENIED = 23101,  # ivErr_InvSN               = 2

    """ General """
    SPEECH_ERROR_AITALK_INVALID_PARA = 23102,  # ivErr_InvArg              = 3
    SPEECH_ERROR_AITALK_BUFFER_OVERFLOW = 23103,  # ivErr_BufferFull          = 4  """音频数据缓冲区已满"""
    SPEECH_ERROR_AITALK_FAILED = 23104,  # ivErr_Failed              = 5
    SPEECH_ERROR_AITALK_NOT_SUPPORTED = 23105,  # ivErr_NotSupport          = 6  """引擎不支持"""
    SPEECH_ERROR_AITALK_OUT_OF_MEMORY = 23106,  # ivErr_OutOfMemory         = 7
    SPEECH_ERROR_AITALK_INVALID_RESOURCE = 23107,  # ivErr_InvResource         = 8  """资源无效"""
    SPEECH_ERROR_AITALK_NOT_FOUND = 23108,  # ivErr_NotFound            = 9  """打开文件失败"""
    SPEECH_ERROR_AITALK_INVALID_GRAMMAR = 23109,  # ivErr_InvGrmr             = 10 """识别语法错误"""

    """ For object status """
    SPEECH_ERROR_AITALK_INVALID_CALL = 23110,  # ivErr_InvCall             = 11 """无效调用"""

    """ For ASR Input """
    SPEECH_ERROR_AITALK_SYNTAX_ERROR = 23111,  # ivErr_InvCall             = 12

    """ For Message Call Back """
    SPEECH_ERROR_AITALK_RESET = 23112,  # ivErr_Reset               = 13
    SPEECH_ERROR_AITALK_ENDED = 23113,  # ivErr_Ended               = 14
    SPEECH_ERROR_AITALK_IDLE = 23114,  # ivErr_Idle                = 15
    SPEECH_ERROR_AITALK_CANNOT_SAVE_FILE = 23115,  # ivErr_CanNotSaveFile      = 16

    """ For Lexicon name """
    SPEECH_ERROR_AITALK_INVALID_GRAMMAR_NAME = 23116,  # ivErr_InvName             = 17 """文法或词典名称非法"""

    SPEECH_ERROR_AITALK_BUFFER_EMPTY = 23117,  # ivErr_BufferEmpty         = 18

    SPEECH_ERROR_AITALK_GET_RESULT = 23118,  # ivErr_GetResult           = 19

    SPEECH_ERROR_AITALK_REACT_OUT_TIME = 23119,  # ivErr_ReactOutTime        = 20 """反应超时"""
    SPEECH_ERROR_AITALK_SPEECH_OUT_TIME = 23120,  # ivErr_SpeechOutTime       = 21 """语音超时"""

    SPEECH_ERROR_AITALK_AUDIO_CUT = 23121,  # ivErr_CUT                 = 22 """录音质量过高"""
    SPEECH_ERROR_AITALK_AUDIO_LOWER = 23122,  # ivErr_LOWER               = 23 """录音质量过低"""

    SPEECH_ERROR_AITALK_INSUFFICIENT_PERMISSIONS = 23123,  # ivErr_Limitted            = 24 """授权不够"""
    SPEECH_ERROR_AITALK_RESULT_ERROR = 23124,  # ivErr_ResultError         = 25 """解码器Wfst输出后,依然有cmd输出"""
    SPEECH_ERROR_AITALK_SHORT_PAUSE = 23125,  # ivErr_ShortPause          = 26
    SPEECH_ERROR_AITALK_BUSY = 23126,  # ivErr_Busy                = 27
    SPEECH_ERROR_AITALK_GRM_NOT_UPDATE = 23127,  # ivErr_GrmNotUpdate        = 28 """语法未更新"""
    SPEECH_ERROR_AITALK_STARTED = 23128,  # ivErr_Started             = 29
    SPEECH_ERROR_AITALK_STOPPED = 23129,  # ivErr_Stopped             = 30
    SPEECH_ERROR_AITALK_ALREADY_STARTED = 23130,  # ivErr_AlreadyStarted      = 31
    SPEECH_ERROR_AITALK_ALREADY_STOPPED = 23131,  # ivErr_AlreadyStopped      = 32
    SPEECH_ERROR_AITALK_TOO_MANY_COMMAND = 23132,  # ivErr_TooManyCmd          = 33
    SPEECH_ERROR_AITALK_WAIT = 23133,  # ivErr_Wait                = 34 """程序可能在做一些操作,主线程需要等待"""
    SPEECH_ERROR_AITALK_MAE_RIGHT = 23134,  # ivErr_MAERight            = 35
    SPEECH_ERROR_AITALK_MAE_WRONG = 23135,  # ivErr_MAEWrong            = 36

    SPEECH_ERROR_AITALK_GRM_ERR = 23300,  # 语法错误

    """Error Code Of AiSound"""

    """Error Code Of AiSound Operation"""
    SPEECH_ERROR_TTS_INVALID_PARA = 24000, """ 错误参数 """
    SPEECH_ERROR_TTS_INVALID_PARA_VALUE = 24001, """ 无效的参数值"""
    SPEECH_ERROR_TTS_OUT_OF_MEMORY = 24002, """ 内存不足"""
    SPEECH_ERROR_TTS_INVALID_HANDLE = 24003, """ 无效的句柄"""
    SPEECH_ERROR_TTS_CREATE_HANDLE_FAILED = 24004, """ 创建句柄失败"""
    SPEECH_ERROR_TTS_INVALID_RESOURCE = 24005,	""" 无效资源 """
    SPEECH_ERROR_TTS_INVALID_VOICE_NAME = 24006,	""" 无效发言人"""
    SPEECH_ERROR_TTS_ENGINE_UNINIT = 24007, """ 引擎未初始化 """
    SPEECH_ERROR_TTS_ENGINE_INIT_FAILED = 24008,	""" 引擎初始化失败 """
    SPEECH_ERROR_TTS_ENGINE_BUSY = 24009, """ 引擎忙 """

    """Error Code Of AiSound Engine"""
    SPEECH_ERROR_AISOUND_BASE = 24100,
    SPEECH_ERROR_AISOUND_UNIMPEMENTED = 24100,  """ unimplemented function """
    SPEECH_ERROR_AISOUND_UNSUPPORTED = 24101,  """ unsupported on this platform """
    SPEECH_ERROR_AISOUND_INVALID_HANDLE = 24102,  """ invalid handle """
    SPEECH_ERROR_AISOUND_INVALID_PARA = 24103,  """ invalid parameter(s) """
    SPEECH_ERROR_AISOUND_INSUFFICIENT_HEAP = 24104,  """ insufficient heap size  """
    SPEECH_ERROR_AISOUND_STATE_REFUSE = 24105,  """ refuse to do in current state  """
    SPEECH_ERROR_AISOUND_INVALID_PARA_ID = 24106,  """ invalid parameter ID """
    SPEECH_ERROR_AISOUND_INVALID_PARA_VALUE = 24107,  """ invalid parameter value """
    SPEECH_ERROR_AISOUND_RESOURCE = 24108,  """ Resource is error """
    SPEECH_ERROR_AISOUND_RESOURCE_READ = 24109,  """ read resource error """
    SPEECH_ERROR_AISOUND_LBENDIAN = 24110,  """ the Endian of SDK  is error """
    SPEECH_ERROR_AISOUND_HEADFILE = 24111,  """ the HeadFile is different of the SDK """
    SPEECH_ERROR_AISOUND_BUFFER_OVERFLOW = 24112,  """ get data size exceed the data buffer """
    SPEECH_ERROR_AISOUND_INVALID_ISAMPA = 24113,  """ !Invalid iSampa format or input iSampa text contain invalid alphabet"""
    SPEECH_ERROR_AISOUND_INVALID_CSSML = 24114,   """ !Invalid cssml format """

    """Error Code Of ivw"""

    """Error Code Of ivw Operation"""
    SPEECH_ERROR_IVW_ENGINE_UNINI = 25000,  """ 引擎未初始化 """
    SPEECH_ERROR_IVW_RESVER_NOMATCH = 25001,  """ 资源版本不匹配 """
    SPEECH_ERROR_IVW_BUFFERED_AUDIOD_LITTLE = 25002,  """ 唤醒加识别缓存音频过少 """
    SPEECH_ERROR_IVW_INVALID_RESTYPE = 25003,  """ 不合法的资源类型 """
    SPEECH_ERROR_IVW_INVALID_RESHEADVER = 25004,  """ 不合法的资源头部版本号 """

    """Error Code Of ivw Engine"""
    SPEECH_ERROR_IVW_INVALID_CALL = 25101,   # IvwErr_InvCal       = 1
    SPEECH_ERROR_IVW_INVALID_ARG = 25102,   # IvwErr_InvArg	    = 2
    SPEECH_ERROR_IVW_TELL_SIZE = 25103,   # IvwErr_TellSize     = 3
    SPEECH_ERROR_IVW_OUT_OF_MEMORY = 25104,   # IvwErr_OutOfMemory  = 4
    SPEECH_ERROR_IVW_OUT_BUFFER_FULL = 25105,   # IvwErr_BufferFull	= 5
    SPEECH_ERROR_IVW_OUT_BUFFER_EMPTY = 25106,   # IvwErr_BufferEmpty	= 6
    SPEECH_ERROR_IVW_INVALID_RESOURCE = 25107,   # IvwErr_InvRes		= 7
    SPEECH_ERROR_IVW_REPETITIOPN_ENTER = 25108,   # IvwErr_ReEnter		= 8
    SPEECH_ERROR_IVW_NOT_SUPPORT = 25109,   # IvwErr_NotSupport	= 9
    SPEECH_ERROR_IVW_NOT_FOUND = 25110,   # IvwErr_NotFound		= 10
    SPEECH_ERROR_IVW_INVALID_SN = 25111,   # IvwErr_InvSN		= 11
    SPEECH_ERROR_IVW_LIMITTED = 25112,   # IvwErr_Limitted		= 12
    SPEECH_ERROR_IVW_TIME_OUT = 25113,   # IvwErr_TimeOut		= 13

    SPEECH_ERROR_IVW_ENROLL1_SUCESS = 25114,   # IvwErr_Enroll1_Success = 14
    SPEECH_ERROR_IVW_ENROLL1_FAILED = 25115,   # IvwErr_Enroll1_Failed  = 15
    SPEECH_ERROR_IVW_ENROLL2_SUCESS = 25116,   # IvwErr_Enroll2_Success = 16
    SPEECH_ERROR_IVW_ENROLL2_FAILED = 25117,   # IvwErr_Enroll2_Failed  = 17
    SPEECH_ERROR_IVW_ENROLL3_SUCESS = 25118,   # IvwErr_Enroll3_Success = 18
    SPEECH_ERROR_IVW_ENROLL3_FAILED = 25119,   # IvwErr_Enroll3_Failed  = 19
    SPEECH_ERROR_IVW_SPEECH_TOO_SHORT = 25120,   # IvwErr_SpeechTooShort  = 20
    SPEECH_ERROR_IVW_SPEECH_STOP = 25121,   # IvwErr_SpeechStop      = 21

    """ 非实时转写错误码: 26000~26999 """
    SPEECH_ERROR_LFASR_BASE = 26000,	""" 非实时转写错误码基码 """


'''
/**
 * @file    msp_cmn.h
 * @brief   Mobile Speech Platform Common Interface Header File
 * 
 *  This file contains the quick common programming interface (API) declarations 
 *  of MSP. Developer can include this file in your project to build applications.
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
 * @date    2012/09/01
 * 
 * @see        
 * 
 * History:
 * index    version        date            author        notes
 * 0        1.0            2012/09/01      MSC40        Create this file
 */

#ifndef __MSP_CMN_H__
#define __MSP_CMN_H__

#include "msp_types.h"

#ifdef __cplusplus
extern "C" {
#endif /* C++ */
//#ifdef MSP_WCHAR_SUPPORT
/** 
 * @fn		Wchar2Mbytes
 * @brief	wchar to mbytes
 * 
 *  User login.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const wchar_t* wcstr	- [in] Null-terminated source string(wchar_t *).
 * @param	char* mbstr				- [in] Destination string(char *).
 * @param   int len					- [in] The maximum number of bytes that can be stored in the multibyte output string.
 * @see		
 */

char *Wchar2Mbytes(const wchar_t* wcstr);

/** 
 * @fn		Mbytes2Wchar
 * @brief	mbytes to wchar
 * 
 *  User login.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* mbstr		- [in] Null-terminated source string(char *).
 * @param	wchar_t* wcstr			- [in] Destination string(wchar_t *).
 * @param   int wlen				- [in] The maximum number of multibyte characters to convert.
 * @see		
 */
wchar_t *Mbytes2Wchar(const char *mbstr);

//#endif /*MSP_WCHAR_SUPPORT*/

/** 
 * @fn		MSPLogin
 * @brief	user login interface
 * 
 *  User login.
 * 
 * @return	int MSPAPI			- Return 0 in success, otherwise return error code.
 * @param	const char* usr		- [in] user name.
 * @param	const char* pwd		- [in] password.
 * @param	const char* params	- [in] parameters when user login.
 * @see		
 */
int MSPAPI MSPLogin(const char* usr, const char* pwd, const char* params);
typedef int (MSPAPI *Proc_MSPLogin)(const char* usr, const char* pwd, const char* params);
//#ifdef MSP_WCHAR_SUPPORT
int MSPAPI MSPLoginW(const wchar_t* usr, const wchar_t* pwd, const wchar_t* params);
typedef int (MSPAPI *Proc_MSPLoginW)(const wchar_t* usr, const wchar_t* pwd, const wchar_t* params);
//#endif/*MSP_WCHAR_SUPPORT*/
/** 
 * @fn		MSPLogout
 * @brief	user logout interface
 * 
 *  User logout
 * 
 * @return	int MSPAPI			- Return 0 in success, otherwise return error code.
 * @see		
 */
int MSPAPI MSPLogout();
typedef int (MSPAPI *Proc_MSPLogout)();
//#ifdef MSP_WCHAR_SUPPORT
int MSPAPI MSPLogoutW();
typedef int (MSPAPI *Proc_MSPLogoutW)();
//#endif/*MSP_WCHAR_SUPPORT*/
/** 
 * @fn		MSPUpload
 * @brief	Upload User Specific Data
 * 
 *  Upload data such as user config, custom grammar, etc.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* dataName	- [in] data name, should be unique to diff other data.
 * @param	const char* params		- [in] parameters about uploading data.
 * @param	const char* dataID		- [in] id of the data to be operated.
 * @see		
 */
int MSPAPI MSPUpload( const char* dataName, const char* params, const char* dataID);
typedef int (MSPAPI* Proc_MSPUpload)( const char* dataName, const char* params, const char* dataID);

/** 
 * @fn		MSPDownload
 * @brief	Download User Specific Data
 * 
 *  Download data such as user config, etc.
 * 
 * @return	int MSPAPI				- Return 0 in success, otherwise return error code.
 * @param	const char* params		- [in] parameters about data to be downloaded.
 * @see		
 */
typedef int (*DownloadStatusCB)(int errorCode, long param1, const void *param2, void *userData);
typedef int (*DownloadResultCB)(const void *data, long dataLen, void *userData);
int MSPAPI MSPDownload(const char* dataName, const char* params, DownloadStatusCB statusCb, DownloadResultCB resultCb, void*userData);
typedef int (MSPAPI* Proc_MSPDownload)(const char* dataName, const char* params, DownloadStatusCB statusCb, DownloadResultCB resultCb, void*userData);
int MSPAPI MSPDownloadW(const wchar_t* wdataName, const wchar_t* wparams, DownloadStatusCB statusCb, DownloadResultCB resultCb, void*userData);
typedef int (MSPAPI* Proc_MSPDownloadW) (const wchar_t* wdataName, const wchar_t* wparams, DownloadStatusCB statusCb, DownloadResultCB resultCb, void*userData);

/** 
 * @fn		MSPAppendData
 * @brief	Append Data.
 * 
 *  Write data to msc, such as data to be uploaded, searching text, etc.
 * 
 * @return	int MSPAPI					- Return 0 in success, otherwise return error code.
 * @param	void* data					- [in] the data buffer pointer, data could be binary.
 * @param	unsigned int dataLen		- [in] length of data.
 * @param	unsigned int dataStatus		- [in] data status, 2: first or continuous, 4: last.
 * @see		
 */
int MSPAPI MSPAppendData(void* data, unsigned int dataLen, unsigned int dataStatus);
typedef int (MSPAPI* Proc_MSPAppendData)(void* data, unsigned int dataLen, unsigned int dataStatus);

/** 
 * @fn		MSPGetResult
 * @brief	Get Result
 * 
 *  Get result of uploading, downloading or searching, etc.
 * 
 * @return	const char* MSPAPI		- Return result of uploading, downloading or searching, etc.
 * @param	int* rsltLen			- [out] Length of result returned.
 * @param	int* rsltStatus			- [out] Status of result returned.
 * @param	int* errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const char* MSPAPI MSPGetResult(unsigned int* rsltLen, int* rsltStatus, int *errorCode);
typedef const char * (MSPAPI *Proc_MSPGetResult)(unsigned int* rsltLen, int* rsltStatus, int *errorCode);

/** 
 * @fn		MSPSetParam
 * @brief	set params of msc
 * 
 *  set param of msc
 * 
 * @return	int	- Return 0 if success, otherwise return errcode.
 * @param	const char* paramName	- [in] param name.
 * @param	const char* paramValue	- [in] param value
 * @see		
 */
int MSPAPI MSPSetParam( const char* paramName, const char* paramValue );
typedef int (MSPAPI *Proc_MSPSetParam)(const char* paramName, const char* paramValue);

/** 
 * @fn		MSPGetParam
 * @brief	get params of msc
 * 
 *  get param of msc
 * 
 * @return	int	- Return 0 if success, otherwise return errcode.
 * @param	const char* paramName	- [in] param name.
 * @param	const char* paramValue	- [out] param value
 * @param	const char* valueLen	- [in/out] param value (buffer) length
 * @see		
 */
int MSPAPI MSPGetParam( const char *paramName, char *paramValue, unsigned int *valueLen );
typedef int (MSPAPI *Proc_MSPGetParam)( const char *paramName, char *paramValue, unsigned int *valueLen );

/** 
 * @fn		MSPUploadData
 * @brief	Upload User Specific Data
 * 
 *  Upload data such as user config, custom grammar, etc.
 * 
 * @return	const char* MSPAPI		- data id returned by Server, used for special command.
 * @param	const char* dataName	- [in] data name, should be unique to diff other data.
 * @param	void* data				- [in] the data buffer pointer, data could be binary.
 * @param	unsigned int dataLen	- [in] length of data.
 * @param	const char* params		- [in] parameters about uploading data.
 * @param	int* errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const char* MSPAPI MSPUploadData(const char* dataName, void* data, unsigned int dataLen, const char* params, int* errorCode);
typedef const char* (MSPAPI* Proc_MSPUploadData)(const char* dataName, void* data, unsigned int dataLen, const char* params, int* errorCode);

/** 
 * @fn		MSPDownloadData
 * @brief	Download User Specific Data
 * 
 *  Download data such as user config, etc.
 * 
 * @return	const void*	MSPAPI		- received data buffer pointer, data could be binary, NULL if failed or data does not exsit.
 * @param	const char* params		- [in] parameters about data to be downloaded.
 * @param	unsigned int* dataLen	- [out] length of received data.
 * @param	int* errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const void* MSPAPI MSPDownloadData(const char* params, unsigned int* dataLen, int* errorCode);
typedef const void* (MSPAPI* Proc_MSPDownloadData)(const char* params, unsigned int* dataLen, int* errorCode);
//#ifdef MSP_WCHAR_SUPPORT
const void* MSPAPI MSPDownloadDataW(const wchar_t* params, unsigned int* dataLen, int* errorCode);
typedef const void* (MSPAPI* Proc_MSPDownloadDataW)(const wchar_t* params, unsigned int* dataLen, int* errorCode);
//#endif/*MSP_WCHAR_SUPPORT*/
/** 
 * @fn		MSPSearch
 * @brief	Search text for result
 * 
 *  Search text content, and got text result
 * 
 * @return	const void*	MSPAPI		- received data buffer pointer, data could be binary, NULL if failed or data does not exsit.
 * @param	const char* params		- [in] parameters about data to be downloaded.
 * @param	unsigned int* dataLen	- [out] length of received data.
 * @param	int* errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see		
 */
const char* MSPAPI MSPSearch(const char* params, const char* text, unsigned int* dataLen, int* errorCode);
typedef const char* (MSPAPI* Proc_MSPSearch)(const char* params, const char* text, unsigned int* dataLen, int* errorCode);



typedef int (*NLPSearchCB)(const char *sessionID, int errorCode, int status, const void* result, long rsltLen, void *userData);
const char* MSPAPI MSPNlpSearch(const char* params, const char* text, unsigned int textLen, int *errorCode, NLPSearchCB callback, void *userData);
typedef const char* (MSPAPI* Proc_MSPNlpSearch)(const char* params, const char* text, unsigned int textLen, int *errorCode, NLPSearchCB callback, void *userData);
int MSPAPI MSPNlpSchCancel(const char *sessionID, const char *hints);

/** 
 * @fn		MSPRegisterNotify
 * @brief	Register a Callback
 * 
 *  Register a Callback
 * 
 * @return	int                     -
 * @param	msp_status_ntf_handler statusCb		- [in] notify handler
 * @param	void *userData                   	- [in] userData
 * @see		
 */
typedef void ( *msp_status_ntf_handler)( int type, int status, int param1, const void *param2, void *userData );
int MSPAPI MSPRegisterNotify( msp_status_ntf_handler statusCb, void *userData );
typedef const char* (MSPAPI* Proc_MSPRegisterNotify)( msp_status_ntf_handler statusCb, void *userData );

/**
 * @fn		MSPGetVersion
 * @brief	Get version of MSC or Local Engine
 *
 * Get version of MSC or Local Engine
 * 
 * @return	const char * MSPAPI		- Return version value if success, NULL if fail.
 * @param	const char *verName		- [in] version name, could be "msc", "aitalk", "aisound", "ivw".
 * @param	int *errorCode			- [out] Return 0 in success, otherwise return error code.
 * @see
 */
const char* MSPAPI MSPGetVersion(const char *verName, int *errorCode);
typedef const char* (MSPAPI * Proc_MSPGetVersion)(const char *verName, int *errorCode);

#ifdef __cplusplus
} /* extern "C" */	
#endif /* C++ */

#endif /* __MSP_CMN_H__ */
'''

msc.MSPLogin.argtypes = [c_char_p, c_char_p, c_char_p]
msc.MSPLogin.restype = c_int

msc.MSPLogout.argtypes = []
msc.MSPLogout.restype = c_int

msc.MSPUpload.argtypes = [c_char_p, c_char_p, c_char_p]
msc.MSPUpload.restype = c_int

DownloadStatusCB = CFUNCTYPE(c_int, c_int, c_long, c_void_p, c_void_p)
DownloadResultCB = CFUNCTYPE(c_int, c_void_p, c_long, c_void_p)
msc.MSPDownload.argtypes = [c_char_p, c_char_p,
                            DownloadStatusCB, DownloadResultCB, c_void_p]
msc.MSPDownload.restype = c_int

msc.MSPAppendData.argtypes = [c_void_p, c_uint, c_uint]
msc.MSPAppendData.restype = c_int

msc.MSPGetResult.argtypes = [POINTER(c_uint), POINTER(c_int), POINTER(c_int)]
msc.MSPGetResult.restype = c_char_p

msc.MSPSetParam.argtypes = [c_char_p, c_char_p]
msc.MSPSetParam.restype = c_int

msc.MSPGetParam.argtypes = [c_char_p, c_char_p, POINTER(c_uint)]
msc.MSPGetParam.restype = c_int

msc.MSPUploadData.argtypes = [
    c_char_p, c_void_p, c_uint, c_char_p, POINTER(c_int)]
msc.MSPUploadData.restype = c_char_p

msc.MSPDownloadData.argtypes = [c_char_p, POINTER(c_uint), POINTER(c_int)]
msc.MSPDownloadData.restype = c_void_p

msc.MSPSearch.argtypes = [c_char_p, c_char_p, POINTER(c_uint), POINTER(c_int)]
msc.MSPSearch.restype = c_char_p

NLPSearchCB = CFUNCTYPE(c_int, c_char_p, c_int, c_int,
                        c_void_p, c_long, c_void_p)
msc.MSPNlpSearch.argtypes = [c_char_p, c_char_p,
                             c_uint, POINTER(c_int), NLPSearchCB, c_void_p]
msc.MSPNlpSearch.restype = c_char_p

msc.MSPNlpSchCancel.argtypes = [c_char_p, c_char_p]
msc.MSPNlpSchCancel.restype = c_int

msp_status_ntf_handler = CFUNCTYPE(
    None, c_int, c_int, c_int, c_void_p, c_void_p)
msc.MSPRegisterNotify.argtypes = [msp_status_ntf_handler, c_void_p]
msc.MSPRegisterNotify.restype = c_int

msc.MSPGetVersion.argtypes = [c_char_p, POINTER(c_int)]
msc.MSPGetVersion.restype = c_char_p


def MSPAssert(errorCode: int, errorMsg: str):
    assert errorCode == MSPStatus.MSP_SUCCESS, '%s, error code: %d, error name: %s' % (
        errorMsg,
        errorCode,
        MSPStatus(errorCode).name
    )


def MSPLogin(usr: str, pwd: str, params: str):
    usr = usr.encode('UTF-8') if usr else None
    pwd = pwd.encode('UTF-8') if pwd else None
    params = params.encode('UTF-8') if params else None
    errorCode: int = msc.MSPLogin(usr, pwd, params)
    MSPAssert(errorCode, 'MSPLogin failed')


def MSPLogout():
    errorCode: int = msc.MSPLogout()
    MSPAssert(errorCode, 'MSPLogout failed')


def MSPUpload(dataName: str, params: str, dataID: str):
    dataName = dataName.encode('UTF-8') if dataName else None
    params = params.encode('UTF-8') if params else None
    dataID = dataID.encode('UTF-8') if dataID else None
    errorCode: int = msc.MSPUpload(dataName, params, dataID)
    MSPAssert(errorCode, 'MSPUpload failed')


def MSPDownload(dataName: str, params: str, statusCb: _FuncPointer, resultCb: _FuncPointer, userData: bytes):
    dataName = dataName.encode('UTF-8') if dataName else None
    params = params.encode('UTF-8') if params else None
    errorCode: int = msc.MSPDownload(
        dataName,
        params,
        statusCb,
        resultCb,
        userData
    )
    MSPAssert(errorCode, 'MSPDownload failed')


def MSPAppendData(data: bytes, dataLen: int, dataStatus: int):
    errorCode: int = msc.MSPAppendData(data, dataLen, dataStatus)
    MSPAssert(errorCode, 'MSPAppendData failed')


def MSPGetResult() -> str:
    rsltLen = c_uint()
    rsltStatus = c_int()
    errorCode = c_int()
    result: bytes = msc.MSPGetResult(
        byref(rsltLen),
        byref(rsltStatus),
        byref(errorCode)
    )
    MSPAssert(errorCode.value, 'MSPGetResult failed')
    return result.decode('UTF-8') if result else None


def MSPSetParam(paramName: str, paramValue: str):
    paramName = paramName.encode('UTF-8') if paramName else None
    paramValue = paramValue.encode('UTF-8') if paramValue else None
    errorCode: int = msc.MSPSetParam(paramName, paramValue)
    MSPAssert(errorCode, 'MSPSetParam failed')


def MSPGetParam(paramName: str) -> str:
    paramName = paramName.encode('UTF-8') if paramName else None
    paramValue = c_char_p()
    valueLen = c_uint()
    errorCode: int = msc.MSPGetParam(paramName, paramValue, byref(valueLen))
    MSPAssert(errorCode, 'MSPGetParam failed')
    return paramValue.value.decode('UTF-8') if paramValue.value else None


def MSPUploadData(dataName: str, data: bytes, dataLen: int, params: str):
    dataName = dataName.encode('UTF-8') if dataName else None
    params = params.encode('UTF-8') if params else None
    errorCode: int = msc.MSPUploadData(dataName, data, dataLen, params)
    MSPAssert(errorCode, 'MSPUploadData failed')


def MSPDownloadData(params: str) -> bytes:
    params = params.encode('UTF-8') if params else None
    dataLen = c_uint()
    errorCode = c_int()
    data: c_void_p = msc.MSPDownloadData(
        params, byref(dataLen), byref(errorCode))
    MSPAssert(errorCode.value, 'MSPDownloadData failed')
    return string_at(data, dataLen.value) if data else None


def MSPSearch(params: str, text: str) -> str:
    params = params.encode('UTF-8') if params else None
    text = text.encode('UTF-8') if text else None
    dataLen = c_uint()
    errorCode = c_int()
    result: bytes = msc.MSPSearch(
        params, text, byref(dataLen), byref(errorCode))
    MSPAssert(errorCode.value, 'MSPSearch failed')
    return result.decode('UTF-8') if result else None


def MSPNlpSearch(params: str, text: str, textLen: int) -> str:
    params = params.encode('UTF-8') if params else None
    text = text.encode('UTF-8') if text else None
    errorCode = c_int()
    result: bytes = msc.MSPNlpSearch(params, text, textLen, byref(errorCode))
    MSPAssert(errorCode.value, 'MSPNlpSearch failed')
    return result.decode('UTF-8') if result else None


def MSPNlpSchCancel(sessionID: str, hints: str):
    sessionID = sessionID.encode('UTF-8') if sessionID else None
    hints = hints.encode('UTF-8') if hints else None
    errorCode: int = msc.MSPNlpSchCancel(sessionID, hints)
    MSPAssert(errorCode, 'MSPNlpSchCancel failed')


def MSPRegisterNotify(statusCb: _FuncPointer, userData: bytes):
    errorCode: int = msc.MSPRegisterNotify(statusCb, userData)
    MSPAssert(errorCode, 'MSPRegisterNotify failed')


def MSPGetVersion(verName: str) -> str:
    verName = verName.encode('UTF-8') if verName else None
    errorCode = c_int()
    version: bytes = msc.MSPGetVersion(verName, byref(errorCode))
    MSPAssert(errorCode.value, 'MSPGetVersion failed')
    return version.decode('UTF-8') if version else None
