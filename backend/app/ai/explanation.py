from ..matching.utils import normalize_list, semantic_match
from ..matching.knowledge import (
    MAJOR_GROUPS,
    INTEREST_SYNONYMS,
    SKILL_SYNONYMS,
    LEADERSHIP_KEYWORDS,
    VOLUNTEER_KEYWORDS,
    CERTIFICATION_GROUPS,
)


def is_real_requirement(value):
    """
    Determines whether a field contains a meaningful value.
    """

    if value is None:
        return False

    value = str(value).strip().lower()

    if not value:
        return False

    invalid_values = {
        "string",
        "none",
        "null",
        "n/a",
        "na",
    }

    return value not in invalid_values


def text_matches(
    student_value,
    scholarship_value,
    knowledge_base=None
):
    """
    Determines whether two comma-separated text fields match.

    Supports:
    - Exact matching
    - Semantic matching through a knowledge base
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_items = normalize_list(
        str(student_value)
    )

    scholarship_items = normalize_list(
        str(scholarship_value)
    )

    if not student_items or not scholarship_items:
        return False

    # Exact match
    for scholarship_item in scholarship_items:

        if scholarship_item in student_items:
            return True

    # Semantic match
    if knowledge_base:

        matched, _, _ = semantic_match(
            student_items,
            scholarship_items,
            knowledge_base
        )

        if matched:
            return True

    return False


def major_matches(
    student_major,
    scholarship_major
):
    """
    Determines whether the student's major matches
    the scholarship requirement.
    """

    if not is_real_requirement(student_major):
        return False

    if not is_real_requirement(scholarship_major):
        return False

    student_major = str(
        student_major
    ).strip().lower()

    scholarship_major = str(
        scholarship_major
    ).strip().lower()

    # Exact match
    if student_major == scholarship_major:
        return True

    # Major group match
    for group_name, majors in MAJOR_GROUPS.items():

        group_name = group_name.lower()

        majors = [
            major.lower()
            for major in majors
        ]

        scholarship_matches_group = (
            scholarship_major == group_name
            or scholarship_major in majors
        )

        student_matches_group = (
            student_major == group_name
            or student_major in majors
        )

        if (
            scholarship_matches_group
            and student_matches_group
        ):
            return True

    return False


def gpa_matches(
    student_gpa,
    scholarship_gpa
):
    """
    Determines whether the student's GPA meets
    the scholarship GPA requirement.
    """

    if not is_real_requirement(student_gpa):
        return False

    if not is_real_requirement(scholarship_gpa):
        return False

    try:
        student_gpa = float(student_gpa)
        scholarship_gpa = float(scholarship_gpa)
    except (ValueError, TypeError):
        return False

    return student_gpa >= scholarship_gpa


def keyword_match(
    student_value,
    scholarship_value,
    keywords
):
    """
    Determines whether the student's value contains
    a meaningful keyword associated with the scholarship
    requirement.
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_text = str(
        student_value
    ).strip().lower()

    scholarship_text = str(
        scholarship_value
    ).strip().lower()

    # Exact text match
    if scholarship_text in student_text:
        return True

    # Keyword match
    for keyword in keywords:

        keyword = keyword.lower()

        if keyword in scholarship_text:
            if keyword in student_text:
                return True

    return False


def certification_matches(
    student_value,
    scholarship_value
):
    """
    Determines whether the student's certification
    matches the scholarship certification requirement.
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_items = normalize_list(
        str(student_value)
    )

    scholarship_items = normalize_list(
        str(scholarship_value)
    )

    # Exact match
    for scholarship_item in scholarship_items:

        if scholarship_item in student_items:
            return True

    # Semantic certification match
    matched, _, _ = semantic_match(
        student_items,
        scholarship_items,
        CERTIFICATION_GROUPS
    )

    return matched


def generate_explanation(result):
    """
    Generates a human-readable summary of a recommendation.
    """

    scholarship = result["scholarship"]

    lines = []

    lines.append(
        f"You are a strong candidate for the "
        f"{scholarship.name}."
    )

    for explanation in result["explanations"]:

        category = explanation.get(
            "category",
            ""
        )

        details = explanation.get(
            "details",
            []
        )

        if details:

            lines.append(
                f"{category}: {' '.join(details)}"
            )

    return " ".join(lines)


def generate_match_details(
    student,
    scholarship,
    explanations
):
    """
    Generates:

    - why_you_match
    - missing_requirements

    Important:
    - Only matched categories are added to why_you_match.
    - Only genuine mismatches are added to missing_requirements.
    - Semantic matches count as matches.
    """

    why_you_match = []
    missing_requirements = []

    # ==========================================================
    # WHY YOU MATCH
    # ==========================================================

    for explanation in explanations:

        category = explanation.get(
            "category",
            ""
        )

        category_lower = category.lower()

        details = explanation.get(
            "details",
            []
        )

        # ------------------------------------------------------
        # MAJOR
        # ------------------------------------------------------

        if category_lower == "major":

            if major_matches(
                student.major,
                scholarship.major
            ):
                why_you_match.append(
                    f"Your {student.major} major matches "
                    f"the scholarship's major requirement "
                    f"of {scholarship.major}."
                )

        # ------------------------------------------------------
        # GPA
        # ------------------------------------------------------

        elif category_lower == "gpa":

            if gpa_matches(
                student.gpa,
                scholarship.gpa_requirement
            ):
                why_you_match.append(
                    f"Your GPA of {float(student.gpa):.1f} "
                    f"meets the scholarship's GPA requirement "
                    f"of {float(scholarship.gpa_requirement):.1f}."
                )

        # ------------------------------------------------------
        # STATE
        # ------------------------------------------------------

        elif category_lower == "state":

            if (
                is_real_requirement(student.state)
                and
                is_real_requirement(scholarship.state)
                and
                str(student.state).strip().lower()
                ==
                str(scholarship.state).strip().lower()
            ):
                why_you_match.append(
                    f"Your location in {student.state} "
                    f"matches the scholarship's state "
                    f"requirement of {scholarship.state}."
                )

        # ------------------------------------------------------
        # CITIZENSHIP
        # ------------------------------------------------------

        elif category_lower == "citizenship":

            if (
                is_real_requirement(student.citizenship)
                and
                is_real_requirement(
                    scholarship.citizenship
                )
                and
                str(student.citizenship).strip().lower()
                ==
                str(
                    scholarship.citizenship
                ).strip().lower()
            ):
                why_you_match.append(
                    f"Your {student.citizenship} citizenship "
                    f"matches the scholarship's citizenship "
                    f"requirement."
                )

        # ------------------------------------------------------
        # INTERESTS
        # ------------------------------------------------------

        elif category_lower == "interests":

            if text_matches(
                student.interests,
                scholarship.interests,
                INTEREST_SYNONYMS
            ):
                why_you_match.append(
                    f"Your interests in {student.interests} "
                    f"align with the scholarship's interests: "
                    f"{scholarship.interests}."
                )

        # ------------------------------------------------------
        # SKILLS
        # ------------------------------------------------------

        elif category_lower == "skills":

            if text_matches(
                student.skills,
                scholarship.skills,
                SKILL_SYNONYMS
            ):

                # Prefer the actual match returned
                # by the matching engine.
                if details:

                    why_you_match.append(
                        details[0]
                    )

                else:

                    why_you_match.append(
                        f"Your skills in {student.skills} "
                        f"align with the scholarship's "
                        f"required skills: "
                        f"{scholarship.skills}."
                    )

        # ------------------------------------------------------
        # PROJECTS
        # ------------------------------------------------------

        elif category_lower == "projects":

            if is_real_requirement(
                student.projects
            ) and is_real_requirement(
                scholarship.projects
            ):
                why_you_match.append(
                    f"Your project experience, including "
                    f"'{student.projects}', aligns with "
                    f"the scholarship's project requirement: "
                    f"'{scholarship.projects}'."
                )

        # ------------------------------------------------------
        # LEADERSHIP
        # ------------------------------------------------------

        elif category_lower == "leadership":

            if keyword_match(
                student.leadership,
                scholarship.leadership,
                LEADERSHIP_KEYWORDS
            ):
                why_you_match.append(
                    f"Your leadership experience in "
                    f"'{student.leadership}' aligns with "
                    f"the scholarship's leadership "
                    f"requirement."
                )

        # ------------------------------------------------------
        # VOLUNTEER
        # ------------------------------------------------------

        elif category_lower == "volunteer":

            if keyword_match(
                student.volunteer,
                scholarship.volunteer,
                VOLUNTEER_KEYWORDS
            ):
                why_you_match.append(
                    f"Your volunteer experience in "
                    f"'{student.volunteer}' matches the "
                    f"scholarship's volunteer requirement."
                )

        # ------------------------------------------------------
        # CERTIFICATIONS
        # ------------------------------------------------------

        elif category_lower == "certifications":

            if certification_matches(
                student.certifications,
                scholarship.certifications
            ):
                why_you_match.append(
                    f"Your {student.certifications} "
                    f"certification matches the "
                    f"scholarship's certification "
                    f"requirement: "
                    f"{scholarship.certifications}."
                )

    # ==========================================================
    # MISSING REQUIREMENTS
    # ==========================================================

    # ----------------------------------------------------------
    # GPA
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.gpa_requirement
    ):

        if not is_real_requirement(
            student.gpa
        ):

            missing_requirements.append(
                f"Scholarship requires a GPA of "
                f"{scholarship.gpa_requirement} "
                f"or higher. Add your GPA to your profile."
            )

        elif not gpa_matches(
            student.gpa,
            scholarship.gpa_requirement
        ):

            missing_requirements.append(
                f"Your GPA of {student.gpa} is below "
                f"the required GPA of "
                f"{scholarship.gpa_requirement}."
            )

    # ----------------------------------------------------------
    # MAJOR
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.major
    ):

        if not major_matches(
            student.major,
            scholarship.major
        ):
            missing_requirements.append(
                f"Your major ({student.major}) does not "
                f"match the scholarship's required major "
                f"({scholarship.major})."
            )

    # ----------------------------------------------------------
    # STATE
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.state
    ):

        if not (
            is_real_requirement(student.state)
            and
            str(student.state).strip().lower()
            ==
            str(scholarship.state).strip().lower()
        ):
            missing_requirements.append(
                f"Your state ({student.state}) does not "
                f"match the scholarship's required state "
                f"({scholarship.state})."
            )

    # ----------------------------------------------------------
    # CITIZENSHIP
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.citizenship
    ):

        if not (
            is_real_requirement(
                student.citizenship
            )
            and
            str(student.citizenship).strip().lower()
            ==
            str(
                scholarship.citizenship
            ).strip().lower()
        ):
            missing_requirements.append(
                f"Your citizenship ({student.citizenship}) "
                f"does not match the scholarship's required "
                f"citizenship ({scholarship.citizenship})."
            )

    # ----------------------------------------------------------
    # INTERESTS
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.interests
    ):

        if not text_matches(
            student.interests,
            scholarship.interests,
            INTEREST_SYNONYMS
        ):
            missing_requirements.append(
                f"Your interests ({student.interests}) do not "
                f"match the scholarship's required interests "
                f"({scholarship.interests})."
            )

    # ----------------------------------------------------------
    # SKILLS
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.skills
    ):

        if not text_matches(
            student.skills,
            scholarship.skills,
            SKILL_SYNONYMS
        ):
            missing_requirements.append(
                f"Your skills ({student.skills}) do not "
                f"match the scholarship's required skills "
                f"({scholarship.skills})."
            )

    # ----------------------------------------------------------
    # PROJECTS
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.projects
    ):

        if not is_real_requirement(
            student.projects
        ):
            missing_requirements.append(
                f"Scholarship requires project experience "
                f"in {scholarship.projects}. "
                f"Add your project experience to your profile."
            )

        elif not text_matches(
            student.projects,
            scholarship.projects
        ):
            missing_requirements.append(
                f"Your projects ({student.projects}) do not "
                f"match the scholarship's required projects "
                f"({scholarship.projects})."
            )

    # ----------------------------------------------------------
    # LEADERSHIP
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.leadership
    ):

        if not keyword_match(
            student.leadership,
            scholarship.leadership,
            LEADERSHIP_KEYWORDS
        ):
            missing_requirements.append(
                f"Your leadership experience "
                f"({student.leadership}) does not match "
                f"the scholarship's required leadership "
                f"experience ({scholarship.leadership})."
            )

    # ----------------------------------------------------------
    # VOLUNTEER
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.volunteer
    ):

        if not keyword_match(
            student.volunteer,
            scholarship.volunteer,
            VOLUNTEER_KEYWORDS
        ):
            missing_requirements.append(
                f"Your volunteer experience "
                f"({student.volunteer}) does not match "
                f"the scholarship's required volunteer "
                f"experience ({scholarship.volunteer})."
            )

    # ----------------------------------------------------------
    # CERTIFICATIONS
    # ----------------------------------------------------------

    if is_real_requirement(
        scholarship.certifications
    ):

        if not certification_matches(
            student.certifications,
            scholarship.certifications
        ):
            missing_requirements.append(
                f"Your certifications "
                f"({student.certifications}) do not match "
                f"the scholarship's required certifications "
                f"({scholarship.certifications})."
            )

    return {
        "why_you_match": why_you_match,
        "missing_requirements": missing_requirements
    }



