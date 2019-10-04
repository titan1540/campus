import json
import os
import datetime
import copy

from flask import Flask, url_for, request, render_template, redirect
from flask import jsonify, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class RouteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    images = db.Column(db.Text(), unique=True, nullable=True)
    subscription = db.Column(db.Text(), unique=False, nullable=False)
    time_bound = db.Column(db.Text(), unique=False, nullable=False)
    categories = db.Column(db.Text(), unique=False, nullable=False)
    tags = db.Column(db.Text(), unique=False, nullable=False)

    def __repr__(self):
        return '<Route {} {}>'.format(
            self.id, self.name)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    routes = RouteModel.query.all()
    tags = set()
    for route_way in routes:
        way_tags = route_way.tags.split(';')
        for tag in way_tags:
            tags.add(tag)
    tags = list(tags)
    return render_template('search.html', routes=routes, tags=tags)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
