from test_DD import db
# from db import db.Column,db. Integer, String, DateTime, JSON, PrimaryKeyConstraint, Sequence
from geoalchemy2 import Geometry, functions
from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
import datetime
from functools import partial
import pyproj
import numpy
from shapely.ops import transform
from geoalchemy2.elements import WKTElement


def converter_for_json(itemFromClass):
    '''
    функция преобразовывает поля таблицы в корректый формат для передачи в json
    нужна для функции Gis_poligon.as_dict()
    ловит datetime и WKBElement и преобразует их
    :args 
        поля класса
    :return
        поле класса в строком представлении
    -------------------------------------------------------------------------
    собственно это довольно узкое место, так как если нужно менять в разные
    форматы данные - способ не подходящий. но он вполне неплохо подходит для
    выполнения тз
    '''
    if isinstance(itemFromClass, datetime.datetime):
        return itemFromClass.__str__()
    if isinstance(itemFromClass, WKBElement):
        item = to_shape(itemFromClass)
        project = partial(
            pyproj.transform,
            pyproj.Proj(init='epsg:4326'),
            pyproj.Proj(init='epsg:26913'))
        item = transform(project, item)
        return item.to_wkt()
    else:
        return itemFromClass


class Gis_poligon(db.Model):
    __tablename__ = 'gis_polygon'

    _created = db.Column(db.DateTime())
    _update = db.Column(db.DateTime())
    id = db.Column(db.Integer(), db.Sequence(__tablename__ + '_id_seq'), nullable=False, primary_key=True)
    class_id = db.Column(db.Integer())
    name = db.Column(db.String())
    props = db.Column(db.JSON())
    geom = db.Column(Geometry('POLYGON', 4326))
    db.PrimaryKeyConstraint(id, name='gis_polygon_pkey')

    def __init__(self, _created=None, _update=None, class_id=None, name=None, props=None, geom=None):
        self._created = _created
        self._update = _update
        self.class_id = class_id
        self.name = name
        self.props = props
        self.geom = geom

    def change_attr(self, attrDict):
        '''
        функция для изменения полей
        :args 
            json, который приходит с запроса
        :return
            будет объект, с полями из json.
        '''
        for column, data in attrDict.items():
            if column == 'geom':
                data = WKTElement(data, srid=4326)
            setattr(self, column, data)

    def as_dict(self):
        '''
        представляет поля класса в виде словаря, готового к упаковке в json
        :return 
            словарь, с полями, готовыми к отправке
            в том числе здесь, посредством конвертера и преобразуются данные
            в нужный формат.
        '''
        return [converter_for_json(getattr(self, column.name)) for column in self.__table__.columns]

    def __repr__(self):
        return '<Gis_poligon> %r %r %r %r %r %r' % (self._created, self._update, self.class_id, self.name, self.props, self.geom)
