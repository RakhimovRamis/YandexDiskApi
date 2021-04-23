import requests
import os
from datetime import datetime
from progress.bar import Bar

class YandexApi:
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

    def create_folder(self, path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        r = requests.put(f'{self.URL}?path={path}', headers=self.headers)
        if r.status_code != 201:
            print(r.json()['message'])
            #raise Exception(r.json())

    def upload_file(self, loadfile, savefile, replace='false'):
        """Загрузка файла. \n savefile: Путь к файлу на Диске \
            loadfile: Путь к загружаемому файлу \n replace: true or false Замена файла на Диске"""
        r = requests.get(f'{self.URL}/upload?path={savefile}&overwrite={replace}', headers=self.headers).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(r['href'], files={'file':f})
            except KeyError:
                print(r['message'])
                #raise Exception(r)

class Disk(YandexApi):

    def backup(self, savepath, loadpath):
        """Загрузка папки на Диск. \n savepath: Путь к папке на Диске для сохранения \n loadpath: Путь к загружаемой папке"""
        dateFolder = datetime.now().strftime('%Y%m%d-%H%M%S')
        self.create_folder(savepath)
        bar = Bar('Загрузка', max=len([i for i in os.walk(loadpath)]))
        for address, dirs, files in os.walk(loadpath):
            bar.next()
            address = address.replace('\\', '/')
            self.create_folder(f'{savepath}/{dateFolder}/{address.replace(loadpath, "")[1:]}')
            for file in files:
                self.upload_file(f'{address}/{file}', \
                    f'{savepath}/{dateFolder}{address.replace(loadpath, "")}/{file}')
        bar.finish()


#d1 = Disk(token='TOKEN')
#d1.backup('Backup', '//10.0.0.4/Share')
