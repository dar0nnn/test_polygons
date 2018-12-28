# -*- coding: utf-8 -*-
from flask import request, jsonify, make_response, abort
from . import api
from test_DD import db, models, logger
from sqlalchemy.exc import InvalidRequestError
import json

@api.route('/', methods=['GET'])
def index():
    '''
    просто index для проверки ожило ли все. ничего серьезного.
    '''
    return make_response(jsonify({'status': 'its alive!'}), 200)


@api.route('/test_dd/create_poligon', methods=['POST'])
def create_poligon():
    '''
    создает полигон в базе. проверки данных нет, так как в тз не описаны условия
    формата сообщений
    :args 
        json from POST
    :return response 
        201 в случае успеха, 
        400 в случае несуществующих данных
        500 в остальных случаях
    '''
    if request.data:
        try:
            # все равно не знаю какие поля надо проверять, поэтому от лени закидываю весь json
            poligon = models.Gis_poligon()
            data = json.loads(request.data)
            poligon.change_attr(data)
            db.session.add(poligon)
            db.session.commit()
            logger.info('poligon {} created'.format(data['name']))
            return make_response(jsonify({'status': 'created'}), 201)
        except InvalidRequestError as e:
            logger.error(e)
            db.session.rollback()
            abort(400)
        except Exception as e:
            print(type(e).__name__)
            logger.critical(e)
            db.session.rollback()
            abort(500)
    else: 
        abort(400)


@api.route('/test_dd/delete_poligon/<int:id>', methods=['DELETE'])
def delete_poligon(id):
    '''
    удаляет полигон по id
    :args
        id from url
    :return response  
        200 в случае успеха
        500 в остальных случаях  
    '''
    try:
        poligon = models.Gis_poligon.query.filter_by(id=id).first()
        logger.info('poligon {} deleted'.format(poligon.name))
        db.session.delete(poligon)
        db.session.commit()
        return make_response(jsonify({'status': 'deleted'}), 200)
    except Exception as e:
        logger.critical(str(e))
        db.session.rollback()
        abort(500)


@api.route('/test_dd/update_poligon/<int:id>', methods=['PUT'])
def update_poligon(id):
    '''
    изменяет существующий в базе полигон по id. проверки данных нет,
    так как в тз не описаны условия формата сообщений
    :args
        id from url
        json from PUT
    :return response
        200 в случае успеха
        400 в случае несуществующих данных
        500 в остальных случаях
    '''
    if request.data:
        try:
            poligon = models.Gis_poligon.query.filter_by(id=id).first()
            data = json.loads(request.data)
            poligon.change_attr(data)
            db.session.commit()
            logger.info('poligon {} updated'.format(poligon.name))
            return make_response(jsonify({'status': 'changed'}), 200)
        except Exception as e:
            logger.critical(str(e))
            db.session.rollback()
            abort(500)
    else:
        abort(400)

@api.route('/test_dd/get_poligons', methods=['GET'])
def get_poligons():
    '''
    метод получения всех полигонов из базы данных в формате EPSG:32644
    стоит отметить, что формат координат не могу проверить, так как не смог
    придумать тестовый пример корректных координат.
    :return response
        200 в случае успешной отправки сообщения
        500 в остальных случаях
    '''
    try:
        poligons = models.Gis_poligon.query.all()
        poligons_arr = []
        for poligon in poligons:
            poligons_arr.append(poligon.as_dict())
        return make_response(jsonify({'poligons': poligons_arr}), 200)
    except Exception as e:
        logger.critical(str(e))
        db.session.rollback()
        abort(500)
