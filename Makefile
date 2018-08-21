SHELL := /usr/bin/env bash


run:
	python main.py


setup:
	touch .env
	touch db/watchlist