import os
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup


session = requests.Session()
session.headers.update({'User-Agent': 'Chrome/54.0.2840.71'})
HEAD = 'https://2ch.hk'


def create_parser():
    argument = argparse.ArgumentParser()
    argument.add_argument('-d', '--download')
    argument.add_argument('-f', '--force', action='store_true', default=False)
    return argument


def print_progress(iteration, total, name_file):
    percent = round((iteration / total) * 100)
    print('\r{}% downloaded | {} of {} | last file: {}'.format(str(percent), iteration, total, name_file),
          end='', flush=True)
    if iteration == total:
        print(end='\n')


def parse_web(url, mode):
    response = session.get(url)
    name_dir = url.split('/')[-1].split('.')[0]

    if not os.path.exists(name_dir):
        os.mkdir(name_dir)
    else:
        print('Directory exist')
        return 'err'

    os.chdir(name_dir)

    list_file = list()
    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('div', {'class': 'image-link'}, 'a'):
        list_file.append(link.a.get('href'))

    items = list(range(0, len(list_file)))
    i = 0
    l = len(items)

    for part in items:
        r = requests.get(HEAD+list_file[part])
        if r.status_code == 200:
            file_name = list_file[part].split('/')[-1]
            file = open(file_name, 'wb')
            file.write(r.content)
            time.sleep(0.1)
            i += 1
            print_progress(i, l, file_name)


if __name__ == '__main__':
    parse = create_parser()
    namespace = parse.parse_args(sys.argv[1:])
    if namespace.download:
        parse_web(namespace.download, namespace.force)
