import os

from datetime import datetime, timedelta
from sqlalchemy import select
from .database import configure,Base
from . import models

def create_app(database_url=None):
    from flask import Flask, render_template
    app=Flask(__name__)
    app.config['SECRET_KEY']=os.getenv('SECRET_KEY','development-key-change-me')
    engine,maker=configure(database_url)
    Base.metadata.create_all(engine)
    app.extensions['session_factory']=maker
    from .routes.web import bp as web
    from .routes.api import bp as api
    app.register_blueprint(web);app.register_blueprint(api)
    @app.errorhandler(404)
    def not_found(e):return render_template('404.html'),404
    @app.errorhandler(500)
    def server_error(e):return render_template('error.html',message='Внутренняя ошибка'),500
    @app.cli.command('seed-demo')
    def seed_demo():
        with maker.begin() as session:
            stations = []
            for name in ('Москва', 'Казань', 'Санкт-Петербург'):
                station = session.scalar(select(models.Station).where(models.Station.name == name))
                if station is None:
                    station = models.Station(name=name)
                    session.add(station)
                stations.append(station)
            session.flush()
            routes = [(stations[0], stations[1]), (stations[1], stations[0]), (stations[0], stations[2])]
            for index, (origin, destination) in enumerate(routes, start=1):
                number = f'РЖД-{900 + index}'
                if session.scalar(select(models.Train.id).where(models.Train.number == number)) is None:
                    session.add(models.Train(
                        number=number,
                        origin_id=origin.id,
                        destination_id=destination.id,
                        departure=(datetime.now() + timedelta(days=index)).replace(hour=12, minute=0),
                        fare=1800 + index * 350,
                        seats=50,
                    ))

    return app
