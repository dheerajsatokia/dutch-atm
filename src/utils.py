from app import db
from app import ATM, WeekDays


def create(data):
    db.session.add(data)
    db.session.commit()
    return data


def select_all_atms():
    atms = ATM.query.all()
    return atms


def select_weekdays(atm_id):
    query = WeekDays.query.filter(WeekDays.atm_id == atm_id)
    return query


def update_atm(atm_id, data):
    query = db.session.query(ATM).filter(ATM.id == atm_id).update(
        {
            ATM.distance: data.get('distance'),
            ATM.functionality: data.get('functionality'),
            ATM.type: data.get('type'),
            ATM.street: data.get('street'),
            ATM.house_number: data.get('house_number'),
            ATM.postal_code: data.get('postal_code'),
            ATM.city: data.get('city'),
            ATM.lat: data.get('lat'),
            ATM.long: data.get('long')
        })
    db.session.commit()
    return query


def delete_atm(atm_id):
    ATM.query.filter(ATM.id == atm_id).delete()
    WeekDays.query.filter(WeekDays.atm_id == atm_id).delete()
    db.session.commit()


