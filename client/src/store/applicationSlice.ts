import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { type BorrowerDraft, type GuarantorDraft, type LoanDraft } from '@/types'

interface ApplicationState {
  borrower: BorrowerDraft
  guarantor: GuarantorDraft
  loan: LoanDraft
  // Set after successful API calls
  createdBorrowerId: number | null
  createdLoanRequestId: number | null
}

const initialState: ApplicationState = {
  borrower: {
    company_name: '',
    industry: '',
    state: '',
    years_in_business: '',
    revenue: '',
  },
  guarantor: {
    first_name: '',
    last_name: '',
    fico_score: '',
    has_bankruptcy: false,
    has_judgments: false,
    has_liens: false,
    ownership_pct: '',
  },
  loan: {
    amount: '',
    term_months: '',
    equipment_type: '',
    equipment_year: '',
    equipment_cost: '',
    equipment_description: '',
  },
  createdBorrowerId: null,
  createdLoanRequestId: null,
}

const applicationSlice = createSlice({
  name: 'application',
  initialState,
  reducers: {
    setBorrower(state, action: PayloadAction<BorrowerDraft>) {
      state.borrower = action.payload
    },
    setGuarantor(state, action: PayloadAction<GuarantorDraft>) {
      state.guarantor = action.payload
    },
    setLoan(state, action: PayloadAction<LoanDraft>) {
      state.loan = action.payload
    },
    setCreatedBorrowerId(state, action: PayloadAction<number>) {
      state.createdBorrowerId = action.payload
    },
    setCreatedLoanRequestId(state, action: PayloadAction<number>) {
      state.createdLoanRequestId = action.payload
    },
    resetApplication() {
      return initialState
    },
  },
})

export const {
  setBorrower,
  setGuarantor,
  setLoan,
  setCreatedBorrowerId,
  setCreatedLoanRequestId,
  resetApplication,
} = applicationSlice.actions

export default applicationSlice.reducer
