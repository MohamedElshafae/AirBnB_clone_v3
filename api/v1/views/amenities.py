#!/usr/bin/python3
"""Create a new view for Amenity objects that handles"""

from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieve a list of all Amenity objects.

    Returns:
        JSON response: A JSON response containing
        a list of all Amenity objects.
    """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())

    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve a Amenity object."""
    Amenity = storage.get(Amenity, amenity_id)
    if Amenity is None:
        abort(404)
    return jsonify(Amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a Amenity object."""
    Amenity = storage.get(Amenity, amenity_id)
    if Amenity is None:
        abort(404)
    Amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a Amenity object."""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update a Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


if __name__ == '__main__':
    pass
