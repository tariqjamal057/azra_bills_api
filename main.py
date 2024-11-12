from fastapi import FastAPI

app = FastAPI(
    title="AZRA Bills API",
    summary="A SaaS laundry management system for single and multi-store businesses, "
    "facilitating bill generation, updates, customer assignment, and cash payment logging. "
    "Customers can view and pay bills through multiple channels and receive status reminders. "
    "It includes dashboards, transaction reporting, and high-value alerts for efficient and "
    "secure operations.",
    description="This SaaS-based laundry management solution supports both single-location and "
    "multi-store setups, streamlining billing and payment processes. It enables businesses to "
    "generate, update, and assign bills, log cash payments, and provide reminders on order "
    "status. Customers benefit from convenient bill viewing and payment options, including "
    "UPI, wallets and cards. Robust features such as customizable dashboards, detailed "
    "transaction reports, and alerts for high-value orders ensure secure handling and "
    "improved operational oversight for businesses and customers alike.",
    version="1.0.0",
)


@app.get("/health-check")
async def health_check():
    return {"status": True}
