import pandas as pd

from src.db.model import db, Wave, Weather, Conditions, Wind, Tide, Spot


def make_df(table, spot, start_date):
    query = db.session.query(table)
    if spot is not None:
        query = query.filter_by(spot_id=spot.api_id)
    if start_date is not None:
        query = query.filter(table.timestamp > start_date)
    query = query.order_by(table.timestamp.asc())
    return pd.read_sql_query(query.statement, db.session.bind)


def get_wave_df(spot, start_date):
    return make_df(Wave, spot, start_date)


def get_weather_df(spot, start_date):
    return make_df(Weather, spot, start_date)


def get_conditions_df(spot, start_date):
    return make_df(Conditions, spot, start_date)


def get_wind_df(spot, start_date):
    return make_df(Wind, spot, start_date)


def get_tides_df(spot, start_date):
    return make_df(Tide, spot, start_date)


def available_spots():
    return {spot.api_id for spot in db.session.query(Spot)}


def available_spots_df():
    query = db.session.query(Spot).filter(Spot.country.isnot(None)).order_by(Spot.name.asc())
    return pd.read_sql_query(query.statement, db.session.bind)
