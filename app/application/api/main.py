from fastapi import FastAPI, APIRouter

from application.api.v1.organizations.handlers import router as organizations_router

def create_app() -> FastAPI:

    app = FastAPI(
        title="Organizations API",
        docs_url="/api/docs",
        debug=True
    )

    v1_api_router = APIRouter(prefix="/api/v1")
    v1_api_router.include_router(organizations_router)

    app.include_router(v1_api_router)

    return app