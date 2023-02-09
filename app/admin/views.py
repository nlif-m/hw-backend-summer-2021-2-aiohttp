from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_session import new_session
from aiohttp_apispec import docs, request_schema, response_schema, json_schema

from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response, hash_password
from app.web.app import View
from app.admin.schemes import (
    AdminLoginResponseSchema,
    AdminLoginRequestSchema,
    AdminCurrentResponseSchema,
    AdminSchema,
)


class AdminLoginView(View):
    @docs()
    @json_schema(AdminLoginRequestSchema)
    @response_schema(AdminLoginResponseSchema, 200)
    async def post(self):
        raw_body = await self.request.json()
        admin = await self.store.admins.get_by_email(raw_body["email"])
        if admin is None:
            raise HTTPForbidden(reason="not found admin")
        if hash_password(raw_body["password"]) != admin.password:
            raise HTTPForbidden(reason="invalid password")
        session = await new_session(self.request)
        raw_admin = AdminSchema().dump(admin)
        session["admin"] = raw_admin
        return json_response(data=raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @docs()
    @response_schema(AdminCurrentResponseSchema, 200)
    async def get(self):
        return json_response(data=AdminCurrentResponseSchema().dump(self.request.admin))
