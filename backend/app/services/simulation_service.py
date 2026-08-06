from .. import crud
from ..ai import simulator


def simulate(
    db,
    student_id,
    improvement
):

    student = crud.get_student(
        db,
        student_id
    )

    scholarships = crud.get_scholarships(
        db
    )

    return simulator.simulate_improvement(
        student,
        scholarships,
        improvement
    )