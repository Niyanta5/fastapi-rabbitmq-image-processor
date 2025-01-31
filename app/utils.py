import os
from PIL import Image 
from io import BytesIO
from pathlib import Path 
import logging
from .config import settings

logger = logging.getLogger(__name__)

def compress_image(filename: str) -> str:
    """Compress image and save it to processed directory"""
    try:
        input_path = Path(settings.upload_folder)/filename
        output_path = Path(settings.processed_folder)/f"compressed_{filename}"

        if not input_path.exists():
            raise FileNotFoundError(f"Source filename {filename} not found")

        with Image.open(input_path) as img:
            # Main aspect ratio with max dimensions is 800x800
            # Also convert to RGB if PNG with alpha channel
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # Optimize and compress
            buffer = BytesIO()
            img.save(
                buffer,
                format="JPEG",
                quality=70,
                optimize=True,
                progressive=True
            )
            
            # Save compressed image
            output_path.write_bytes(buffer.getvalue())

        logger.info(f"Compressed filename {filename} successfully")
        return str(output_path)

    except Exception as e:
        logger.error(f"Error processing filename {filename}: {str(e)}")
        raise e  # Re-raise exception after logging it
