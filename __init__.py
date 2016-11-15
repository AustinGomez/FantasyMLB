#!flask/bin/python
from flask import Flask, request, make_response, jsonify, Response, abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

e = create_engine('sqlite:////var/www/api/api/baseball.db')

app = Flask(__name__)
api = Api(app, catch_all_404s=True)


# Returns JSON containing all playerIDs, and their respective first names and last names 
class PlayerList(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select distinct playerID, nameFirst, nameLast from master")
        data ={'data':[dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        dump = dumps(data)
        response =  Response(dump, status=200, mimetype='application/json')
        return response

# Returns a JSON containing all batting and fielding stats for a specific playerID, a different json object for each year, position, or team
# TODO: add functionality to only include stats for their respective position
class Player(Resource):
    def get(self, playerID):
        conn = e.connect()
        find_query = conn.execute("select * from master where playerID=(?)", (playerID,))
        print playerID
        print find_query.cursor.rowcount
        if len(find_query.fetchall())== 0:
            abort(404, description="Player with playerID {0} not found.".format(playerID))

        query = conn.execute("select batters.*, fielders.POS, fielders.G, fielders.InnOuts, fielders.PO, fielders.A, fielders.E, fielders.DP, fielders.PB, fielders.WP, fielders.SB, fielders.CS, fielders.ZR from batters inner join fielders on (batters.playerID=fielders.playerID and batters.yearID=fielders.yearID and batters.teamID=fielders.teamID) where batters.playerID=(?)", (playerID,))

        data = {'data':[dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        dump = dumps(data)

        response =  Response(dump, status=200, mimetype='application/json') 
        return response

# Returns JSON containing a players batting and fielding stats for a specific year in the same format as above.
class PlayerYear(Resource):
    def get(self, playerID, yearID):
        conn = e.connect()
  
        query = conn.execute("select batters.*, fielders.POS, fielders.G, fielders.InnOuts, fielders.PO, fielders.A, fielders.E, fielders.DP, fielders.PB, fielders.WP, fielders.SB, fielders.CS, fielders.ZR from batters inner join fielders on (batters.playerID=fielders.playerID and batters.yearID=fielders.yearID and batters.teamID=fielders.teamID) where batters.playerID=(?) and batters.yearID=(?)", (playerID, yearID))
        data = {'data':[dict(zip(tuple (query.keys()), i)) for i in query.cursor]}
        dump = dumps(data)
        response =  Response(dump, status=200, mimetype='application.json')
        return response


class Year_Batter(Resource):
    def get(self, yearID, category, playerID):
        conn = e.connect()
        query = conn.execute("select * from {0} where yearID=(?) and playerID=(?)".format(category), (yearID, playerID))
        data = {'data': [dict(zip(tuple (query.keys()), i)) for i in query.cursor]} 
        dump = dumps(data)
        response = Response(dump, status=200, mimetype='application.json')
        return response

api.add_resource(PlayerList, '/api/v1.0/players/')
api.add_resource(Player, '/api/v1.0/players/<string:playerID>/')
api.add_resource(PlayerYear, '/api/v1.0/players/<string:playerID>/<string:yearID>/')
api.add_resource(Year_Batter, '/years/<string:yearID>/<string:category>/<string:playerID>/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
