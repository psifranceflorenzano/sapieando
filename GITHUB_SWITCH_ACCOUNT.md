# 🔄 Como Trocar de Conta no GitHub

Guia completo para fazer login com outra conta do GitHub, tanto na interface web quanto no terminal.

---

## 🌐 Método 1: Interface Web do GitHub

### Opção A: Fazer Logout e Login Novamente

1. **Fazer Logout**:
   - Clique no seu **avatar** (canto superior direito)
   - Role até o final do menu
   - Clique em **"Sign out"**

2. **Fazer Login com Outra Conta**:
   - Acesse [github.com](https://github.com)
   - Clique em **"Sign in"**
   - Digite o **username** ou **email** da outra conta
   - Digite a **senha**
   - Se tiver 2FA habilitado, informe o código

### Opção B: Usar Janela Anônima/Privada

1. Abra uma **janela anônima/privada** no navegador:
   - **Chrome/Edge**: `Cmd + Shift + N` (macOS) ou `Ctrl + Shift + N` (Windows)
   - **Firefox**: `Cmd + Shift + P` (macOS) ou `Ctrl + Shift + P` (Windows)
   - **Safari**: `Cmd + Shift + N` (macOS)

2. Acesse [github.com](https://github.com) e faça login com a outra conta

3. **Vantagem**: Mantém sua conta original logada na janela normal

### Opção C: Usar Perfis Diferentes do Navegador

- **Chrome/Edge**: Crie perfis separados para cada conta GitHub
- **Firefox**: Use Containers para separar contas
- Isso permite ter ambas as contas abertas simultaneamente

---

## 💻 Método 2: Terminal/Git CLI

### Opção A: Atualizar Credenciais Salvas (macOS)

#### 1. Remover Credenciais Antigas do Keychain

```bash
# Ver credenciais salvas
git credential-osxkeychain erase
host=github.com
protocol=https
# Pressione Enter duas vezes para confirmar
```

Ou use o **Keychain Access**:
- Abra **Keychain Access** (Aplicativos → Utilitários)
- Procure por **"github.com"**
- Delete as entradas relacionadas

#### 2. Fazer Push com Nova Conta

Quando fizer `git push`, o Git pedirá credenciais:

```bash
# Navegue até o projeto
cd ~/Documents/Projects/Sapieando

# Tente fazer push
git push origin main
```

**Quando pedir credenciais**:
- **Username**: username da NOVA conta GitHub
- **Password**: use um **Personal Access Token** (não a senha!)
  - Crie em: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  - Permissões necessárias: `repo`, `workflow`

#### 3. Atualizar Remote URL (se necessário)

Se o repositório pertence à outra conta:

```bash
# Ver remote atual
git remote -v

# Atualizar para nova conta (substitua USERNAME e REPO)
git remote set-url origin https://github.com/USERNAME/REPO.git

# Ou usar SSH (mais seguro)
git remote set-url origin git@github.com:USERNAME/REPO.git
```

### Opção B: Usar Personal Access Token

1. **Criar Token na Nova Conta**:
   - Faça login no GitHub com a outra conta
   - Vá em **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
   - Clique em **"Generate new token (classic)"**
   - Dê um nome (ex: "Sapieando Blog")
   - Selecione permissões: ✅ **repo**, ✅ **workflow**
   - Clique em **"Generate token"**
   - **COPIE O TOKEN** (você só verá uma vez!)

2. **Usar o Token**:
   - Quando o Git pedir senha, cole o **token** (não a senha)
   - O token será salvo no Keychain

### Opção C: Usar SSH (Recomendado para Múltiplas Contas)

#### 1. Gerar Chave SSH para Nova Conta

```bash
# Gerar nova chave SSH (use email da nova conta)
ssh-keygen -t ed25519 -C "email-da-nova-conta@example.com"

# Quando pedir nome do arquivo, use um nome único:
# Exemplo: ~/.ssh/id_ed25519_nova_conta

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_nova_conta
```

#### 2. Adicionar Chave SSH ao GitHub

```bash
# Copiar chave pública
pbcopy < ~/.ssh/id_ed25519_nova_conta.pub
```

Depois:
- Faça login no GitHub com a NOVA conta
- Vá em **Settings** → **SSH and GPG keys**
- Clique em **"New SSH key"**
- Cole a chave e salve

#### 3. Configurar SSH para Múltiplas Contas

Crie/edite `~/.ssh/config`:

```bash
# Conta original
Host github.com-original
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# Nova conta
Host github.com-nova
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_nova_conta
```

#### 4. Atualizar Remote URL

```bash
# Para usar a nova conta
git remote set-url origin git@github.com-nova:USERNAME/REPO.git

# Para usar a conta original
git remote set-url origin git@github.com-original:USERNAME/REPO.git
```

---

## 🔐 Criar Personal Access Token

Se precisar criar um token para autenticação:

1. **No GitHub** (logado com a conta desejada):
   - Clique no **avatar** → **Settings**
   - Menu lateral: **Developer settings**
   - **Personal access tokens** → **Tokens (classic)**
   - **Generate new token (classic)**

2. **Configure**:
   - **Note**: Nome descritivo (ex: "Sapieando Blog Deploy")
   - **Expiration**: Escolha um prazo (ou "No expiration")
   - **Scopes**: Marque pelo menos:
     - ✅ **repo** (acesso completo aos repositórios)
     - ✅ **workflow** (se usar GitHub Actions)

3. **Gere e Copie**:
   - Clique em **"Generate token"**
   - **COPIE O TOKEN IMEDIATAMENTE** (você não verá novamente!)
   - Use este token como "senha" quando o Git pedir credenciais

---

## ✅ Verificar Qual Conta Está Sendo Usada

### No Terminal:

```bash
# Ver configuração do Git
git config user.name
git config user.email

# Ver remote configurado
git remote -v

# Testar autenticação (se usar SSH)
ssh -T git@github.com
# ou
ssh -T git@github.com-nova  # se configurou alias
```

### No GitHub Web:

- Olhe o **avatar** no canto superior direito
- O nome/avatar mostra qual conta está logada

---

## 🎯 Cenário Específico: Deploy do Sapieando

Se você quer fazer deploy do blog Sapieando com outra conta:

### Passo 1: Criar Repositório na Nova Conta

1. Faça login no GitHub com a **nova conta** (via web)
2. Crie um novo repositório:
   - Nome: `sapieando` ou `usuario-novo.github.io`
   - Visibilidade: **Public**

### Passo 2: Configurar Git Local

```bash
cd ~/Documents/Projects/Sapieando

# Configurar Git para nova conta (opcional, só para commits)
git config user.name "Nome da Nova Conta"
git config user.email "email-da-nova-conta@example.com"

# Adicionar remote da nova conta
git remote set-url origin https://github.com/USERNAME-NOVO/sapieando.git

# Ou remover e adicionar novo
git remote remove origin
git remote add origin https://github.com/USERNAME-NOVO/sapieando.git
```

### Passo 3: Fazer Push

```bash
git push -u origin main
```

Quando pedir credenciais:
- **Username**: username da nova conta
- **Password**: Personal Access Token da nova conta

---

## 🆘 Problemas Comuns

### "Authentication failed" ou "Permission denied"

**Solução**:
- Verifique se está usando o **token correto** (não a senha)
- Confirme que o token tem permissão **repo**
- Se usar SSH, verifique se a chave está adicionada ao GitHub

### Credenciais Antigas Ainda Sendo Usadas

**Solução**:
```bash
# Limpar credenciais do macOS Keychain
git credential-osxkeychain erase
host=github.com
protocol=https
# Enter duas vezes
```

Ou delete manualmente no **Keychain Access**.

### "Repository not found"

**Solução**:
- Verifique se o repositório existe na conta que você está usando
- Confirme que você tem acesso ao repositório
- Verifique se o remote URL está correto: `git remote -v`

---

## 📚 Recursos Úteis

- [GitHub: Managing multiple accounts](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-user-account/managing-user-account-settings/managing-multiple-accounts)
- [GitHub: Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub: Using SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**Dica**: Para trabalhar com múltiplas contas regularmente, considere usar **SSH com aliases** (Método 2, Opção C) - é mais seguro e conveniente a longo prazo!
