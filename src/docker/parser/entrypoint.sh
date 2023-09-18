#!/bin/bash

sleep 15

# Use migrations

alembic upgrade head

# Start parsing

# scrapy crawl stroydacha