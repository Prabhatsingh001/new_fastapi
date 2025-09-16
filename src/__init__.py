from fastapi import FastAPI
from src.books.routes import router as books_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from .middleware import register_middleware
from .errors import register_error_handlers

version = "v1"
app = FastAPI(
    title="Books API",
    description="A simple API to manage books",
    version = version
)

register_error_handlers(app)
register_middleware(app)
app.include_router(books_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Review"])