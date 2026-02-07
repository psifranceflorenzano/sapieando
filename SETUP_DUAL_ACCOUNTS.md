# 🔐 Configuração: Usar Duas Contas GitHub

Este projeto está configurado para usar a conta **psifranceflorenzano**, enquanto outros projetos continuam usando **mollinetti**.

---

## ✅ O Que Já Foi Configurado

1. **Git local config** para este repositório:
   - `user.name`: psifranceflorenzano
   - `user.email`: psifranceflorenzano@users.noreply.github.com

2. **Remote URL**: `https://github.com/psifranceflorenzano/sapieando`

---

## 🔑 Método Recomendado: HTTPS com Credential Helper

### Passo 1: Criar Personal Access Token para psifranceflorenzano

1. Faça login no GitHub com a conta **psifranceflorenzano**
2. Vá em **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Clique em **"Generate new token (classic)"**
4. Configure:
   - **Note**: "Sapieando Blog"
   - **Expiration**: Escolha um prazo
   - **Scopes**: ✅ **repo**, ✅ **workflow**
5. Clique em **"Generate token"**
6. **COPIE O TOKEN** (você só verá uma vez!)

### Passo 2: Configurar Credential Helper

O Git vai pedir credenciais quando você fizer push. Use:
- **Username**: `psifranceflorenzano`
- **Password**: Cole o **Personal Access Token** (não a senha!)

O macOS Keychain vai salvar essas credenciais especificamente para `github.com/psifranceflorenzano`, então não vai interferir com outros projetos.

### Passo 3: Testar

```bash
cd ~/Documents/Projects/Sapieando
git push origin main
```

Quando pedir credenciais, use o token da conta psifranceflorenzano.

---

## 🔐 Método Alternativo: SSH (Mais Seguro)

Se preferir usar SSH em vez de HTTPS:

### Passo 1: Gerar Chave SSH para psifranceflorenzano

```bash
# Gerar nova chave SSH
ssh-keygen -t ed25519 -C "psifranceflorenzano@users.noreply.github.com"

# Quando pedir nome do arquivo:
# Digite: ~/.ssh/id_ed25519_psifranceflorenzano

# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_psifranceflorenzano
```

### Passo 2: Adicionar Chave ao GitHub

```bash
# Copiar chave pública
pbcopy < ~/.ssh/id_ed25519_psifranceflorenzano.pub
```

Depois:
1. Faça login no GitHub com a conta **psifranceflorenzano**
2. Vá em **Settings** → **SSH and GPG keys**
3. Clique em **"New SSH key"**
4. Cole a chave e salve

### Passo 3: Configurar SSH Config

Adicione ao arquivo `~/.ssh/config`:

```
Host github.com-psifranceflorenzano
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_psifranceflorenzano
```

### Passo 4: Atualizar Remote URL

```bash
cd ~/Documents/Projects/Sapieando
git remote set-url origin git@github.com-psifranceflorenzano:psifranceflorenzano/sapieando.git
```

### Passo 5: Testar

```bash
# Testar conexão SSH
ssh -T git@github.com-psifranceflorenzano

# Deve mostrar: "Hi psifranceflorenzano! You've successfully authenticated..."

# Fazer push
git push origin main
```

---

## ✅ Verificar Configuração

### Ver qual conta está configurada neste projeto:

```bash
cd ~/Documents/Projects/Sapieando

# Ver user config local
git config --local user.name
git config --local user.email

# Ver remote
git remote -v
```

### Ver conta global (para outros projetos):

```bash
git config --global user.name
git config --global user.email
```

---

## 🎯 Como Funciona

- **Este projeto (Sapieando)**: Usa `psifranceflorenzano`
  - Configurado localmente no repositório
  - Remote aponta para `psifranceflorenzano/sapieando`
  - Credenciais salvas separadamente

- **Outros projetos**: Continuam usando `mollinetti`
  - Configuração global permanece como `mollinetti`
  - Não é afetada pela configuração deste projeto

---

## 🆘 Problemas Comuns

### "Authentication failed" ao fazer push

**Solução**:
- Se usar HTTPS: Verifique se está usando o **Personal Access Token** correto
- Se usar SSH: Verifique se a chave está adicionada ao GitHub e ao ssh-agent

### Credenciais erradas sendo usadas

**Solução**:
```bash
# Limpar credenciais específicas do GitHub
git credential-osxkeychain erase
host=github.com
protocol=https
# Enter duas vezes
```

Depois, tente fazer push novamente e informe as credenciais corretas.

### "Permission denied" com SSH

**Solução**:
```bash
# Verificar se a chave está no ssh-agent
ssh-add -l

# Se não estiver, adicionar
ssh-add ~/.ssh/id_ed25519_psifranceflorenzano

# Testar conexão
ssh -T git@github.com-psifranceflorenzano
```

---

## 📝 Resumo Rápido

**Para usar este projeto:**
- Já está configurado para `psifranceflorenzano`
- Ao fazer push, use credenciais da conta `psifranceflorenzano`
- Outros projetos continuam usando `mollinetti` normalmente

**Próximo passo:**
- Escolha um método (HTTPS ou SSH) acima
- Siga os passos para configurar autenticação
- Teste fazendo um push
