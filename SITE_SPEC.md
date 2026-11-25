# SITE_SPEC: ricardolimongi.github.io

Especificação do site pessoal de Ricardo Limongi. Fonte da verdade para o Claude Code: se um prompt contradisser este arquivo, pergunte antes de agir.

## 1. Objetivo

- Ser o destino do link da bio (Instagram), da descrição do YouTube, do LinkedIn e das assinaturas de e-mail.
- Reunir em um só lugar: quem é Ricardo, linhas de pesquisa, HI-Lab, materiais para baixar, vídeos, palestras e publicações.
- Ser bilíngue desde o início: português (padrão) e inglês.
- Ser atualizado em minutos, por prompt, sem editar HTML à mão.

## 2. Tecnologia

- **Jekyll nativo do GitHub Pages**, sem GitHub Actions para publicar. Push na branch `main` publica.
- Nenhuma dependência de JavaScript para mostrar conteúdo. Todo texto sai no HTML (bom para o Google e para leitores de tela). JavaScript só para o alternador de contraste, o menu (celular e seção atual) a âncora do alternador de idioma, mover eventos passados para o histórico e tocar vídeos, copiar modelos e contar acessos e cliques (GoatCounter, sem cookies; código em `_config.yml`). Sem JavaScript, todo o conteúdo continua acessível.
- Endereço: `https://ricardolimongi.github.io/` (sem domínio próprio por enquanto; a estrutura deve permitir adicionar um `CNAME` depois sem mudar nada).

## 3. Bilíngue: como funciona

- Português em `/` e inglês em `/en/`. As duas páginas são geradas pelo mesmo layout, com `lang: pt` ou `lang: en` na página.
- **Todo o conteúdo mora em arquivos de dados em `_data/`, nunca em HTML.** Cada item tem os campos de texto nos dois idiomas:

```yaml
- id: guia-portaria-3004
  date: 2026-11-24
  type: material            # material | video | palestra | noticia
  title:
    pt: "Portaria CNPq 3.004/2026: guia prático e modelo de declaração"
    en: "CNPq Ordinance 3,004/2026: practical guide and AI-use statement template"
  summary:
    pt: "..."
    en: "..."
  links:
    - label: { pt: "Baixar planilha (.xlsx)", en: "Download spreadsheet (.xlsx)" }
      url: /assets/files/caderno-uso-ia.xlsx
  content_language: pt      # idioma do material em si (pt, en ou both)
```

- Textos fixos da interface (menu, botões, rótulos) ficam em `_data/i18n.yml`, com chaves `pt` e `en`.
- Quando um material só existe em português, a versão em inglês mostra o título e o resumo traduzidos e a etiqueta "In Portuguese".
- O alternador PT | EN no topo leva à mesma seção no outro idioma (âncoras iguais nos dois).
- Tags `hreflang` e `<html lang>` corretas nas duas versões.

## 4. Estrutura da página (página única com âncoras, mais páginas de material)

Ordem e conteúdo. Uma seção só aparece se tiver itens no arquivo de dados correspondente (nada de seção vazia).

| Âncora | PT | EN | Fonte de dados |
| --- | --- | --- | --- |
| `#inicio` | Início | Home | `profile.yml` |
| `#sobre` | Sobre | About | `profile.yml` (bio e números) |
| `#pesquisa` | Temas de pesquisa | Research topics | `research.yml` |
| `#hilab` | HI-Lab | HI-Lab | `lab.yml` |
| `#eventos` | Eventos | Events | `events.yml` (agenda e histórico) |
| `#materiais` | Materiais | Resources | `items.yml` (type: material) |
| `#videos` | Vídeos | Videos | `items.yml` (type: video) |
| `#palestras` | Palestras | Talks | `items.yml` (type: palestra) |
| `#publicacoes` | Publicações | Publications | `publications.yml` |
| `#contato` | Contato | Contact | `profile.yml` (links) |

- **Início:** foto, nome, cargo, frase de posicionamento, três botões (Materiais, Vídeos, Contato).
- **Sobre:** bio curta (até 130 palavras), uma fileira de três números, cargos editoriais e institucionais, até cinco destaques (prêmios) com ano, uma linha de experiência internacional e link para o Lattes.
- **Pesquisa:** 3 a 4 linhas, cada uma com título e 2 a 3 frases.
- **HI-Lab:** descrição curta e link para hilab.face.ufg.br. Membros são opcionais (o site institucional é o lugar deles).
- **Eventos:** agenda com nome, data, horário, local e link (se houver). Próximos primeiro; os passados vão para "Anteriores" (`<details>`), na geração do site e também no navegador, por data.
- **Materiais, Vídeos, Palestras:** cartões com miniatura, data, título, resumo e links. Mostrar os 6 mais recentes e um botão "ver todos" que expande (sem JavaScript: elemento `<details>`).
- **Lista completa:** `/publicacoes/` e `/en/publications/` reúnem artigos (`publications.yml`) e demais produções (`productions.yml`), por tipo, no formato de "Mais recentes".
- **Páginas de material:** conteúdos longos ganham página própria em `/materiais/<slug>/` e `/en/resources/<slug>/`, com layout `material` e conteúdo em `_data/paginas/<nome>.yml` (blocos md, video, modelo e arquivo, sempre pt e en). O cartão em Materiais aponta para ela.
- **Vídeos:** tocam no próprio cartão após o clique (campo `youtube`); playlists usam `playlist: true`.
- **Publicações:** lista em texto, mais recentes primeiro, gerada de `publications.yml`. Cada artigo liga ao DOI e mostra citações (Google Scholar, com data) e a classificação do periódico (`journals.yml`: Nova Classificação CAPES 2025-2028 via Periódicos-ADM só na versão em português, SJR do SCImago e ABS via Periódicos-ADM, com nota de fonte e data). DOI: `_tools/publicacoes.py`. Citações: `_tools/scholar.py`. Depois das 5 mais recentes, "Mais citadas" traz 5 produções de qualquer tipo (`most_cited.yml`, Google Scholar, com data). Mostrar as 5 mais recentes e link para Google Scholar, ORCID e Lattes.
- **Contato:** canal do YouTube em destaque e links: Lattes, ORCID, Google Scholar, YouTube, Instagram, LinkedIn, Substack.

## 5. Identidade visual

Direção: imersiva, escura, uma cena de fundo por seção, com a foto em destaque na abertura.

| Token | Valor | Uso |
| --- | --- | --- |
| noite | #0A0F1E | fundo geral (derivado da tinta #14213D) |
| tinta | #14213D | texto sobre amarelo |
| papel | #F7F4EE | texto principal sobre o escuro |
| amarelo | #F5C400 | destaques, botão principal, sublinhado de links (mesmo amarelo das capas dos Reels) |
| névoa | #B9C0CF | datas e textos secundários |

- Cenas: `assets/img/cena-<seção>.webp`, arte original gerada por `_tools/arte.py` (fluxo humano em amarelo, malha da máquina em azul, e uma cor por seção). Até 200 KB cada, com `loading="lazy"`.
- Fontes: `Source Serif 4` (nome, títulos e números) e `Inter` (texto), via Google Fonts com `display=swap`.
- Menu lateral fixo no desktop, com a seção atual marcada; menu recolhido no celular.
- Cartões com cantos de 14 px só em materiais, vídeos e palestras. Nas demais seções, texto direto sobre a cena. Gradientes só para garantir a leitura.
- Modo alto contraste (preto e branco puros, sublinhados, sem cenas) com alternador no topo; preferência salva em `localStorage` dentro de `try/catch`.
- Responsivo, pensado primeiro para celular (a maior parte do tráfego virá do Instagram).
- Acessibilidade: contraste AA no modo normal, `alt` em todas as imagens de conteúdo (cenas são decorativas), foco visível, navegação por teclado.

## 6. Estrutura de arquivos

```
_config.yml
_data/
  i18n.yml          # textos fixos da interface
  profile.yml       # nome, cargo, bio, números, links (pt/en)
  research.yml      # linhas de pesquisa (pt/en)
  lab.yml           # HI-Lab (pt/en)
  items.yml         # materiais, vídeos, palestras, notícias (pt/en)
  events.yml        # agenda e histórico (pt/en)
  journals.yml      # classificação dos periódicos (CAPES, SJR, ABS)
  productions.yml   # livros, capítulos, congressos e demais produções
  most_cited.yml    # produções mais citadas, todos os tipos
  paginas/          # páginas de material (pt/en)
  publications.yml  # publicações (título no idioma original)
_includes/          # uma include por seção + head, header, footer, card
_layouts/home.html
assets/css/site.css
assets/img/         # foto, miniaturas (WebP, máx. 200 KB cada)
assets/files/       # materiais para baixar
index.md            # lang: pt
en/index.md         # lang: en
CLAUDE.md
.claude/commands/
```

## 7. SEO e compartilhamento

- `<title>` e `<meta description>` por idioma, Open Graph e Twitter Card com a foto.
- `sitemap.xml` (plugin `jekyll-sitemap`, aceito no GitHub Pages) e `robots.txt`.
- Dados estruturados `schema.org/Person` com `sameAs` para Lattes, ORCID, Scholar, YouTube, Instagram e LinkedIn.

## 8. Regras de conteúdo

- Nada inventado: números, cargos, datas e links vêm do usuário ou de fontes que ele indicar. O que faltar fica como `TODO` no YAML e não aparece no site até ser preenchido.
- Textos sem travessão (—). Usar vírgula, dois-pontos ou frases curtas.
- Inglês acadêmico natural, não tradução literal. Termos fixos no glossário de `CLAUDE.md`.
- Materiais sobre normas (como a Portaria CNPq 3.004) levam data, link para a fonte oficial e o aviso de que não substituem orientação oficial.

## 9. Verificação antes de cada publicação

1. `bundle exec jekyll build` sem erros (ou, se Ruby não estiver instalado, conferir com a prévia do GitHub Pages após push em branch de teste).
2. As duas versões (`/` e `/en/`) têm as mesmas seções e os mesmos itens.
3. Nenhum `TODO` visível no HTML gerado.
4. Todos os links internos funcionam; arquivos em `assets/files/` existem.
5. Captura de tela da página em largura de celular (390 px) e desktop (1280 px), conferida antes de avisar o usuário.
