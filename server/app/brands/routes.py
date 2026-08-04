# Brands routes — HTTP route declarations for brand DNA generation.
# Responsibilities:
#   - POST /brands/generate : accept URL, run scrape + AI, return brand DNA
#   - GET  /brands/         : return all brand DNA records for current user
#   - GET  /brands/{id}     : return a single brand DNA record
#   - All routes require auth + sufficient credits (via require_credits dependency)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import require_auth, require_credits
from app.users.models import User
from app.brands import schemas, controller
import uuid

router = APIRouter()

@router.post("/generate", response_model=schemas.BrandDNAOut)
async def generate(
    body: schemas.BrandRequest,
    user: User = Depends(require_credits),
    db: Session = Depends(get_db)
):
    return await controller.generate_brand_dna(body, user, db)

@router.get("/", response_model=list[schemas.BrandDNAOut])
async def list_brands(
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    return controller.get_all(current_user.id, db)

@router.get("/{brand_id}", response_model=schemas.BrandDNAOut)
async def get_brand(
    brand_id: uuid.UUID,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    return controller.get_one(brand_id, current_user.id, db)

@router.delete("/{brand_id}")
async def delete_brand(
    brand_id: uuid.UUID,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    return controller.delete_brand_dna(brand_id, current_user.id, db)

from fastapi.responses import Response
from app.core.pdf_generator import generate_brand_dna_pdf

@router.get("/{brand_id}/pdf")
async def get_brand_pdf(
    brand_id: uuid.UUID,
    current_user: User = Depends(require_auth),
    db: Session = Depends(get_db)
):
    record = controller.get_one(brand_id, current_user.id, db)
    
    import json
    dna_data = record.dna
    if isinstance(dna_data, str):
        dna_data = json.loads(dna_data)
        
    pdf_bytes = generate_brand_dna_pdf(dna_data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="brand_dna_{brand_id}.pdf"'
        }
    )
