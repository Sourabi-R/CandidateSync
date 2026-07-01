from typing import List, Optional
from pydantic import BaseModel


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


class Links(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    other: List[str] = []


class Skill(BaseModel):
    name: str
    confidence: float
    sources: List[str]


class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    summary: Optional[str] = None


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None
    end_year: Optional[int] = None


class Provenance(BaseModel):
    field: str
    source: str
    method: str


class CandidateProfile(BaseModel):

    candidate_id: str

    full_name: Optional[str] = None

    emails: List[str] = []

    phones: List[str] = []

    location: Optional[Location] = None

    links: Optional[Links] = None

    headline: Optional[str] = None

    current_company: Optional[str] = None
    current_title: Optional[str] = None
    experience_summary: Optional[str] = None

    years_experience: Optional[float] = None

    skills: List[Skill] = []

    experience: List[Experience] = []

    education: List[Education] = []

    provenance: List[Provenance] = []

    overall_confidence: Optional[float] = None