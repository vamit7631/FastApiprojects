from app.models.role_model import RoleModel
from app.models.role_permissions_model import RolePermission
from app.models.sub_module_model import SubModuleModel
from app.models.permission_model import Permission
from app.models.module_model import ModuleModel
from app.models.user_model import User
from app.models.organisation_model import Organisation
# Import other models as needed

from sqlalchemy.orm import configure_mappers

# This forces SQLAlchemy to resolve all string relationships now
configure_mappers()