from pydantic import BaseModel

# ---------------- Book ---------------- #
class BookBase(BaseModel):
    title: str | None
    authors: str | None
    subjects: str | None

class BookSchema(BookBase):
    id: int

    model_config = {
        "from_attributes": True  # Allows reading from ORM objects or dicts
    }

