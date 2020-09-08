import requests
import os
import csv
from app import providers, regions, city_by_region, data_by_region, providers_by_region, logger
from shutil import copy


file_names = ('ABC-3xx.csv',
              'ABC-4xx.csv',
              'ABC-8xx.csv',
              'DEF-9xx.csv')


def get_file(name, session):
    file_data = session.get(f'https://rossvyaz.ru/data/{name}')
    if not file_data.ok:
        logger.error(f'Unable to download {name}. Using the previous version instead.')
        return 0
    copy(name, f'backup/{name}')
    logger.info(f'File {name} backed up.')
    with open(name, 'w') as file:
        file.write(file_data.text)
    logger.info(f'File {name} downloaded successfully.')


def parse_location(s):
    ss = s.split('|')
    key = ss.pop(-1)
    if not city_by_region.get(key):
        city_by_region[key] = set()
    city_by_region[key].update(["".join(ss)])
    return key


def small_format(s):
    if s[0] == ' ':
        return s[1:]
    return s


def write_to_db(name):
    with open(name) as file:
        dr = csv.DictReader(file, delimiter=';')
        for i in dr:
            data_provider = small_format(i['Оператор'])
            data_region = small_format(i['Регион'])

            region = parse_location(data_region)
            if providers_by_region.get(region, -1) != -1:
                providers_by_region[region].update([data_provider])
            else:
                providers_by_region[region] = set(['Любой'])

            data_by_region.append((i['АВС/ DEF'],
                                   i['От'],
                                   i['До'],
                                   i['Емкость'],
                                   data_provider,
                                   data_region))

            providers.update([data_provider])

            regions.update([region])
    logger.info(f'File {name} parsed successfully.')


def load_database(update=True):
    logger.info('Started updating .csv files.')
    os.chdir('./app/data')
    with requests.Session() as session:
        for name in file_names:
            if update:
                get_file(name, session)
            write_to_db(name)
    logger.info('Files updated successfully.')
