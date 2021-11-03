from flask import Blueprint
from flask import request

import requests
import logging
import json

from flask import jsonify
from dateutil import parser

from src.model import models
from src.utils import create, select_all_atms, select_weekdays, update_atm, delete_atm

urls_blueprint = Blueprint('urls', __name__, )


@urls_blueprint.route('/', methods=['post'])
def sync_api_data():
    req = requests.get('https://www.ing.nl/api/locator/atms/')
    req_text = req.text

    # converting uncertain api response into proper json data
    formatted_json_data = json.loads('{ "data" : ' + req_text[5:len(req_text) + 1] + '}')

    for atm in formatted_json_data['data']:
        atm_object = models.ATM(
            distance=atm.get('distance'),
            functionality=atm.get('functionality'),
            type=atm.get('type'),
            street=atm['address']['street'],
            house_number=atm['address']['housenumber'],
            postal_code=atm['address']['postalcode'],
            city=atm['address']['city'],
            lat=atm['address']['geoLocation'].get('lat'),
            long=atm['address']['geoLocation'].get('lng'),
        )

        atm_obj = create(atm_object)

        for weekday in atm['openingHours']:
            weekday_obj = models.WeekDays(
                atm_id=atm_obj.id,
                days_of_week=weekday['dayOfWeek'],
                hour_from=parser.parse(weekday['hours'][0]['hourFrom'] if weekday['hours'] else None),
                hour_to=parser.parse(weekday['hours'][0]['hourTo']) if weekday['hours'] else None,
            )

            create(weekday_obj)

    return jsonify({'message': 'sync api data'})


@urls_blueprint.route('/atms', methods=['get'])
def get_atms_data():
    atms = select_all_atms()
    atm_list = []
    try:
        for atm in atms:
            weekday = select_weekdays(atm.id)
            working_times = []
            if weekday:
                for working_time in weekday:
                    working_times.append({
                        'day_of_week': working_time.days_of_week,
                        'from': working_time.hour_from,
                        'to': working_time.hour_to

                    })
            atm_list.append({
                'distance': atm.distance,
                'functionality': atm.functionality,
                'type': atm.type,
                'address': {'street': atm.street,
                            'house_number': atm.house_number,
                            'postal_code': atm.postal_code,
                            'city': atm.city,
                            'lat': atm.lat,
                            'long': atm.long
                            },
                'working_times': working_times
            })
    except Exception as e:
        logging.exception(e)
        return jsonify({'error': 'something went wrong, please check log or contact for administration support'}), 400

    return jsonify({'data': atm_list})


@urls_blueprint.route('/atms/update', methods=['put'])
def update_atms():
    data = dict(request.form)
    atm_id = request.args.get('atm_id')
    try:
        update_atm(atm_id, data)
    except Exception as e:
        logging.exception(e)
        return jsonify({'error': 'something went wrong, please check log or contact for administration support'}), 400
    return jsonify({'data': 'data updated successfully'}), 200


@urls_blueprint.route('/atms/delete', methods=['delete'])
def delete_atms():
    atm_id = request.args.get('atm_id')
    delete_atm(atm_id)
    return jsonify({'message': 'deleted successfully'})
