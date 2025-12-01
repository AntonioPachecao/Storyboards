import unittest

from storyboards import MockImageGenerator, StoryMetadata, StoryboardPipeline


class StoryboardPipelineTests(unittest.TestCase):
    def test_run_generates_prompts_and_images(self) -> None:
        script = (
            "1. Abertura numa sala iluminada; personagens: Ana e Bruno.\n"
            "- Ana sente a brisa\n"
            "- Bruno prepara café\n"
            "2) Cena externa na varanda, falando sobre viagem."
        )
        metadata = StoryMetadata(
            title="Viagem",
            art_style="aquarela cinematográfica",
            color_palette="tons pastel",
            continuity_notes="manter clima suave",
        )

        pipeline = StoryboardPipeline(generator=MockImageGenerator())
        results = pipeline.run(script, metadata)

        self.assertEqual(len(results), 2)
        for idx, result in enumerate(results, start=1):
            with self.subTest(frame=idx):
                self.assertEqual(result.frame.index, idx)
                self.assertTrue(result.prompt)
                self.assertTrue(result.image_uri)
                self.assertEqual(result.generator_metadata.get("generator"), "mock")

    def test_describe_outputs_human_readable(self) -> None:
        script = "1. Teste rápido."
        metadata = StoryMetadata(
            title="Teste",
            art_style="rabisque simplificado",
            color_palette="monocromático",
            continuity_notes="",
        )

        pipeline = StoryboardPipeline(generator=MockImageGenerator())
        description = pipeline.describe(pipeline.run(script, metadata))

        self.assertIn("Quadro 01", description)
        self.assertIn("Prompt:", description)


if __name__ == "__main__":
    unittest.main()
