from hashlib import sha256

from aiohttp_session import new_session, get_session
from aiohttp_apispec import docs, request_schema, response_schema

from app.admin.models import Admin
from app.web.utils import json_response, error_json_response, hash_password
from app.web.app import View
from app.admin.schemes import AdminLoginResponseSchema, AdminLoginRequestSchema, AdminCurrentResponseSchema


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
                                       message="Not Authorized")
        session = await new_session(request=self.request)
        # TODO: need to Add Admin, but just now cannot because Admin type is not jsonable
        session['admin'] = admin.email
        return json_response(data=AdminLoginResponseSchema().dump(admin))


class AdminCurrentView(View):
    @docs()
    @response_schema(AdminCurrentResponseSchema, 200)
    async def get(self):
        session = await get_session(self.request)
        if "admin" not in session:
            return error_json_response(http_status=401,
                                       message="Not Authorized")
        admin_email = session["admin"]
        admin = await self.store.admins.get_by_email(admin_email)
        return json_response(data=AdminCurrentResponseSchema().dump(admin))
