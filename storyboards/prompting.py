"""Build consistent image prompts for each storyboard frame."""

from __future__ import annotations

from typing import List

from .models import FrameDraft, StoryMetadata


class PromptBuilder:
    """Compose detailed prompts that preserve style and continuity."""

    def __init__(self, language: str = "pt-BR") -> None:
        self.language = language

    def build_prompt(self, frame: FrameDraft, metadata: StoryMetadata) -> str:
        parts: List[str] = []
        parts.append(
            f"Storyboard visual no estilo {metadata.art_style}, paleta de cores {metadata.color_palette}, proporção {metadata.aspect_ratio}."
        )
        if metadata.continuity_notes:
            parts.append(f"Manter continuidade: {metadata.continuity_notes}.")

        if frame.title:
            parts.append(f"Título do quadro: {frame.title}.")

        focus = frame.focus or frame.beats[0] if frame.beats else frame.raw_text
        parts.append(f"Foco principal: {focus}.")

        if frame.setting:
            parts.append(f"Cenário: {frame.setting}.")
        if frame.characters:
            parts.append("Personagens: " + ", ".join(frame.characters) + ".")
        if frame.mood:
            parts.append(f"Clima/emoção: {frame.mood}.")

        if frame.beats:
            beat_text = " | ".join(frame.beats)
            parts.append(f"Momentos-chave: {beat_text}.")

        parts.append("Consistir com quadros anteriores: manter enquadramento, cores e figurinos coerentes.")

        return " ".join(parts)
