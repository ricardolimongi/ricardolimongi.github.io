---
description: Adiciona, corrige ou cancela um evento da agenda, nos dois idiomas
argument-hint: nome, data, horário, local e link (se houver); pode colar o convite
---

Atualize a agenda seguindo `CLAUDE.md` e `SITE_SPEC.md`.

Evento informado pelo usuário: $ARGUMENTS

1. Extraia nome, data, data final (se durar mais de um dia), horário, fuso (se não for Brasília), local e link. Pode haver vários eventos de uma vez.
2. Pergunte só se faltar nome ou data. Horário, local e link são opcionais: se faltarem, omita o campo. Não invente nada.
3. Não publique link privado de reunião (Zoom, Meet, Teams) nem endereço residencial sem confirmar com o usuário.
4. Confira em `_data/events.yml` se o evento já existe. Se existir, atualize em vez de duplicar.
5. Escreva o item com `id` único, `name.pt`, `name.en`, `date`, `end_date`, `time.pt` e `time.en` ("19h" / "7 pm"), `timezone`, `place.pt`, `place.en` e `url`. Traduza pelo glossário; nomes oficiais de eventos ficam como são nos dois idiomas.
6. Nunca apague eventos passados: eles formam o histórico e mudam de lista sozinhos.
7. Rode a verificação da seção 9 do `SITE_SPEC.md`, mostre os dois idiomas e espere "pode publicar".
8. Commit `evento: <nome em português>` e `git push`. Confira `/#eventos` e `/en/#eventos`.
