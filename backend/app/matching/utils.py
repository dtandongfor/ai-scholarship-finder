def normalize_list(value):

    if not value:
        return []

    return [
        item.strip().lower()
        for item in value.split(",")
        if item.strip()
    ]


def semantic_match(student_items, scholarship_items, knowledge_base):

    # Exact match
    for scholarship_item in scholarship_items:
        if scholarship_item in student_items:
            return True, scholarship_item, scholarship_item

    # Knowledge graph match
    for scholarship_item in scholarship_items:

        for root, synonyms in knowledge_base.items():

            family = [root] + synonyms

            if scholarship_item in family:

                for student_item in student_items:

                    if student_item in family:

                        return True, student_item, scholarship_item

    return False, None, None

