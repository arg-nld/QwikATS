def normalize_skills(skills: str) -> set[str]:
    return {
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    }


def calculate_compatibility(job, candidate):
    required = normalize_skills(
        job.required_skills
    )

    preferred = normalize_skills(
        job.preferred_skills
    )

    candidate_skills = normalize_skills(
        candidate.skills
    )


    if required:
        required_matches = (
            required & candidate_skills
        )

        required_percentage = (
            len(required_matches)
            / len(required)
        )

        required_score = (
            required_percentage
            * job.required_skills_weight
        )
    else:
        required_matches = set()
        required_score = job.required_skills_weight


    if preferred:
        preferred_matches = (
            preferred & candidate_skills
        )

        preferred_percentage = (
            len(preferred_matches)
            / len(preferred)
        )

        preferred_score = (
            preferred_percentage
            * job.preferred_skills_weight
        )
    else:
        preferred_matches = set()
        preferred_score = job.preferred_skills_weight


    if job.minimum_experience_years > 0:
        experience_percentage = min(
            candidate.experience_years
            / job.minimum_experience_years,
            1.0,
        )

        experience_score = (
            experience_percentage
            * job.experience_weight
        )
    else:
        experience_score = job.experience_weight


    total_score = round(
        required_score
        + preferred_score
        + experience_score,
        2,
    )

    return {
        "score": total_score,

        "scoring_weights": {
            "required_skills": job.required_skills_weight,
            "preferred_skills": job.preferred_skills_weight,
            "experience": job.experience_weight,
        },

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