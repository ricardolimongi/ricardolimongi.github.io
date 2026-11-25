# CLAUDE.md: site ricardolimongi.github.io

Instruções permanentes para o Claude Code neste repositório. Leia também `SITE_SPEC.md`.

## Regras de ouro

1. **Conteúdo mora em `_data/*.yml`, nunca em HTML.** Para adicionar ou mudar qualquer texto, edite o YAML.
2. **Tudo é bilíngue.** Todo campo de texto tem `pt` e `en`. Nunca salve um item com só um idioma. Se o usuário escrever só em português, você traduz para o inglês; se escrever só em inglês, traduz para o português.
3. **Nada inventado.** Números, cargos, datas, links e nomes vêm do usuário. O que faltar vira `TODO` e não é publicado.
4. **Sem travessão (—)** em nenhum dos idiomas.
5. **Publique só com aprovação.** Mostre o que vai mudar (diff do YAML e as frases nos dois idiomas) e espere o "pode publicar" antes do `git push`.
6. **Rode a verificação da seção 9 do `SITE_SPEC.md`** antes de pedir aprovação.

## Tom e tradução

- Português: claro, direto, primeira pessoa quando for a bio ("Pesquiso...").
- Inglês: acadêmico natural, como um pesquisador escreveria, não tradução palavra por palavra. Títulos em inglês seguem Title Case só em nomes próprios; o resto em sentence case.
- Resumos de cartão: até 25 palavras em cada idioma.

## Glossário fixo (pt → en)

| Português | Inglês |
| --- | --- |
| Professor Associado | Associate Professor |
| Universidade Federal de Goiás (UFG) | Federal University of Goiás (UFG) |
| Faculdade de Administração, Ciências Contábeis e Ciências Econômicas (FACE) | School of Business, Accounting and Economics (FACE) |
| Bolsista de Produtividade em Pesquisa do CNPq | CNPq Research Productivity Fellow |
| Bolsista de Produtividade em Desenvolvimento Tecnológico e Extensão Inovadora do CNPq | CNPq Technological Development and Innovative Extension Fellow |
| editor-chefe | Editor-in-Chief |
| Brazilian Administration Review (BAR) | Brazilian Administration Review (BAR) |
| Programa de Pós-Graduação em Administração (PPGADM) | Graduate Program in Business Administration (PPGADM) |
| inteligência híbrida | hybrid intelligence |
| IA generativa | generative AI |
| amostras sintéticas | silicon samples / synthetic samples |
| integridade científica | research integrity |
| declaração de uso de IA | AI-use statement |
| Portaria CNPq nº 3.004/2026 | CNPq Ordinance No. 3,004/2026 |
| palestra | talk |
| materiais | resources |
| eventos | events |

Se aparecer um termo novo que se repetirá, adicione-o a esta tabela e avise o usuário.

## Comandos disponíveis

- `/novo-conteudo` adiciona um material, vídeo, palestra ou notícia nos dois idiomas.
- `/novo-evento` adiciona ou corrige um evento da agenda nos dois idiomas.
- `/atualizar-perfil` muda bio, números, cargos ou links.
- `/revisar-site` roda a verificação completa e lista problemas.
