import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { setBorrower } from '@/store/applicationSlice'
import StepLayout from '@/components/StepLayout'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { US_STATES } from '@/data/state'


export default function BorrowerStep() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const borrower = useAppSelector(s => s.application.borrower)

  const isValid =
    borrower.company_name.trim() &&
    borrower.industry.trim() &&
    borrower.state.trim() &&
    borrower.years_in_business.trim() &&
    borrower.revenue.trim()

  const handleNext = () => {
    dispatch(setBorrower(borrower))
    navigate('/apply/guarantor')
  }

  return (
    <StepLayout
      currentStep={1}
      onNext={handleNext}
      nextDisabled={!isValid}
    >
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Business Information</h2>
          <p className="text-gray-500 mt-1">Tell us about the business applying for the loan.</p>
        </div>

        <div className="space-y-4 pb-20">
          <div className="space-y-1.5">
            <Label htmlFor="company_name">Company Name</Label>
            <Input
              id="company_name"
              placeholder="Acme Equipment LLC"
              value={borrower.company_name}
              onChange={e => dispatch(setBorrower({ ...borrower, company_name: e.target.value }))}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="industry">Industry</Label>
            <Input
              id="industry"
              placeholder="e.g. Construction, Manufacturing, Transportation"
              value={borrower.industry}
              onChange={e => dispatch(setBorrower({ ...borrower, industry: e.target.value }))}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="state">State</Label>
            <select
              id="state"
              value={borrower.state}
              onChange={e => dispatch(setBorrower({ ...borrower, state: e.target.value }))}
              className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm focus:outline-none focus:ring-1 focus:ring-ring"
            >
              <option value="">Select a state</option>
              {US_STATES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="years_in_business">Years in Business</Label>
            <Input
              id="years_in_business"
              type="number"
              min={0}
              placeholder="5"
              value={borrower.years_in_business}
              onChange={e => dispatch(setBorrower({ ...borrower, years_in_business: e.target.value }))}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="revenue">Annual Revenue ($)</Label>
            <Input
              id="revenue"
              type="number"
              min={0}
              placeholder="1000000"
              value={borrower.revenue}
              onChange={e => dispatch(setBorrower({ ...borrower, revenue: e.target.value }))}
            />
          </div>
        </div>
      </div>
    </StepLayout>
  )
}
