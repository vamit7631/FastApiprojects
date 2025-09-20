from fastapi import APIRouter
from app.api.v1.controllers.user import router as user_router
from app.api.v1.controllers.auth import router as auth_router
from app.api.v1.controllers.organisation import router as org_router
from app.api.v1.controllers.role import router as role_router
from app.api.v1.controllers.module import router as module_router
from app.api.v1.controllers.permission import router as permission_router

routers = APIRouter()

router_list = [user_router, auth_router, org_router, role_router, module_router, permission_router]

for router in router_list:
    router.tags.append("v1")
    routers.include_router(router)