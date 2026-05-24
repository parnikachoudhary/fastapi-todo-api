from sqlmodel import SQLModel, Field
from typing import Optional

# 1. Database table model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"

# 2. Create schema - POST body (no id is kept here)
class TodoCreate(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"

# 3. Put schema - full replace
class TodoPut(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool
    priority: str

# 4. Patch schema - partial update (all fields are optional here)
class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None

# 5. Bulk update (id is must)
class TodoBulkUpdateItem(SQLModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None