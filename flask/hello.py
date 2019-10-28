from flask import Flask
from flask_restful import Resource, Api
from flask import Response

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, '/hello')

@app.route('/hello', methods = ['GET'])
def api_hello():
    data = {"hello":"world"}

    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0:8080')
