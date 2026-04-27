import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { setLoan } from '@/store/applicationSlice'
import StepLayout from '@/components/StepLayout'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function LoanStep() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const loan = useAppSelector(s => s.application.loan)

  const isValid =
    loan.amount.trim() &&
    loan.term_months.trim() &&
    loan.equipment_type.trim() &&
    loan.equipment_year.trim() &&
    loan.equipment_cost.trim()

  const handleNext = () => {
    dispatch(setLoan(loan))
    navigate('/apply/review')
  }

  const update = (field: string, value: string) =>
    dispatch(setLoan({ ...loan, [field]: value }))

  return (
    <StepLayout
      currentStep={3}
      onNext={handleNext}
      nextDisabled={!isValid}
    >
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Loan Request</h2>
          <p className="text-gray-500 mt-1">Details about the loan and equipment being financed.</p>
        </div>

        <div className="space-y-4 pb-20">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="amount">Loan Amount ($)</Label>
              <Input
                id="amount"
                type="number"
                min={0}
                placeholder="150000"
                value={loan.amount}
                onChange={e => update('amount', e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="term_months">Term (months)</Label>
              <Input
                id="term_months"
                type="number"
                min={1}
                placeholder="60"
                value={loan.term_months}
                onChange={e => update('term_months', e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="equipment_type">Equipment Type</Label>
            <Input
              id="equipment_type"
              placeholder="e.g. Excavator, Semi-Truck, CNC Machine"
              value={loan.equipment_type}
              onChange={e => update('equipment_type', e.target.value)}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="equipment_year">Equipment Year</Label>
              <Input
                id="equipment_year"
                type="number"
                min={1900}
                max={new Date().getFullYear() + 1}
                placeholder="2023"
                value={loan.equipment_year}
                onChange={e => update('equipment_year', e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="equipment_cost">Equipment Cost ($)</Label>
              <Input
                id="equipment_cost"
                type="number"
                min={0}
                placeholder="160000"
                value={loan.equipment_cost}
                onChange={e => update('equipment_cost', e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="equipment_description">Equipment Description</Label>
            <Input
              id="equipment_description"
              placeholder="e.g. 2023 CAT 320 Hydraulic Excavator"
              value={loan.equipment_description}
              onChange={e => update('equipment_description', e.target.value)}
            />
          </div>
        </div>
      </div>
    </StepLayout>
  )
}
