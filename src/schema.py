from pydantic import BaseModel, Field

class CaseStudySearchQuery(BaseModel):
    query: str = Field(description="The query to search for case studies")