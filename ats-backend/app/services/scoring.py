def normalize_skills(skills: str) -> set[str]:
    return {
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    }


def calculate_compatibility(job, candidate):
    required = normalize_skills(job.required_skills)
    preferred = normalize_skills(job.preferred_skills)
    candidate_skills = normalize_skills(candidate.skills)

    if required:
        required_matches = required & candidate_skills
        required_score = (
            len(required_matches) / len(required)
        ) * 70
    else:
        required_matches = set()
        required_score = 70

    if preferred:
        preferred_matches = preferred & candidate_skills
        preferred_score = (
            len(preferred_matches) / len(preferred)
        ) * 20
    else:
        preferred_matches = set()
        preferred_score = 20

    if job.minimum_experience_years > 0:
        experience_score = min(
            candidate.experience_years
            / job.minimum_experience_years,
            1,
        ) * 10
    else:
        experience_score = 10

    total_score = round(
        required_score
        + preferred_score
        + experience_score,
        2,
    )

    return {
        "score": total_score,
        "required_skills": {
            "matched": sorted(required_matches),
            "total": sorted(required),
        },
        "preferred_skills": {
            "matched": sorted(preferred_matches),
            "total": sorted(preferred),
        },
        "experience": {
            "candidate_years": candidate.experience_years,
            "required_years": job.minimum_experience_years,
        },
    }