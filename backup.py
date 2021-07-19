import requests
import os
from datetime import datetime
from progress.bar import Bar

class YandexDiskApi:
    URL = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

    def create_folder(self, path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        requests.put(f'{self.URL}?path={path}', headers=self.headers)

    def upload_file(self, loadfile, savefile, replace='false'):
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        loadfile: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""
        res = requests.get(f'{self.URL}/upload?path={savefile}&overwrite={replace}', headers=self.headers).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file':f})
            except KeyError:
                print(res)

class Disk(YandexDiskApi):
    
    def file_backup(self, savepath, loadpath):
        """Загрузка папки на Диск. \n savepath: Путь к папке на Диске для сохранения \n loadpath: Путь к загружаемой папке"""
        date_folder = '{0}_{1}'.format(loadpath.split('\\')[-1], datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
        self.create_folder(savepath)
        for address, _, files in os.walk(loadpath):
            self.create_folder('{0}/{1}/{2}'.format(savepath, date_folder, address.replace(loadpath, "")[1:].replace("\\", "/")))
            bar = Bar('Loading', fill='X', max=len(files))
            for file in files:
                bar.next()
                self.upload_file('{0}\{1}'.format(address, file),\
                            '{0}/{1}{2}/{3}'.format(savepath, date_folder, address.replace(loadpath, "").replace("\\", "/"), file))
        bar.finish()


if __name__ == '__main__':
    d1 = Disk(token='AQAAAAAz55vbAAdBSHeydEoSe0fclxSSABT-y_U')
    #d1.file_backup('Backup', r'C:\myproject')
    d1.file_backup('Backup', os.getcwd())
