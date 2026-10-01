from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class JobBase(BaseModel):
    title: str
    description: str | None = None
    department: str | None = None
    location: str | None = None
    employment_type: str | None = None
    status: str = "draft"

    minimum_experience_years: int = 0

    required_skills: str = ""
    preferred_skills: str = ""

    required_skills_weight: float = 70.0
    preferred_skills_weight: float = 20.0
    experience_weight: float = 10.0

    @model_validator(mode="after")
    def validate_scoring_weights(self):
        total = (
            self.required_skills_weight
            + self.preferred_skills_weight
            + self.experience_weight
        )

        if abs(total - 100.0) > 0.01:
            raise ValueError(
                "Scoring weights must total 100%"
            )

        weights = [
            self.required_skills_weight,
            self.preferred_skills_weight,
            self.experience_weight,
        ]

        if any(weight < 0 or weight > 100 for weight in weights):
            raise ValueError(
                "Scoring weights must be between 0 and 100"
            )

        return self


class JobCreate(JobBase):
    tenant_id: int


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    department: str | None = None
    location: str | None = None
    employment_type: str | None = None
    status: str | None = None

    minimum_experience_years: int | None = None

    required_skills: str | None = None
    preferred_skills: str | None = None

    required_skills_weight: float | None = None
    preferred_skills_weight: float | None = None
    experience_weight: float | None = None

    @model_validator(mode="after")
    def validate_scoring_weights(self):
        weights = [
            self.required_skills_weight,
            self.preferred_skills_weight,
            self.experience_weight,
        ]

        provided_weights = [
            weight for weight in weights
            if weight is not None
        ]

        if provided_weights:
            if len(provided_weights) != 3:
                raise ValueError(
                    "When updating scoring weights, "
                    "provide all three weights"
                )

            total = sum(provided_weights)

            if abs(total - 100.0) > 0.01:
                raise ValueError(
                    "Scoring weights must total 100%"
                )

            if any(
                weight < 0 or weight > 100
                for weight in provided_weights
            ):
                raise ValueError(
                    "Scoring weights must be between 0 and 100"
                )

        return self


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    created_at: datetime
    updated_at: datetime