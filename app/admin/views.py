from hashlib import sha256

from aiohttp_session import new_session, get_session
from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.models import Admin
from app.web.utils import json_response, error_json_response, hash_password
from app.web.app import View
from app.admin.schemes import AdminLoginResponseSchema, AdminLoginRequestSchema


class AdminLoginView(View):
    @docs()
    @request_schema(AdminLoginRequestSchema)
    @response_schema(AdminLoginResponseSchema, 200)
    async def post(self):
        raw_json = await self.request.json()
        admin = await self.store.admins.get_by_email(raw_json['email'])
        if admin is None:
            return error_json_response(http_status=403,
                                       message="Not Authorized",
                                       data={})
        if admin.password != hash_password(raw_json['password']):
            return error_json_response(http_status=403,
                                       message="Not Authorized",
                                       data={})
        session = await new_session(request=self.request)
        session['admin'] = admin.email
        return json_response(data=AdminLoginResponseSchema().dump(admin))


class AdminCurrentView(View):
    async def get(self):
        raise NotImplementedError
