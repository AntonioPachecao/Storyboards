"""Image generator abstraction layer."""

from __future__ import annotations

import datetime as _dt
from abc import ABC, abstractmethod
from typing import Dict, Optional

from .models import StoryboardFrameResult


class ImageGenerator(ABC):
    """Interface for pluggable image generators (e.g., DALL·E, Stability)."""

    @abstractmethod
    def generate_image(self, prompt: str, frame_index: int) -> StoryboardFrameResult:
        raise NotImplementedError


class MockImageGenerator(ImageGenerator):
    """Simple generator stub that simulates image creation."""

    def __init__(self) -> None:
        self._store: Dict[int, str] = {}

    def generate_image(self, prompt: str, frame_index: int) -> StoryboardFrameResult:
        timestamp = _dt.datetime.utcnow().isoformat()
        uri = f"mock://frame-{frame_index}-{timestamp}"
        self._store[frame_index] = uri
        return StoryboardFrameResult(
            frame=None,  # to be filled by pipeline
            prompt=prompt,
            image_uri=uri,
            generator_metadata={
                "generator": "mock",
                "generated_at": timestamp,
                "frame_index": frame_index,
            },
        )

    def get_image_uri(self, frame_index: int) -> Optional[str]:
        return self._store.get(frame_index)
