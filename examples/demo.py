"""Exemplo de execução rápida do pipeline de storyboard."""

from storyboards import MockImageGenerator, StoryMetadata, StoryboardPipeline


SCRIPT = """
1. Cena: sala de estar ao amanhecer. Personagens: Ana e Bruno.
   - Ana observa a luz entrando pela janela.
   - Bruno prepara café.
2) Varanda com vista para a cidade. Foco: conversa sobre viagem.
"""


def main() -> None:
    metadata = StoryMetadata(
        title="Viagem",
        art_style="aquarela cinematográfica",
        color_palette="tons pastel",  # paleta de cores consistente
        continuity_notes="iluminação suave em todos os quadros",
    )

    pipeline = StoryboardPipeline(generator=MockImageGenerator())
    results = pipeline.run(SCRIPT, metadata)

    print("Storyboards gerados:\n")
    print(pipeline.describe(results))


if __name__ == "__main__":
    main()
