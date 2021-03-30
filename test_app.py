
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
import json

def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

def test_post_user(client):
    res = client.post("/users", data=json.dumps({"name":"shaqued", "age": 24, "team":"good"}), headers={'Content-Type': 'application/json'})
    assert res.status_code == 200

    res_user = res.json["result"]
    assert res_user["name"] == "shaqued"
    assert res_user["age"] == 24
    assert res_user["team"] == "good"

def test_delete_user(client):
    res = client.delete("/users/1")
    assert res.status_code == 200
