from sqlalchemy.orm import Session

from .. import models


def search_scholarships(
    db: Session,
    keyword=None,
    major=None,
    state=None,
    citizenship=None
):

    query = db.query(
        models.Scholarship
    )


    if keyword:

        query = query.filter(
            models.Scholarship.name.contains(keyword)
            |
            models.Scholarship.eligibility.contains(keyword)
        )


    if major:

        query = query.filter(
            models.Scholarship.major == major
        )


    if state:

        query = query.filter(
            models.Scholarship.state == state
        )


    if citizenship:

        query = query.filter(
            models.Scholarship.citizenship == citizenship
        )


    return query.all()