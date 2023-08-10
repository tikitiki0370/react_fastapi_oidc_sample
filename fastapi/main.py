import os
import secrets

import uvicorn
from authlib.integrations.starlette_client import OAuth
from convert_hs256jwks import convert_hs256jwks
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import RedirectResponse


app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))

origins = ["http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")


oauth = OAuth()
if os.getenv("GOOGLE_CLIENT_ID"):
    oauth.register(
        "google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid",
        },
    )


if os.getenv("LINE_CHANNEL_ID"):
    oauth.register(
        "line",
        client_id=os.getenv("LINE_CHANNEL_ID"),
        client_secret=os.getenv("LINE_CHANNEL_SECRET"),
        client_kwargs={
            "scope": "openid",
        },
        token_endpoint="https://api.line.me/oauth2/v2.1/token",
        authorize_url="https://access.line.me/oauth2/v2.1/authorize",
        id_token_signing_alg_values_supported=["HS256"],
        jwks=convert_hs256jwks(os.getenv("LINE_CHANNEL_SECRET")),
    )


@router.get("/login/callback/{provider}")
async def login_callback(request: Request, provider: str):
    if provider == "google":
        token = await oauth.google.authorize_access_token(request)
    elif provider == "line":
        token = await oauth.line.authorize_access_token(request)

    response = RedirectResponse(url="http://127.0.0.1:8080/Check")
    response.set_cookie(
        key="token",
        value=token["id_token"],
        httponly=True,
        domain="127.0.0.1",
        path="/",
        samesite="lax",
    )
    response.set_cookie(
        key="token_provider",
        value=provider,
        httponly=False,
        domain="127.0.0.1",
        path="/",
        samesite="lax",
    )
    return response


@router.get("/login/{provider}")
async def login(request: Request, provider: str):
    redirect_uri = request.url_for("login_callback", provider=provider)
    print(redirect_uri)
    if provider == "google":
        return await oauth.google.authorize_redirect(request, redirect_uri)
    elif provider == "line":
        return await oauth.line.authorize_redirect(request, redirect_uri)


@router.get("/check")
async def check(request: Request):
    raw_token = request.cookies.get("token")
    token_provider = request.cookies.get("token_provider")
    if token_provider == "google":
        token = await oauth.google.parse_id_token({"id_token": raw_token}, nonce=None)
    elif token_provider == "line":
        token = await oauth.line.parse_id_token({"id_token": raw_token}, nonce=None)
    return token

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app)
