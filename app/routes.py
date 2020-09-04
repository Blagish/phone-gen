from app import app, providers, regions, city_by_region, data_by_region, logger
from flask import render_template, request, redirect, url_for
from app.forms import BaseForm
from app.randomize import randomize

providers_sorted = list(sorted(providers))
regions_sorted = list(sorted(regions))


@app.route('/', methods=['GET', 'POST'])
def home():
    form = BaseForm()
    form.region.choices = [(k, regions_sorted[k]) for k in range(len(regions_sorted))]
    form.provider.choices = [(k, providers_sorted[k]) for k in range(len(providers_sorted))]
    if form.validate_on_submit():
        return redirect(url_for('get_things',
                                region_id=form.region.data,
                                provider_id=form.provider.data,
                                count=form.count.data))
    return render_template('home.html', title='Заглавная страница', form=form)


@app.route('/get_things')  # , methods=['GET, POST'])
def get_things():
    region = regions_sorted[int(request.args.get('region_id'))]
    cities = city_by_region[region]
    all_locations = []
    for i in cities:
        sep = f'{i}|'
        if i == '':
            sep = ''
        all_locations.append(f'{sep}{region}')

    provider = providers_sorted[int(request.args.get('provider_id'))]
    count = int(request.args.get('count'))
    logger.info(f'Called API method /get_things with parameters ' +\
                f'region_id={request.args.get("region_id")}, ' +\
                f'provider_id={request.args.get("provider_id")}, count={count}')
    data_sorted = list(filter(lambda x: data_by_region[x][4] == provider and data_by_region[x][5] in all_locations,
                              range(len(data_by_region))))

    phones = randomize(count, [(data_by_region[i][0],  # code
                                int(data_by_region[i][1]),  # start
                                int(data_by_region[i][2])) for i in data_sorted])  # end
    if phones:
        return '<br/>'.join(list(phones))
    return 'No phones can be generated with these parameters.'


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
    if not int(phone) or len(phone) != 10:
        return '{"code": "nan"}'  # not a number
    code = phone[:3]
    phone = phone[3:]
    regions_by_code = list(filter(lambda x: data_by_region[x][0] == code, range(len(data_by_region))))
    regions_by_code.sort(key=lambda x: data_by_region[x][1])
    for i in regions_by_code:
        if data_by_region[i][1] < phone < data_by_region[i][2]:
            location = data_by_region[i][5].split('|')
            return '{"code": "ok",' \
                   f'"provider": "{data_by_region[i][4]}",' \
                   f'"region": "{location.pop(-1)}",' \
                   f'"location": "{"|".join(location)}"' + '}'
    return '{"code": "ne"}'  # not exist
