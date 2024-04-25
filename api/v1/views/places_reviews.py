#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    retrieves all Review objects by place
   
    """
    review_lists = []
    places_obj = storage.get("Place", str(place_id))

    if places_obj is None:
        abort(404)

    for obj in places_obj.reviews:
        review_lists.append(obj.to_json())

    return jsonify(review_lists)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """
    create REview route
    newly created Review obj
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    reply = jsonify(new_review.to_json())
    reply.status_code = 201

    return reply


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    gets a specific Review object by ID
    review obj with the specified id or error
   
    """

    get_obj = storage.get("Review", str(review_id))

    if get_obj is None:
        abort(404)

    return jsonify(get_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    updates specific Review object by ID
  
    """
    location_json = request.get_json(silent=True)

    if location_json is None:
        abort(400, 'Not a JSON')

   get_obj = storage.get("Review", str(review_id))

    if get_obj is None:
        abort(404)

    for key, val in location_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(get_obj, key, val)

    get_obj.save()

    return jsonify(get_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    deletes Review by id
    """

    get_obj = storage.get("Review", str(review_id))

    if get_obj is None:
        abort(404)

    storage.delete(get_obj)
    storage.save()

    return jsonify({})
