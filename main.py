from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import user_router
from models import ApiResponse

app = FastAPI(
    title="User Management API",
    description="A FastAPI backend service for User Management with RESTful APIs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with consistent response format"""
    return JSONResponse(
        status_code=400,
        content=ApiResponse(
            code=400,
            data=None,
            msg="Validation error: Invalid request data"
        ).dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent response format"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else ApiResponse(
            code=exc.status_code,
            data=None,
            msg=str(exc.detail)
        ).dict()
    )

# Include routers
app.include_router(user_router.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "User Management API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "User Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

