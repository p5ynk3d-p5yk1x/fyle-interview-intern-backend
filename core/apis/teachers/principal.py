from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.assignments import Assignment,AssignmentStateEnum

from .schema import TeacherSchema
from core.apis.assignments.schema import AssignmentSchema
principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    teachers = Teacher.get_teachers()
    t_dump = TeacherSchema().dump(teachers, many = True)
    return APIResponse.respond(data=t_dump)

