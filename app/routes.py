from app import app, providers, regions, city_by_region, data_by_region, logger, providers_by_region
from flask import render_template, request, redirect, url_for, flash, send_file
from app.forms import BaseForm
from app.various import randomize, interval_bin_search
import tempfile
import os

providers_sorted = ['Любой'] + list(sorted(providers))
regions_sorted = list(sorted(regions))


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = BaseForm()
    form.region_id.choices = [(k, regions_sorted[k]) for k in range(len(regions_sorted))]
    form.provider_id.choices = [(0, '')]
    form.region_chosen.data = False
    return render_template('home.html', title='Заглавная страница', form=form)


@app.route('/region<int:region_id>', methods=['GET', 'POST'])
@app.route('/home/region<int:region_id>', methods=['GET', 'POST'])
def next_step(region_id):
    form = BaseForm()
    form.region_id.choices = [(k, regions_sorted[k]) for k in range(len(regions_sorted))]
    form.provider_id.choices = [(k, providers_sorted[k]) for k in range(len(providers_sorted))]

    form.region_id.process_data(region_id)
    form.provider_id.choices = providers_by_region[form.region_id.data]
    form.region_chosen.data = True
#    if form.is_submitted():
#        return redirect(url_for('get_phones',
#                                region_id=form.region.data,
#                                provider_id=form.provider.data,
#                                count=form.count.data))

    return render_template('home.html', title='Заглавная страница', form=form)


def get_phones(region_id, provider_id, count):
    # Create all locations to chosen city
    region = regions_sorted[region_id]
    cities = city_by_region[region]
    all_locations = []
    for i in cities:
        sep = f'{i}|'
        if i == '':
            sep = ''
        all_locations.append(f'{sep}{region}')

    provider = providers_sorted[provider_id]

    logger.info(f'Called API method /get_things with parameters ' + \
                f'region={region_id}, ' + \
                f'provider={provider_id}, count={count}')
    data_sorted = list(filter(
        lambda x: ((data_by_region[x][4] == provider) or not provider_id) and data_by_region[x][5] in all_locations,
        range(len(data_by_region))))

    phones = randomize(count, [(data_by_region[i][0],  # code
                                int(data_by_region[i][1]),  # start
                                int(data_by_region[i][2])) for i in data_sorted])  # end
    return phones


@app.route('/get_phones', methods=['GET', 'POST'])
def get_phones_data():
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = dict(request.data)
        if not data:
            data = dict(request.form)

    pre_region, pre_provider, pre_count = data.get('region_id'), data.get(
        'provider_id'), data.get('count')

    if not (pre_region and pre_provider and pre_count):  # Check for NoneType
        flash('Недопустимые значения параметров.')
        return redirect(url_for('home'))

    if not (pre_region.isdigit() and pre_provider.isdigit() and pre_count.isdigit()):
        flash('Недопустимые значения параметров.')
        return redirect(url_for('home'))
    count = int(pre_count)
    if count > 1000000:
        flash('Число номеров не должно превышать 1000000 (одного миллиона).')
        return redirect(url_for('home'))

    phones = get_phones(int(pre_region), int(pre_provider), count)

    if phones:
        tfile, path = tempfile.mkstemp()
        with open(path, 'w') as f:
            for phone in phones:
                f.write(phone+'\n')
        os.close(tfile)
        return send_file(path, as_attachment=True, attachment_filename='base.csv')
    flash('У выбранного провайдера нет номеров в данном регионе.')
    return redirect(url_for(f'home/{pre_region}'))


@app.route('/api')
def api():
    return render_template('api.html', title='API')


@app.route('/show_regions')
def show_regions():
    return str(regions)


@app.route('/show_providers')
def show_providers():
    return str(providers)


@app.route('/get_info')
def get_info():
    phone = request.args.get('phone')
    logger.info(f'Called API method /get_info with parameter phone={phone}')
    if len(phone) == 11:
        phone = phone[1:]
    if not phone.isdigit() or len(phone) != 10:
        return '{"code": "nan"}'  # not a number
    code = phone[:3]
    phone = phone[3:]
    regions_by_code = list(filter(lambda x: data_by_region[x][0] == code, range(len(data_by_region))))
    res = interval_bin_search(phone, data_by_region, regions_by_code)
    if res != -1:
        location = data_by_region[regions_by_code[res]][5].split('|')
        logger.info(f'Calculated')
        return '{"code": "ok",' \
               f'"provider": "{data_by_region[regions_by_code[res]][4]}",' \
               f'"region": "{location.pop(-1)}",' \
               f'"location": "{"|".join(location)}"' + '}'
    return '{"code": "ne"}'  # not exist
