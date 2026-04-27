import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '@/store/hooks'
import { setGuarantor } from '@/store/applicationSlice'
import StepLayout from '@/components/StepLayout'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function GuarantorStep() {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()
  const guarantor = useAppSelector(s => s.application.guarantor)

  const isValid =
    guarantor.first_name.trim() &&
    guarantor.last_name.trim() &&
    guarantor.fico_score.trim() &&
    guarantor.ownership_pct.trim()

  const handleNext = () => {
    dispatch(setGuarantor(guarantor))
    navigate('/apply/loan')
  }

  const update = (field: string, value: string | boolean) =>
    dispatch(setGuarantor({ ...guarantor, [field]: value }))

  return (
    <StepLayout
      currentStep={2}
      onNext={handleNext}
      nextDisabled={!isValid}
    >
      <div className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Personal Guarantor</h2>
          <p className="text-gray-500 mt-1">Information about the personal guarantor for this loan.</p>
        </div>

        <div className="space-y-4 pb-20">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label htmlFor="first_name">First Name</Label>
              <Input
                id="first_name"
                placeholder="Jane"
                value={guarantor.first_name}
                onChange={e => update('first_name', e.target.value)}
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="last_name">Last Name</Label>
              <Input
                id="last_name"
                placeholder="Smith"
                value={guarantor.last_name}
                onChange={e => update('last_name', e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="fico_score">FICO Score</Label>
            <Input
              id="fico_score"
              type="number"
              min={300}
              max={850}
              placeholder="720"
              value={guarantor.fico_score}
              onChange={e => update('fico_score', e.target.value)}
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="ownership_pct">Ownership Percentage (%)</Label>
            <Input
              id="ownership_pct"
              type="number"
              min={0}
              max={100}
              placeholder="100"
              value={guarantor.ownership_pct}
              onChange={e => update('ownership_pct', e.target.value)}
            />
          </div>

          <div className="space-y-3 pt-2">
            <p className="text-sm font-medium text-gray-700">Credit History Flags</p>

            {([
              { key: 'has_bankruptcy', label: 'Prior Bankruptcy', desc: 'Has the guarantor ever filed for bankruptcy?' },
              { key: 'has_judgments', label: 'Outstanding Judgments', desc: 'Are there any outstanding judgments against the guarantor?' },
              { key: 'has_liens', label: 'Tax Liens', desc: 'Are there any outstanding tax liens?' },
            ] as const).map(({ key, label, desc }) => (
              <div
                key={key}
                className={`flex items-center justify-between p-3 rounded-lg border cursor-pointer
                  ${guarantor[key] ? 'border-red-300 bg-red-50' : 'border-gray-200 bg-white'}
                `}
                onClick={() => update(key, !guarantor[key])}
              >
                <div>
                  <p className="text-sm font-medium text-gray-800">{label}</p>
                  <p className="text-xs text-gray-500">{desc}</p>
                </div>
                <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0
                  ${guarantor[key] ? 'bg-red-500 border-red-500 text-white' : 'border-gray-300'}
                `}>
                  {guarantor[key] && <span className="text-xs">✓</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </StepLayout>
  )
}
