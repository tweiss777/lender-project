export interface Borrower {
  borrower_id: number
  company_name: string
  industry: string
  state: string
  years_in_business: number
  revenue: number
}

export interface PersonalGuarantor {
  guarantor_id: number
  borrower_id: number
  first_name: string
  last_name: string
  fico_score: number
  has_bankruptcy: boolean
  has_judgments: boolean
  has_liens: boolean
  ownership_pct: number
}

export interface BusinessCredit {
  bc_id: number
  borrower_id: number
  paynet_score: number
  trade_lines: number
  days_beyond_terms: number
  high_credit: number
  derogatory_marks: number
}

export interface LoanRequest {
  loan_request_id: number
  borrower_id: number
  amount: number
  term_months: number
  equipment_type: string
  equipment_year: number
  equipment_cost: number
  equipment_description: string
  status: 'pending' | 'approved' | 'rejected' | 'funded'
}

export interface CriterionResult {
  name: string
  passed: boolean
  reason: string
}

export interface MatchResult {
  match_id: number
  loan_request_id: number
  lender_name: string
  program_name: string
  is_eligible: boolean
  match_score: number
  status: 'eligible' | 'ineligible'
  criteria_results: CriterionResult[]
}

export interface LenderPolicyPreview {
  program_name: string
  min_loan_amount: number | null
  max_loan_amount: number | null
  min_term_months: number | null
  max_term_months: number | null
  min_fico: number | null
  min_paynet_score: number | null
  min_years_in_business: number | null
  min_revenue: number | null
  max_equipment_age_years: number | null
  equipment_restrictions: string[]
  allowed_states: string[]
  excluded_states: string[]
  allowed_industries: string[]
  excluded_industries: string[]
  no_bankruptcy: boolean | null
  min_years_since_bankruptcy: number | null
  allows_judgments: boolean | null
  allows_liens: boolean | null
  requires_us_citizen: boolean | null
}

export interface LenderPreview {
  lender_name: string
  programs: LenderPolicyPreview[]
}

// Redux store shape for the in-progress application
export interface BorrowerDraft {
  company_name: string
  industry: string
  state: string
  years_in_business: string
  revenue: string
}

export interface GuarantorDraft {
  first_name: string
  last_name: string
  fico_score: string
  has_bankruptcy: boolean
  has_judgments: boolean
  has_liens: boolean
  ownership_pct: string
}

export interface LoanDraft {
  amount: string
  term_months: string
  equipment_type: string
  equipment_year: string
  equipment_cost: string
  equipment_description: string
}
