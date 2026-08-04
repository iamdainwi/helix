# Brands controller — business logic for brand DNA generation and retrieval.
# Responsibilities:
#   - Orchestrate: scrape URL → pass to AI → save result → deduct credit
#   - Retrieve brand DNA records for a user
#   - Raise HTTPException if brand not found or not owned by user
#
# Functions:
#   - generate_brand_dna(body, user, db) : full pipeline, returns BrandDNA record
#   - get_all(user_id, db)               : returns all records for user
#   - get_one(brand_id, user_id, db)     : returns single record or 404

import json
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.brands.models import BrandDNA
from app.brands.schemas import BrandRequest
from app.users.models import User
from app.core.scraper import scrape_website
from app.core.ai import extract_brand_dna
from app.credits.controller import deduct_credit

async def generate_brand_dna(body: BrandRequest, user: User, db: Session):
    url_str = str(body.url)
    try:
        scraped = await scrape_website(url_str)
        if "error" in scraped:
            raise HTTPException(400, f"Scraping failed: {scraped['error']}")
    except ValueError as e:
        raise HTTPException(400, str(e))
        
    dna = await extract_brand_dna(scraped)

    record = BrandDNA(
        user_id      = user.id,
        url          = url_str,
        scraped_data = json.dumps(scraped),
        dna          = json.dumps(dna),
    )
    db.add(record)
    deduct_credit(db, user.id, reason="brand_dna_generation")
    db.commit()
    db.refresh(record)
    return record

import uuid

def get_all(user_id: uuid.UUID, db: Session):
    return db.query(BrandDNA).filter(BrandDNA.user_id == user_id).all()

def get_one(brand_id: uuid.UUID, user_id: uuid.UUID, db: Session):
    record = db.query(BrandDNA).filter(
        BrandDNA.id == brand_id,
        BrandDNA.user_id == user_id
    ).first()
    if not record:
        raise HTTPException(404, "Brand DNA record not found")
    return record

def delete_brand_dna(brand_id: uuid.UUID, user_id: uuid.UUID, db: Session):
    record = get_one(brand_id, user_id, db)
    db.delete(record)
    db.commit()
    return {"message": "Brand DNA deleted successfully"}
