---
description: Atualiza bio, números, cargos ou links do perfil, nos dois idiomas
argument-hint: o que mudou
---

Atualize o perfil seguindo `CLAUDE.md` e `SITE_SPEC.md`.

Mudança informada: $ARGUMENTS

1. Leia `_data/profile.yml` (e `research.yml` ou `lab.yml`, se a mudança for nessas seções).
2. Aplique a mudança nos dois idiomas. Números e cargos só com o valor que o usuário informou.
3. Se a bio passar de 130 palavras em algum idioma, proponha uma versão mais curta.
4. Rode a verificação da seção 9 do `SITE_SPEC.md`.
5. Mostre o antes e o depois nos dois idiomas e espere "pode publicar".
6. Commit `perfil: <resumo da mudança>` e `git push`. Confira as duas versões publicadas.
