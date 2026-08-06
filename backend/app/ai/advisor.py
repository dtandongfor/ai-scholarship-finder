def generate_advice(student, analysis):

    advice = []

    if "No GPA provided" in analysis["weaknesses"]:
        advice.append(
            "Add your GPA so scholarships can evaluate your academic standing."
        )

    if "Low GPA" in analysis["weaknesses"]:
        advice.append(
            "Improving your GPA will greatly increase your scholarship eligibility."
        )

    if "No skills listed" in analysis["weaknesses"]:
        advice.append(
            "Add programming languages, software, and technical skills to your profile."
        )

    if "No projects listed" in analysis["weaknesses"]:
        advice.append(
            "Complete one or two portfolio projects to demonstrate experience."
        )

    if "No leadership experience" in analysis["weaknesses"]:
        advice.append(
            "Take on a leadership role in a student organization or project team."
        )

    if "Limited volunteer experience" in analysis["weaknesses"]:
        advice.append(
            "Volunteer in your community or participate in STEM outreach activities."
        )

    if "No certifications" in analysis["weaknesses"]:
        advice.append(
            "Earn an industry certification such as AWS Cloud Practitioner or Google Cloud."
        )

    if analysis["profile_strength"] >= 90:
        summary = (
            "Excellent profile. You are highly competitive for many scholarships."
        )

    elif analysis["profile_strength"] >= 75:
        summary = (
            "Strong profile with a few areas that could be improved."
        )

    elif analysis["profile_strength"] >= 50:
        summary = (
            "Average profile. Strengthening a few sections will significantly improve your chances."
        )

    else:
        summary = (
            "Your profile needs additional experience before it will be competitive."
        )

    return {
        "summary": summary,
        "advice": advice
    }