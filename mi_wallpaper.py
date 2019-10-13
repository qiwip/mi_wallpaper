import os
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import time

timeout = 5
socket.setdefaulttimeout(timeout)


class Crawler:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}

    def __init__(self, t=0.1):
        self.__counter = 0
        self.time_sleep = t

    @staticmethod
    def get_referrer(url):
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

    def save_images(self, rsp_data):
        if not os.path.exists('./pic'):
            os.mkdir('./pic')
        for i in rsp_data:
            try:
                url = 'http://file.market.xiaomi.com/thumbnail/jpeg/w965/' + i['frontCover']
                time.sleep(self.time_sleep)

                name = i['name']
                refer = self.get_referrer(url)
                # 指定UA和referrer，减少403
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                urllib.request.install_opener(opener)
                urllib.request.urlretrieve(url, './pic' + os.sep + url[-5:] + str(name) + '.png')
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print('产生未知错误，放弃保存')
                continue
            else:
                print('+1,已下载{}张图片'.format(self.__counter))
                self.__counter += 1
        return

    def download_images(self, pa):
        pn = 82
        while pn < pa+1:
            print('读取第{}页'.format(pn))
            url = 'http://zhuti.xiaomi.com/wallpaper?page={}&sort=Hot&ajax=1&count=30&act=list&keywords=&subjectId='.format(pn)
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('utf-8')
            except UnicodeDecodeError as e:
                print(e)
                print('UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print('urlErrorurl:', url)
            except socket.timeout as e:
                print(e)
                print('socket timout:', url)
            else:
                page.close()
                rsp_data = json.loads(rsp)
                self.save_images(rsp_data)
            pn += 1
        print('下载结束')
        return


if __name__ == '__main__':
    crawler = Crawler(0.05)
    crawler.download_images(5637)
