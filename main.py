from fastapi import FastAPI

app = FastAPI(
    title="AZRA bills",
    summary="A web-based billing management system that allows organizations and vendors to handle bill creation, customer assignment, and secure payments, with reporting and alert features.",
    description="A web-based billing management platform enabling organizations and vendors to create, update, assign, and close bills. It supports customer payments through UPI, digital wallets, and cards, with reporting on outstanding payments, customer-specific insights, and high-value transaction alerts for secure management.",
    version="1.0.0",
)


@app.get("/health-check")
async def health_check():
    return {"status": True}
