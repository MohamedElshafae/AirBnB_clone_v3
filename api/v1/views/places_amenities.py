#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions.
"""
from os import getenv
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from models.user import User

storage_type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """Get all Amenities."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage_type == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    all_amenities = []
    for amenity in amenities:
        all_amenities.append(amenity.to_dict())
    return jsonify(all_amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Delete amenity by id depending on storage."""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        p_amenities = place.amenities
    else:
        p_amenities = place.amenity_ids
    if amenity not in amenities:
        abort(404)
    p_amenity.remove(amenity)
    place.save()
    return jsonify({}), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    """Create amenities depending on storage."""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if place is None or amenity is None:
        abort(404)
    if storage_type == 'db':
        p_amenities = place.amenities
    else:
        p_amenities = place.amenity_ids
    if amenity not in amenities:
        abort(404)
    p_amenity.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
