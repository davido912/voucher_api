from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from deprecate.security_api import auth, identity

app = Flask(__name__)
app.secret_key = "jose"
jwt = JWT(app, auth, identity)


items = []


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": None}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"message": f"ITEM {name} ALREADY EXISTS"}, 400
        # data = request.get_json(force=True) # forces JSON formatting headers
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"items": items}


if __name__ == '__main__':
    api = Api(app)
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    app.run(port=5000, debug=True)