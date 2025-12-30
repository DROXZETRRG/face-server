#!/usr/bin/env python3
"""Development setup script."""
import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and print its status."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    print(f"✅ Success: {description}")
    return True


def main():
    """Main setup function."""
    print("🚀 Face Server Development Setup")
    print("⚠️  Note: Local development uses uv, Docker uses pip")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file from .env.example...")
        if os.path.exists(".env.example"):
            subprocess.run("copy .env.example .env", shell=True)
            print("✅ .env file created. Please review and update if needed.")
        else:
            print("⚠️ .env.example not found. Please create .env manually.")
    
    # Create storage directory
    if not os.path.exists("storage"):
        os.makedirs("storage")
        print("✅ Storage directory created")
    
    # Install dependencies with uv
    if not run_command(
        "uv pip install -e .",
        "Installing Python dependencies with uv (local development)"
    ):
        print("\n⚠️ If uv is not installed, install it with: pip install uv")
        print("Or install dependencies with pip: pip install -e .")
        return
    
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Start PostgreSQL:")
    print("   docker-compose up postgres -d")
    print("\n2. Run database migrations:")
    print("   alembic upgrade head")
    print("\n3. Start the development server:")
    print("   uvicorn app.main:app --reload")
    print("\n4. Access the API documentation:")
    print("   http://localhost:8000/docs")
    print("\n5. Or start everything with Docker Compose:")
    print("   docker-compose up")


if __name__ == "__main__":
    main()
