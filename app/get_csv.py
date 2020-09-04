import requests
import os
import csv
from app import providers, regions, city_by_region, data_by_region

file_names = ('ABC-3xx.csv',
              'ABC-4xx.csv',
              'ABC-8xx.csv',
              'DEF-9xx.csv')

def get_file(name, session):
    file_data = session.get(f'https://rossvyaz.ru/data/{name}')
    with open(name, 'w') as file:
        file.write(file_data.text)


def find_last(s, i):
    rev = reversed(s)


#def clear_table():
#    num = PhoneRange.query.delete()
#    print(f'deleted {num} rows')
#    db.session.commit()


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
    k = 0
    with open(name, encoding='utf-8') as file:
        dr = csv.DictReader(file, delimiter=';')
        for i in dr:
            data_provider = small_format(i['Оператор'])
            data_region = small_format(i['Регион'])

            region = parse_location(data_region)

            data_by_region.append((i['АВС/ DEF'],
                                    i['От'],
                                    i['До'],
                                    i['Емкость'],
                                    data_provider,
                                    data_region))

            providers.update([data_provider])

            regions.update([region])
            k += 1
    return k


def update_database():
    os.chdir('.')
    m = []
    print(os.listdir())
    print(os.curdir)
    os.chdir('./app/data')
    print(os.getcwd())
    with requests.Session() as session:
        for name in file_names:
#           get_file(name, session)
            k = write_to_db(name)
            m.append(k)
            print('file done')

    with open('providers.json', 'w') as pros:
        pros.write(str(sorted(providers)))
    with open('city_by_region.json', 'w') as regs:
        regs.write(str(city_by_region))
    with open('data_by_region.json', 'w') as regs:
        regs.write(str(data_by_region))
    with open('regions.json', 'w') as regs:
        regs.write(str(sorted(regions)))
    os.chdir('.')
    return m

