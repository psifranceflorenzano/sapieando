# 🚀 Guia Rápido: Deploy no GitHub Pages

## Método 1: Via Interface Web (Mais Fácil)

### Passo 1: Criar Repositório

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito → **"New repository"**
3. Configure:
   - **Repository name**: `seu-usuario.github.io` (para site pessoal) OU `sapieando` (para projeto)
   - **Description**: "Blog sobre psicanálise"
   - **Visibility**: ✅ **Public** (obrigatório para GitHub Pages gratuito)
   - ❌ **NÃO** marque "Add a README file"
4. Clique em **"Create repository"**

### Passo 2: Fazer Upload dos Arquivos

1. No repositório criado, você verá uma página com instruções
2. Clique em **"uploading an existing file"** (ou arraste arquivos)
3. Abra a pasta do projeto `Sapieando` no Finder
4. **Arraste TODOS os arquivos e pastas** para o GitHub:
   - `_config.yml`
   - `_layouts/` (pasta inteira)
   - `_includes/` (pasta inteira)
   - `_posts/` (pasta inteira)
   - `assets/` (pasta inteira)
   - `index.html`
   - `Gemfile`
   - `.gitignore`
   - `README.md`
   - **NÃO** inclua a pasta `site-export/` (é do WordPress antigo)
5. Role até o final da página
6. Em **"Commit changes"**, escreva: "Initial commit: Jekyll blog"
7. Clique em **"Commit changes"**

### Passo 3: Ativar GitHub Pages

1. No repositório, clique na aba **"Settings"** (Configurações)
2. No menu lateral esquerdo, clique em **"Pages"**
3. Em **"Source"**, configure:
   - Selecione **"Deploy from a branch"**
   - **Branch**: escolha `main`
   - **Folder**: escolha `/ (root)`
4. Clique em **"Save"**
5. ⏳ **Aguarde 2-5 minutos** para o GitHub processar
6. Você verá uma mensagem verde: *"Your site is live at https://seu-usuario.github.io"*

### Passo 4: Acessar seu Site

- Se o repositório for `seu-usuario.github.io`: `https://seu-usuario.github.io`
- Se for outro nome: `https://seu-usuario.github.io/nome-do-repo`

---

## Método 2: Via Git (Mais Profissional)

### Pré-requisitos

Instale o Git se ainda não tiver:
- **macOS**: `brew install git` (com Homebrew) ou baixe de [git-scm.com](https://git-scm.com)
- Verifique: `git --version` no Terminal

### Passo 1: Criar Repositório no GitHub

(Siga os mesmos passos do Método 1, Passo 1)

### Passo 2: Conectar e Fazer Upload

Abra o Terminal e execute:

```bash
# 1. Navegue até a pasta do projeto
cd ~/Documents/Projects/Sapieando

# 2. Inicialize o Git
git init

# 3. Adicione todos os arquivos
git add .

# 4. Faça o primeiro commit
git commit -m "Initial commit: Jekyll blog setup"

# 5. Renomeie o branch para 'main' (se necessário)
git branch -M main

# 6. Adicione o repositório remoto (SUBSTITUA seu-usuario e nome-do-repo)
git remote add origin https://github.com/seu-usuario/nome-do-repo.git

# 7. Envie para o GitHub
git push -u origin main
```

**Nota**: Você precisará fazer login no GitHub. Se pedir credenciais:
- **Username**: seu usuário do GitHub
- **Password**: use um **Personal Access Token** (não sua senha)
  - Crie em: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Permissões: `repo`

### Passo 3: Ativar GitHub Pages

(Siga os mesmos passos do Método 1, Passo 3)

---

## ✅ Verificar se Funcionou

1. Aguarde alguns minutos após ativar o Pages
2. Acesse a URL do seu site
3. Você deve ver:
   - O título "Sapieando"
   - O post de exemplo "Bem-vindo ao Sapieando"
   - O layout com cores #873D35 e #E3CAB1

---

## 🔧 Solução de Problemas

### Site não aparece / Erro 404

- ✅ Verifique se o repositório é **Public**
- ✅ Confirme que o branch está correto (`main`)
- ✅ Aguarde mais alguns minutos (pode levar até 10 minutos)
- ✅ Verifique em **Settings → Pages** se há erros no build

### Erro no Build

1. Vá em **Settings → Pages**
2. Role até **"Build and deployment"**
3. Clique em **"Actions"** para ver logs de erro
4. Erros comuns:
   - **Erro de sintaxe no `_config.yml`**: Verifique vírgulas e espaços
   - **Plugin não suportado**: GitHub Pages tem plugins limitados (os do Gemfile estão OK)

### Estilos não Carregam

- Verifique se o arquivo `assets/css/main.scss` está presente
- O GitHub Pages compila SCSS automaticamente para `main.css`
- Aguarde alguns minutos após o primeiro deploy

### Posts não Aparecem

- Verifique o formato do nome: `YYYY-MM-DD-titulo.md`
- Confirme que há front matter (`---`) no início
- Verifique se a data não é futura

---

## 📝 Próximos Passos

Depois que o site estiver funcionando:

1. **Configurar Giscus (Comentários)**:
   - Edite `_layouts/post.html`
   - Substitua `USERNAME/REPO` pelo seu repositório
   - Configure em [giscus.app](https://giscus.app)

2. **Personalizar**:
   - Edite `_config.yml` para mudar título/descrição
   - Adicione mais posts em `_posts/`
   - Customize cores em `assets/css/main.scss`

3. **Atualizar Site**:
   - Faça mudanças nos arquivos
   - Commit e push (se usar Git) ou faça upload via web
   - O GitHub Pages atualiza automaticamente

---

## 🆘 Precisa de Ajuda?

- [Documentação GitHub Pages](https://docs.github.com/pages)
- [Documentação Jekyll](https://jekyllrb.com/docs/)
- Verifique o `README.md` completo para mais detalhes
