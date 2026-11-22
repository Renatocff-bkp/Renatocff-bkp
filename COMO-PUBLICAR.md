# Como publicar

1. No GitHub, crie um repositório público com **exatamente o mesmo nome do seu usuário** (ex.: `renato/renato`).
2. Edite `generator/config.json`: `username`, links, e preencha os projetos marcados com `"draft": true` (ou apague-os).
3. Rode `python generator/build.py` (Python 3, sem dependências). Ele regenera `README.md` e `assets/`.
4. Faça commit de tudo e push na branch `main`.
5. Em **Actions**, rode "Atividade neural (contribuições)" uma vez: ele cria a branch `output` com o gráfico de contribuições.

Para mudar textos, projetos ou stack depois: edite o config.json e rode o script de novo.
