from datetime import datetime, timedelta

import pandas as pd
import pytz
from flasgger import SwaggerView, fields
from marshmallow import Schema
from webargs.flaskparser import use_kwargs

from src.db.datasets import get_wave_df, get_tides_df, get_weather_df, \
    get_wind_df, get_conditions_df, available_spots_df
from src.db.model import db, Spot


class APISchema(Schema):
    class Meta:
        strict = True


def parse_spot(spot_id):
    return db.session.query(Spot).filter_by(api_id=spot_id).one()


class Resource(APISchema):
    start_date = fields.DateTime(
        missing=(datetime.now(tz=pytz.utc) - timedelta(days=300)).isoformat())
    spot = fields.Function(
        missing="5842041f4e65fad6a7708c8d", deserialize=parse_spot, load_from='spot_id')


class GlobalConditionsView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the global conditions at once. """
        df_wave = get_wave_df(spot, start_date)
        df_tides = get_tides_df(spot, start_date)
        df_weather = get_weather_df(spot, start_date)
        df_wind = get_wind_df(spot, start_date)

        def suffix(df, suffix="", inplace=False):
            return df.rename(
                columns={c: suffix + c for c in df.columns if c != "timestamp"},
                inplace=inplace)

        df = pd.merge(
            suffix(df_wave, "wave_"), suffix(df_wind, "wind_"), on='timestamp')
        df = pd.merge(
            df, suffix(df_weather, "weather_"), on='timestamp')
        df = pd.merge(
            df, suffix(df_tides, "tides_"), on='timestamp')

        return df.to_json(orient='records')


class TidesView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the tides data. """
        df = get_tides_df(spot, start_date)
        return df.to_json(orient='records')


class WindView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the wind data. """
        df = get_wind_df(spot, start_date)
        return df.to_json(orient='records')


class ConditionsView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the conditions data. """
        df = get_conditions_df(spot, start_date)
        return df.to_json(orient='records')


class WavesView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the waves data. """
        df = get_wave_df(spot, start_date)
        return df.to_json(orient='records')


class WeatherView(SwaggerView):
    parameters = Resource

    @use_kwargs(Resource())
    def get(self, spot, start_date):
        """ Gets the weather data. """
        df = get_weather_df(spot, start_date)
        return df.to_json(orient='records')


class SpotView(SwaggerView):
    def get(self):
        df = available_spots_df()
        return df.to_json(orient='records')
