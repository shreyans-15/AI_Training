from fastapi import FastAPI
from routers.ticket_router import router as ticket_router

app = FastAPI(title="Smart IT Support AI")
app.include_router(ticket_router)
