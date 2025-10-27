Projeto-Adrine — site estático para cálculos de engenharia

Como publicar no Netlify

1. Faça commit das alterações e envie ao GitHub.
2. Acesse https://app.netlify.com -> New site -> Import from Git.
3. Conecte seu repositório GitHub e selecione o branch `main`.
4. Em "Build settings":
   - Build command: (deixe vazio)
   - Publish directory: Projeto-Adrine
5. Clique em Deploy site.

Observações:
- O arquivo `netlify.toml` no root já aponta `publish = "Projeto-Adrine"`.
- O arquivo `_redirects` garante que rotas do SPA sirvam `index.html`.
