from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import router

desc = """
Phục vụ upload file ảnh, video, âm thanh
"""
tags_metadata = [
]

app = FastAPI(
    title='APIs upload',
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