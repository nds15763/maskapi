from conf.conf import Conf

def Response(err_code):
    return {
        "code":err_code,
        "msg":Conf.httpcode[err_code]
    }