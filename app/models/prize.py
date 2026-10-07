from sqlmodel import Field, SQLModel


class Prize(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    name: str
    description: str
    cost_in_hours: float
    quantity_available: int = Field(default=0)