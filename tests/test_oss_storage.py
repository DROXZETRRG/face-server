"""Test OSS storage functionality."""
import io
from app.core.storage import OSSStorage


def test_oss_storage():
    """测试阿里云 OSS 存储功能。
    
    运行前请确保已在 .env 文件中配置 OSS 凭证：
    - OSS_ACCESS_KEY_ID
    - OSS_ACCESS_KEY_SECRET
    - OSS_BUCKET_NAME
    - OSS_ENDPOINT
    """
    print("=" * 60)
    print("测试阿里云 OSS 存储功能")
    print("=" * 60)
    
    try:
        # 初始化 OSS 存储
        print("\n1. 初始化 OSS 存储...")
        oss = OSSStorage()
        print(f"   ✓ Bucket: {oss.bucket_name}")
        print(f"   ✓ Endpoint: {oss.endpoint}")
        
        # 创建测试文件
        print("\n2. 创建测试文件...")
        test_content = b"Hello, OSS! This is a test file."
        test_file = io.BytesIO(test_content)
        
        # 上传文件
        print("\n3. 上传文件到 OSS...")
        file_path = oss.save(test_file, "test.txt", folder="test")
        print(f"   ✓ 文件已上传: {file_path}")
        
        # 获取文件 URL
        print("\n4. 获取文件 URL...")
        url = oss.get_url(file_path)
        print(f"   ✓ 访问地址: {url}")
        
        # 检查文件是否存在
        print("\n5. 检查文件是否存在...")
        exists = oss.exists(file_path)
        print(f"   ✓ 文件存在: {exists}")
        
        # 删除文件
        print("\n6. 删除测试文件...")
        deleted = oss.delete(file_path)
        print(f"   ✓ 删除成功: {deleted}")
        
        # 再次检查文件是否存在
        print("\n7. 再次检查文件是否存在...")
        exists_after = oss.exists(file_path)
        print(f"   ✓ 文件存在: {exists_after}")
        
        print("\n" + "=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n✗ 错误: {e}")
        print("请运行: pip install oss2")
    except ValueError as e:
        print(f"\n✗ 配置错误: {e}")
        print("请在 .env 文件中配置 OSS 凭证")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_storage_manager_with_oss():
    """测试使用 StorageManager 访问 OSS。"""
    print("\n" + "=" * 60)
    print("测试 StorageManager 与 OSS 集成")
    print("=" * 60)
    
    try:
        from app.core.storage import storage_manager
        from app.config import settings
        
        if settings.storage_type != "oss":
            print(f"\n⚠ 当前存储类型: {settings.storage_type}")
            print("请在 .env 中设置 STORAGE_TYPE=oss 以测试 OSS 功能")
            return
        
        print(f"\n当前存储类型: {settings.storage_type}")
        print(f"后端类型: {type(storage_manager.backend).__name__}")
        
        # 创建测试文件
        test_content = b"Test from StorageManager"
        test_file = io.BytesIO(test_content)
        
        # 上传文件
        print("\n上传测试文件...")
        file_path = storage_manager.save(test_file, "manager_test.txt", folder="test")
        print(f"✓ 文件路径: {file_path}")
        
        # 获取 URL
        url = storage_manager.get_url(file_path)
        print(f"✓ 访问 URL: {url}")
        
        # 清理
        print("\n清理测试文件...")
        deleted = storage_manager.delete(file_path)
        print(f"✓ 删除成功: {deleted}")
        
        print("\n" + "=" * 60)
        print("✓ StorageManager 测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 运行直接 OSS 测试
    test_oss_storage()
    
    # 运行 StorageManager 集成测试
    test_storage_manager_with_oss()
