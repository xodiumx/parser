from datetime import datetime

from sqlalchemy import (Column, Date, Integer, Numeric, String, Table,
                        UniqueConstraint, )

from db.connect import metadata


petrovich_analytics = Table(
    'petrovich_analytics',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('vimos_name', String(512), nullable=True, ),
    Column('vimos_gcode', String(512), nullable=True, ),
    Column(
        'vimos_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('petrovich_name', String(512), nullable=True, ),
    Column(
        'petrovich_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('vimos_category', String(128), nullable=True),
    Column(
        'abs_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'relative_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    UniqueConstraint(
        'vimos_name', 'created_at', name='petrovich_analytics_unique'),
)

stroyudacha_analytics = Table(
    'stroyudacha_analytics',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('vimos_name', String(512), nullable=True, ),
    Column(
        'vimos_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('stroyudacha_name', String(512), nullable=True, ),
    Column(
        'stroyudacha_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('vimos_category', String(128), nullable=True),
    Column(
        'abs_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'relative_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    UniqueConstraint(
        'vimos_name', 'created_at', name='stroyudacha_analytics_unique'),
)

saturn_analytics = Table(
    'saturn_analytics',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('vimos_name', String(512), nullable=True, ),
    Column(
        'vimos_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('saturn_name', String(512), nullable=True, ),
    Column(
        'saturn_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('vimos_category', String(128), nullable=True),
    Column(
        'abs_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'relative_diff',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    UniqueConstraint(
        'vimos_name', 'created_at', name='saturn_analytics_unique'),
)
