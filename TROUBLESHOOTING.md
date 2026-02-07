# 🔧 Solução de Problemas - GitHub Pages

## Erro: "Multiple artifacts named 'github-pages'"

Este erro ocorre quando há múltiplos builds tentando criar o mesmo artefato simultaneamente.

### Solução 1: Usar Build Automático do GitHub Pages (Recomendado)

Para sites Jekyll, o GitHub Pages faz o build automaticamente. **NÃO é necessário** criar workflows customizados.

**Passos:**

1. **Remover workflows customizados** (se existirem):
   - Vá em **Settings → Pages**
   - Em **Build and deployment**, certifique-se de que está:
     - **Source**: "Deploy from a branch"
     - **Branch**: `main` (ou `master`)
     - **Folder**: `/ (root)`
   - **NÃO** use "GitHub Actions" como source

2. **Cancelar builds em execução**:
   - Vá em **Actions** no seu repositório
   - Cancele qualquer workflow em execução
   - Delete workflows duplicados se houver

3. **Limpar cache**:
   - Vá em **Settings → Pages**
   - Role até o final
   - Clique em **"Clear cache"** (se disponível)

4. **Fazer novo commit**:
   ```bash
   git commit --allow-empty -m "Trigger rebuild"
   git push
   ```

### Solução 2: Usar GitHub Actions (Se necessário)

Se você realmente precisa de um workflow customizado, use este:

**Crie `.github/workflows/pages.yml`:**

```yaml
name: Deploy GitHub Pages

on:
  push:
    branches:
      - main  # ou 'master' se for o branch padrão

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
          working-directory: ./
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Build with Jekyll
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./_site

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

**IMPORTANTE:** Se usar este workflow:
1. Vá em **Settings → Pages**
2. Mude **Source** para **"GitHub Actions"**
3. Delete qualquer outro workflow que faça deploy

### Solução 3: Verificar Configurações do Repositório

1. **Verificar branch padrão**:
   - Vá em **Settings → General**
   - Confirme qual é o branch padrão (`main` ou `master`)
   - Use o mesmo branch nas configurações do Pages

2. **Verificar permissões**:
   - Vá em **Settings → Actions → General**
   - Em **Workflow permissions**, certifique-se de que está:
     - ✅ "Read and write permissions"
     - ✅ "Allow GitHub Actions to create and approve pull requests"

3. **Verificar Actions habilitadas**:
   - Vá em **Settings → Actions → General**
   - Certifique-se de que **"Allow all actions and reusable workflows"** está selecionado

### Solução 4: Limpar e Recomeçar

Se nada funcionar:

1. **Desabilitar GitHub Pages temporariamente**:
   - Vá em **Settings → Pages**
   - Mude **Source** para **"None"**
   - Salve

2. **Aguardar 5 minutos**

3. **Reabilitar**:
   - Mude de volta para **"Deploy from a branch"**
   - Branch: `main`
   - Folder: `/ (root)`
   - Salve

4. **Fazer novo commit**:
   ```bash
   git commit --allow-empty -m "Rebuild pages"
   git push
   ```

## Erros Comuns e Soluções

### Erro: "Build failed"

**Causa**: Erro no código Jekyll ou configuração

**Solução**:
- Verifique os logs em **Actions**
- Procure por erros de sintaxe no `_config.yml`
- Verifique se todos os arquivos necessários estão presentes

### Erro: "404 Not Found"

**Causa**: Site ainda não foi publicado ou URL incorreta

**Solução**:
- Aguarde 5-10 minutos após ativar Pages
- Verifique a URL correta em **Settings → Pages**
- Confirme que o repositório é **Public**

### Erro: "Styles not loading"

**Causa**: Caminho incorreto para CSS

**Solução**:
- Verifique em `_layouts/default.html` se o caminho está correto:
  ```html
  <link rel="stylesheet" href="{{ '/assets/css/main.css' | relative_url }}">
  ```
- Certifique-se de que `assets/css/main.scss` existe
- O GitHub Pages compila SCSS automaticamente

### Erro: "Posts not appearing"

**Causa**: Formato incorreto do nome do arquivo ou front matter

**Solução**:
- Nome do arquivo: `YYYY-MM-DD-titulo.md`
- Front matter obrigatório:
  ```yaml
  ---
  title: "Título"
  date: 2026-02-07
  ---
  ```

## Verificação Rápida

Antes de pedir ajuda, verifique:

- [ ] Repositório é **Public**
- [ ] Branch padrão está correto (`main` ou `master`)
- [ ] `_config.yml` tem sintaxe válida
- [ ] `index.html` existe na raiz
- [ ] `_posts/` contém arquivos `.md` válidos
- [ ] Não há workflows duplicados em `.github/workflows/`
- [ ] GitHub Pages está configurado corretamente em Settings

## Ainda com Problemas?

1. Verifique os logs completos em **Actions → [workflow name]**
2. Procure por mensagens de erro específicas
3. Verifique o status do GitHub: [status.github.com](https://www.githubstatus.com/)
4. Tente fazer um commit vazio para forçar rebuild:
   ```bash
   git commit --allow-empty -m "Force rebuild"
   git push
   ```
