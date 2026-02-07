# 📁 Estrutura do Projeto GitHub Pages

Esta é a estrutura correta para um site Jekyll no GitHub Pages.

## Estrutura de Arquivos

```
Sapieando/
├── _config.yml                 # Configuração do Jekyll (OBRIGATÓRIO)
├── _layouts/                   # Templates HTML
│   ├── default.html            # Layout base
│   ├── post.html               # Layout de post individual
│   └── index.html              # Layout da listagem de posts
├── _includes/                  # Componentes reutilizáveis
│   ├── header.html             # Cabeçalho do site
│   ├── footer.html             # Rodapé do site
│   └── post-meta.html          # Metadados dos posts
├── _posts/                     # Posts do blog (OBRIGATÓRIO)
│   └── YYYY-MM-DD-titulo.md    # Formato obrigatório
├── assets/                     # Arquivos estáticos
│   ├── css/
│   │   └── main.scss           # Estilos (compilado automaticamente)
│   └── fonts/                  # Fontes personalizadas
│       └── *.otf               # Arquivos de fonte
├── index.html                  # Página inicial (OBRIGATÓRIO)
├── Gemfile                     # Dependências Ruby/Jekyll
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Documentação (opcional)
```

## Arquivos na Raiz

### Obrigatórios
- **`_config.yml`** - Configuração do Jekyll
- **`index.html`** - Página inicial do site
- **`_posts/`** - Pasta com os posts (pode estar vazia inicialmente)

### Recomendados
- **`Gemfile`** - Define plugins e versões do Jekyll
- **`.gitignore`** - Evita commit de arquivos desnecessários
- **`README.md`** - Documentação do projeto

### Opcionais (Documentação)
- `DEPLOY_GITHUB_PAGES.md` - Guia de deploy
- `DEPLOYMENT_GUIDE.md` - Guia alternativo
- `FREE_HOSTING_ALTERNATIVES.md` - Alternativas de hospedagem

## Pastas Especiais do Jekyll

### `_layouts/`
Contém os templates HTML que definem a estrutura das páginas.
- `default.html` - Layout base usado por todos
- `post.html` - Layout específico para posts
- `index.html` - Layout para a página inicial

### `_includes/`
Componentes HTML reutilizáveis incluídos nos layouts.
- Usados com `{% include nome.html %}`

### `_posts/`
Posts do blog em formato Markdown.
- **Formato obrigatório**: `YYYY-MM-DD-titulo-do-post.md`
- Exemplo: `2026-02-07-bem-vindo.md`

### `assets/`
Arquivos estáticos (CSS, JS, imagens, fontes).
- `assets/css/` - Estilos SCSS (compilados automaticamente)
- `assets/fonts/` - Fontes personalizadas
- `assets/images/` - Imagens (criar se necessário)

## Arquivos Excluídos do Build

Estes arquivos estão em `_config.yml` → `exclude`:
- `Gemfile`, `Gemfile.lock` - Não são processados pelo Jekyll
- `README.md` - Documentação, não é página
- Arquivos `.md` de documentação
- Pasta `site-export/` - Arquivos do WordPress antigo

## Como GitHub Pages Processa

1. **Detecta Jekyll** automaticamente pela presença de `_config.yml`
2. **Processa arquivos**:
   - Compila `*.scss` → `*.css`
   - Processa `*.md` com front matter
   - Aplica layouts e includes
3. **Gera site estático** na pasta `_site/` (não commitada)
4. **Publica** em `https://usuario.github.io`

## Boas Práticas

✅ **Faça:**
- Mantenha estrutura organizada
- Use nomes descritivos para arquivos
- Commit apenas arquivos necessários
- Mantenha `.gitignore` atualizado

❌ **Evite:**
- Arquivos grandes desnecessários
- Pastas de build (`_site/`, `.sass-cache/`)
- Arquivos de sistema (`.DS_Store`)
- Dados sensíveis (senhas, tokens)

## Verificação Rápida

Antes de fazer commit, verifique:

```bash
# Estrutura mínima necessária
✅ _config.yml existe
✅ index.html existe
✅ _posts/ existe (mesmo que vazia)
✅ assets/css/main.scss existe
```

## Próximos Passos

1. ✅ Estrutura organizada
2. 📝 Adicionar mais posts em `_posts/`
3. 🎨 Personalizar layouts em `_layouts/`
4. 🚀 Fazer deploy no GitHub Pages
