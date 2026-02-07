# ⚠️ IMPORTANTE: Leia Antes de Usar

## Quando Usar Este Workflow

Este workflow (`pages.yml`) é **OPCIONAL** e deve ser usado **APENAS** se:

1. Você mudou **Settings → Pages → Source** para **"GitHub Actions"**
2. Você precisa de controle total sobre o processo de build
3. Você está tendo problemas com o build automático

## Quando NÃO Usar Este Workflow

Para a maioria dos sites Jekyll, **NÃO é necessário** este workflow porque:

- ✅ GitHub Pages faz build automático do Jekyll
- ✅ Mais simples e rápido
- ✅ Menos propenso a erros

## Como Usar

### Opção 1: Build Automático (Recomendado)

1. **DELETE este arquivo** `.github/workflows/pages.yml`
2. Vá em **Settings → Pages**
3. Configure:
   - Source: **"Deploy from a branch"**
   - Branch: `main` (ou `master`)
   - Folder: `/ (root)`
4. Salve e aguarde

### Opção 2: Usar GitHub Actions

1. **MANTENHA** este arquivo `.github/workflows/pages.yml`
2. Vá em **Settings → Pages**
3. Configure:
   - Source: **"GitHub Actions"**
4. Salve e aguarde

## ⚠️ Erro "Multiple artifacts"?

Se você receber erro de múltiplos artefatos:

1. **DELETE** este workflow (`.github/workflows/pages.yml`)
2. Use **Opção 1** acima (build automático)
3. Isso resolve 99% dos problemas

## Verificação

Para verificar qual método está sendo usado:

- Vá em **Settings → Pages**
- Veja o que está em **"Build and deployment" → Source**
- Se for "Deploy from a branch" → build automático
- Se for "GitHub Actions" → usa este workflow
