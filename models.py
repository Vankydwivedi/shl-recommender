from pydantic import BaseModel, field_validator
from typing import Optional


class Message(BaseModel):
    role: str
    content: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ("user", "assistant"):
            raise ValueError("role must be 'user' or 'assistant'")
        return v


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatRequest(BaseModel):
    messages: list[Message]

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: list[Message]) -> list[Message]:
        if not v:
            raise ValueError("messages cannot be empty")
        if v[-1].role != "user":
            raise ValueError("last message must be from user")
        return v


class ChatResponse(BaseModel):
    reply: str
    recommendations: list[Recommendation]
    end_of_conversation: bool


class CatalogItem(BaseModel):
    name: str
    url: str
    test_types: list[str]
    description: Optional[str] = None
    job_levels: Optional[list[str]] = None
    remote_testing: Optional[bool] = None
    adaptive_irt: Optional[bool] = None
    languages: Optional[list[str]] = None

    def to_search_text(self) -> str:
        type_map = {
            "A": "Ability Aptitude cognitive reasoning intelligence",
            "B": "Biodata Situational Judgement behavioral scenarios",
            "C": "Competencies skills behavioral evaluation",
            "D": "Development 360 feedback growth",
            "E": "Assessment Exercises structured simulation exercise",
            "K": "Knowledge Skills technical proficiency test",
            "P": "Personality Behavior style questionnaire traits",
            "S": "Simulations realistic work scenarios",
        }
        type_text = " ".join(type_map.get(t, t) for t in self.test_types)
        desc = self.description or ""
        levels = " ".join(self.job_levels or [])
        return f"{self.name} {type_text} {desc} {levels}".strip()

    def to_context_str(self) -> str:
        types = ", ".join(self.test_types)
        desc = f" — {self.description}" if self.description else ""
        remote = " [Remote]" if self.remote_testing else ""
        return f"- {self.name} | types: {types}{remote}{desc} | URL: {self.url}"
