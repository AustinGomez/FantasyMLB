#!flask/bin/python
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

e = create_engine('sqlite:////var/www/api/api/players.db')

app = Flask(__name__)
api = Api(app)


# Gets a list of all years on record.
class Year_Meta(Resource):
    def get(self):
        conn = e.connect()

        query = conn.execute("select distinct yearID from batting")
        return {'years': [i[0] for i in query.cursor.fetchall()]}


# Returns a list of all stat categories
class Year_Categories(Resource):
    def get(self, yearID):
        return {'categories': ['batting', 'fielding', 'pitching']}


# Returns JSON containing all players and their respective stats.
class Year_Stat(Resource):
    def get(self, yearID, category):
        conn = e.connect()
        query = conn.execute("select * from {0} where yearID=(?)".format(category), (yearID,))
        result = {category: [dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        return result

api.add_resource(Year_Meta, '/years')
api.add_resource(Year_Categories, '/years/<string:yearID>')
api.add_resource(Year_Stat, '/years/<string:yearID>/<string:category>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
