from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.Lender import Lender
from app.models.LenderPolicy import LenderPolicy
from app.models.LenderAllowedIndustry import LenderAllowedIndustry
from app.models.LenderAllowedState import LenderAllowedState
from app.models.LenderExcludedIndustry import LenderExcludedIndustry
from app.models.LenderExcludedState import LenderExcludedState
from app.models.LenderEquipmentRestriction import LenderEquipmentRestriction
from app.Schemas.lender_policy_preview import LenderPreview
from app.services.pdf_parser import parse_lender_pdf

lender_routes = APIRouter()


@lender_routes.get("/")
def list_lenders(db: Session = Depends(get_db)):
    lenders = db.query(Lender).all()
    return [
        {
            "lender_id": l.lender_id,
            "lender_name": l.lender_name,
            "policies": [
                {
                    "policy_id": p.policy_id,
                    "program_name": p.program_name,
                    "min_fico": p.min_fico,
                    "min_paynet_score": p.min_paynet_score,
                    "min_years_in_business": p.min_years_in_business,
                    "min_loan_amount": p.min_loan_amount,
                    "max_loan_amount": p.max_loan_amount,
                    "max_equipment_age_years": p.max_equipment_age_years,
                }
                for p in l.policies
            ],
        }
        for l in lenders
    ]


@lender_routes.post("/parse", response_model=LenderPreview)
async def parse_lender_pdf_route(file: UploadFile = File(...)):
    """
    Upload a lender guidelines PDF.
    Returns a structured preview of the parsed policies for user review.
    Nothing is saved to the database at this stage.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")

    pdf_bytes = await file.read()

    try:
        preview = parse_lender_pdf(pdf_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    return preview


@lender_routes.post("/confirm", status_code=201)
def confirm_lender_preview(preview: LenderPreview, db: Session = Depends(get_db)):
    """
    Confirm and save a parsed lender preview to the database.
    Upserts the Lender by name, and upserts each program by (lender_id, program_name).
    Re-uploading the same PDF is safe — existing programs are updated, not duplicated.
    """
    # Upsert lender by name
    lender = db.query(Lender).filter(Lender.lender_name == preview.lender_name).first()
    if not lender:
        lender = Lender(lender_name=preview.lender_name)
        db.add(lender)
        db.flush()

    created_programs = []
    updated_programs = []

    for program in preview.programs:
        # Upsert policy by (lender_id, program_name)
        policy = db.query(LenderPolicy).filter(
            LenderPolicy.lender_id == lender.lender_id,
            LenderPolicy.program_name == program.program_name,
        ).first()

        if policy:
            # Update scalar fields on existing policy
            policy.min_loan_amount = program.min_loan_amount
            policy.max_loan_amount = program.max_loan_amount
            policy.min_term_months = program.min_term_months
            policy.max_term_months = program.max_term_months
            policy.min_fico = program.min_fico
            policy.min_paynet_score = program.min_paynet_score
            policy.min_years_in_business = program.min_years_in_business
            policy.min_revenue = program.min_revenue
            policy.max_equipment_age_years = program.max_equipment_age_years
            policy.no_bankruptcy = program.no_bankruptcy
            policy.min_years_since_bankruptcy = program.min_years_since_bankruptcy
            policy.allows_judgments = program.allows_judgments
            policy.allows_liens = program.allows_liens
            policy.requires_us_citizen = program.requires_us_citizen

            # Delete existing join table rows — cascade will handle it
            # since all relationships are defined with cascade='all, delete-orphan'
            db.query(LenderAllowedIndustry).filter_by(policy_id=policy.policy_id).delete()
            db.query(LenderExcludedIndustry).filter_by(policy_id=policy.policy_id).delete()
            db.query(LenderAllowedState).filter_by(policy_id=policy.policy_id).delete()
            db.query(LenderExcludedState).filter_by(policy_id=policy.policy_id).delete()
            db.query(LenderEquipmentRestriction).filter_by(policy_id=policy.policy_id).delete()
            db.flush()
            updated_programs.append(program.program_name)
        else:
            policy = LenderPolicy(
                lender_id=lender.lender_id,
                program_name=program.program_name,
                min_loan_amount=program.min_loan_amount,
                max_loan_amount=program.max_loan_amount,
                min_term_months=program.min_term_months,
                max_term_months=program.max_term_months,
                min_fico=program.min_fico,
                min_paynet_score=program.min_paynet_score,
                min_years_in_business=program.min_years_in_business,
                min_revenue=program.min_revenue,
                max_equipment_age_years=program.max_equipment_age_years,
                no_bankruptcy=program.no_bankruptcy,
                min_years_since_bankruptcy=program.min_years_since_bankruptcy,
                allows_judgments=program.allows_judgments,
                allows_liens=program.allows_liens,
                requires_us_citizen=program.requires_us_citizen,
            )
            db.add(policy)
            db.flush()
            created_programs.append(program.program_name)

        # Insert fresh join table rows for both create and update paths
        for industry in program.allowed_industries:
            db.add(LenderAllowedIndustry(policy_id=policy.policy_id, industry=industry))
        for industry in program.excluded_industries:
            db.add(LenderExcludedIndustry(policy_id=policy.policy_id, industry=industry))
        for state in program.allowed_states:
            db.add(LenderAllowedState(policy_id=policy.policy_id, state=state))
        for state in program.excluded_states:
            db.add(LenderExcludedState(policy_id=policy.policy_id, state=state))
        for equipment in program.equipment_restrictions:
            db.add(LenderEquipmentRestriction(policy_id=policy.policy_id, equipment_type=equipment))

    db.commit()

    return {
        "lender_name": preview.lender_name,
        "programs_created": created_programs,
        "programs_updated": updated_programs,
    }
