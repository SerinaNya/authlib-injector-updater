import os
import re
import hashlib

import requests


def get_latest():
    r = requests.get(
        'https://authlib-injector.yushi.moe/artifact/latest.json')
    return r.json()


def get_versions():
    files = os.listdir()
    ai_jars = set()
    for origin_filename in files:
        if re.match(r'^authlib-injector-(.*)\.jar$', origin_filename):
            ai_jars.add(origin_filename)
    versions = set()
    for i in ai_jars:
        start, end = re.search(r'([0-9]*)\.([0-9]*)\.([0-9]*)', i).span()
        versions.add(i[start:end])
    return versions


def check_is_outdated(latest_json, local_versions):
    return not latest_json['version'] in local_versions


def download(url):
    r = requests.get(url)
    return r.content


def write_to_file(origin_filename, content):
    with open(origin_filename, 'wb') as f:
        f.write(content)


def checksum(content, sha256):
    return hashlib.sha256(content).hexdigest() == sha256


def main():
    print('=== authlib-injector 更新程序 ===')
    print('正在获取版本信息')
    latest_json = get_latest()
    local_versions = get_versions()
    is_outdated = check_is_outdated(latest_json, local_versions)
    if is_outdated:
        url = latest_json['download_url']
        start, end = re.search(r'authlib-injector-(.*)\.jar', url).span()
        origin_filename = url[start:end]
        custom_filename = 'authlib-injector.jar'
        print(f'正在下载 {origin_filename}')
        d = download(url)
        if checksum(d, latest_json['checksums']['sha256']):
            write_to_file(custom_filename, d)
            print(f'{origin_filename} 下载完成')
        else:
            raise Exception('完整性校验失败')
    else:
        exit('你的 authlib-injector 已是最新版本')


if __name__ == "__main__":
    main()
