def generate_explanation(result):

    scholarship = result["scholarship"]

    lines = []

    lines.append(
        f"You are a strong candidate for the "
        f"{scholarship.name}."
    )

    for explanation in result["explanations"]:

        category = explanation["category"]

        details = explanation["details"]

        if details:
            lines.append(
                f"{category}: {details[0]}"
            )

    return " ".join(lines)