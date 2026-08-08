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
    Determines whether a scholarship field actually contains
    a meaningful requirement.
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


def text_matches(student_value, scholarship_value, knowledge_base=None):
    """
    Determines whether two text fields match.

    Supports:
    - Exact matching
    - Semantic matching through a knowledge base
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_items = normalize_list(str(student_value))
    scholarship_items = normalize_list(str(scholarship_value))

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


def major_matches(student_major, scholarship_major):
    """
    Handles exact major matches and major-group matches.
    """

    if not is_real_requirement(student_major):
        return False

    if not is_real_requirement(scholarship_major):
        return False

    student_major = str(student_major).strip().lower()
    scholarship_major = str(scholarship_major).strip().lower()

    # Exact match
    if student_major == scholarship_major:
        return True

    # Same major group
    for group, majors in MAJOR_GROUPS.items():

        if student_major in majors and scholarship_major in majors:
            return True

    return False


def keyword_match(student_value, scholarship_value, keywords):
    """
    Checks whether the student field contains a meaningful
    keyword associated with the scholarship requirement.
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_text = str(student_value).lower()
    scholarship_text = str(scholarship_value).lower()

    # Direct overlap
    scholarship_words = scholarship_text.split()

    for word in scholarship_words:
        if len(word) > 3 and word in student_text:
            return True

    # Known keywords
    for keyword in keywords:
        if keyword.lower() in student_text:
            for scholarship_word in scholarship_words:
                if len(scholarship_word) > 3:
                    if (
                        keyword.lower() in scholarship_word
                        or scholarship_word in keyword.lower()
                    ):
                        return True

    return False


def certification_matches(student_value, scholarship_value):
    """
    Handles certification matching using certification groups.

    Examples:

    CompTIA A+
    CompTIA Security+

    belong to the CompTIA family.

    AWS Cloud Practitioner
    AWS Developer Associate

    belong to the AWS family.
    """

    if not is_real_requirement(student_value):
        return False

    if not is_real_requirement(scholarship_value):
        return False

    student_text = str(student_value).lower()
    scholarship_text = str(scholarship_value).lower()

    # Exact match
    if student_text == scholarship_text:
        return True

    # Check certification families
    for family, certifications in CERTIFICATION_GROUPS.items():

        family_student = (
            family in student_text
            and any(
                cert.lower() in student_text
                for cert in certifications
            )
        )

        family_scholarship = (
            family in scholarship_text
            and any(
                cert.lower() in scholarship_text
                for cert in certifications
            )
        )

        if family_student and family_scholarship:
            return True

    return False


def gpa_matches(student_gpa, scholarship_gpa):
    """
    Checks whether the student's GPA meets the scholarship GPA.
    """

    if not is_real_requirement(student_gpa):
        return False

    if not is_real_requirement(scholarship_gpa):
        return False

    try:
        student_gpa = float(student_gpa)
        scholarship_gpa = float(scholarship_gpa)

        return student_gpa >= scholarship_gpa

    except (ValueError, TypeError):
        return False


def get_skill_matches(student_value, scholarship_value):
    """
    Returns individual skill matches and missing scholarship skills.

    Comparisons are case-insensitive, but the original
    capitalization from the scholarship is preserved.

    Example:

    Student:
        Java, Git, SQL

    Scholarship:
        JavaScript, Git

    Returns:
        matched = ["Git"]
        missing = ["JavaScript"]
    """

    if not is_real_requirement(student_value):
        return [], normalize_list(str(scholarship_value))

    if not is_real_requirement(scholarship_value):
        return [], []

    student_items = normalize_list(str(student_value))

    # Keep original scholarship values for display
    scholarship_original = [
        item.strip()
        for item in str(scholarship_value).split(",")
        if item.strip()
    ]

    scholarship_items = normalize_list(
        str(scholarship_value)
    )

    matched = []
    missing = []

    for index, scholarship_item in enumerate(
        scholarship_items
    ):

        item_matched = False

        # Original capitalization for output
        display_item = scholarship_item

        if index < len(scholarship_original):
            display_item = scholarship_original[index]

        # -----------------------------
        # Exact match
        # -----------------------------

        if scholarship_item in student_items:

            matched.append(display_item)
            item_matched = True

        # -----------------------------
        # Semantic match
        # -----------------------------

        if not item_matched:

            for student_item in student_items:

                semantic_found, _, _ = semantic_match(
                    [student_item],
                    [scholarship_item],
                    SKILL_SYNONYMS
                )

                if semantic_found:

                    matched.append(display_item)
                    item_matched = True
                    break

        # -----------------------------
        # No match
        # -----------------------------

        if not item_matched:
            missing.append(display_item)

    return matched, missing


def generate_explanation(
    student,
    scholarship,
    matched_on,
    explanations
):
    """
    Generates human-readable explanations for a recommendation.

    Important:
    - matched_on determines what the matching engine actually matched.
    - missing_requirements contains ONLY genuine mismatches.
    - Exact matches are never reported as missing.
    - Semantic matches are treated as matches.
    """

    why_you_match = []
    missing_requirements = []

    # ==========================================================
    # WHY YOU MATCH
    # ==========================================================

    for item in explanations:

        category = item.get("category", "")
        category_lower = category.lower()

        # ------------------------------------------------------
        # MAJOR
        # ------------------------------------------------------

        if category_lower == "major":

            if major_matches(
                student.major,
                scholarship.major
            ):
                why_you_match.append(
                    f"Your {student.major} major matches the "
                    f"scholarship's major requirement of "
                    f"{scholarship.major}."
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
                    f"Your GPA of {student.gpa} meets the "
                    f"scholarship's GPA requirement of "
                    f"{scholarship.gpa_requirement}."
                )

        # ------------------------------------------------------
        # STATE
        # ------------------------------------------------------

        elif category_lower == "state":

            if (
                is_real_requirement(student.state)
                and is_real_requirement(scholarship.state)
                and str(student.state).strip().lower()
                == str(scholarship.state).strip().lower()
            ):
                why_you_match.append(
                    f"Your location in {student.state} matches "
                    f"the scholarship's state requirement of "
                    f"{scholarship.state}."
                )

        # ------------------------------------------------------
        # CITIZENSHIP
        # ------------------------------------------------------

        elif category_lower == "citizenship":

            if (
                is_real_requirement(student.citizenship)
                and is_real_requirement(scholarship.citizenship)
                and str(student.citizenship).strip().lower()
                == str(scholarship.citizenship).strip().lower()
            ):
                why_you_match.append(
                    f"Your {student.citizenship} citizenship matches "
                    f"the scholarship's citizenship requirement."
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
                    f"Your interests in {student.interests} align "
                    f"with the scholarship's interests: "
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
                details = item.get("details", [])

                if details:
                    why_you_match.append(
                        details[0]
                )
                else:
                    why_you_match.append(
                        f"Your skills in {student.skills} align with "
                        f"the scholarship's required skills: "
                        f"{scholarship.skills}."
                )

        # ------------------------------------------------------
        # PROJECTS
        # ------------------------------------------------------

        elif category_lower == "projects":

            if text_matches(
                student.projects,
                scholarship.projects
            ):
                why_you_match.append(
                    f"Your project experience, including "
                    f"'{student.projects}', aligns with the "
                    f"scholarship's project requirement: "
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
                    f"'{student.leadership}' aligns with the "
                    f"scholarship's leadership requirement."
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
                    f"Your {student.certifications} certification "
                    f"matches the scholarship's certification "
                    f"requirement: {scholarship.certifications}."
                )

    # ==========================================================
    # MISSING REQUIREMENTS
    # ==========================================================

    # ----------------------------------------------------------
    # GPA
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.gpa_requirement):

        if not is_real_requirement(student.gpa):

            missing_requirements.append(
                f"GPA requirement of "
                f"{scholarship.gpa_requirement} cannot be verified "
                f"because no GPA is listed."
            )

        elif not gpa_matches(
            student.gpa,
            scholarship.gpa_requirement
        ):

            missing_requirements.append(
                f"Your GPA ({student.gpa}) does not meet the "
                f"scholarship's required GPA "
                f"({scholarship.gpa_requirement})."
            )

    # ----------------------------------------------------------
    # MAJOR
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.major):

        if not is_real_requirement(student.major):

            missing_requirements.append(
                f"The scholarship requires a major in "
                f"{scholarship.major}, but no major is listed "
                f"on your profile."
            )

        elif not major_matches(
            student.major,
            scholarship.major
        ):

            missing_requirements.append(
                f"Your major ({student.major}) does not match "
                f"the scholarship's required major "
                f"({scholarship.major})."
            )

    # ----------------------------------------------------------
    # STATE
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.state):

        if not is_real_requirement(student.state):

            missing_requirements.append(
                f"The scholarship requires students from "
                f"{scholarship.state}, but no state is listed "
                f"on your profile."
            )

        elif (
            str(student.state).strip().lower()
            != str(scholarship.state).strip().lower()
        ):

            missing_requirements.append(
                f"Your state ({student.state}) does not match "
                f"the scholarship's required state "
                f"({scholarship.state})."
            )

    # ----------------------------------------------------------
    # CITIZENSHIP
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.citizenship):

        if not is_real_requirement(student.citizenship):

            missing_requirements.append(
                f"The scholarship requires "
                f"{scholarship.citizenship} citizenship, but "
                f"no citizenship is listed on your profile."
            )

        elif (
            str(student.citizenship).strip().lower()
            != str(scholarship.citizenship).strip().lower()
        ):

            missing_requirements.append(
                f"Your citizenship ({student.citizenship}) does "
                f"not match the scholarship's required "
                f"citizenship ({scholarship.citizenship})."
            )

    # ----------------------------------------------------------
    # INTERESTS
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.interests):

        if not is_real_requirement(student.interests):

            missing_requirements.append(
                f"The scholarship looks for interests related "
                f"to {scholarship.interests}, but no interests "
                f"are listed on your profile."
            )

        elif not text_matches(
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

    if is_real_requirement(scholarship.skills):

        if not is_real_requirement(student.skills):

            missing_requirements.append(
                f"Required skills include {scholarship.skills}, "
                f"but no skills are listed on your profile."
            )

        else:

            matched_skills, missing_skills = get_skill_matches(
                student.skills,
                scholarship.skills
            )

            # Only report skills that are genuinely missing
            if missing_skills:

                missing_text = ", ".join(missing_skills)

                if matched_skills:

                    matched_text = ", ".join(matched_skills)

                    missing_requirements.append(
                        f"Your {matched_text} skill(s) match the "
                        f"scholarship requirement, but you are "
                        f"missing the following required skill(s): "
                        f"{missing_text}."
                    ) 

                else:

                    missing_requirements.append(
                        f"Your skills ({student.skills}) do not match "
                        f"the scholarship's required skills "
                        f"({scholarship.skills})."
                    )

    # ----------------------------------------------------------
    # PROJECTS
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.projects):

        if not is_real_requirement(student.projects):

            missing_requirements.append(
                "This scholarship values relevant project "
                "experience, but no projects are listed on "
                "your profile."
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

    if is_real_requirement(scholarship.leadership):

        if not is_real_requirement(student.leadership):

            missing_requirements.append(
                "Leadership experience is listed as a "
                "requirement, but no leadership experience "
                "is listed on your profile."
            )

        elif not keyword_match(
            student.leadership,
            scholarship.leadership,
            LEADERSHIP_KEYWORDS
        ):

            missing_requirements.append(
                f"Your leadership ({student.leadership}) does "
                f"not match the scholarship's required "
                f"leadership ({scholarship.leadership})."
            )

    # ----------------------------------------------------------
    # VOLUNTEER
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.volunteer):

        if not is_real_requirement(student.volunteer):

            missing_requirements.append(
                "Volunteer experience is listed as a "
                "requirement, but no volunteer experience "
                "is listed on your profile."
            )

        elif not keyword_match(
            student.volunteer,
            scholarship.volunteer,
            VOLUNTEER_KEYWORDS
        ):

            missing_requirements.append(
                f"Your volunteer experience ({student.volunteer}) "
                f"does not match the scholarship's required "
                f"volunteer experience ({scholarship.volunteer})."
            )

    # ----------------------------------------------------------
    # CERTIFICATIONS
    # ----------------------------------------------------------

    if is_real_requirement(scholarship.certifications):

        if not is_real_requirement(student.certifications):

            missing_requirements.append(
                f"Required certifications include "
                f"{scholarship.certifications}, but no "
                f"certifications are listed on your profile."
            )

        elif not certification_matches(
            student.certifications,
            scholarship.certifications
        ):

            missing_requirements.append(
                f"Your certifications ({student.certifications}) "
                f"do not match the scholarship's required "
                f"certifications ({scholarship.certifications})."
            )

    # ==========================================================
    # APPLICATION TIP
    # ==========================================================

    if missing_requirements:

        application_tip = (
            "Review the missing requirements above and highlight "
            "any relevant experience you have that may not yet "
            "be included in your profile."
        )

    else:

        application_tip = (
            "You meet all listed scholarship requirements. "
            "Highlight your strongest matching skills, projects, "
            "leadership, and experiences in your application."
        )

    return {
        "why_you_match": why_you_match,
        "missing_requirements": missing_requirements,
        "application_tip": application_tip,
    }





