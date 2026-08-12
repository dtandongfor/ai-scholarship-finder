"""Evaluate source-reviewed requirements that go beyond general match scoring."""


def evaluate_verified_requirements(student, scholarship):
    # Imported lazily to avoid the eligibility/state matcher import cycle.
    from .eligibility import normalize_state

    criteria = scholarship.requirements or {}
    review_items = []
    disqualifiers = []

    excluded_states = {
        normalize_state(state)
        for state in criteria.get("excluded_residency_states", [])
        if normalize_state(state)
    }
    student_state = normalize_state(student.state)
    if student_state and student_state in excluded_states:
        disqualifiers.append(
            "This opportunity is not open to residents of your state."
        )

    affiliation_keywords = [
        keyword.lower()
        for keyword in criteria.get("required_affiliation_keywords", [])
    ]
    if affiliation_keywords:
        affiliations = (getattr(student, "affiliations", None) or "").lower()
        if not any(keyword in affiliations for keyword in affiliation_keywords):
            disqualifiers.append(
                "This opportunity requires an employer, union, or organization affiliation that is not listed in your profile."
            )

    school_keywords = [keyword.lower() for keyword in criteria.get("required_school_keywords", [])]
    if school_keywords and not any(
        keyword in (student.university or "").lower() for keyword in school_keywords
    ):
        disqualifiers.append("This opportunity is limited to students at a specific school that is not listed in your profile.")

    if criteria.get("requires_demonstrated_financial_need"):
        if student.demonstrated_financial_need is None:
            review_items.append("Confirm that you meet the source's financial-need standard.")
        elif student.demonstrated_financial_need is False:
            disqualifiers.append("This opportunity requires demonstrated financial need.")

    minimum_term_credits = criteria.get("min_planned_term_credits")
    if minimum_term_credits is not None:
        if student.planned_term_credits is None:
            review_items.append("Add your planned term credit load to confirm this requirement.")
        elif student.planned_term_credits < minimum_term_credits:
            disqualifiers.append(f"Requires enrollment in at least {minimum_term_credits} credits per term.")

    checks = (
        ("requires_financial_aid_submission", "financial_aid_submitted", "Complete the FAFSA or the source's listed financial-aid application."),
        ("requires_pell_eligibility", "pell_eligible", "Confirm whether you are Pell eligible."),
        ("requires_full_time", "enrollment_status", "Confirm that you will enroll full time."),
        ("requires_good_standing", "disciplinary_good_standing", "Confirm that you are in good disciplinary standing."),
        ("requires_service_commitment", "accepts_service_commitment", "Confirm that you accept the required post-graduation service commitment."),
        ("requires_first_generation", "is_first_generation", "Confirm that you meet the first-generation student definition used by this opportunity."),
        ("requires_women_tech_eligibility", "eligible_for_women_tech_scholarships", "Confirm that you meet this opportunity's women-in-technology eligibility definition."),
        ("requires_security_clearance_eligibility", "can_seek_security_clearance", "Confirm that you can pursue the security clearance required by this opportunity."),
    )
    for criterion, attribute, message in checks:
        if not criteria.get(criterion):
            continue
        value = getattr(student, attribute, None)
        if value is None:
            review_items.append(message)
        elif criterion == "requires_full_time" and value != "full_time":
            disqualifiers.append("This opportunity requires full-time enrollment.")
        elif criterion != "requires_full_time" and value is False:
            disqualifiers.append(message)

    for criterion, attribute, label in (
        ("min_completed_credits", "completed_credits", "earned credits"),
        ("min_volunteer_hours", "volunteer_hours", "volunteer hours"),
        ("min_work_hours", "work_hours", "paid work hours"),
    ):
        minimum = criteria.get(criterion)
        if minimum is None:
            continue
        value = getattr(student, attribute, None)
        if value is None:
            review_items.append(f"Add your {label} to confirm this requirement.")
        elif value < minimum:
            disqualifiers.append(f"Requires at least {minimum} {label}.")

    if not scholarship.requirements_complete:
        review_items.append("The official requirements for this opportunity are still being fully structured and reviewed.")

    return {
        "disqualifiers": disqualifiers,
        "review_items": review_items,
        "application_checklist": criteria.get("application_checklist", []),
        "selection_notes": criteria.get("selection_notes", []),
    }
