"""
Multimodal input processing module for MediProof.
Handles image, audio, video, and text input for claim verification.
"""

from .image_input import process_image

__all__ = [
    'process_image',
]
