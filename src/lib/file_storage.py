"""File storage utility library for EMIS."""
import hashlib
import os
from pathlib import Path
from typing import Optional
from uuid import uuid4
import aiofiles

from fastapi import UploadFile
from src.config import settings
from src.lib.logging import get_logger

logger = get_logger(__name__)


class FileStorage:
    """Service for handling file uploads and storage."""

    def __init__(self):
        self.base_path = Path(getattr(settings, "UPLOAD_DIR", "./uploads"))
        self.max_file_size = getattr(settings, "MAX_FILE_SIZE", 10 * 1024 * 1024)  # 10MB
        self.allowed_extensions = {
            "image": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
            "document": {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"},
            "archive": {".zip", ".tar", ".gz", ".rar"},
        }
        
        # Create upload directory if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def save_upload_file(
        self,
        file: UploadFile,
        category: str = "general",
        allowed_types: Optional[set] = None,
    ) -> dict:
        """Save an uploaded file."""
        try:
            # Validate file size
            contents = await file.read()
            if len(contents) > self.max_file_size:
                raise ValueError(f"File size exceeds maximum allowed size of {self.max_file_size} bytes")

            # Validate file extension
            file_ext = Path(file.filename).suffix.lower()
            if allowed_types and file_ext not in allowed_types:
                raise ValueError(f"File type {file_ext} not allowed")

            # Generate unique filename
            file_hash = hashlib.sha256(contents).hexdigest()[:16]
            unique_filename = f"{uuid4()}_{file_hash}{file_ext}"
            
            # Create category directory
            category_path = self.base_path / category
            category_path.mkdir(parents=True, exist_ok=True)
            
            # Save file
            file_path = category_path / unique_filename
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(contents)

            logger.info(f"File saved: {file_path}")

            return {
                "filename": unique_filename,
                "original_filename": file.filename,
                "path": str(file_path),
                "url": f"/uploads/{category}/{unique_filename}",
                "size": len(contents),
                "content_type": file.content_type,
            }

        except Exception as e:
            logger.error(f"Failed to save file {file.filename}: {e}", exc_info=True)
            raise

    async def delete_file(self, file_path: str) -> bool:
        """Delete a file."""
        try:
            path = Path(file_path)
            if path.exists() and path.is_file():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}", exc_info=True)
            return False

    def get_file_url(self, category: str, filename: str) -> str:
        """Get URL for a file."""
        return f"/uploads/{category}/{filename}"

    async def save_profile_picture(self, file: UploadFile) -> dict:
        """Save a profile picture."""
        return await self.save_upload_file(
            file,
            category="profiles",
            allowed_types=self.allowed_extensions["image"]
        )

    async def save_document(self, file: UploadFile) -> dict:
        """Save a document."""
        return await self.save_upload_file(
            file,
            category="documents",
            allowed_types=self.allowed_extensions["document"]
        )

    async def save_assignment_file(self, file: UploadFile) -> dict:
        """Save an assignment file."""
        allowed_types = self.allowed_extensions["document"] | self.allowed_extensions["archive"]
        return await self.save_upload_file(
            file,
            category="assignments",
            allowed_types=allowed_types
        )


# Global file storage instance
file_storage = FileStorage()
