from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

docs_router = APIRouter(
    prefix="/docs"
)

@docs_router.get("/")
def get_documentation():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Custom Swagger UI",
        swagger_css_url="https://cdn.jsdelivr.net/gh/jcphlux/swagger-ui-themes@main/dist/swagger-dark-ui.css",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "nord",
            "displayRequestDuration": True,
            "tryItOutEnabled": True,
            "persistAuthorization": True,
        },
    )