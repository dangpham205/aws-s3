from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import baongay, workflow, public

desc = """
Phục vụ upload file ảnh, video, âm thanh
"""
tags_metadata = [
    {
        "name": "APIS",
        "description": "Service CMS xài phần này",
    },
    {
        "name": "Workflow",
        "description": "Workflow xài phần này",
    },
    {
        "name": "Public",
        "description": "Upload các resource public",
    },
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

app.include_router(baongay.router)
app.include_router(workflow.router)
app.include_router(public.router)