---
description: Adiciona um material, vídeo, palestra ou notícia ao site, nos dois idiomas
argument-hint: descreva o conteúdo em português ou inglês, com links e arquivos
---

Adicione um novo item ao site seguindo `CLAUDE.md` e `SITE_SPEC.md`.

Conteúdo informado pelo usuário: $ARGUMENTS

Passos:

1. **Classifique** o item como `material`, `video`, `palestra` ou `noticia`. Se não estiver claro, pergunte.
2. **Reúna o que falta.** Confira se tem: título, data, resumo, links (YouTube, arquivo, página externa) e miniatura. Pergunte só o que faltar e for necessário. Se for um vídeo do YouTube, use o ID do vídeo para gerar a miniatura (`https://i.ytimg.com/vi/<ID>/hqdefault.jpg`) e o link.
3. **Arquivos.** Se o usuário indicou um arquivo para baixar, copie para `assets/files/` com nome em minúsculas, sem acentos e com hífens. Converta miniaturas para WebP com no máximo 200 KB em `assets/img/`.
4. **Escreva o item em `_data/items.yml`**, no topo da lista, com `id` único (slug do título em português), `date`, `type`, `title.pt`, `title.en`, `summary.pt`, `summary.en`, `links` com rótulos nos dois idiomas e `content_language`.
5. **Traduza** seguindo o tom e o glossário do `CLAUDE.md`. Resumo de até 25 palavras em cada idioma.
6. **Verifique** com a seção 9 do `SITE_SPEC.md`.
7. **Mostre ao usuário**, nesta ordem:
   - o título e o resumo nos dois idiomas, lado a lado;
   - os links e arquivos adicionados;
   - termos novos que você adicionou ao glossário, se houver.
8. **Espere aprovação.** Ajuste o que ele pedir. Com "pode publicar", faça commit com a mensagem `conteúdo: <título em português>` e `git push`.
9. **Depois do push**, aguarde a publicação do GitHub Pages, abra `https://ricardolimongi.github.io/#<secao>` e `/en/#<secao>` e confirme que o item aparece nas duas versões.
