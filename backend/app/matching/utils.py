def normalize_list(value):

    if not value:
        return []

    return [
        item.strip().lower()
        for item in value.split(",")
        if item.strip()
    ]



def semantic_match(
    student_items,
    scholarship_items,
    knowledge_base
):
    """
    Finds a semantic match between student items
    and scholarship requirements.

    Returns:
        (
            matched,
            student_match,
            scholarship_match
        )
    """

    # ------------------------------------------
    # EXACT MATCH
    # ------------------------------------------

    for scholarship_item in scholarship_items:

        for student_item in student_items:

            if student_item == scholarship_item:

                return (
                    True,
                    student_item,
                    scholarship_item
                )

    # ------------------------------------------
    # SYNONYM / KNOWLEDGE-BASE MATCH
    # ------------------------------------------

    for scholarship_item in scholarship_items:

        for student_item in student_items:

            # Check every semantic group
            for group_name, synonyms in knowledge_base.items():

                group_name = group_name.lower()

                synonyms = [
                    synonym.lower()
                    for synonym in synonyms
                ]

                # ------------------------------------------
                # Does scholarship item belong to group?
                # ------------------------------------------

                scholarship_matches_group = (
                    scholarship_item.lower() == group_name
                    or scholarship_item.lower() in synonyms
                )

                # ------------------------------------------
                # Does student item belong to same group?
                # ------------------------------------------

                student_matches_group = (
                    student_item.lower() == group_name
                    or student_item.lower() in synonyms
                )

                # ------------------------------------------
                # SEMANTIC MATCH
                # ------------------------------------------

                if (
                    scholarship_matches_group
                    and student_matches_group
                ):

                    return (
                        True,
                        student_item,
                        scholarship_item
                    )

    # ------------------------------------------
    # NO MATCH
    # ------------------------------------------

    return (
        False,
        None,
        None
    )


def find_requirement_matches(
    student_items,
    scholarship_items,
    knowledge_base=None,
    match_function=None,
):
    """Match each scholarship requirement to at most one student item.

    The returned pairs are ordered as ``(student_item, scholarship_item)``.
    This makes list-based categories eligible for proportional scoring without
    allowing one student item to satisfy several requirements.
    """

    matches = []
    used_student_items = set()

    for scholarship_item in scholarship_items:
        for student_item in student_items:
            if student_item in used_student_items:
                continue

            if match_function:
                is_match = match_function(student_item, scholarship_item)
            elif student_item == scholarship_item:
                is_match = True
            elif knowledge_base:
                is_match, _, _ = semantic_match(
                    [student_item],
                    [scholarship_item],
                    knowledge_base,
                )
            else:
                is_match = False

            if is_match:
                matches.append((student_item, scholarship_item))
                used_student_items.add(student_item)
                break

    return matches


def requirement_match_ratio(
    student_items,
    scholarship_items,
    knowledge_base=None,
    match_function=None,
):
    """Return the proportion of scholarship requirements the student meets."""

    if not scholarship_items:
        return 0.0, []

    matches = find_requirement_matches(
        student_items,
        scholarship_items,
        knowledge_base,
        match_function,
    )

    return len(matches) / len(scholarship_items), matches




def is_valid_value(value):

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
        "na"
    }

    if value in invalid_values:
        return False

    return True
