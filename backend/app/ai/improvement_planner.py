from collections import Counter

from ..matching.engine import match_one


IMPROVEMENT_ACTIONS = {
    "Major": "Choose coursework or projects related to your target scholarships.",
    "GPA": "Improve your GPA and include your academic achievements.",
    "State": "Search for scholarships available in your state or location.",
    "Citizenship": "Look for scholarships matching your citizenship eligibility.",
    "Interests": "Add more interests related to your academic and career goals.",
    "Skills": "Add technical skills, tools, programming languages, or software experience.",
    "Projects": "Create portfolio projects that demonstrate your abilities.",
    "Leadership": "Join a student organization or take leadership in a project.",
    "Volunteer": "Participate in community service or STEM outreach activities.",
    "Certifications": "Earn an industry certification such as AWS or Google Cloud."
}


def generate_plan(student, scholarships):

    improvements = Counter()

    for scholarship in scholarships:

        result = match_one(
            student,
            scholarship
        )

        matched = {
            item.lower()
            for item in result["matched_on"]
        }

        categories = [
            "Major",
            "GPA",
            "State",
            "Citizenship",
            "Interests",
            "Skills",
            "Projects",
            "Leadership",
            "Volunteer",
            "Certifications"
        ]

        for category in categories:

            if (
                getattr(scholarship, category.lower(), None)
                and category.lower() not in matched
            ):
                improvements[category] += 1


    plan = []

    for category, count in improvements.most_common():

        plan.append(
            {
                "category": category,
                "scholarships": count,
                "reason": (
                    f"{count} scholarships require "
                    f"{category.lower()} experience or qualifications."
                ),
                "action": IMPROVEMENT_ACTIONS.get(
                    category,
                    "Improve this area of your profile."
                )
            }
        )

    return plan