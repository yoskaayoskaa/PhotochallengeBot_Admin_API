from aiohttp.web import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema, docs
from aiohttp_session import new_session

from app.admin.schemes import AdminSchema, AdminLoginSchema, AdminResponseSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @docs(tags=["Admin"], summary="Login admin", description="Admin authentication")
    @request_schema(AdminLoginSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        email, password = self.data["email"], self.data["password"]
        admin = await self.store.admins.get_by_email(email=email)  # Admin | None

        if admin is None or not admin.is_password_valid(password=password):
            raise HTTPForbidden

        session = await new_session(request=self.request)
        session["admin"] = {"id": admin.id, "email": admin.email}

        return json_response(data=AdminSchema().dump(admin))


class AdminCurrentView(AuthRequiredMixin, View):
    @docs(tags=["Admin"], summary="Current admin", description="Show info about current admin if authenticated")
    @response_schema(AdminResponseSchema, 200)
    async def get(self):
        self.login_required(self.request)
        return json_response(data=AdminSchema().dump(self.request.admin))
