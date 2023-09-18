from datetime import datetime

from sqlalchemy import (DECIMAL, Boolean, Column, Date, Integer, Numeric,
                        String, Table, )

from db.connect import metadata

petrovich_products = Table(
    'petrovich_products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String(512), nullable=True, ),
    Column('gcode', String(512), nullable=True, ),
    Column(
        'price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'cart_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('currency', String(10), nullable=True, ),
    Column('url', String(512), nullable=True, ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('measurement', String(64), nullable=True),
    Column('category', String(128), nullable=True),
    Column('exists', Boolean, nullable=True),
)

stroyudacha_products = Table(
    'stroyudacha_products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String(512), nullable=True, ),
    Column('gcode', String(512), nullable=True, ),
    Column(
        'price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'cart_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('currency', String(10), nullable=True, ),
    Column('url', String(512), nullable=True, ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('measurement', String(64), nullable=True),
    Column('category', String(128), nullable=True),
    Column('exists', Boolean, nullable=True),
)

saturn_products = Table(
    'saturn_products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String(512), nullable=True, ),
    Column('gcode', String(512), nullable=True, ),
    Column(
        'price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'cart_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('currency', String(10), nullable=True, ),
    Column('url', String(512), nullable=True, ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('measurement', String(64), nullable=True),
    Column('category', String(128), nullable=True),
    Column('exists', Boolean, nullable=True),
)

leroy_products = Table(
    'leroy_products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('gcode', String(512), nullable=True, ),
    Column('name', String(512), nullable=True, ),
    Column(
        'price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column(
        'cart_price',
        Numeric(asdecimal=True, decimal_return_scale=1),
        nullable=True
    ),
    Column('currency', String(10), nullable=True, ),
    Column('url', String(512), nullable=True, ),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('measurement', String(64), nullable=True),
    Column('category', String(128), nullable=True),
    Column('exists', Boolean, nullable=True),
)

vimos_products = Table(
    'vimos_products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String(512), nullable=True, ),
    Column('gcode', String(512), nullable=True, ),
    Column('price', DECIMAL, nullable=True),
    Column(
        'created_at',
        Date,
        default=datetime.now,
    ),
    Column('measurement', String(64), nullable=True),
    Column('currency', String(10), nullable=True, ),
    Column('category', String(512), nullable=True, ),
)
