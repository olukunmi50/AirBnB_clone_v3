#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    retrieves all location objects by city
    """
    location_list = []
    city_obj = storage.get("City", str(city_id))
    for obj in city_obj.places:
        location_list.append(obj.to_json())

    return jsonify(location_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    create location route
    :return: newly created location obj
    """
    location_json = request.get_json(silent=True)
    if location_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", location_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in location_json:
        abort(400, 'Missing user_id')
    if "name" not in location_json:
        abort(400, 'Missing name')

    location_json["city_id"] = city_id

    new_location =locatin(**location_json)
    new_location.save()
    resp = jsonify(new_location.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    gets a specific Place object by ID
    :return: place obj with the specified id or error
    """

    get_obj = storage.get("Place", str(place_id))

    if get_obj is None:
        abort(404)

    return jsonify(get_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    updates specific Place object by ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    location_json = request.get_json(silent=True)

    if location_json is None:
        abort(400, 'Not a JSON')

   get_obj = storage.get("Place", str(place_id))

    if get_obj is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(get_obj, key, val)

    get_obj.save()

    return jsonify(get_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    deletes Place by id
    :param place_id: Place object id
    :return: empty dict with 200 or 404 if not found
    """

   get_obj = storage.get("Place", str(place_id))

    if get_obj is None:
        abort(404)

    storage.delete(get_obj)
    storage.save()

    return jsonify({})
