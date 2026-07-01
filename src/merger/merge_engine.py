from typing import Any

from src.config.enums import DataSource
from src.models.schema import Experience, Location, Skill, Provenance
from src.normalizer.phone_normalizer import PhoneNormalizer
from src.normalizer.skill_normalizer import normalize_skills
from src.reporting.conflict_report import ConflictReport
from src.utils.validators import is_valid_email


class MergeEngine:
    @staticmethod
    def merge(csv_profile: Any, resume_data: dict[str, Any]) -> tuple[Any, ConflictReport]:
        """Merge recruiter CSV and resume data into a canonical profile."""
        report = ConflictReport()

        if resume_data.get("email") and is_valid_email(resume_data["email"]):
            if resume_data["email"] not in csv_profile.emails:
                csv_profile.emails.append(resume_data["email"])
        elif resume_data.get("email"):
            report.add(
                field="email",
                csv_value=csv_profile.emails[0] if csv_profile.emails else None,
                resume_value=resume_data["email"],
                selected=csv_profile.emails[0] if csv_profile.emails else None,
                reason="Invalid resume email",
            )

        if resume_data.get("phone"):
            normalized_phone = PhoneNormalizer.normalize(resume_data["phone"])
            if normalized_phone:
                if normalized_phone not in csv_profile.phones:
                    csv_profile.phones.append(normalized_phone)
            else:
                report.add(
                    field="phone",
                    csv_value=csv_profile.phones[0] if csv_profile.phones else None,
                    resume_value=resume_data["phone"],
                    selected=csv_profile.phones[0] if csv_profile.phones else None,
                    reason="Invalid resume phone",
                )

        resume_skills = normalize_skills(resume_data.get("skills", []) or [])
        existing_skill_names = {skill.name for skill in csv_profile.skills}
        for skill in resume_skills:
            if skill not in existing_skill_names:
                csv_profile.skills.append(
                    Skill(
                        name=skill,
                        confidence=0.95,
                        sources=["resume"],
                    )
                )
                existing_skill_names.add(skill)

        if resume_data.get("headline") and not csv_profile.headline:
            csv_profile.headline = resume_data["headline"]

        if resume_data.get("location") and not csv_profile.location:
            csv_profile.location = Location(city=resume_data["location"])

        if resume_data.get("current_company") and not csv_profile.current_company:
            csv_profile.current_company = resume_data["current_company"]

        if resume_data.get("current_title") and not csv_profile.current_title:
            csv_profile.current_title = resume_data["current_title"]

        if resume_data.get("experience_summary") and not csv_profile.experience_summary:
            csv_profile.experience_summary = resume_data["experience_summary"]

        resume_experience = resume_data.get("experience")[0] if resume_data.get("experience") else None
        if csv_profile.experience:
            if resume_experience:
                existing_experience = csv_profile.experience[0]
                if not existing_experience.start and resume_experience.get("start"):
                    existing_experience.start = resume_experience.get("start")
                if not existing_experience.end and resume_experience.get("end"):
                    existing_experience.end = resume_experience.get("end")
                if not existing_experience.summary and resume_experience.get("summary"):
                    existing_experience.summary = resume_experience.get("summary")
        elif resume_experience:
            csv_profile.experience.append(
                Experience(
                    company=resume_experience.get("company"),
                    title=resume_experience.get("title"),
                    start=resume_experience.get("start"),
                    end=resume_experience.get("end"),
                    summary=resume_experience.get("summary"),
                )
            )

        csv_company = None
        csv_title = None
        if csv_profile.experience:
            csv_company = csv_profile.experience[0].company
            csv_title = csv_profile.experience[0].title

        resume_company = resume_data.get("current_company")
        resume_title = resume_data.get("current_title")

        if csv_company and resume_company and csv_company != resume_company:
            report.add(
                field="current_company",
                csv_value=csv_company,
                resume_value=resume_company,
                selected=csv_company,
                reason="CSV confidence higher",
                winning_source=DataSource.CSV.value,
                confidence=0.95,
            )

        if csv_title and resume_title and csv_title != resume_title:
            report.add(
                field="current_title",
                csv_value=csv_title,
                resume_value=resume_title,
                selected=csv_title,
                reason="CSV confidence higher",
                winning_source=DataSource.CSV.value,
                confidence=0.95,
            )

        csv_profile.provenance.extend(
            [
                Provenance(
                    field="full_name",
                    source="recruiter.csv",
                    method="csv_mapping",
                ),
                Provenance(
                    field="emails",
                    source="recruiter.csv",
                    method="csv_mapping",
                ),
                Provenance(
                    field="phones",
                    source="recruiter.csv",
                    method="phone_normalization",
                ),
                Provenance(
                    field="skills",
                    source="resume",
                    method="keyword_extraction",
                ),
                Provenance(
                    field="experience",
                    source="recruiter.csv",
                    method="csv_mapping",
                ),
            ]
        )

        return csv_profile, report
