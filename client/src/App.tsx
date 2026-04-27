import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import BorrowerStep from '@/pages/apply/BorrowerStep'
import GuarantorStep from '@/pages/apply/GuarantorStep'
import LoanStep from '@/pages/apply/LoanStep'
import ReviewStep from '@/pages/apply/ReviewStep'
import ResultsPage from '@/pages/ResultsPage'
import LendersPage from '@/pages/LendersPage'
import AddLenderPage from '@/pages/AddLenderPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/apply/borrower" replace />} />
        <Route path="/apply/borrower" element={<BorrowerStep />} />
        <Route path="/apply/guarantor" element={<GuarantorStep />} />
        <Route path="/apply/loan" element={<LoanStep />} />
        <Route path="/apply/review" element={<ReviewStep />} />
        <Route path="/applications/:borrower_id/results" element={<ResultsPage />} />
        <Route path="/lenders" element={<LendersPage />} />
        <Route path="/lenders/add" element={<AddLenderPage />} />
      </Routes>
    </BrowserRouter>
  )
}
