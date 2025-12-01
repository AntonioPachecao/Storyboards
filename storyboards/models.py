"""Core data models for storyboard creation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class StoryMetadata:
    """Global styling and continuity configuration."""

    title: str
    art_style: str
    color_palette: str
    aspect_ratio: str = "16:9"
    continuity_notes: Optional[str] = None


@dataclass
class FrameDraft:
    """Representation of a single frame parsed from the user's script."""

    index: int
    raw_text: str
    title: Optional[str] = None
    focus: Optional[str] = None
    setting: Optional[str] = None
    mood: Optional[str] = None
    characters: List[str] = field(default_factory=list)
    beats: List[str] = field(default_factory=list)


@dataclass
class StoryboardFrameResult:
    """Holds the generated prompt and image metadata for a frame."""

    frame: FrameDraft
    prompt: str
    image_uri: Optional[str]
    generator_metadata: Dict[str, str] = field(default_factory=dict)
