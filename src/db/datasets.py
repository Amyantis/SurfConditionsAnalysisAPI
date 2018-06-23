import pandas as pd

from src.db.model import db, Wave, Weather, Conditions, Wind, Tide


def get_wave_df():
    query = db.session.query(Wave).order_by(Wave.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)


def get_weather_df():
    query = db.session.query(Weather).order_by(Weather.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)


def get_conditions_df():
    query = db.session.query(Conditions).order_by(Conditions.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)


def get_wind_df():
    query = db.session.query(Wind).order_by(Wind.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)


def get_tides_df():
    query = db.session.query(Tide).order_by(Tide.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)
