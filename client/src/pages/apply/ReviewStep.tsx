import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { setCreatedBorrowerId, setCreatedLoanRequestId, resetApplication } from '@/store/applicationSlice'
import StepLayout from '@/components/StepLayout'

export default function ReviewStep() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const { borrower, guarantor, loan } = useAppSelector(s => s.application)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async () => {
    setIsLoading(true)
    setError(null)

    try {
      // 1. Create borrower
      const borrowerRes = await fetch('/api/v1/borrowers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          company_name: borrower.company_name,
          industry: borrower.industry,
          state: borrower.state,
          years_in_business: Number(borrower.years_in_business),
          revenue: Number(borrower.revenue),
        }),
      })
      if (!borrowerRes.ok) throw new Error('Failed to create borrower')
      const borrowerData = await borrowerRes.json()
      const borrowerId: number = borrowerData.borrower_id
      dispatch(setCreatedBorrowerId(borrowerId))

      // 2. Create loan request
      const loanRes = await fetch('/api/v1/loan_requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          borrower_id: borrowerId,
          amount: Number(loan.amount),
          term_months: Number(loan.term_months),
          equipment_type: loan.equipment_type,
          equipment_year: Number(loan.equipment_year),
          equipment_cost: Number(loan.equipment_cost),
          equipment_description: loan.equipment_description,
          status: 'pending',
        }),
      })
      if (!loanRes.ok) throw new Error('Failed to create loan request')
      const loanData = await loanRes.json()
      const loanRequestId: number = loanData.loan_request_id
      dispatch(setCreatedLoanRequestId(loanRequestId))

      // 3. Run underwriting
      const underwriteRes = await fetch(`/api/v1/borrowers/${borrowerId}/underwrite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ loan_request_id: loanRequestId }),
      })
      if (!underwriteRes.ok) throw new Error('Failed to run underwriting')

      dispatch(resetApplication())
      navigate(`/applications/${borrowerId}/results?loan_request_id=${loanRequestId}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setIsLoading(false)
    }
  }

  const Section = ({ title, rows }: { title: string; rows: [string, string][] }) => (
    <div className="bg-white rounded-lg border p-4 space-y-3">
      <h3 className="font-semibold text-gray-800">{title}</h3>
      <div className="divide-y">
        {rows.map(([label, value]) => (
          <div key={label} className="flex justify-between py-2 text-sm">
            <span className="text-gray-500">{label}</span>
            <span className="font-medium text-gray-800 text-right max-w-[60%]">{value || '—'}</span>
          </div>
        ))}
      </div>
    </div>
  )

  return (
    <StepLayout
      currentStep={4}
      onNext={handleSubmit}
      nextLabel="Submit & Run Underwriting"
      isLoading={isLoading}
    >
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Review Application</h2>
          <p className="text-gray-500 mt-1">Review all details before submitting.</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
            {error}
          </div>
        )}

        <div className="space-y-4 pb-20">
          <Section
            title="Business Information"
            rows={[
              ['Company Name', borrower.company_name],
              ['Industry', borrower.industry],
              ['State', borrower.state],
              ['Years in Business', borrower.years_in_business],
              ['Annual Revenue', borrower.revenue ? `$${Number(borrower.revenue).toLocaleString()}` : ''],
            ]}
          />

          <Section
            title="Personal Guarantor"
            rows={[
              ['Name', `${guarantor.first_name} ${guarantor.last_name}`],
              ['FICO Score', guarantor.fico_score],
              ['Ownership %', guarantor.ownership_pct ? `${guarantor.ownership_pct}%` : ''],
              ['Prior Bankruptcy', guarantor.has_bankruptcy ? 'Yes' : 'No'],
              ['Judgments', guarantor.has_judgments ? 'Yes' : 'No'],
              ['Tax Liens', guarantor.has_liens ? 'Yes' : 'No'],
            ]}
          />

          <Section
            title="Loan Request"
            rows={[
              ['Loan Amount', loan.amount ? `$${Number(loan.amount).toLocaleString()}` : ''],
              ['Term', loan.term_months ? `${loan.term_months} months` : ''],
              ['Equipment Type', loan.equipment_type],
              ['Equipment Year', loan.equipment_year],
              ['Equipment Cost', loan.equipment_cost ? `$${Number(loan.equipment_cost).toLocaleString()}` : ''],
              ['Description', loan.equipment_description],
            ]}
          />
        </div>
      </div>
    </StepLayout>
  )
}
