# Prompts para criar o site no Claude Code

Sequência para criar `ricardolimongi.github.io`, bilíngue, e deixar pronta a rotina de novos conteúdos.

## Antes de começar

1. Garanta que o repositório `ricardolimongi.github.io` existe na sua conta do GitHub. Se ainda não existir, crie no site do GitHub com esse nome exato, público.
2. No Terminal, clone o repositório para uma pasta sua:
   ```
   cd ~/Documents
   git clone https://github.com/ricardolimongi/ricardolimongi.github.io.git
   cd ricardolimongi.github.io
   ```
3. Copie para dentro dessa pasta os arquivos deste pacote: `SITE_SPEC.md`, `CLAUDE.md`, `CONTEUDO_INICIAL.md`, `PROMPTS_SITE.md` e a pasta `.claude/` inteira (ela fica oculta no Finder: use Cmd+Shift+. para ver).
4. Revise e complete o `CONTEUDO_INICIAL.md` (os campos TODO e CONFIRMAR). Coloque na pasta a foto, o arquivo .xlsx da planilha e o PDF do Lattes com o nome `lattes.pdf`.
5. Rode `claude` nessa pasta. Modelo sugerido: Opus nas etapas 2 a 4; Sonnet no resto.

## Etapa 1. Diagnóstico

```
Leia CLAUDE.md, SITE_SPEC.md e CONTEUDO_INICIAL.md por inteiro.
Depois:
1. Liste o que já existe neste repositório. Se já houver um site, me mostre o que tem e NÃO apague nada sem eu aprovar.
2. Verifique se tenho Ruby e Bundler para rodar o Jekyll localmente. Se não tiver, me diga como instalar no Mac (Homebrew) e espere minha aprovação.
3. Confira as configurações de Pages do repositório com o gh CLI, se estiver instalado (branch main, pasta raiz).
4. Me diga em 5 linhas o que entendeu e liste dúvidas sobre a especificação.
```

## Etapa 2. Esqueleto bilíngue (com aprovação)

```
Modo de planejamento: mostre o plano antes.

Crie a estrutura da seção 6 do SITE_SPEC.md:
- _config.yml com jekyll-sitemap e os dados básicos;
- _layouts/home.html e uma include por seção, todas lendo de _data/ e escolhendo o idioma por page.lang;
- index.md (lang: pt) e en/index.md (lang: en);
- _data/i18n.yml com todos os textos fixos da interface nos dois idiomas;
- assets/css/site.css com os tokens da seção 5, modo alto contraste e versão para celular;
- alternador PT | EN que leva à mesma âncora no outro idioma.

Por enquanto, preencha _data/ com dois itens de exemplo marcados como "exemplo" para testarmos o layout.
Rode o site localmente, tire capturas em 390 px e 1280 px nas duas línguas, olhe você mesmo e corrija problemas.
PARE e me mostre as capturas.
```

## Etapa 3. Conteúdo real

```
Substitua os exemplos pelo conteúdo de CONTEUDO_INICIAL.md:
- profile.yml, research.yml, lab.yml e os quatro primeiros itens em items.yml, nos dois idiomas;
- foto em assets/img/ (converta para WebP, até 200 KB) e a planilha em assets/files/;
- campos TODO ficam no YAML, mas não aparecem no site.
Para publicações: converta os artigos em periódicos do lattes.pdf (que está nesta pasta) em _data/publications.yml, mais recentes primeiro. Liste também as palestras de 2025 e 2026 do Lattes para eu escolher de 4 a 6 que entram no site.

Siga o glossário e o tom do CLAUDE.md na tradução.
Rode a verificação da seção 9 do SITE_SPEC.md e me mostre: lista de TODO restantes, capturas nas duas línguas e qualquer texto que você traduziu e eu deveria conferir.
```

## Etapa 4. Publicação

```
Tudo aprovado. Faça commit com a mensagem "site: primeira versão bilíngue" e git push.
Aguarde a publicação do GitHub Pages, abra https://ricardolimongi.github.io/ e /en/, confira as seções, os links e o alternador de idioma, e me diga se está tudo no ar.
```

## Etapa 5. Testar a rotina de novos conteúdos

Este é o teste de que a rotina funciona. Use um conteúdo real, por exemplo o Reel do caderno de laboratório quando for publicado:

```
/novo-conteudo Vídeo: "O caderno de laboratório de quem usa IA", Reel publicado em [data], link [URL]. Mostra uma planilha de 5 colunas para registrar o uso de IA na pesquisa e montar a declaração. A planilha está em assets/files/caderno-uso-ia.xlsx.
```

O Claude Code vai classificar, traduzir, mostrar os dois idiomas e esperar o seu "pode publicar".

## Depois: a rotina do dia a dia

- **Publicou um vídeo, Reel ou material?** `/novo-conteudo` com uma ou duas frases e o link. Pode escrever só em português: a versão em inglês sai junto.
- **Mudou cargo, número ou link?** `/atualizar-perfil` com o que mudou.
- **Uma vez por mês:** `/revisar-site`, que confere idiomas, links quebrados, conteúdos velhos e TODOs.

Uma sugestão de hábito: sempre que publicar no YouTube, rode o `/novo-conteudo` no mesmo dia. Assim o site nunca fica parado.

## Quando quiser um domínio próprio

```
Quero usar o domínio [ricardolimongi.com.br]. Crie o arquivo CNAME, ajuste _config.yml e me diga exatamente quais registros DNS cadastrar no Registro.br.
```
