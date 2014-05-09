#!/usr/bin/python

import flask_peewee.db as db
from flask import Flask, make_response, jsonify, json, url_for, request, abort

app = Flask(__name__)

dyerDB = db.SqliteDatabase('Dyer.db', threadlocals=True)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': error}), 404)

class BaseModel(db.Model):
    class Meta:
        database = dyerDB

class Location(BaseModel):
    location_id = db.IntegerField(primary_key=True)
    desc = db.TextField()
    external_ip = db.TextField()

    def to_json(self):
        return {"loc_id": self.location_id, "ex_ip": self.external_ip, "desc": self.desc}

    def to_json_with_device(self, devicesSqlQuery):
        devices = []
        for device in devicesSqlQuery:
            devices.append(device.to_json())

        return self.to_json()

class Device(BaseModel):
    device_id = db.PrimaryKeyField()
    location = db.ForeignKeyField(Location, related_name='devices')
    desc = db.TextField()

    def to_json(self):
        return {"desc": self.desc, "loc_id": self.location.location_id, "dev_id": self.device_id}

    def to_json_with_outlets(self, outletSqlQuery):
        outlets = []
        for outlet in outletSqlQuery:
            outlets.append(outlet.to_json())

        return {"desc": self.desc, "loc_id": self.location.location_id, "dev_id": self.device_id, "outlets": outlets}

class Outlet(BaseModel):
    outlet_id = db.PrimaryKeyField()
    device = db.ForeignKeyField(Device, related_name='outlets')
    desc = db.TextField()

    def to_json(self):
        return {"desc": self.desc, "dev_id": self.device.device_id, "out_id": self.outlet_id}


@app.route('/location', methods=['POST'])
def save_location():
    new_location = Location(desc=request.json['desc'], external_ip=request.json['external_ip'])
    new_location.save()
    return jsonify(new_location.to_json())

@app.route('/location', methods=['GET'])
def get_locations():
    locations = [location.to_json() for location in Location.select()]
    return jsonify(locations=locations)

@app.route('/location/<location_id>', methods=['GET'])
def get_location(location_id):
    loc_devices = [device.to_json() for device in Device.select().where(Location.location_id == location_id)]
    return jsonify(location=loc_devices)

@app.route('/location/<location_id>', methods=['DELETE'])
def delete_location(location_id):
    loc = Location.get(Location.location_id == location_id)
    loc.delete_instance()
    return jsonify(message="Successfully deleted location instance")


@app.route('/device', methods=['POST'])
def save_device():
    new_device = Device(location=request.json['location_id'], desc=request.json['desc'])
    new_device.save()
    return jsonify(new_device.to_json())

@app.route('/device', methods=['GET'])
def get_devices():
    devices = [device.to_json() for device in Device.select()]
    return jsonify(devices=devices)

@app.route('/device/<dev_id>', methods=['GET'])
def get_device(dev_id):
    device = [device.to_json_with_outlets(Outlet.select().where(Device.device_id == dev_id)) for device in Device.select().where(Device.device_id == dev_id)]
    return jsonify(device=device)

@app.route('/device/<dev_id>', methods=['DELETE'])
def delete_device(dev_id):
    device = Device.get().where(Device.device_id == dev_id)
    device.delete()
    return jsonify(device=device.to_json())


@app.route('/outlet', methods=['POST'])
def save_outlet():
    new_outlet = Outlet(device=request.json['device_id'], desc=request.json['desc'])
    new_outlet.save()
    return jsonify(new_outlet.to_json())

@app.route('/outlet', methods=['GET'])
def get_outlets():
    outlets = [outlet.to_json() for outlet in Outlet.select()]
    return jsonify(outlets=outlets)

@app.route('/outlet/<out_id>', methods=['GET'])
def get_outlet(out_id):
    device_outlets = [outlet.to_json() for outlet in Outlet.select().where(Outlet.outlet_id == out_id)]
    return jsonify(location=device_outlets)

@app.route('/outlet/<out_id>', methods=['DELETE'])
def delete_outlet(out_id):
    outlet = Outlet.get().where(Outlet.outlet_id == out_id)
    for out in outlet:
        out.delete()
    return jsonify(outlet=out.to_json())

if __name__ == '__main__':

    dyerDB.connect()
    # Location.create_table()
    # Device.create_table()
    # Outlet.create_table()

    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')
