from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/users")
def get_users() -> Tuple[Response, int]:
    users = db.get('users')
    filterByField = lambda user, field: str(user[field]) == request.args[field]
    fields = ["team", "age"]

    for field in fields:
        if field in request.args:
            users = list(filter(lambda user: filterByField(user, field), users))

    return create_response({"users": users})


@app.route("/users/<int:id>")
def get_user(id : int) -> Tuple[Response, int]:
    user = db.getById('users', id)

    if user is None:
        return create_response(status=404, message="user cannot be found")

    return create_response({"user": user})


@app.route('/users', methods=['POST'])
def post() -> Tuple[Response, int]:
    data = request.json
    new_user = db.create('users', data)

    return create_response(new_user)

@app.route('/users/<int:id>', methods=['PUT'])
def put(id: int) -> Tuple[Response, int]:
    data = request.json
    keys = ['name', 'age', 'team']
    props = dict((k, data[k]) for k in keys if k in data)
    updated_user = db.updateById('users', id, props)

    if updated_user is None:
        return create_response(status=404, message="user to update cannot be found")

    return create_response(updated_user)

@app.route('/users/<int:id>', methods=['DELETE'])
def delete(id: int) -> Tuple[Response, int]:
    user = db.getById('users', id)

    if user is None:
        return create_response(status=404, message="user to delete cannot be found")

    db.deleteById('users', id)

    return create_response(status=200, message="deleted user successfully")

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
