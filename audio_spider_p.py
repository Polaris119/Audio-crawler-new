import requests
import re  # 正则表达式
import json
import os


def bv_name(bv, name, page):
    page = int(page)
    directory = f"D:/video/{name}"
    os.makedirs(directory, exist_ok=True)

    url_headers = []  # 存放所有分p视频的url
    i = 1
    while(i <= page):
        URL = f'https://www.bilibili.com/video/{bv}?p={i}'

        headers = {
            'referer': f'https://www.bilibili.com/video/{bv}?p={i}spm_id_from=333.337.search-card.all.click',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        url_headers.append({URL: headers})
        i += 1

    return directory, url_headers


def music_name(bv):
    """提取视频分集名"""
    URL = f'https://www.bilibili.com/video/{bv}?p=1'

    headers = {
        'referer': f'https://www.bilibili.com/video/{bv}?p=1&vd_source=3038ec1ee5ab67fefa6275a8aa5b5e60',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    response = requests.get(url=URL, headers=headers).text
    # 提取文件名
    name_data = re.findall(r'"part":"(.*?)"', response)
    # print(name_data)
    return name_data


def send_request(url, header):
    response = requests.get(url=url, headers=header)
    return response


def get_video_data(html_data, header):
    """解析视频数据"""

    # 提取视频对应的json数据
    json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]
    json_data = json.loads(json_data)

    try:
        # 提取音频的url地址
        audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
        # print('解析到的音频地址:', audio_url)
        audio_data = send_request(audio_url, header).content
    except:
        audio_data = 1

    return audio_data


def save_data(file_name, audio_data, music):
    # 请求数据
    # audio_data = send_request(audio_url, headers).content
    with open(file_name + f'/{music}.mp3', mode='wb') as f:
        f.write(audio_data)
    # print(f"file_name + '_{i}.mp3'下载完毕！！！")

