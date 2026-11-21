# aula_python

Repositório de estudos do usuário. Além dos exercícios de Python na raiz, tem o app de estudo de francês em `frances/`.

## App de francês (`frances/`)

- App de estudo baseado no *Tex's French Grammar* (UT Austin). Publicado como artefato: https://claude.ai/artifact/UvcJPCRSvVqK38WUTybMWB
- `frances/grammaire-tex.html` é gerado: edite `frances/src/app.html` e rode `python3 frances/src/build.py`.
- Dados: `src/lessons.json` (HTML limpo das lições, imagens embutidas), `src/study.json` (flashcards e termos, gerados por `src/cards.py`), `src/titles_pt.json`, `src/index.json`. Áudios: `frances/audiopack/<lição>.js`.
- Visual: caderno escolar francês (pauta Seyès, tinta azul, margem vermelha); no escuro, lousa. Textos da interface em português.
- Lições reescritas (meu formato, em português) ficam em `src/novas.json`: `ideia`, `resumo`, `blocos[{t, txt, itens[{fr, pt, ex, obs, a}]}]`, `armadilhas`, `treino[{q, r, pt, alt}]`. Prontas: substantivos (no1–no5) e advérbios (adv1–adv6). Cada palavra de lista vira um item com exemplo (`ex: "frase fr · tradução"`).
- Tradução e exemplos que faltam são gerados pelo Claude dentro do app (capacidade `sample`) e guardados no db do artefato (`traducoes/`, `exemplos/`).

### Direção combinada com o usuário (lembrar sempre)

- As páginas das lições, como estão hoje, servem só para dar uma ideia do conteúdo. **Elas precisam ser retrabalhadas para ficarem mais gostosas de estudar**, e não apenas reproduzir o site original.
- O usuário prefere listas a tabelas apertadas, cada item com exemplo; letra e espaçamento compactos; tudo em português.
