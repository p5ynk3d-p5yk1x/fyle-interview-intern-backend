from flask import Blueprint
from core import db
from core.apis import decorators
from core.libs import assertions


from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum

from core.apis.assignments.schema import AssignmentSchema
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

@principal_assignments_resources.route('/', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_submitted_assignments(p):
    assignments  = Assignment.filter(Assignment.state.in_([AssignmentStateEnum.GRADED,AssignmentStateEnum.SUBMITTED]))
    a_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=a_dump)


@principal_assignments_resources.route('/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    assertions.assert_valid(incoming_payload['id'] is not None, "Enter Assignment Id")    
    assDCheck = Assignment.get_by_id(incoming_payload['id'])
    assertions.assert_found(assDCheck, 'No assignment with this id was found')
    assertions.assert_valid(assDCheck.state is not AssignmentStateEnum.DRAFT, "Assignment Not Submitted")
    assignment = Assignment.mark_grade(incoming_payload['id'], incoming_payload['grade'],p)
    a_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=a_dump)