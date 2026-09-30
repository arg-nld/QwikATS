from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantResponse


router = APIRouter(
    prefix="/api/tenants",
    tags=["Tenants"],
)


@router.get("/", response_model=list[TenantResponse])
def get_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
):
    tenant = (
        db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .first()
    )

    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found",
        )

    return tenant


@router.post("/", response_model=TenantResponse, status_code=201)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Tenant)
        .filter(Tenant.slug == tenant_data.slug)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Tenant slug already exists",
        )

    tenant = Tenant(
        name=tenant_data.name,
        slug=tenant_data.slug,
    )

    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    return tenant