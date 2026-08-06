WEIGHTS = {
    "major": 25,
    "gpa": 20,
    "state": 10,
    "citizenship": 10,
    "interests": 10,
    "skills": 15,
    "projects": 5,
    "leadership": 5,
}


def calculate_score(matches):
    score = 0

    for match in matches:
        if match["matched"]:
            score += WEIGHTS.get(
                match["category"],
                0
            )

    return score