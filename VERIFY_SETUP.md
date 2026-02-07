# ✅ Verificação de Configuração

Use este checklist para verificar se tudo está configurado corretamente:

## Arquivos Essenciais

- [x] `_config.yml` - Configuração do Jekyll
- [x] `index.html` - Página inicial
- [x] `_posts/` - Pasta com posts
- [x] `_layouts/` - Templates HTML
- [x] `_includes/` - Componentes
- [x] `assets/css/main.scss` - Estilos
- [x] `Gemfile` - Dependências

## Configuração do GitHub Pages

### Método Recomendado: Build Automático

1. Vá em **Settings → Pages**
2. Verifique:
   - [ ] Source: **"Deploy from a branch"**
   - [ ] Branch: `main` (ou `master`)
   - [ ] Folder: `/ (root)`
   - [ ] **NÃO** está em "GitHub Actions"

### Se Usar GitHub Actions

1. Vá em **Settings → Pages**
2. Verifique:
   - [ ] Source: **"GitHub Actions"**
   - [ ] Arquivo `.github/workflows/pages.yml` existe
   - [ ] Workflow está correto

## Problemas Comuns

### Erro: "Multiple artifacts"

**Solução**: Use build automático (não GitHub Actions)

1. Delete `.github/workflows/pages.yml` (se existir)
2. Settings → Pages → Source: "Deploy from a branch"
3. Salve

### Build Falha

**Verifique**:
- [ ] `_config.yml` tem sintaxe válida (sem erros de YAML)
- [ ] Todos os arquivos necessários estão presentes
- [ ] Branch padrão está correto

### Site Não Aparece

**Verifique**:
- [ ] Repositório é **Public**
- [ ] Aguardou 5-10 minutos após ativar Pages
- [ ] URL está correta

## Teste Local (Opcional)

Para testar localmente antes de fazer deploy:

```bash
# Instalar dependências
bundle install

# Executar servidor local
bundle exec jekyll serve

# Acessar http://localhost:4000
```

## Próximos Passos

1. ✅ Verificar configuração acima
2. 📝 Fazer commit e push
3. ⏳ Aguardar build (2-5 minutos)
4. 🌐 Verificar site funcionando

## Ainda com Problemas?

Consulte:
- `FIX_DEPLOY_ERROR.md` - Solução rápida
- `TROUBLESHOOTING.md` - Guia completo
- `DEPLOY_GITHUB_PAGES.md` - Instruções de deploy
