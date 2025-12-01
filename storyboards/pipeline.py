"""Orchestrates parsing, prompt building, and image generation."""

from __future__ import annotations

from dataclasses import replace
from typing import Iterable, List

from .generator import ImageGenerator
from .models import FrameDraft, StoryMetadata, StoryboardFrameResult
from .parser import StoryParser
from .prompting import PromptBuilder


class StoryboardPipeline:
    """High-level pipeline for transforming a script into storyboard images."""

    def __init__(
        self,
        parser: StoryParser | None = None,
        prompt_builder: PromptBuilder | None = None,
        generator: ImageGenerator | None = None,
    ) -> None:
        self.parser = parser or StoryParser()
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.generator = generator

    def run(self, script: str, metadata: StoryMetadata) -> List[StoryboardFrameResult]:
        frames = self.parser.parse(script)
        if not frames:
            return []

        results: List[StoryboardFrameResult] = []
        for frame in frames:
            prompt = self.prompt_builder.build_prompt(frame, metadata)
            generated = self.generator.generate_image(prompt, frame.index) if self.generator else None
            if generated:
                generated = replace(generated, frame=frame, prompt=prompt)
                results.append(generated)
            else:
                results.append(
                    StoryboardFrameResult(
                        frame=frame,
                        prompt=prompt,
                        image_uri=None,
                        generator_metadata={},
                    )
                )
        return results

    def describe(self, results: Iterable[StoryboardFrameResult]) -> str:
        lines = []
        for result in results:
            uri = result.image_uri or "(não gerada)"
            lines.append(f"Quadro {result.frame.index:02d}: {uri}\nPrompt: {result.prompt}\n")
        return "\n".join(lines)
