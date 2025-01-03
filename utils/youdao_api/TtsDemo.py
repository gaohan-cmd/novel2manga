import os

import requests
from dotenv import load_dotenv

from utils.youdao_api.utils.AuthV3Util import addAuthParams

load_dotenv('.env', override=True)

# 尝试加载本地开发环境变量文件
load_dotenv('.local.env', override=True)

# 读取环境变量
youdao_tts_app_key = os.getenv('YOUDAO_TTS_APP_KEY')
youdao_tts_app_secret = os.getenv('YOUDAO_TTS_APP_SECRET')


# 合成音频保存路径, 例windows路径：PATH = "C:\\tts\\media.mp3"
# PATH = 'D:\\PyCharm\\pythonProjects\\novel2manga\\utils\\youdao_api\\media.mp3'


def create_youdao_request(q, path, format='mp3', voiceName='youxiaoqin'):
    '''
    note: 将下列变量替换为需要请求的参数
    '''

    data = {'q': q, 'voiceName': voiceName, 'format': format}

    addAuthParams(youdao_tts_app_key, youdao_tts_app_secret, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/ttsapi', header, data, 'post')
    saveFile(res, path)


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def saveFile(res, path):
    contentType = res.headers['Content-Type']
    if 'audio' in contentType:
        fo = open(path, 'wb')
        fo.write(res.content)
        fo.close()
        print('save file path: ' + path)
    else:
        print(str(res.content, 'utf-8'))


# 网易有道智云语音合成服务api调用demo
# api接口: https://openapi.youdao.com/ttsapi
if __name__ == '__main__':
    create_youdao_request()
