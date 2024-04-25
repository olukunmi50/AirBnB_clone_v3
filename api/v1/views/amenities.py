#!/usr/bin/python3
"""
route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    retrieves all Amenity objects
    :return: json of all states
    """
    amenities_list = []
    amenities_obj = storage.all("Amenity")
    for obj in amenities_obj.values():
        amenities_list.append(obj.to_json())

    return jsonify(amenities_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    create amenity route
    :return: newly created amenity obj
    """
    amenities_json = request.get_json(silent=True)
    if amenities_json is None:
        abort(400, 'Not a JSON')
    if "name" not in am_json:
        abort(400, 'Missing name')

    new_amenities = Amenity(**am_json)
    new_amenities.save()
    resp = jsonify(new_amenities.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    gets a specific Amenity object by ID
    :param amenity_id: amenity object id
    :return: state obj with the specified id or error
    """

   get_obj = storage.get("Amenity", str(amenity_id))

    if get_obj is None:
        abort(404)

    return jsonify(get_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    :return: amenity object and 200 on success, or 400 or 404 on failure
    """
    amenities_json = request.get_json(silent=True)
    if amenities_json is None:
        abort(400, 'Not a JSON')
    get_obj = storage.get("Amenity", str(amenity_id))
    if get_obj is None:
        abort(404)
    for key, val in am_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(get_obj, key, val)
    get_obj.save()
    return jsonify(get_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    :return: empty dict with 200 or 404 if not found
    """

    get_obj = storage.get("Amenity", str(amenity_id))

    if get_obj is None:
        abort(404)

    storage.delete(get_obj)
    storage.save()

    return jsonify({})
