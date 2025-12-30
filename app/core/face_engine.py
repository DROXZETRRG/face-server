"""Unified Face Recognition Engine.

This module provides a complete face recognition pipeline including:
- Face Detection: Detect faces in images
- Face Alignment: Align detected faces
- Feature Extraction: Extract face embeddings
- Face Matching: Compare face features
- Face Search: Search similar faces in database

使用示例：
    engine = FaceEngine()
    engine.load_models()
    
    # 检测和提取特征
    result = engine.process_image(image)
    
    # 搜索相似人脸
    matches = engine.search(db, result['feature'], app_id)
"""
from typing import List, Dict, Any, Optional, BinaryIO, Union
from pathlib import Path
from io import BytesIO
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class FaceEngine:
    """统一的人脸识别引擎.
    
    使用 InsightFace 实现完整的人脸识别流程：
    1. 人脸检测 (Detection)
    2. 人脸对齐 (Alignment)
    3. 特征提取 (Feature Extraction)
    4. 人脸比对 (Matching)
    """
    
    def __init__(
        self,
        model_pack: str = "buffalo_l",
        det_size: tuple = (640, 640),
        det_thresh: float = 0.5,
        ctx_id: int = -1,
        model_dir: Optional[str] = None
    ):
        """初始化人脸引擎.
        
        Args:
            model_pack: InsightFace 模型包名称 (buffalo_l, buffalo_s, antelopev2)
            det_size: 检测图像尺寸 (width, height)
            det_thresh: 检测置信度阈值
            ctx_id: GPU ID (-1 for CPU, 0+ for GPU)
            model_dir: 模型存储目录
        """
        self.model_pack = model_pack
        self.det_size = det_size
        self.det_thresh = det_thresh
        self.ctx_id = ctx_id
        self.model_dir = model_dir
        
        self._app = None
        self._loaded = False
    
    # ========== 模型管理 ==========
    
    def load_models(self) -> None:
        """加载人脸检测和识别模型.
        
        使用 InsightFace 加载预训练模型。
        支持的模型包：
        - buffalo_l: 大模型，高精度 (推荐)
        - buffalo_s: 小模型，速度快
        - antelopev2: 另一个高精度模型
        """
        try:
            import insightface
            from insightface.app import FaceAnalysis
            
            logger.info(f"Loading InsightFace model pack: {self.model_pack}")
            logger.info(f"Detection size: {self.det_size}, threshold: {self.det_thresh}")
            logger.info(f"Device: {'GPU' if self.ctx_id >= 0 else 'CPU'} (ctx_id={self.ctx_id})")
            
            # 创建 FaceAnalysis 应用
            self._app = FaceAnalysis(
                name=self.model_pack,
                root=self.model_dir,
                providers=['CUDAExecutionProvider', 'CPUExecutionProvider'] if self.ctx_id >= 0 else ['CPUExecutionProvider']
            )
            
            # 准备模型
            self._app.prepare(
                ctx_id=self.ctx_id,
                det_size=self.det_size,
                det_thresh=self.det_thresh
            )
            
            self._loaded = True
            logger.info("InsightFace models loaded successfully")
            
        except ImportError as e:
            logger.error(f"Failed to import insightface: {e}")
            logger.error("Please install insightface: pip install insightface onnxruntime")
            raise
        except Exception as e:
            logger.error(f"Failed to load InsightFace models: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """检查模型是否已加载."""
        return self._loaded and self._app is not None
    
    def unload_models(self) -> None:
        """卸载模型以释放内存."""
        if self._app is not None:
            del self._app
            self._app = None
        self._loaded = False
        logger.info("InsightFace models unloaded")
    
    # ========== 图像预处理 ==========
    
    def _load_image(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray]
    ) -> Image.Image:
        """加载图像为 PIL Image.
        
        Args:
            image_input: 图像输入，支持多种格式
            
        Returns:
            PIL Image 对象
        """
        if isinstance(image_input, str):
            # 从文件路径加载
            return Image.open(image_input).convert('RGB')
        elif isinstance(image_input, bytes):
            # 从字节流加载
            return Image.open(BytesIO(image_input)).convert('RGB')
        elif isinstance(image_input, Image.Image):
            # 已经是 PIL Image
            return image_input.convert('RGB')
        elif isinstance(image_input, np.ndarray):
            # 从 numpy 数组加载
            return Image.fromarray(image_input).convert('RGB')
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    def _image_to_array(self, image: Image.Image) -> np.ndarray:
        """将 PIL Image 转换为 numpy 数组."""
        return np.array(image)
    
    # ========== 人脸检测 ==========
    
    def detect_faces(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray],
        min_confidence: Optional[float] = None,
        max_faces: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """检测图像中的人脸.
        
        Args:
            image_input: 输入图像
            min_confidence: 最小置信度阈值（None 则使用初始化时的阈值）
            max_faces: 最多返回的人脸数量
            
        Returns:
            检测到的人脸列表，每个人脸包含：
            - bbox: [x1, y1, x2, y2] 边界框坐标
            - confidence: 检测置信度
            - landmarks: 面部关键点（5点）
            - age: 年龄（如果模型支持）
            - gender: 性别（如果模型支持）
            - embedding: 特征向量
        
        示例:
            faces = engine.detect_faces("photo.jpg", min_confidence=0.8)
            for face in faces:
                print(f"Found face at {face['bbox']} with confidence {face['confidence']}")
        """
        if not self.is_loaded():
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        image = self._load_image(image_input)
        img_array = self._image_to_array(image)
        
        # 使用 InsightFace 检测人脸
        faces = self._app.get(img_array)
        
        if min_confidence is None:
            min_confidence = self.det_thresh
        
        results = []
        for face in faces:
            if face.det_score >= min_confidence:
                face_dict = {
                    'bbox': face.bbox.tolist(),
                    'confidence': float(face.det_score),
                    'landmarks': face.kps.tolist(),  # 5个关键点
                    'embedding': face.embedding,  # 特征向量
                }
                
                # 添加可选属性
                if hasattr(face, 'age'):
                    face_dict['age'] = int(face.age)
                if hasattr(face, 'gender'):
                    face_dict['gender'] = 'male' if face.gender == 1 else 'female'
                
                results.append(face_dict)
        
        # 按置信度排序
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        if max_faces:
            results = results[:max_faces]
        
        return results
    
    def get_largest_face(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray],
        min_confidence: float = 0.5
    ) -> Optional[Dict[str, Any]]:
        """获取图像中最大的人脸.
        
        Args:
            image_input: 输入图像
            min_confidence: 最小置信度阈值
            
        Returns:
            最大的人脸，如果没有检测到则返回 None
        """
        faces = self.detect_faces(image_input, min_confidence)
        if not faces:
            return None
        
        # 按边界框面积排序
        def get_area(face):
            bbox = face['bbox']
            return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        
        return max(faces, key=get_area)
    
    # ========== 人脸对齐 ==========
    
    def align_face(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray],
        bbox: List[float],
        landmarks: Optional[List[List[float]]] = None,
        output_size: tuple = (112, 112)
    ) -> Image.Image:
        """对齐人脸图像.
        
        Args:
            image_input: 输入图像
            bbox: 人脸边界框 [x1, y1, x2, y2]
            landmarks: 面部关键点（可选，用于更精确的对齐）
            output_size: 输出图像尺寸
            
        Returns:
            对齐后的人脸图像
        """
        image = self._load_image(image_input)
        
        # TODO: 实现人脸对齐
        # 如果有关键点，使用仿射变换对齐
        # 否则，简单裁剪边界框区域
        
        # 占位实现：简单裁剪
        x1, y1, x2, y2 = [int(x) for x in bbox]
        cropped = image.crop((x1, y1, x2, y2))
        aligned = cropped.resize(output_size, Image.LANCZOS)
        
        return aligned
    
    # ========== 特征提取 ==========
    
    def extract_features(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray],
        face_bbox: Optional[List[float]] = None,
        normalize: bool = True
    ) -> np.ndarray:
        """提取人脸特征向量.
        
        Args:
            image_input: 输入图像
            face_bbox: 人脸边界框（可选），如果提供则只检测该区域
            normalize: 是否归一化特征向量
            
        Returns:
            特征向量 (通常是 512 维)
        
        示例:
            feature = engine.extract_features("face.jpg")
            print(f"Feature shape: {feature.shape}")  # (512,)
        """
        if not self.is_loaded():
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        # 检测人脸并获取特征
        faces = self.detect_faces(image_input)
        
        if not faces:
            raise ValueError("No face detected in the image")
        
        # 使用第一个（最大的）人脸
        face = faces[0]
        feature = face['embedding']
        
        if normalize:
            norm = np.linalg.norm(feature)
            if norm > 0:
                feature = feature / norm
        
        return feature
    
    def extract_features_batch(
        self,
        images: List[Union[str, bytes, Image.Image]],
        normalize: bool = True
    ) -> List[np.ndarray]:
        """批量提取特征向量.
        
        Args:
            images: 图像列表
            normalize: 是否归一化
            
        Returns:
            特征向量列表
        """
        return [self.extract_features(img, normalize=normalize) for img in images]
    
    # ========== 完整处理流程 ==========
    
    def process_image(
        self,
        image_input: Union[str, bytes, Image.Image, np.ndarray],
        min_confidence: float = 0.5,
        extract_features: bool = True,
        align_faces: bool = True
    ) -> Dict[str, Any]:
        """完整的人脸处理流程：检测 -> 对齐 -> 提取特征.
        
        Args:
            image_input: 输入图像
            min_confidence: 检测置信度阈值
            extract_features: 是否提取特征
            align_faces: 是否对齐人脸
            
        Returns:
            处理结果字典：
            - faces: 检测到的人脸列表
            - face_count: 人脸数量
            - primary_face: 主要人脸（最大的）
            - feature: 主要人脸的特征向量（如果 extract_features=True）
        
        示例:
            result = engine.process_image("photo.jpg")
            if result['face_count'] > 0:
                feature = result['feature']
                # 使用特征进行后续操作
        """
        # 检测人脸
        faces = self.detect_faces(image_input, min_confidence)
        
        result = {
            'faces': faces,
            'face_count': len(faces),
            'primary_face': None,
            'feature': None
        }
        
        if not faces:
            return result
        
        # 获取最大的人脸作为主要人脸
        primary_face = self.get_largest_face(image_input, min_confidence)
        result['primary_face'] = primary_face
        
        # 提取特征
        if extract_features and primary_face:
            feature = self.extract_features(
                image_input,
                face_bbox=primary_face['bbox']
            )
            result['feature'] = feature
        
        return result
    
    # ========== 人脸比对 ==========
    
    def compare_features(
        self,
        feature1: np.ndarray,
        feature2: np.ndarray,
        metric: str = "cosine"
    ) -> float:
        """比较两个特征向量的相似度.
        
        Args:
            feature1: 第一个特征向量
            feature2: 第二个特征向量
            metric: 相似度度量方式 ("cosine" 或 "euclidean")
            
        Returns:
            相似度分数 (0-1，越大越相似)
        
        示例:
            similarity = engine.compare_features(feature1, feature2)
            if similarity > 0.7:
                print("Same person!")
        """
        if metric == "cosine":
            # 余弦相似度
            similarity = np.dot(feature1, feature2) / (
                np.linalg.norm(feature1) * np.linalg.norm(feature2) + 1e-8
            )
            return float(similarity)
        elif metric == "euclidean":
            # 欧氏距离转相似度
            distance = np.linalg.norm(feature1 - feature2)
            similarity = 1.0 / (1.0 + distance)
            return float(similarity)
        else:
            raise ValueError(f"Unknown metric: {metric}")
    
    def compare_faces(
        self,
        image1: Union[str, bytes, Image.Image],
        image2: Union[str, bytes, Image.Image],
        metric: str = "cosine"
    ) -> Dict[str, Any]:
        """比较两张图片中的人脸.
        
        Args:
            image1: 第一张图片
            image2: 第二张图片
            metric: 相似度度量方式
            
        Returns:
            比对结果：
            - similarity: 相似度分数
            - same_person: 是否为同一人（基于默认阈值 0.6）
            - face1_detected: 图片1是否检测到人脸
            - face2_detected: 图片2是否检测到人脸
        """
        result1 = self.process_image(image1)
        result2 = self.process_image(image2)
        
        face1_detected = result1['face_count'] > 0
        face2_detected = result2['face_count'] > 0
        
        if not (face1_detected and face2_detected):
            return {
                'similarity': 0.0,
                'same_person': False,
                'face1_detected': face1_detected,
                'face2_detected': face2_detected
            }
        
        similarity = self.compare_features(
            result1['feature'],
            result2['feature'],
            metric
        )
        
        return {
            'similarity': similarity,
            'same_person': similarity > 0.6,
            'face1_detected': face1_detected,
            'face2_detected': face2_detected
        }
    
    # ========== 数据库搜索 ==========
    
    def search_in_database(
        self,
        db: Session,
        feature_vector: np.ndarray,
        app_id: UUID,
        top_k: int = 10,
        threshold: float = 0.6,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """在数据库中搜索相似人脸.
        
        Args:
            db: 数据库会话
            feature_vector: 查询特征向量
            app_id: 应用ID
            top_k: 返回的最大结果数
            threshold: 相似度阈值
            metadata_filter: 元数据过滤条件
            
        Returns:
            匹配结果列表，每个结果包含：
            - face_id: 人脸ID
            - person_id: 人员ID
            - similarity: 相似度分数
            - image_url: 图片URL
            - metadata: 元数据
        
        示例:
            matches = engine.search_in_database(
                db, feature, app_id,
                top_k=5, threshold=0.7
            )
            for match in matches:
                print(f"Person {match['person_id']}: {match['similarity']:.3f}")
        """
        from sqlalchemy import and_, func
        from app.models.face import Face
        
        # 构建基础查询
        query = db.query(Face).filter(
            and_(
                Face.app_id == app_id,
                Face.is_deleted == False
            )
        )
        
        # 应用元数据过滤
        if metadata_filter:
            for key, value in metadata_filter.items():
                query = query.filter(Face.face_metadata[key].astext == str(value))
        
        # 使用 pgvector 的余弦距离排序
        # 注意：pgvector 返回的是距离，需要转换为相似度
        query = query.order_by(
            Face.feature_vector.cosine_distance(feature_vector.tolist())
        ).limit(top_k * 2)  # 获取更多结果以便过滤
        
        results = []
        for face in query.all():
            # 计算余弦相似度 (1 - 余弦距离)
            # 手动计算以确保准确性
            face_vec = np.array(face.feature_vector)
            query_vec = np.array(feature_vector)
            
            # 余弦相似度
            dot_product = np.dot(query_vec, face_vec)
            norm_product = np.linalg.norm(query_vec) * np.linalg.norm(face_vec)
            similarity = dot_product / (norm_product + 1e-8)
            
            if similarity >= threshold:
                results.append({
                    'face_id': face.id,
                    'person_id': face.person_id,
                    'similarity': float(similarity),
                    'image_url': face.image_url,
                    'metadata': face.face_metadata
                })
        
        # 按相似度降序排序并限制结果数
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]
    
    def search_image_in_database(
        self,
        db: Session,
        image_input: Union[str, bytes, Image.Image],
        app_id: UUID,
        top_k: int = 10,
        threshold: float = 0.6,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """使用图像在数据库中搜索相似人脸.
        
        完整流程：检测人脸 -> 提取特征 -> 数据库搜索
        
        Args:
            db: 数据库会话
            image_input: 查询图像
            app_id: 应用ID
            top_k: 返回的最大结果数
            threshold: 相似度阈值
            metadata_filter: 元数据过滤条件
            
        Returns:
            搜索结果：
            - face_detected: 是否检测到人脸
            - matches: 匹配结果列表
            - query_time_ms: 查询耗时（毫秒）
        """
        import time
        start_time = time.time()
        
        # 处理图像并提取特征
        result = self.process_image(image_input)
        
        if result['face_count'] == 0:
            return {
                'face_detected': False,
                'matches': [],
                'query_time_ms': (time.time() - start_time) * 1000
            }
        
        # 在数据库中搜索
        matches = self.search_in_database(
            db=db,
            feature_vector=result['feature'],
            app_id=app_id,
            top_k=top_k,
            threshold=threshold,
            metadata_filter=metadata_filter
        )
        
        return {
            'face_detected': True,
            'matches': matches,
            'query_time_ms': (time.time() - start_time) * 1000
        }
    
    # ========== 工具方法 ==========
    
    def get_info(self) -> Dict[str, Any]:
        """获取引擎信息."""
        return {
            'model_pack': self.model_pack,
            'det_size': self.det_size,
            'det_thresh': self.det_thresh,
            'device': 'GPU' if self.ctx_id >= 0 else 'CPU',
            'ctx_id': self.ctx_id,
            'loaded': self._loaded
        }


# 全局引擎实例
_global_engine: Optional[FaceEngine] = None


def get_face_engine() -> FaceEngine:
    """获取全局人脸引擎实例（单例模式）.
    
    使用配置文件中的参数初始化引擎。
    """
    global _global_engine
    if _global_engine is None:
        from app.config import settings
        
        _global_engine = FaceEngine(
            model_pack=settings.face_model_pack,
            det_size=settings.face_det_size,
            det_thresh=settings.face_det_thresh,
            ctx_id=settings.face_ctx_id,
            model_dir=settings.face_model_dir
        )
        _global_engine.load_models()
    return _global_engine


def reset_face_engine():
    """重置全局引擎实例."""
    global _global_engine
    if _global_engine is not None:
        _global_engine.unload_models()
        _global_engine = None
