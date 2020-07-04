import os
import re
import hashlib

import requests

from cliui import UIPrinter
UI = UIPrinter('authlib-injector-updater')

custom_filename = 'authlib-injector.jar'


def get_latest():
    r = requests.get(
        'https://authlib-injector.yushi.moe/artifact/latest.json')
    return r.json()


def check_is_outdated(sha256) -> bool():
    if not custom_filename in os.listdir():
        return True
    with open(custom_filename, 'rb') as f:
        return not checksum(f.read(), sha256)


def download(url):
    r = requests.get(url)
    return r.content


def write_to_file(origin_filename, content):
    with open(origin_filename, 'wb') as f:
        f.write(content)


def checksum(content, sha256):
    return hashlib.sha256(content).hexdigest() == sha256


def main():
    UI.wait('正在获取版本信息')
    latest_json = get_latest()
    download_url = latest_json['download_url']
    latest_version = latest_json['version']
    sha256 = latest_json['checksums']['sha256']
    is_outdated = check_is_outdated(sha256)
    if is_outdated:
        url = latest_json['download_url']
        UI.wait(f'正在下载 {latest_version}')
        UI.note(f'URL: {url}')
        d = download(url)
        if checksum(d, latest_json['checksums']['sha256']):
            UI.succ('文件完整性校验通过')
            write_to_file(custom_filename, d)
            UI.succ(f'{latest_version} 已保存至 {custom_filename}')
        else:
            UI.fail('完整性校验失败')
            raise Exception('完整性校验失败')
    else:
        UI.succ('你的 authlib-injector 已是最新版本')
        exit()


if __name__ == "__main__":
    main()
