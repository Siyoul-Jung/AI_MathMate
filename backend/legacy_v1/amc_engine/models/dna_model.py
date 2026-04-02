from pydantic import BaseModel, Field, model_validator
from typing import List, Optional, Any
from .tags import MathCategory, ContextType

class LogicStep(BaseModel):
    step: int = Field(..., description="Step number")
    title: str = Field(..., description="Short title of the step")
    description: str = Field(..., description="Detailed pedagogical explanation")

class SeedConstraint(BaseModel):
    min_val: Optional[Any] = None
    max_val: Optional[Any] = None
    type: str = "int"
    description: Optional[str] = None

class DNAModel(BaseModel):
    specific_tag: str = Field(..., description="Unique technical tag for the problem logic")
    categories: List[MathCategory] = Field(..., description="List of mathematical domains involved")
    context_type: ContextType = Field(default=ContextType.ABSTRACT, description="Problem narrative style")
    level: int = Field(..., ge=1, le=15, description="AIME problem number (1-15)")
    has_image: bool = Field(default=False, description="Whether the solver generates a supporting image")
    is_mock_ready: bool = Field(default=True, description="Ready for production mock exams")
    topics: List[str] = Field(default_factory=list, description="Specific sub-topics (e.g., Polynomials, Base Conversion)")
    seed_constraints: dict[str, Any] = Field(default_factory=dict, description="Numerical safety bounds (can be level-specific)")
    
    # Pedagogical Layer (Optional but Recommended)
    logic_steps_count: Optional[int] = Field(None, description="Number of logical steps defined")

    @model_validator(mode='before')
    @classmethod
    def handle_legacy_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            # 1. Handle 'category' -> 'categories'
            if "category" in data and "categories" not in data:
                cat = data.pop("category")
                data["categories"] = [cat] if isinstance(cat, str) else cat
            
            # 2. Extract Topics from specific_tag (ID-based inference)
            tag = data.get("specific_tag", "")
            new_topics = data.get("topics", [])
            tag_topic_map = {
                "NT-BASE": "Base Conversion",
                "COMB-PAIRING": "Probability",
                "NUM-CUBIC": "Modular Arithmetic",
                "GEO-TRAP": "Quadrilaterals",
                "ALG-POLY": "Polynomials",
                "GEO-TRIANGLE": "Triangles"
            }
            for pattern, topic in tag_topic_map.items():
                if pattern in tag and topic not in new_topics:
                    new_topics.append(topic)

            # 3. Split and Map legacy names, and Extract Topics from Strings
            if "categories" in data and isinstance(data["categories"], list):
                category_map = {
                    "Combinations": "Combinatorics",
                    "Piecewise": "Algebra",
                    "Functions": "Algebra",
                    "Complex Numbers": "Algebra",
                    "Trigonometry": "Geometry",
                    "Rotation": "Geometry",
                    "Complex Geometry": "Geometry",
                    "Complex Geo": "Geometry",
                    "Number Theory (Base)": "Number Theory",
                    "Expected Value": "Probability"
                }
                
                topic_hints = {
                    "Number Theory (Base)": "Base Conversion",
                    "Complex Geometry": "Complex Numbers",
                    "Rotation": "Rotation",
                    "Expected Value": "Expected Value",
                    "Probability": "Probability"
                }

                new_cats = []
                for c in data["categories"]:
                    if isinstance(c, str):
                        parts = [p.strip() for p in c.replace(",", "/").split("/")]
                        for p in parts:
                            if p in topic_hints:
                                if topic_hints[p] not in new_topics:
                                    new_topics.append(topic_hints[p])
                            mapped_cat = category_map.get(p, p)
                            new_cats.append(mapped_cat)
                    else:
                        new_cats.append(c)
                
                data["categories"] = new_cats
                data["topics"] = list(set(new_topics))
        return data
