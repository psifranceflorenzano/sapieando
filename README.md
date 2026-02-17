# Sapieando - Blog Jekyll

Blog sobre psicanálise construído com Jekyll e hospedado no GitHub Pages.

## 📖 Visão Geral

Este projeto consiste em dois componentes principais:

1. **Blog Jekyll**: Site estático gerado pelo Jekyll e hospedado no GitHub Pages, com integração de comentários via Giscus
2. **Flask GUI Manager**: Aplicação web Python que permite gerenciar posts do blog através de uma interface amigável, sem necessidade de conhecimento de Git ou linha de comando

O sistema automatiza todo o fluxo de publicação: criar/editar posts → gerar site Jekyll → commit Git → push para GitHub → deploy automático no GitHub Pages.

## 🚀 Instalação e Configuração

### Requisitos

- **Python 3.8+** (para o Flask GUI Manager)
- **Ruby 2.7+** e **Bundler** (para Jekyll)
- **Git** (para controle de versão)
- Conta no **GitHub** (para hospedagem)

### Instalação Rápida

1. **Clone ou baixe este repositório**

```bash
git clone https://github.com/seu-usuario/sapieando.git
cd sapieando
```

2. **Instale as dependências Python**

```bash
# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

3. **Instale as dependências Jekyll**

```bash
# Instale o Bundler (se ainda não tiver)
gem install bundler

# Instale as dependências do Jekyll
bundle install
```

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

## 🖥️ Usando o Flask GUI Manager

O Flask GUI Manager é uma aplicação web que permite gerenciar posts sem usar linha de comando.

### Iniciar o Gerenciador

**Opção 1: Usando o Launcher (Recomendado para Usuários Não-Técnicos)**

Para usuários que não têm familiaridade com terminal/linha de comando, basta clicar duas vezes no arquivo apropriado:

- **Windows**: Clique duas vezes em `start-blog-manager.bat`
- **macOS/Linux**: Clique duas vezes em `start-blog-manager.sh`

O launcher irá:
1. Verificar se o ambiente virtual Python existe
2. Ativar o ambiente virtual automaticamente
3. Iniciar o Blog Manager
4. Abrir automaticamente no seu navegador padrão em `http://127.0.0.1:7856`

**Opção 2: Via Terminal (Para Usuários Avançados)**

```bash
# Ative o ambiente virtual (se ainda não estiver ativo)
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Execute o gerenciador
python blog_manager.py
```

O servidor iniciará em `http://127.0.0.1:7856`

### Funcionalidades

**Página Principal**
- Lista todos os posts existentes em uma tabela
- Mostra título, data, autor e categorias de cada post
- Botões para editar ou deletar cada post
- Botão "Novo Post" para criar novos posts
- Botão "Fechar Programa" para encerrar o servidor

**Criar Novo Post**
1. Clique em "Novo Post"
2. Preencha todos os campos:
   - **Título**: Título do post
   - **Autor**: Nome do autor (pré-preenchido com valor padrão)
   - **Categorias**: Lista separada por vírgulas (ex: "Psicanálise, Reflexões")
   - **Resumo**: Breve descrição que aparece na listagem
   - **Data**: Data de publicação (pré-preenchida com hoje)
   - **Conteúdo**: Texto do post em Markdown
3. Clique em "Salvar"

O sistema automaticamente:
- Cria o arquivo do post com nome no formato `YYYY-MM-DD-titulo.md`
- Gera o site Jekyll localmente (se Jekyll estiver instalado)
- Faz commit das mudanças no Git
- Envia (push) para o GitHub
- GitHub Pages reconstrói e publica o site automaticamente

**Editar Post Existente**
1. Na página principal, clique em "Editar" no post desejado
2. Modifique os campos necessários
3. Clique em "Salvar"

Se você alterar a data, o sistema:
- Deleta o arquivo antigo
- Cria um novo arquivo com o nome atualizado
- Mantém todo o conteúdo

**Deletar Post**
1. Na página principal, clique em "Deletar" no post desejado
2. Confirme a exclusão no diálogo
3. O post será removido e as mudanças enviadas ao GitHub

**Encerrar o Gerenciador**
- Clique no botão "Fechar Programa" na interface, ou
- Pressione `Ctrl+C` no terminal

## 🌐 Servidor Jekyll Local

Para visualizar o site localmente antes de publicar:

```bash
# Execute o servidor Jekyll
bundle exec jekyll serve

# Acesse http://localhost:4000
```

O servidor Jekyll regenera automaticamente o site quando você modifica arquivos. Útil para:
- Visualizar mudanças antes de publicar
- Testar novos layouts ou estilos
- Verificar como os posts aparecem no site

**Nota**: O Flask GUI Manager e o servidor Jekyll podem rodar simultaneamente em terminais diferentes.

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

### Problemas com GitHub Pages

**Site não aparece após deploy**
- Aguarde 5-10 minutos para o GitHub processar
- Verifique se o repositório é público
- Confirme que o branch está correto nas configurações do Pages
- Verifique se há erros em **Settings** → **Pages** → **Build log**

**Estilos não carregam**
- Verifique se o caminho em `_layouts/default.html` está correto: `/assets/css/main.css`
- Certifique-se de que o arquivo SCSS está sendo compilado (GitHub Pages compila automaticamente)
- Limpe o cache do navegador (`Ctrl+Shift+R` ou `Cmd+Shift+R`)

**Posts não aparecem**
- Verifique o formato do nome do arquivo: `YYYY-MM-DD-titulo.md`
- Confirme que há front matter (---) no início do arquivo
- Verifique se a data não é futura
- Certifique-se de que o front matter YAML é válido

### Problemas com Flask GUI Manager

**Erro ao iniciar: "ModuleNotFoundError"**
```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Reinstale as dependências
pip install -r requirements.txt
```

**Erro: "Port 7856 already in use"**
```bash
# Encontre e mate o processo usando a porta 7856
# No macOS/Linux:
lsof -ti:7856 | xargs kill -9

# No Windows:
netstat -ano | findstr :7856
taskkill /PID <PID> /F
```

**Git operations falham**
- Verifique se você está em um repositório Git: `git status`
- Configure seu nome e email do Git:
  ```bash
  git config user.name "Seu Nome"
  git config user.email "seu@email.com"
  ```
- Verifique se tem permissão de escrita no repositório
- Certifique-se de que está autenticado no GitHub (use SSH keys ou Personal Access Token)

**Jekyll build falha**
- Verifique se Jekyll está instalado: `bundle exec jekyll --version`
- Reinstale as dependências: `bundle install`
- Verifique erros de sintaxe no front matter YAML dos posts
- Verifique se todos os layouts referenciados existem em `_layouts/`

### Problemas com Jekyll Local

**Erro: "bundle: command not found"**
```bash
# Instale o Bundler
gem install bundler
```

**Erro: "Could not find gem 'jekyll'"**
```bash
# Instale as dependências
bundle install
```

**Erro de permissão ao instalar gems**
```bash
# Use um gerenciador de versões Ruby (recomendado)
# macOS com Homebrew:
brew install ruby

# Ou instale gems no diretório do usuário
bundle install --path vendor/bundle
```

**Site não atualiza após mudanças**
- Pare o servidor (`Ctrl+C`) e reinicie: `bundle exec jekyll serve`
- Limpe o cache: `bundle exec jekyll clean && bundle exec jekyll serve`
- Verifique se o arquivo modificado não está na lista `exclude` do `_config.yml`

### Problemas com Giscus (Comentários)

**Comentários não aparecem**
- Verifique se GitHub Discussions está habilitado no repositório:
  - Vá em **Settings** → **General** → **Features**
  - Marque **Discussions**
- Verifique se o repositório é público
- Confirme que a app Giscus está instalada no repositório
- Verifique se os IDs no script Giscus em `_layouts/post.html` estão corretos

**Como reconfigurar Giscus**
1. Acesse [giscus.app](https://giscus.app)
2. Conecte seu repositório
3. Copie o novo código gerado
4. Substitua o script em `_layouts/post.html`

## ⚙️ Guia de Configuração

### Arquivo _config.yml

O arquivo `_config.yml` contém as configurações principais do site:

```yaml
# Informações do Site
title: "Sapieando"                    # Título do site
description: "Blog description"        # Descrição do site
lang: pt-BR                            # Idioma

# URLs
baseurl: /                             # Caminho base (/ para raiz)
url: https://seu-usuario.github.io    # URL completo do site

# Autor
author:
  name: "France Florenzano"            # Nome padrão do autor
  email: "seu@email.com"               # Email do autor

# Logo
logo: /assets/images/sapi_logo_quadrado.png

# Processamento
markdown: kramdown                     # Processador Markdown
highlighter: rouge                     # Syntax highlighter
permalink: /:year/:month/:day/:title/  # Formato de URLs

# Plugins
plugins:
  - jekyll-feed        # Gera RSS feed
  - jekyll-seo-tag     # Otimização SEO
  - jekyll-sitemap     # Gera sitemap.xml

# Arquivos a excluir do site gerado
exclude:
  - Gemfile
  - Gemfile.lock
  - venv
  - blog_manager.py
  - templates
  - requirements.txt
  - tests
  - .cursor
  - .pytest_cache
  - .hypothesis
```

**Campos importantes para personalizar:**
- `title`: Nome do seu blog
- `description`: Descrição que aparece em mecanismos de busca
- `url`: URL completo onde o site será hospedado
- `author.name`: Nome padrão usado ao criar novos posts
- `author.email`: Seu email de contato

### Arquivo requirements.txt

Dependências Python para o Flask GUI Manager:

```
Flask>=3.0.0      # Framework web
pyyaml>=6.0       # Parser YAML para front matter
hypothesis>=6.0.0 # Property-based testing (desenvolvimento)
pytest>=7.0.0     # Framework de testes (desenvolvimento)
```

### Arquivo Gemfile

Dependências Ruby para Jekyll:

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-feed", "~> 0.12"
gem "jekyll-seo-tag", "~> 2.8"
gem "jekyll-sitemap", "~> 1.4"
```

### Estrutura de Diretórios

```
Sapieando/
├── _config.yml           # Configuração Jekyll
├── _posts/               # Posts do blog (YYYY-MM-DD-titulo.md)
├── _layouts/             # Templates HTML
│   ├── default.html      # Layout base
│   ├── post.html         # Layout de post individual
│   └── index.html        # Layout da página inicial
├── _includes/            # Componentes reutilizáveis
│   ├── header.html       # Cabeçalho do site
│   ├── footer.html       # Rodapé do site
│   ├── main-header.html  # Variante do cabeçalho
│   ├── sidebar-header.html # Cabeçalho da sidebar
│   └── post-meta.html    # Metadados do post (data, autor)
├── assets/               # Arquivos estáticos
│   ├── css/              # Estilos (main.scss)
│   ├── fonts/            # Fontes customizadas (Albura)
│   └── images/           # Imagens
├── templates/            # Templates Flask (para GUI)
│   ├── index.html        # Lista de posts
│   ├── edit.html         # Formulário criar/editar
│   └── shutdown.html     # Página de encerramento
├── tests/                # Testes automatizados
├── venv/                 # Ambiente virtual Python (não versionado)
├── _site/                # Site gerado (não versionado)
├── blog_manager.py       # Aplicação Flask GUI
├── requirements.txt      # Dependências Python
├── Gemfile               # Dependências Ruby
└── README.md            # Este arquivo
```

### Personalização de Cores

Edite `assets/css/main.scss` para alterar as cores do tema:

```scss
// Cores principais
$text-color: #873D35;      // Cor do texto
$background-color: #E3CAB1; // Cor de fundo
$button-color: #873D35;     // Cor dos botões
$button-text: #E3CAB1;      // Cor do texto dos botões
```

### Configuração do Giscus

Para configurar comentários nos posts:

1. Habilite **Discussions** no repositório GitHub
2. Acesse [giscus.app](https://giscus.app) e configure:
   - Repository: `seu-usuario/seu-repositorio`
   - Category: Escolha uma categoria de Discussions
   - Mapping: `pathname` (recomendado)
   - Language: `pt-BR`
   - Theme: `light`
3. Copie o código gerado
4. Edite `_layouts/post.html` e substitua o script Giscus

## 🚀 Deploy e Publicação

### Deploy Automático via GitHub Pages

O deploy é automático quando você faz push para o GitHub:

1. **Usando o Flask GUI Manager**: O sistema faz commit e push automaticamente após criar/editar/deletar posts
2. **Manualmente via Git**:
   ```bash
   git add .
   git commit -m "Descrição das mudanças"
   git push origin main
   ```

O GitHub Pages detecta as mudanças e reconstrói o site automaticamente (leva 1-5 minutos).

### Verificar Status do Deploy

1. Vá ao seu repositório no GitHub
2. Clique na aba **Actions**
3. Veja o status do build mais recente
4. Se houver erros, clique no build para ver detalhes

### Deploy Manual Local (Teste)

Para gerar o site localmente sem publicar:

```bash
# Gerar site em _site/
bundle exec jekyll build

# Ou gerar e servir localmente
bundle exec jekyll serve
```

### Workflow de Publicação Recomendado

1. **Desenvolvimento Local**:
   - Use o Flask GUI Manager para criar/editar posts
   - Execute `bundle exec jekyll serve` em outro terminal
   - Visualize mudanças em `http://localhost:4000`

2. **Publicação**:
   - O Flask GUI Manager faz commit e push automaticamente
   - Ou faça push manual: `git push origin main`
   - Aguarde o GitHub Pages reconstruir (1-5 minutos)
   - Verifique o site publicado

3. **Verificação**:
   - Acesse seu site em `https://seu-usuario.github.io`
   - Verifique se o post aparece corretamente
   - Teste os comentários Giscus (se configurado)

### Domínio Customizado (Opcional)

Para usar um domínio próprio (ex: `www.seublog.com`):

1. No repositório GitHub, vá em **Settings** → **Pages**
2. Em **Custom domain**, digite seu domínio
3. Configure DNS no seu provedor de domínio:
   - Adicione um registro `CNAME` apontando para `seu-usuario.github.io`
   - Ou adicione registros `A` para os IPs do GitHub Pages
4. Aguarde propagação DNS (pode levar até 48 horas)
5. Habilite **Enforce HTTPS** nas configurações do Pages

Mais detalhes: [GitHub Pages Custom Domain](https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site)

## 📚 Recursos Úteis

- [Documentação do Jekyll](https://jekyllrb.com/docs/)
- [GitHub Pages Docs](https://docs.github.com/pages)
- [Markdown Guide](https://www.markdownguide.org/)
- [Giscus Documentation](https://giscus.app/)

## 📄 Licença

Este projeto usa a licença GPL v2 ou posterior, mantendo a licença do tema Bibliophile original.

---

**Desenvolvido com ❤️ usando Jekyll e GitHub Pages**
