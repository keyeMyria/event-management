from flask.ext.restplus import Namespace

from app.models.microlocation import Microlocation as MicrolocationModel
from app.api.helpers import custom_fields as fields
from app.api.helpers.helpers import (
    can_create,
    can_update,
    can_delete,
    requires_auth
)
from app.api.helpers.utils import PAGINATED_MODEL, PaginatedResourceBase, ServiceDAO, \
    PAGE_PARAMS, POST_RESPONSES, PUT_RESPONSES, SERVICE_RESPONSES
from app.api.helpers.utils import Resource, ETAG_HEADER_DEFN

api = Namespace('microlocations', description='Microlocations', path='/')

MICROLOCATION = api.model('Microlocation', {
    'id': fields.Integer(required=True),
    'name': fields.String(required=True),
    'latitude': fields.Float(),
    'longitude': fields.Float(),
    'floor': fields.Integer(),
    'room': fields.String(),
})

MICROLOCATION_PAGINATED = api.clone('MicrolocationPaginated', PAGINATED_MODEL, {
    'results': fields.List(fields.Nested(MICROLOCATION))
})

MICROLOCATION_POST = api.clone('MicrolocationPost', MICROLOCATION)
del MICROLOCATION_POST['id']


# Create DAO
class MicrolocationDAO(ServiceDAO):
    version_key = 'microlocations_ver'


DAO = MicrolocationDAO(MicrolocationModel, MICROLOCATION_POST)


@api.route('/events/<int:event_id>/microlocations/<int:microlocation_id>')
@api.doc(responses=SERVICE_RESPONSES)
class Microlocation(Resource):
    @api.doc('get_microlocation')
    @api.header(*ETAG_HEADER_DEFN)
    @api.marshal_with(MICROLOCATION)
    def get(self, event_id, microlocation_id):
        """Fetch a microlocation given its id"""
        return DAO.get(event_id, microlocation_id)

    @requires_auth
    @can_delete(DAO)
    @api.doc('delete_microlocation')
    @api.marshal_with(MICROLOCATION)
    def delete(self, event_id, microlocation_id):
        """Delete a microlocation given its id"""
        return DAO.delete(event_id, microlocation_id)

    @requires_auth
    @can_update(DAO)
    @api.doc('update_microlocation', responses=PUT_RESPONSES)
    @api.marshal_with(MICROLOCATION)
    @api.expect(MICROLOCATION_POST)
    def put(self, event_id, microlocation_id):
        """Update a microlocation given its id"""
        return DAO.update(event_id, microlocation_id, self.api.payload)


@api.route('/events/<int:event_id>/microlocations')
class MicrolocationList(Resource):
    @api.doc('list_microlocations')
    @api.header(*ETAG_HEADER_DEFN)
    @api.marshal_list_with(MICROLOCATION)
    def get(self, event_id):
        """List all microlocations"""
        return DAO.list(event_id)

    @requires_auth
    @can_create(DAO)
    @api.doc('create_microlocation', responses=POST_RESPONSES)
    @api.marshal_with(MICROLOCATION)
    @api.expect(MICROLOCATION_POST)
    def post(self, event_id):
        """Create a microlocation"""
        return DAO.create(
            event_id,
            self.api.payload,
            self.api.url_for(self, event_id=event_id)
        )


@api.route('/events/<int:event_id>/microlocations/page')
class MicrolocationListPaginated(Resource, PaginatedResourceBase):
    @api.doc('list_microlocations_paginated', params=PAGE_PARAMS)
    @api.header(*ETAG_HEADER_DEFN)
    @api.marshal_with(MICROLOCATION_PAGINATED)
    def get(self, event_id):
        """List microlocations in a paginated manner"""
        args = self.parser.parse_args()
        return DAO.paginated_list(args=args, event_id=event_id)
