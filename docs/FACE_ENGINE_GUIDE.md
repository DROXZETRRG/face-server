# 人脸引擎使用指南

## 概述

`FaceEngine` 是一个统一的人脸识别引擎，整合了完整的人脸识别流程：

1. **人脸检测 (Detection)** - 在图像中定位人脸
2. **人脸对齐 (Alignment)** - 对齐人脸以提高识别准确度
3. **特征提取 (Feature Extraction)** - 提取人脸特征向量（512维）
4. **人脸比对 (Matching)** - 比较两个人脸的相似度
5. **人脸搜索 (Search)** - 在数据库中搜索相似人脸

## 架构设计

### 为什么使用统一引擎？

**之前的设计：**
- `FaceDetector` - 人脸检测
- `FeatureExtractor` - 特征提取
- `FaceSearcher` - 人脸搜索

这种分散的设计导致：
- ❌ 需要管理多个实例
- ❌ 模型加载和状态管理复杂
- ❌ 调用链路长，易出错
- ❌ 难以实现端到端的流程优化

**现在的设计：**
- `FaceEngine` - 统一的人脸引擎

统一设计的优势：
- ✅ 单一入口，简化使用
- ✅ 统一的模型管理
- ✅ 完整的处理流程
- ✅ 更好的性能优化机会
- ✅ 更清晰的代码结构

## 快速开始

### 1. 初始化引擎

```python
from app.core.face_engine import FaceEngine, get_face_engine

# 方式1：创建新实例
engine = FaceEngine(
    detection_model="retinaface_r50",
    recognition_model="arcface_r100",
    device="cpu"  # 或 "cuda"
)
engine.load_models()

# 方式2：使用全局单例（推荐）
engine = get_face_engine()
```

### 2. 检测人脸

```python
# 从文件路径
faces = engine.detect_faces("photo.jpg", min_confidence=0.8)

# 从字节流
with open("photo.jpg", "rb") as f:
    image_bytes = f.read()
faces = engine.detect_faces(image_bytes)

# 从 PIL Image
from PIL import Image
image = Image.open("photo.jpg")
faces = engine.detect_faces(image)

# 获取最大的人脸
largest_face = engine.get_largest_face("photo.jpg")
```

### 3. 提取特征

```python
# 直接提取（假设整张图是人脸）
feature = engine.extract_features("face.jpg")
print(f"Feature shape: {feature.shape}")  # (512,)

# 带边界框提取
feature = engine.extract_features("photo.jpg", face_bbox=[100, 100, 200, 200])

# 批量提取
features = engine.extract_features_batch(["face1.jpg", "face2.jpg", "face3.jpg"])
```

### 4. 完整处理流程

```python
# 一步完成：检测 -> 对齐 -> 提取特征
result = engine.process_image("photo.jpg")

print(f"检测到 {result['face_count']} 张人脸")
if result['face_count'] > 0:
    print(f"主人脸位置: {result['primary_face']['bbox']}")
    print(f"特征向量: {result['feature'].shape}")
    
    # 可以直接使用特征向量
    feature = result['feature']
```

### 5. 人脸比对

```python
# 比较两张图片
comparison = engine.compare_faces("person1.jpg", "person2.jpg")
print(f"相似度: {comparison['similarity']:.3f}")
print(f"是否同一人: {comparison['same_person']}")

# 比较特征向量
feature1 = engine.extract_features("face1.jpg")
feature2 = engine.extract_features("face2.jpg")
similarity = engine.compare_features(feature1, feature2)
print(f"相似度: {similarity:.3f}")
```

### 6. 数据库搜索

```python
from sqlalchemy.orm import Session

# 使用图像搜索
result = engine.search_image_in_database(
    db=db,
    image_input="query.jpg",
    app_id=app_id,
    top_k=10,
    threshold=0.7,
    metadata_filter={"department": "engineering"}
)

print(f"查询耗时: {result['query_time_ms']:.2f}ms")
for match in result['matches']:
    print(f"Person {match['person_id']}: {match['similarity']:.3f}")

# 使用特征向量搜索
feature = engine.extract_features("query.jpg")
matches = engine.search_in_database(
    db=db,
    feature_vector=feature,
    app_id=app_id,
    top_k=5
)
```

## API 示例

### 注册人脸（已集成）

```python
# app/api/faces.py 中的实现
@router.post("/")
async def register_face(...):
    # 使用统一引擎处理
    result = face_engine.process_image(image_data)
    
    if result['face_count'] == 0:
        raise HTTPException(status_code=400, detail="No face detected")
    
    # 保存特征向量
    feature_vector = result['feature'].tolist()
    face = FaceService.create(db, face_data, feature_vector, ...)
```

### 搜索人脸（已集成）

```python
@router.post("/search")
async def search_faces(...):
    # 完整的搜索流程
    result = face_engine.search_image_in_database(
        db=db,
        image_input=image_data,
        app_id=app_id,
        top_k=top_k,
        threshold=threshold
    )
    
    return FaceSearchResponse(
        query_time_ms=result['query_time_ms'],
        results=result['matches']
    )
```

## 高级用法

### 自定义配置

```python
# 使用不同的模型
engine = FaceEngine(
    detection_model="mobilenet",  # 更快的检测模型
    recognition_model="arcface_r50",  # 更小的识别模型
    device="cuda"  # 使用 GPU 加速
)

# 只检测不提取特征
result = engine.process_image(
    "photo.jpg",
    extract_features=False,
    align_faces=False
)
```

### 对齐人脸

```python
# 手动对齐人脸
aligned_face = engine.align_face(
    image_input="photo.jpg",
    bbox=[100, 100, 200, 200],
    landmarks=[[120, 140], [180, 140], [150, 170], [130, 190], [170, 190]],
    output_size=(112, 112)
)
aligned_face.save("aligned.jpg")
```

### 引擎信息

```python
# 查看引擎配置
info = engine.get_info()
print(info)
# {
#     'detection_model': 'retinaface_r50',
#     'recognition_model': 'arcface_r100',
#     'device': 'cpu',
#     'loaded': True
# }
```

## 性能优化

### 使用全局单例

```python
# 推荐：使用全局单例避免重复加载模型
from app.core.face_engine import get_face_engine

engine = get_face_engine()  # 自动加载模型，全局共享
```

### 批量处理

```python
# 批量提取特征更高效
images = ["face1.jpg", "face2.jpg", "face3.jpg"]
features = engine.extract_features_batch(images)

# 如果需要更高性能，考虑使用 GPU
engine = FaceEngine(device="cuda")
```

### 模型管理

```python
# 卸载模型释放内存
engine.unload_models()

# 检查模型是否加载
if not engine.is_loaded():
    engine.load_models()
```

## 实现自己的模型

当前实现是占位代码，要接入真实的人脸识别模型：

### 1. 安装 InsightFace

```bash
pip install insightface onnxruntime
```

### 2. 修改 `load_models` 方法

```python
def load_models(self) -> None:
    """加载人脸检测和识别模型."""
    import insightface
    
    # 加载人脸分析模型（包含检测和识别）
    self._detection_model = insightface.app.FaceAnalysis()
    self._detection_model.prepare(
        ctx_id=0 if self.device == 'cuda' else -1,
        det_size=(640, 640)
    )
    
    self._loaded = True
```

### 3. 实现检测方法

```python
def detect_faces(self, image_input, min_confidence=0.5, max_faces=None):
    """检测人脸."""
    image = self._load_image(image_input)
    img_array = self._image_to_array(image)
    
    # 使用 InsightFace 检测
    faces = self._detection_model.get(img_array)
    
    results = []
    for face in faces:
        if face.det_score >= min_confidence:
            results.append({
                'bbox': face.bbox.tolist(),
                'confidence': float(face.det_score),
                'landmarks': face.kps.tolist(),
                'age': getattr(face, 'age', None),
                'gender': getattr(face, 'gender', None),
            })
    
    if max_faces:
        results = results[:max_faces]
    
    return results
```

### 4. 实现特征提取

```python
def extract_features(self, image_input, face_bbox=None, normalize=True):
    """提取特征."""
    image = self._load_image(image_input)
    img_array = self._image_to_array(image)
    
    # 获取人脸
    faces = self._detection_model.get(img_array)
    if not faces:
        raise ValueError("No face detected")
    
    # 使用第一张人脸
    face = faces[0]
    feature = face.embedding
    
    if normalize:
        feature = feature / np.linalg.norm(feature)
    
    return feature
```

### 5. 实现数据库搜索

```python
def search_in_database(self, db, feature_vector, app_id, top_k=10, threshold=0.6, metadata_filter=None):
    """搜索数据库."""
    from sqlalchemy import and_
    from app.models.face import Face
    
    query = db.query(Face).filter(
        and_(
            Face.app_id == app_id,
            Face.is_deleted == False
        )
    )
    
    # 元数据过滤
    if metadata_filter:
        for key, value in metadata_filter.items():
            query = query.filter(Face.metadata[key].astext == str(value))
    
    # pgvector 相似度搜索
    query = query.order_by(
        Face.feature_vector.cosine_distance(feature_vector)
    ).limit(top_k)
    
    results = []
    for face in query.all():
        similarity = 1 - face.feature_vector.cosine_distance(feature_vector)
        if similarity >= threshold:
            results.append({
                'face_id': face.id,
                'person_id': face.person_id,
                'similarity': float(similarity),
                'image_url': face.image_url,
                'metadata': face.metadata
            })
    
    return results
```

## 测试

```python
# 测试基本功能
def test_face_engine():
    engine = FaceEngine()
    engine.load_models()
    
    # 测试检测
    faces = engine.detect_faces("test.jpg")
    assert len(faces) > 0
    
    # 测试特征提取
    feature = engine.extract_features("test.jpg")
    assert feature.shape == (512,)
    
    # 测试比对
    similarity = engine.compare_faces("person1.jpg", "person2.jpg")
    assert 0 <= similarity['similarity'] <= 1
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_face_engine()
```

## 常见问题

### Q: 如何选择检测模型？
A: 
- `retinaface_r50`: 平衡准确度和速度
- `mobilenet`: 更快，适合实时处理
- `retinaface_mnet025`: 轻量级选择

### Q: GPU 加速如何配置？
A: 
```python
engine = FaceEngine(device="cuda")
# 确保已安装 CUDA 版本的 onnxruntime
# pip install onnxruntime-gpu
```

### Q: 如何提高搜索速度？
A: 
1. 使用 pgvector 索引
2. 限制 top_k 数量
3. 使用元数据预过滤
4. 考虑使用近似搜索（ANN）

### Q: 支持哪些图像格式？
A: 所有 PIL 支持的格式：JPG, PNG, BMP, GIF 等

## 参考资料

- [InsightFace 文档](https://github.com/deepinsight/insightface)
- [pgvector 文档](https://github.com/pgvector/pgvector)
- [项目文档](../docs/)

## 总结

`FaceEngine` 提供了一个统一、简洁的接口来处理所有人脸识别相关的任务：

✅ **简单易用** - 单一入口，清晰的 API  
✅ **功能完整** - 检测、对齐、提取、比对、搜索  
✅ **高性能** - 支持 GPU，批量处理  
✅ **灵活扩展** - 易于接入不同的模型  
✅ **生产就绪** - 单例模式，资源管理

立即开始使用人脸引擎，构建您的人脸识别应用！🚀
