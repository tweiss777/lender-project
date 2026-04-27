import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'

const STEPS = [
  { label: 'Business', path: '/apply/borrower' },
  { label: 'Guarantor', path: '/apply/guarantor' },
  { label: 'Loan', path: '/apply/loan' },
  { label: 'Review', path: '/apply/review' },
]

interface StepLayoutProps {
  currentStep: number // 1-indexed
  children: React.ReactNode
  onNext?: () => void
  onBack?: () => void
  nextLabel?: string
  nextDisabled?: boolean
  isLoading?: boolean
}

export default function StepLayout({
  currentStep,
  children,
  onNext,
  onBack,
  nextLabel = 'Continue',
  nextDisabled = false,
  isLoading = false,
}: StepLayoutProps) {
  const navigate = useNavigate()

  const handleBack = () => {
    if (onBack) {
      onBack()
    } else if (currentStep > 1) {
      navigate(STEPS[currentStep - 2].path)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top nav */}
      <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900">New Loan Application</h1>
        <span className="text-sm text-gray-500">Step {currentStep} of {STEPS.length}</span>
      </div>

      {/* Progress bar */}
      <div className="bg-white border-b px-6 py-4">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            {STEPS.map((step, i) => (
              <div key={step.label} className="flex items-center">
                <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium
                  ${i + 1 < currentStep ? 'bg-green-500 text-white' : ''}
                  ${i + 1 === currentStep ? 'bg-blue-600 text-white' : ''}
                  ${i + 1 > currentStep ? 'bg-gray-200 text-gray-500' : ''}
                `}>
                  {i + 1 < currentStep ? '✓' : i + 1}
                </div>
                <span className={`ml-2 text-sm hidden sm:block
                  ${i + 1 === currentStep ? 'text-blue-600 font-medium' : 'text-gray-500'}
                `}>
                  {step.label}
                </span>
                {i < STEPS.length - 1 && (
                  <div className={`w-12 h-0.5 mx-3
                    ${i + 1 < currentStep ? 'bg-green-500' : 'bg-gray-200'}
                  `} />
                )}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Page content */}
      <div className="max-w-2xl mx-auto px-6 py-8">
        {children}
      </div>

      {/* Bottom navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t px-6 py-4">
        <div className="max-w-2xl mx-auto flex justify-between">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={currentStep === 1}
          >
            Back
          </Button>
          <Button
            onClick={onNext}
            disabled={nextDisabled || isLoading}
          >
            {isLoading ? 'Saving...' : nextLabel}
          </Button>
        </div>
      </div>
    </div>
  )
}
