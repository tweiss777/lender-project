from fastapi import FastAPI
from app.routes.borrowers import borrower_routes
from app.routes.loan_requests import loan_requests_routes
from app.routes.lenders import lender_routes
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()
PORT = int(os.environ.get("PORT", 3000))
app = FastAPI() 
app.include_router(borrower_routes, prefix="/api/v1/borrowers")
app.include_router(loan_requests_routes, prefix="/api/v1/loan_requests")
app.include_router(lender_routes,prefix="/api/v1/lenders")
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
