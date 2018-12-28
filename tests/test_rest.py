import pytest
from test_DD import create_app, db
from test_DD.models import Gis_poligon
import json
import datetime
from shapely.geometry import Polygon

@pytest.fixture(scope='module')
def test_client():
    '''
    клиент для теста
    '''
    flask_app = create_app('testing')
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


@pytest.fixture(scope='module')
def init_database():
    '''
    базка для теста
    '''
    db.create_all()
    yield db 
    db.drop_all()


def test_home_page(test_client):
    '''
    тест жив ли пациент
    '''
    response = test_client.get('/')
    assert response.status_code == 200
    assert {'status': 'its alive!'} == json.loads(response.data)


def test_poligon_create(test_client, init_database):
    '''
    тест создания полигона
    проверка на запрос с данными и без него
    '''
    pol = Polygon([[-73.08373, 47.76313],
                   [-73.07296, 47.37293],
                   [-73.08303, 47.36239],
                   [-73.08371, 47.36253],
                   [-73.0840, 47.36266],
                   [-73.08373, 47.76313]])
    poligon = {'_created': datetime.datetime.now().__str__(), 'props': {'hello': 'world'},
               'name': 'poligon1', 'class_id': 23, 'geom': pol.to_wkt()}
    response = test_client.post(
        '/test_dd/create_poligon', data=json.dumps(poligon))
    assert response.status_code == 201
    assert {"status": "created"} == json.loads(response.data)
    response = test_client.post('/test_dd/create_poligon')
    assert response.status_code == 400
    assert {'error': 'Bad request'} == json.loads(response.data)


def test_poligon_update(test_client, init_database):
    '''
    тест апдейта, в том числе меняю координаты
    '''
    pol = Polygon([[-78.24058, 58.25489],
                   [-73.07296, 47.37293],
                   [-73.08303, 47.36239],
                   [-73.08371, 47.36253],
                   [-73.0840, 47.36266],
                   [-78.24058, 58.25489]])
    poligon = {'name': 'poligon2', 'class_id': 124, 'geom': pol.to_wkt()}
    response = test_client.put(
        '/test_dd/update_poligon/1', data=json.dumps(poligon))
    assert response.status_code == 200
    assert {'status': 'changed'} == json.loads(response.data)


def test_poligon_get_poligons(test_client, init_database):
    '''
    тест получения полигонов
    '''
    response = test_client.get('/test_dd/get_poligons')
    check = ['poligon', 124]
    data = list(json.loads(response.data))[0]
    assert response.status_code == 200
    assert True == any(item in data for item in check)


def test_poligon_delete(test_client, init_database):
    '''
    тест удаления полигонов
    '''
    response = test_client.delete('/test_dd/delete_poligon/1')
    assert response.status_code == 200
    assert {'status': 'deleted'} == json.loads(response.data)
