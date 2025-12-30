"""Main FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import engine, Base
from app.api.applications import router as applications_router
from app.api.faces import router as faces_router
from app.api.websocket import router as websocket_router
from app.schemas.common import HealthResponse, ErrorResponse

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Face Recognition Server",
    description="""
    ## 🎭 高性能人脸识别服务
    
    基于 FastAPI + PostgreSQL + InsightFace 构建的企业级人脸识别服务
    
    ### 主要功能
    
    * 👤 **应用管理** - 多应用隔离，灵活管理
    * 📸 **人脸注册** - 快速注册人脸特征
    * 🔍 **人脸搜索** - 高效的向量相似度检索
    * 📹 **实时检测** - WebSocket 实时人脸检测
    * 🎯 **高精度** - InsightFace SOTA 级算法
    
    ### 技术栈
    
    * **Web框架**: FastAPI
    * **数据库**: PostgreSQL + pgvector
    * **人脸引擎**: InsightFace (buffalo_l)
    * **向量检索**: pgvector 余弦相似度
    
    ### 快速开始
    
    1. 访问 [演示页面](/static/demo.html) 体验实时人脸检测
    2. 查看 API 文档了解接口详情
    3. 使用 WebSocket 接口实现实时应用
    
    ---
    
    **演示地址**: [/static/demo.html](/static/demo.html)
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "health",
            "description": "健康检查和系统状态"
        },
        {
            "name": "applications",
            "description": "应用管理 - 创建和管理人脸识别应用"
        },
        {
            "name": "faces",
            "description": "人脸管理 - 注册、搜索、删除人脸"
        },
        {
            "name": "websocket",
            "description": "WebSocket 实时检测 - 摄像头实时人脸检测"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for demo page
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

# Mount static files for local storage
if settings.storage_type == "local":
    storage_path = settings.local_storage_path
    if not os.path.exists(storage_path):
        os.makedirs(storage_path)
    app.mount("/storage", StaticFiles(directory=storage_path), name="storage")

# Include routers
app.include_router(applications_router, prefix="/api/v1")
app.include_router(faces_router, prefix="/api/v1")
app.include_router(websocket_router)


@app.get("/", response_model=HealthResponse, tags=["health"])
async def root():
    """Root endpoint - redirect to demo page.
    
    Returns basic server status and provides link to demo page.
    """
    return HealthResponse(
        status="ok",
        message="Face Recognition Server is running. Visit /static/demo.html for demo or /docs for API documentation."
    )


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="All systems operational"
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
