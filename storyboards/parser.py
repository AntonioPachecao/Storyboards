"""Parse raw scripts into structured storyboard frames."""

from __future__ import annotations

import re
from typing import Iterable, List

from .models import FrameDraft


class StoryParser:
    """Heuristic parser that splits a script into frame drafts."""

    def __init__(self, max_beats: int = 3) -> None:
        self.max_beats = max_beats

    def parse(self, script: str) -> List[FrameDraft]:
        sections = self._split_sections(script)
        frames: List[FrameDraft] = []
        for idx, section in enumerate(sections, start=1):
            frames.append(self._build_frame(idx, section))
        return frames

    def _split_sections(self, script: str) -> List[str]:
        normalized = script.replace("\r\n", "\n").strip()
        if not normalized:
            return []

        numbered = re.split(r"(?:^|\n)\s*\d+[\).-]?\s+", normalized)
        numbered = [s.strip() for s in numbered if s.strip()]
        if len(numbered) > 1:
            return numbered

        paragraphs = [p.strip() for p in normalized.split("\n\n") if p.strip()]
        if paragraphs:
            return paragraphs

        return [normalized]

    def _build_frame(self, index: int, text: str) -> FrameDraft:
        title = self._extract_title(text)
        characters = self._extract_list(text, r"personagens?:?\s*(.+)")
        setting = self._extract_first(text, r"cen[aá]rio:?(.*)")
        mood = self._extract_first(text, r"(clima|humor|emo[cç][aã]o):?(.*)")
        beats = self._extract_beats(text)
        focus = self._extract_first(text, r"foco:?(.*)")

        return FrameDraft(
            index=index,
            raw_text=text,
            title=title,
            focus=focus,
            setting=setting,
            mood=mood,
            characters=characters,
            beats=beats,
        )

    def _extract_title(self, text: str) -> str | None:
        match = re.match(r"^(cena|quadro|scene)[:\-]\s*(.+)$", text, flags=re.IGNORECASE)
        if match:
            return match.group(2).strip()
        lines = text.splitlines()
        if len(lines) == 1:
            return None
        headline = lines[0].strip()
        return headline if len(headline.split()) <= 8 else None

    def _extract_list(self, text: str, pattern: str) -> List[str]:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            return []
        items = re.split(r",|/| e ", match.group(1))
        return [item.strip() for item in items if item.strip()]

    def _extract_first(self, text: str, pattern: str) -> str | None:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            return None
        value = match.group(1 if match.lastindex == 1 else 2).strip()
        return value or None

    def _extract_beats(self, text: str) -> List[str]:
        bullets = re.findall(r"[-•]\s*(.+)", text)
        if bullets:
            return bullets[: self.max_beats]

        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        return sentences[: self.max_beats]

    def summarize_frames(self, frames: Iterable[FrameDraft]) -> str:
        lines = []
        for frame in frames:
            title_part = f" - {frame.title}" if frame.title else ""
            lines.append(f"{frame.index:02d}{title_part}: {frame.focus or frame.raw_text[:60]}")
        return "\n".join(lines)
