# Storyboards

Ferramentas para criar storyboards visuais a partir de um roteiro e storytelling.

## Estrutura
- `storyboards.parser.StoryParser`: identifica quadros no roteiro e extrai metadados básicos.
- `storyboards.prompting.PromptBuilder`: monta prompts detalhados mantendo estilo e continuidade.
- `storyboards.generator.ImageGenerator`: interface para geradores de imagem (ex.: DALL·E). Inclui `MockImageGenerator` para testes.
- `storyboards.pipeline.StoryboardPipeline`: orquestra parsing, criação de prompts e geração de imagens.

## Exemplo rápido
```python
from storyboards import StoryMetadata, StoryParser, PromptBuilder, MockImageGenerator, StoryboardPipeline

script = """
1. Cena: Sala de estar ao amanhecer. Personagens: Ana e Bruno.
   - Ana observa a luz entrando pela janela
   - Bruno prepara café
2. Na varanda, ambos discutem calmamente sobre a viagem.
"""

metadata = StoryMetadata(
    title="Viagem",
    art_style="aquarela cinematográfica",
    color_palette="tons pastel com azul dominante",
    continuity_notes="manter figurinos e iluminação suave"
)

pipeline = StoryboardPipeline(generator=MockImageGenerator())
results = pipeline.run(script, metadata)
print(pipeline.describe(results))
```

O pipeline divide o roteiro em quadros, cria prompts consistentes para cada um e aciona o gerador configurado para produzir as imagens.

## Como testar rapidamente

- **Demo interativa**: rode `python examples/demo.py` para gerar prompts e URIs fictícias usando o `MockImageGenerator`.
- **Testes automatizados**: execute `python -m unittest discover -s tests -p "test_*.py"` para validar o parser, o pipeline e a geração mock.
