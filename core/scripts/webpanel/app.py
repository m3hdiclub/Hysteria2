#!/usr/bin/env python3

import sys
import os
import secrets
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles

# Append directory of cli_api.py to be able to import it
HYSTERIA_CORE_DIR = '/etc/hysteria/core/'
sys.path.append(HYSTERIA_CORE_DIR)

import routers  # noqa: This import should be after the sys.path modification, because it imports cli_api
import cli_api  # noqa

# region Setup App
app = FastAPI(debug=True)
secret_key = os.getenv("SESSION_SECRET_KEY", secrets.token_urlsafe(32))

app.mount('/assets', StaticFiles(directory='assets'), name='assets')
templates = Jinja2Templates(directory='templates')

app.add_middleware(SessionMiddleware, secret_key=secret_key)

# endregion


# region Routers

# Add API version 1 router
app.include_router(routers.api.v1.api_v1_router, prefix='/api/v1', tags=['v1'])  # Add API version 1 router
# Add user router
app.include_router(routers.user.router, prefix='/users', tags=['users'])

# Add basic routes


@app.get('/login')
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.get('/logout')
async def logout(request: Request):
    pass


@ app.get('/')
async def index(request: Request):
    users = cli_api.list_users()
    return templates.TemplateResponse('index.html', {'request': request, 'users': users})


@ app.get('/home')
async def home(request: Request):
    return await index(request)
# endregion


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080)
