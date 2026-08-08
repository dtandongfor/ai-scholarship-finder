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
