from app.database import engine, SessionLocal
from app.models.base import Base
from app.models.Borrower import Borrower
from app.models.LoanRequest import LoanRequest, LoanRequestStatus
from app.models.BusinessCredit import BusinessCredit
from app.models.PersonalGuarantor import PersonalGuarantor
from app.models.Lender import Lender
from app.models.LenderPolicy import LenderPolicy
from app.models.LenderAllowedIndustry import LenderAllowedIndustry
from app.models.LenderAllowedState import LenderAllowedState
from app.models.LenderExcludedIndustry import LenderExcludedIndustry
from app.models.LenderExcludedState import LenderExcludedState
from app.models.LenderEquipmentRestriction import LenderEquipmentRestriction
from app.models.MatchResult import MatchResult, MatchStatus


def seed():
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:

        # ── Sample borrower ────────────────────────────────────────────────
        borrower = Borrower(
            borrower_id=1,
            company_name="Acme Equipment LLC",
            industry="Construction",
            state="TX",
            years_in_business=7,
            revenue=2_500_000.0,
        )
        db.add(borrower)
        db.flush()

        loan_request = LoanRequest(
            loan_request_id=1,
            borrower_id=1,
            amount=150_000.0,
            term_months=60,
            equipment_type="Excavator",
            equipment_year=2023,
            equipment_cost=160_000.0,
            equipment_description="2023 CAT 320 Hydraulic Excavator",
            status=LoanRequestStatus.pending,
        )
        db.add(loan_request)

        business_credit = BusinessCredit(
            bc_id=1,
            borrower_id=1,
            paynet_score=720.0,
            trade_lines=8,
            days_beyond_terms=4.5,
            high_credit=300_000.0,
            derogatory_marks=0,
        )
        db.add(business_credit)

        guarantor = PersonalGuarantor(
            guarantor_id=1,
            borrower_id=1,
            first_name="Jane",
            last_name="Smith",
            fico_score=740,
            has_bankruptcy=False,
            has_judgments=False,
            has_liens=False,
            ownership_pct=100.0,
        )
        db.add(guarantor)

        # ── Lender 1: First Capital Finance (placeholder) ─────────────────
        db.add(Lender(lender_id=1, lender_name="First Capital Finance"))
        db.flush()

        db.add(LenderPolicy(
            policy_id=1, lender_id=1,
            program_name="Heavy Equipment Standard",
            min_loan_amount=50_000.0,
            max_loan_amount=500_000.0,
            min_term_months=12,
            max_term_months=84,
            min_fico=680,
            min_paynet_score=650.0,
            min_years_in_business=2,
            min_revenue=500_000.0,
        ))
        db.flush()
        for industry in ["Construction", "Manufacturing", "Agriculture"]:
            db.add(LenderAllowedIndustry(policy_id=1, industry=industry))
        for state in ["TX", "CA", "FL", "NY", "IL"]:
            db.add(LenderAllowedState(policy_id=1, state=state))

        # ── Lender 2: Falcon Equipment Finance ────────────────────────────
        # Source: 112025 Rates - STANDARD.pdf
        db.add(Lender(lender_id=2, lender_name="Falcon Equipment Finance"))
        db.flush()

        db.add(LenderPolicy(
            policy_id=2, lender_id=2,
            program_name="Standard",
            min_fico=680,
            min_paynet_score=660.0,
            min_years_in_business=3,
            min_years_since_bankruptcy=15,
        ))
        db.add(LenderPolicy(
            policy_id=3, lender_id=2,
            program_name="Trucking (Class 8)",
            min_fico=700,
            min_paynet_score=680.0,
            min_years_in_business=5,
            max_equipment_age_years=10,  # Class 8 trucks must be 10 years or newer
            min_years_since_bankruptcy=15,
        ))
        db.flush()
        db.add(LenderAllowedIndustry(policy_id=3, industry="Trucking"))

        # ── Lender 3: Citizens Bank ───────────────────────────────────────
        # Source: 2025 Program Guidelines UPDATED.pdf
        db.add(Lender(lender_id=3, lender_name="Citizens Bank"))
        db.flush()

        # Tier 1: app-only up to $75K
        db.add(LenderPolicy(
            policy_id=4, lender_id=3,
            program_name="Tier 1 — App Only (up to $75K)",
            max_loan_amount=75_000.0,
            min_fico=700,
            min_years_in_business=2,
            min_years_since_bankruptcy=5,
            requires_us_citizen=True,
        ))
        # Tier 3: full financials, $75K–$1M
        db.add(LenderPolicy(
            policy_id=5, lender_id=3,
            program_name="Tier 3 — Full Financials ($75K–$1M)",
            min_loan_amount=75_001.0,
            max_loan_amount=1_000_000.0,
            min_fico=700,
            min_years_in_business=2,
            min_years_since_bankruptcy=5,
            requires_us_citizen=True,
        ))
        db.flush()
        for policy_id in [4, 5]:
            db.add(LenderExcludedState(policy_id=policy_id, state="CA"))
            db.add(LenderExcludedIndustry(policy_id=policy_id, industry="Cannabis"))

        # ── Lender 4: Advantage+ Financing ───────────────────────────────
        # Source: Advantage++Broker+2025.pdf  (non-trucking only, up to $75K)
        db.add(Lender(lender_id=4, lender_name="Advantage+ Financing"))
        db.flush()

        db.add(LenderPolicy(
            policy_id=6, lender_id=4,
            program_name="Standard Non-Trucking (up to $75K)",
            min_loan_amount=10_000.0,
            max_loan_amount=75_000.0,
            max_term_months=60,
            min_fico=680,
            min_years_in_business=3,
            no_bankruptcy=True,       # "Do you finance bankruptcies? No"
            allows_judgments=False,   # "Do you extend credit with judgements? No"
            allows_liens=False,       # "No tax liens"
            requires_us_citizen=True,
        ))
        db.flush()
        db.add(LenderExcludedIndustry(policy_id=6, industry="Trucking"))

        # ── Lender 5: Apex Commercial Capital ────────────────────────────
        # Source: Apex EF Broker Guidelines_082725.pdf
        # Excluded states: CA, NV, ND, VT
        # Excluded industries: Cannabis, Casino/Gambling, Churches, Non-profits,
        #   Oil & Gas, Trucking, Logging, Nail Salons, Audio/Visual
        # Restricted equipment: Aircraft, Boat, ATM, Electric Vehicle, Furniture,
        #   Kiosk, Leasehold Improvement, Signage, Tanning Bed, Copier
        db.add(Lender(lender_id=5, lender_name="Apex Commercial Capital"))
        db.flush()

        apex_tiers = [
            dict(policy_id=7, program_name="A Rate",  min_fico=700, min_paynet_score=660.0, min_years_in_business=5, max_loan_amount=500_000.0),
            dict(policy_id=8, program_name="B Rate",  min_fico=670, min_paynet_score=650.0, min_years_in_business=3, max_loan_amount=250_000.0),
            dict(policy_id=9, program_name="C Rate",  min_fico=640, min_paynet_score=640.0, min_years_in_business=2, max_loan_amount=100_000.0),
        ]
        for tier in apex_tiers:
            db.add(LenderPolicy(
                lender_id=5,
                min_loan_amount=10_000.0,
                min_term_months=24,
                max_term_months=60,
                max_equipment_age_years=15,
                **tier,
            ))
        db.flush()

        apex_excluded_industries = [
            "Cannabis", "Casino", "Gambling", "Church", "Non-profit",
            "Oil & Gas", "Petroleum", "Trucking", "Logging", "Nail Salon", "Audio/Visual",
        ]
        apex_excluded_equipment = [
            "Aircraft", "Boat", "ATM", "Electric Vehicle", "Furniture",
            "Kiosk", "Leasehold Improvement", "Signage", "Tanning Bed", "Copier",
        ]
        for policy_id in [7, 8, 9]:
            for state in ["CA", "NV", "ND", "VT"]:
                db.add(LenderExcludedState(policy_id=policy_id, state=state))
            for industry in apex_excluded_industries:
                db.add(LenderExcludedIndustry(policy_id=policy_id, industry=industry))
            for equipment in apex_excluded_equipment:
                db.add(LenderEquipmentRestriction(policy_id=policy_id, equipment_type=equipment))

        # ── Lender 6: Stearns Bank ────────────────────────────────────────
        # Source: EF Credit Box 4.14.2025.pdf
        # No BK in last 7 years
        # Excluded industries: Gaming/Gambling, Oil & Gas, Restaurants, Car Wash,
        #   OTR, Beauty/Tanning, Tattoo/Piercing, Adult Entertainment,
        #   Hazmat, MSBs, Real Estate, Aesthetic, Weapons/Firearms
        db.add(Lender(lender_id=6, lender_name="Stearns Bank"))
        db.flush()

        stearns_tiers = [
            dict(policy_id=10, program_name="Tier 1", min_fico=725, min_paynet_score=685.0, min_years_in_business=3),
            dict(policy_id=11, program_name="Tier 2", min_fico=710, min_paynet_score=675.0, min_years_in_business=3),
            dict(policy_id=12, program_name="Tier 3", min_fico=700, min_paynet_score=665.0, min_years_in_business=2),
        ]
        for tier in stearns_tiers:
            db.add(LenderPolicy(lender_id=6, min_years_since_bankruptcy=7, **tier))
        db.flush()

        stearns_excluded_industries = [
            "Gaming", "Gambling", "Oil & Gas", "Petroleum", "Restaurant",
            "Car Wash", "OTR", "Beauty", "Tanning", "Tattoo", "Piercing",
            "Adult Entertainment", "Hazmat", "MSB", "Real Estate",
            "Aesthetic", "Weapons", "Firearms",
        ]
        for policy_id in [10, 11, 12]:
            for industry in stearns_excluded_industries:
                db.add(LenderExcludedIndustry(policy_id=policy_id, industry=industry))

        db.commit()
        print("✓ Seeded database.")
        print(f"  6 lenders | 12 programs | sample borrower: Acme Equipment LLC")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed()
