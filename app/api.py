from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import router

desc = """
Khởi tạo, quản lý data phục vụ cho workflow
"""
tags_metadata = [
]

app = FastAPI(
    title='API for workflow',
    description=desc,
    version='0.0.1',
    contact={
        'name': '@dev_tuoitre',
        'email': 'tự search'
    },
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url="/redoc")


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins= ["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)