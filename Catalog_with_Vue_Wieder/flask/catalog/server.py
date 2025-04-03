from flask import Flask, request,jsonify
from sqlalchemy import Column, Integer, Text, Float, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func
from flask_restful import Resource, Api
from dataclasses import dataclass
import json
from flask_cors import CORS, cross_origin

Base = declarative_base()  # Basisklasse aller in SQLAlchemy verwendeten Klassen
metadata = Base.metadata

engine = create_engine('sqlite:///C:/Users/sebi0/OneDrive - HTL Anichstrasse/Schuljahr 2024 - 2025 (5. Klasse)/SWP_Greini/Codes/SWP_Greinoecker_24_25/Catalog_with_Vue_Wieder/flask/catalog/catalog.db')
#engine = create_engine('mysql+pymysql://root:root@localhost/catalog') #mysql

db_session = scoped_session(sessionmaker(autoflush=True, bind=engine))
Base.query = db_session.query_property() #Dadurch hat jedes Base - Objekt (also auch ein GeoInfo) ein Attribut query für Abfragen
app = Flask(__name__) #Die Flask-Anwendung
cors = CORS(app) # Ohne dieser Anweisung darf man von Webseiten aus nicht zugrfeifen
api = Api(app) #Die Flask API

@dataclass #Diese ermoeglicht das Schreiben als JSON mit jsonify
class Catalog(Base):
    __tablename__ = 'card'  # Abbildung auf diese Tabelle
    id: int
    description: str
    thumb: str

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    thumb = Column(Text)

class CatalogREST(Resource):
    def get(self, id):
        info = Catalog.query.get(id)
        return jsonify(info)
    def put(self, id):
        data = request.get_json(force=True)['info']
        print(data)
        info = Catalog(id=data['id'], description=data['description'], thumb=data['thumb'])
        db_session.add(info)
        db_session.flush()
        db_session.commit()
        return jsonify(info)
    def delete(self,id):
        info = Catalog.query.get(id)
        if info is None:
            return jsonify({'message': 'object with id %d does not exist' % id})
        db_session.delete(info)
        db_session.flush()
        db_session.commit()
        return jsonify({'message': '%d deleted' % id})
    def patch(self, id):
        print(request.json)
        info = Catalog.query.get(id)
        if info is None:
            return jsonify({'message': 'object with id %d does not exist' % id})
        description = request.json['params']['description']
        info.description = description
        db_session.add(info)
        db_session.flush()
        db_session.commit()
        return jsonify({'message': 'object with id %d modified' % id})

    @app.route('/cat-search/<q>')
    def cat_search(q):
        infos = Catalog.query.filter(Catalog.description.contains(q)).all()
        return  jsonify(infos)

api.add_resource(CatalogREST, '/cat-item/<int:id>')
@dataclass
class History(Base):
    __tablename__ = 'history'  
    id: int
    card_id: int
    change_date: DateTime = Column(DateTime, default=func.now())
    description: str 
    
    id = Column(Integer, primary_key=True,  autoincrement=True)
    card_id = Column(Integer)
    change_date = Column(DateTime, default=func.now())
    description = Column(Text)

class HistoryREST(Resource):
    def get(self, card_id):
        infos = History.query.filter_by(card_id=card_id).order_by(History.change_date.desc()).all()
        return jsonify(infos)

    def post(self, card_id):
        data = request.get_json(force=True)
        description = data.get('description', '')
        history = History(
            card_id=card_id,
            description=description
        )
        db_session.add(history)
        db_session.commit()
        return jsonify({'message': 'History entry created'})


api.add_resource(HistoryREST, '/history/<int:card_id>')
@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)