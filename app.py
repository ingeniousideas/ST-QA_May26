
from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mock Staff Search API",
    version="1.0.0",
    description="A simple API to search a mock staff database with 3 endpoints."
)

# --------------------------
# Mock "database" (in-memory)
# --------------------------
class Staff(BaseModel):
    id: int
    name: str
    email: str
    department: str
    role: str

# A small but realistic dataset
STAFF_DB: List[Staff] = [
    Staff(id=1, name="Alice Johnson", email="alice.johnson@example.com", department="Engineering", role="Software Engineer"),
    Staff(id=2, name="Bob Smith", email="bob.smith@example.com", department="Engineering", role="DevOps Engineer"),
    Staff(id=3, name="Carol Lee", email="carol.lee@example.com", department="Design", role="Product Designer"),
    Staff(id=4, name="David Kim", email="david.kim@example.com", department="HR", role="HR Manager"),
    Staff(id=5, name="Eva Patel", email="eva.patel@example.com", department="Engineering", role="QA Engineer"),
    Staff(id=6, name="Frank Wu", email="frank.wu@example.com", department="Support", role="Support Specialist"),
    Staff(id=7, name="Grace Nguyen", email="grace.nguyen@example.com", department="Marketing", role="Content Strategist"),
    Staff(id=8, name="Henry Lopez", email="henry.lopez@example.com", department="Finance", role="Accountant"),
    Staff(id=9, name="Isabella Rossi", email="isabella.rossi@example.com", department="Engineering", role="Software Engineer"),
    Staff(id=10, name="Jack Thompson", email="jack.thompson@example.com", department="Sales", role="Sales Executive"),
]

# --------------------------
# Response models
# --------------------------
class StaffSearchResponse(BaseModel):
    total: int = Field(..., description="Total number of matching staff members")
    page: int = Field(..., ge=1, description="Current page number")
    page_size: int = Field(..., ge=1, description="Number of items per page")
    items: List[Staff]

# --------------------------
# 1) Health check
# --------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# --------------------------
# 2) Search staff (filter, sort, paginate)
# --------------------------
@app.get("/staff", response_model=StaffSearchResponse)
def search_staff(
    q: Optional[str] = Query(None, description="Search term (matches name/email, case-insensitive, partial)"),
    department: Optional[str] = Query(None, description="Exact department filter"),
    role: Optional[str] = Query(None, description="Exact role filter"),
    sort_by: Literal["name", "department", "role"] = Query("name", description="Sort field"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
):
    # Filter
    results = STAFF_DB
    if q:
        q_lower = q.lower()
        results = [s for s in results if q_lower in s.name.lower() or q_lower in s.email.lower()]
    if department:
        results = [s for s in results if s.department.lower() == department.lower()]
    if role:
        results = [s for s in results if s.role.lower() == role.lower()]

    # Sort
    reverse = order == "desc"
    if sort_by == "name":
        results.sort(key=lambda s: s.name.lower(), reverse=reverse)
    elif sort_by == "department":
        results.sort(key=lambda s: s.department.lower(), reverse=reverse)
    elif sort_by == "role":
        results.sort(key=lambda s: s.role.lower(), reverse=reverse)

    # Paginate
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    paged = results[start:end]

    return StaffSearchResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=paged
    )

# --------------------------
# 3) Get staff by ID
# --------------------------
@app.get("/staff/{staff_id}", response_model=Staff)
def get_staff(staff_id: int):
    for s in STAFF_DB:
        if s.id == staff_id:
            return s
    raise HTTPException(status_code=404, detail=f"Staff with id {staff_id} not found")

