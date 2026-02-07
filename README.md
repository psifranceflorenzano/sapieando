# Sapieando - Blog Jekyll

Blog sobre psicanálise construído com Jekyll e hospedado no GitHub Pages.

## 🚀 Configuração do GitHub Pages

### Passo 1: Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome do repositório:
   - Para site pessoal: `seu-usuario.github.io`
   - Para projeto: qualquer nome (ex: `sapieando`)
4. Marque como **Public** (necessário para GitHub Pages gratuito)
5. Clique em "Create repository"

### Passo 2: Fazer Upload dos Arquivos

**Opção A: Via GitHub Web Interface**

1. No repositório criado, clique em "uploading an existing file"
2. Arraste todos os arquivos desta pasta para o GitHub
3. Clique em "Commit changes"

**Opção B: Via Git (Recomendado)**

```bash
# Navegue até a pasta do projeto
cd /caminho/para/Sapieando

# Inicialize o repositório Git
git init

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "Initial commit: Jekyll blog setup"

# Adicione o repositório remoto (substitua USERNAME e REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Envie para o GitHub
git branch -M main
git push -u origin main
```

### Passo 3: Ativar GitHub Pages

1. No repositório GitHub, vá em **Settings**
2. No menu lateral, clique em **Pages**
3. Em **Source**, selecione:
   - **Deploy from a branch**
   - Branch: `main`
   - Folder: `/ (root)`
4. Clique em **Save**
5. Aguarde alguns minutos para o build
6. Seu site estará disponível em:
   - `https://seu-usuario.github.io` (se o repositório for `seu-usuario.github.io`)
   - `https://seu-usuario.github.io/nome-do-repo` (para outros nomes)

## 📝 Escrevendo Posts

Os posts ficam na pasta `_posts/` e devem seguir o formato:

```
YYYY-MM-DD-titulo-do-post.md
```

Exemplo: `2026-02-07-meu-primeiro-post.md`

### Estrutura de um Post

```markdown
---
title: "Título do Post"
date: 2026-02-07
author: "France Florenzano"
categories: ["Psicanálise", "Categoria"]
excerpt: "Resumo curto do post que aparece na listagem"
---

Conteúdo do post em Markdown aqui...
```

### Markdown

Você pode usar toda a sintaxe Markdown:

- **Negrito** e *itálico*
- Listas ordenadas e não ordenadas
- Links: `[texto](url)`
- Imagens: `![alt](caminho/para/imagem.jpg)`
- Código: `` `código` `` ou blocos de código
- Citações: `> texto citado`

## 🎨 Personalização

### Cores

As cores do tema estão definidas em `assets/css/main.scss`:

- **Texto principal**: `#873D35`
- **Fundo**: `#E3CAB1`
- **Botões**: `#873D35` com texto `#E3CAB1`

Para alterar, edite as variáveis no início do arquivo SCSS.

### Configuração do Site

Edite `_config.yml` para alterar:
- Título do site
- Descrição
- Autor
- URL do site
- Configurações de Markdown

## 💬 Configurar Giscus (Comentários)

1. Acesse [giscus.app](https://giscus.app)
2. Conecte seu repositório GitHub
3. Configure:
   - **Repository**: Seu repositório do blog
   - **Category**: Discussions ou Announcements
   - **Language**: pt-BR
   - **Theme**: Light
4. Copie o código gerado
5. Edite `_layouts/post.html` e substitua o script do Giscus com suas configurações

**Importante**: Você precisa habilitar Discussions no seu repositório GitHub:
- Vá em **Settings** → **General**
- Role até **Features**
- Marque **Discussions**

## 🛠️ Desenvolvimento Local

Para testar o site localmente antes de publicar:

### Instalar Jekyll

```bash
# Instalar Ruby (se ainda não tiver)
# macOS (com Homebrew):
brew install ruby

# Instalar Bundler
gem install bundler
```

### Criar Gemfile

Crie um arquivo `Gemfile` na raiz do projeto:

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-feed", "~> 0.12"
gem "jekyll-seo-tag", "~> 2.8"
gem "jekyll-sitemap", "~> 1.4"
```

### Instalar e Executar

```bash
# Instalar dependências
bundle install

# Executar servidor local
bundle exec jekyll serve

# Acesse http://localhost:4000
```

## 📁 Estrutura do Projeto

```
Sapieando/
├── _config.yml          # Configuração do Jekyll
├── _layouts/            # Templates HTML
│   ├── default.html     # Layout base
│   ├── post.html        # Layout de post
│   └── index.html       # Layout da listagem
├── _includes/           # Componentes reutilizáveis
│   ├── header.html      # Cabeçalho
│   ├── footer.html      # Rodapé
│   └── post-meta.html   # Metadados do post
├── _posts/              # Posts do blog
│   └── YYYY-MM-DD-*.md
├── assets/
│   ├── css/
│   │   └── main.scss    # Estilos (compilado para main.css)
│   └── fonts/           # Fontes Albura
├── index.html           # Página inicial
└── README.md           # Este arquivo
```

## 🔧 Solução de Problemas

### Site não aparece após deploy

- Aguarde 5-10 minutos para o GitHub processar
- Verifique se o repositório é público
- Confirme que o branch está correto nas configurações do Pages
- Verifique se há erros em **Settings** → **Pages** → **Build log**

### Estilos não carregam

- Verifique se o caminho em `_layouts/default.html` está correto: `/assets/css/main.css`
- Certifique-se de que o arquivo SCSS está sendo compilado (GitHub Pages compila automaticamente)

### Posts não aparecem

- Verifique o formato do nome do arquivo: `YYYY-MM-DD-titulo.md`
- Confirme que há front matter (---) no início do arquivo
- Verifique se a data não é futura

## 📚 Recursos Úteis

- [Documentação do Jekyll](https://jekyllrb.com/docs/)
- [GitHub Pages Docs](https://docs.github.com/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [Giscus Documentation](https://giscus.app/)

## 📄 Licença

Este projeto usa a licença GPL v2 ou posterior, mantendo a licença do tema Bibliophile original.

---

**Desenvolvido com ❤️ usando Jekyll e GitHub Pages**
