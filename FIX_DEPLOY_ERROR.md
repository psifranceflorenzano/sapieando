# 🚨 Solução Rápida: Erro "Multiple artifacts named 'github-pages'"

## O Problema

Você está recebendo este erro:
```
Error: Multiple artifacts named "github-pages" were unexpectedly found
```

Isso acontece quando há **múltiplos builds** tentando fazer deploy ao mesmo tempo.

## ✅ Solução Rápida (5 minutos)

### Opção 1: Usar Build Automático (Mais Simples)

Para sites Jekyll, o GitHub Pages faz build **automaticamente**. Você não precisa de workflows customizados.

**Passos:**

1. **Vá no GitHub → Seu Repositório → Settings → Pages**

2. **Em "Build and deployment"**, configure:
   - **Source**: `Deploy from a branch` (NÃO "GitHub Actions")
   - **Branch**: `main` (ou `master` se for seu branch padrão)
   - **Folder**: `/ (root)`
   - Clique em **Save**

3. **Vá em Actions** (aba no topo do repositório)
   - Cancele qualquer workflow em execução
   - Se houver workflows duplicados, delete-os

4. **Aguarde 2-3 minutos** e verifique se o site está funcionando

### Opção 2: Limpar e Recomeçar

Se a Opção 1 não funcionar:

1. **Desabilitar Pages temporariamente**:
   - Settings → Pages → Source: `None` → Save

2. **Aguardar 2 minutos**

3. **Reabilitar**:
   - Settings → Pages → Source: `Deploy from a branch`
   - Branch: `main` → Folder: `/ (root)` → Save

4. **Fazer commit vazio para forçar rebuild**:
   ```bash
   git commit --allow-empty -m "Fix: Trigger rebuild"
   git push
   ```

## 🔍 Verificações Importantes

### 1. Verificar se há workflows customizados

No GitHub, vá em **Actions** e veja se há workflows listados. Se houver workflows que fazem deploy, você tem duas opções:

**A) Deletar os workflows** (recomendado para Jekyll):
- Vá em **Actions**
- Clique em cada workflow
- Clique nos **3 pontos** → **Delete workflow**

**B) Mudar para usar GitHub Actions**:
- Settings → Pages → Source: `GitHub Actions`
- Use apenas UM workflow de deploy

### 2. Verificar branch padrão

- Settings → General → Default branch
- Use o mesmo branch nas configurações do Pages

### 3. Verificar permissões

- Settings → Actions → General
- Workflow permissions: ✅ "Read and write permissions"

## 📋 Checklist de Solução

Execute estes passos na ordem:

- [ ] Verificar Settings → Pages está configurado para "Deploy from a branch"
- [ ] Cancelar todos os workflows em execução em Actions
- [ ] Deletar workflows duplicados (se houver)
- [ ] Desabilitar e reabilitar Pages (se necessário)
- [ ] Fazer commit vazio para forçar rebuild
- [ ] Aguardar 5-10 minutos
- [ ] Verificar se o site está funcionando

## 🆘 Se Ainda Não Funcionar

1. **Verifique os logs completos**:
   - Vá em **Actions**
   - Clique no workflow que falhou
   - Veja os logs completos para identificar o erro específico

2. **Verifique status do GitHub**:
   - [status.github.com](https://www.githubstatus.com/)
   - Se houver problemas reportados, aguarde

3. **Tente fazer um pequeno commit**:
   ```bash
   # Faça uma pequena mudança
   echo "# Test" >> README.md
   git add README.md
   git commit -m "Test deploy"
   git push
   ```

## 💡 Por Que Isso Acontece?

Este erro geralmente ocorre quando:
- Há múltiplos workflows tentando fazer deploy simultaneamente
- Há conflito entre build automático do GitHub Pages e workflows customizados
- Builds anteriores não foram cancelados corretamente

**Para Jekyll**: Use apenas o build automático do GitHub Pages. Não é necessário criar workflows customizados.

## ✅ Configuração Recomendada para Jekyll

```
Settings → Pages:
├── Source: Deploy from a branch
├── Branch: main (ou master)
└── Folder: / (root)
```

**NÃO** use "GitHub Actions" como source a menos que você realmente precise de um workflow customizado.

---

**Depois de seguir estes passos, seu site deve estar funcionando!** 🎉
