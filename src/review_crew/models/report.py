from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["Critical", "High", "Medium", "Low"]

class ClassifiedFile(BaseModel):
    path: str
    categories: list[str]  # frontend, backend, security, testing, documentation, config etc.
    note: str

class CodebaseAnalysis(BaseModel):
    pr_url: str
    pr_title: str
    base_branch: str
    head_branch: str
    changed_files: list[str]
    files: list[ClassifiedFile] = Field(default_factory=list)
    languages: list[str]
    frameworks: list[str]
    libraries: list[str]
    notes: str = ""

class Finding(BaseModel):
    title: str
    severity: Severity
    location: str
    issue: str
    impact: str
    recommendation: str

class SpecialistReview(BaseModel):
    reviewer_title: str
    findings: list[Finding] = Field(default_factory=list)
    actions_needed: list[str] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)

class LeadReview(SpecialistReview):
    specialist_feedback_assessment: list[str] = Field(default_factory=list)
    cross_cutting_findings: list[Finding] = Field(default_factory=list)
    merge_conflict: bool = False
    merge_ready: bool = False
    merge_status_description: str = ""
    final_feedback: str = ""

class Report(BaseModel):
    project_name: str
    specialist_reviews: list[SpecialistReview] = Field(default_factory=list)
    lead_review: LeadReview = Field(default_factory=LeadReview)
