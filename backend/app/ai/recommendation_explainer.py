def generate_explanation(student, scholarship, matched_on, explanations):
    why_you_match = []

    for item in explanations:
        category = item.get("category", "")
        details = item.get("details", [])

        if details:
            detail_text = ", ".join(details)

            if detail_text.endswith("."):
                detail_text = detail_text[:-1]

            why_you_match.append(
                f"{category}: {detail_text}."
            )

        elif category:
            why_you_match.append(
                f"Your {category.lower()} matches this scholarship."
            )

    missing_requirements = []

    if not student.gpa:
        missing_requirements.append(
            "Add your GPA to improve academic matching."
        )

    if not student.skills:
        missing_requirements.append(
            "Add technical skills to your profile."
        )

    if not student.projects:
        missing_requirements.append(
            "Add relevant projects to your profile."
        )

    if not student.leadership:
        missing_requirements.append(
            "Add leadership experience if applicable."
        )

    if not student.volunteer:
        missing_requirements.append(
            "Add volunteer experience if applicable."
        )

    if not student.certifications:
        missing_requirements.append(
            "Add certifications if applicable."
        )

    application_tip = (
        "Highlight your strongest matching skills, "
        "projects, and experiences in your application."
    )

    return {
        "why_you_match": why_you_match,
        "missing_requirements": missing_requirements,
        "application_tip": application_tip
    }







