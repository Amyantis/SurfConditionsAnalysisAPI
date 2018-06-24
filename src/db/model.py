from datetime import datetime

from dateutil.tz import tzutc
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, types

db = SQLAlchemy()


class UTCDateTime(types.TypeDecorator):
    impl = types.DateTime

    def process_result_value(self, value, engine):
        if value is None:
            return
        return value.replace(tzinfo=tzutc())


class AlreadyReadFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False,
                          default=datetime.utcnow)


class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


class Wave(db.Model):
    __table_args__ = (
        UniqueConstraint('spot_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.String,
                        db.ForeignKey('spot.api_id', ondelete='CASCADE'),
                        nullable=False)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False)

    surf_max = db.Column(db.Float, nullable=False)
    surf_min = db.Column(db.Float, nullable=False)
    surf_optimalScore = db.Column(db.Float, nullable=False)
    wave_direction_0 = db.Column(db.Float, nullable=False)
    wave_height_0 = db.Column(db.Float, nullable=False)
    wave_optimalScore_0 = db.Column(db.Float, nullable=False)
    wave_period_0 = db.Column(db.Float, nullable=False)
    wave_direction_1 = db.Column(db.Float, nullable=False)
    wave_height_1 = db.Column(db.Float, nullable=False)
    wave_optimalScore_1 = db.Column(db.Float, nullable=False)
    wave_period_1 = db.Column(db.Float, nullable=False)
    wave_direction_2 = db.Column(db.Float, nullable=False)
    wave_height_2 = db.Column(db.Float, nullable=False)
    wave_optimalScore_2 = db.Column(db.Float, nullable=False)
    wave_period_2 = db.Column(db.Float, nullable=False)
    wave_direction_3 = db.Column(db.Float, nullable=False)
    wave_height_3 = db.Column(db.Float, nullable=False)
    wave_optimalScore_3 = db.Column(db.Float, nullable=False)
    wave_period_3 = db.Column(db.Float, nullable=False)
    wave_direction_4 = db.Column(db.Float, nullable=False)
    wave_height_4 = db.Column(db.Float, nullable=False)
    wave_optimalScore_4 = db.Column(db.Float, nullable=False)
    wave_period_4 = db.Column(db.Float, nullable=False)
    wave_direction_5 = db.Column(db.Float, nullable=False)
    wave_height_5 = db.Column(db.Float, nullable=False)
    wave_optimalScore_5 = db.Column(db.Float, nullable=False)
    wave_period_5 = db.Column(db.Float, nullable=False)

    spot = db.relationship("Spot")


class Conditions(db.Model):
    __table_args__ = (
        UniqueConstraint('spot_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.String,
                        db.ForeignKey('spot.api_id', ondelete='CASCADE'),
                        nullable=False)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False)

    am_humanRelation = db.Column(db.String, nullable=False)
    am_maxHeight = db.Column(db.Float, nullable=False)
    am_minHeight = db.Column(db.Float, nullable=False)
    am_occasionalHeight = db.Column(db.Float, nullable=True)
    am_plus = db.Column(db.Boolean, nullable=False)
    am_rating = db.Column(db.Float, nullable=True)
    forecaster = db.Column(db.Float, nullable=True)
    human = db.Column(db.Boolean, nullable=False)
    observation = db.Column(db.String, nullable=False)
    pm_humanRelation = db.Column(db.String, nullable=False)
    pm_maxHeight = db.Column(db.Float, nullable=False)
    pm_minHeight = db.Column(db.Float, nullable=False)
    pm_occasionalHeight = db.Column(db.Float, nullable=True)
    pm_plus = db.Column(db.Boolean, nullable=False)
    pm_rating = db.Column(db.Float, nullable=True)

    spot = db.relationship("Spot")


class Tide(db.Model):
    __table_args__ = (
        UniqueConstraint('spot_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.String,
                        db.ForeignKey('spot.api_id', ondelete='CASCADE'),
                        nullable=False)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False)

    height = db.Column(db.Float, nullable=False)
    type = db.Column(db.String, nullable=False)

    spot = db.relationship("Spot")


class Weather(db.Model):
    __table_args__ = (
        UniqueConstraint('spot_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.String,
                        db.ForeignKey('spot.api_id', ondelete='CASCADE'),
                        nullable=False)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False)

    condition = db.Column(db.String, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

    spot = db.relationship("Spot")


class Wind(db.Model):
    __table_args__ = (
        UniqueConstraint('spot_id', 'timestamp'),
    )
    id = db.Column(db.Integer, primary_key=True)

    spot_id = db.Column(db.String,
                        db.ForeignKey('spot.api_id', ondelete='CASCADE'),
                        nullable=False)
    timestamp = db.Column(UTCDateTime(timezone=True), nullable=False)

    direction = db.Column(db.Float, nullable=False)
    optimalScore = db.Column(db.Float, nullable=False)
    speed = db.Column(db.Float, nullable=False)

    spot = db.relationship("Spot")
