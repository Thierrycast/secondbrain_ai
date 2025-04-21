# 📄 Documentação de Prompts

Este projeto utiliza prompts externos em arquivos `.json` para permitir que o comportamento do assistente seja facilmente customizável.

---

## 📁 Estrutura esperada

Os prompts ficam localizados em:

```bash
prompts/
├── default.json       # Prompts neutros e públicos
└── pessoal.json       # Prompts personalizados (não versionado)
```

O arquivo padrão (`default.json`) é versionado e acompanha o projeto.

O arquivo `pessoal.json` **deve ser criado manualmente** e está ignorado no `.gitignore`.

---

## 🔧 Formato de prompt

Cada prompt é uma string com placeholders `{conteudo}` e `{pergunta}` quando necessário:

```json
{
  "pergunta": "Você é um assistente...\n\nContexto:\n{conteudo}\n\nPergunta:\n{pergunta}\n\nResposta:",
  "formatar": "Corrija o texto abaixo...\n\nTexto:\n{conteudo}\n\nTexto corrigido:",
  "resumir": "Resuma o texto abaixo...\n\nTexto:\n{conteudo}\n\nResumo:",
  "revisar": "Reescreva com mais clareza...\n\nTexto:\n{conteudo}\n\nTexto revisado:"
}
```

---

## 🧠 Como o sistema usa os prompts

No código, a função `montar_prompt()` carrega o prompt do tipo solicitado e faz `template.format(...)` com os dados adequados:

```python
prompt = PROMPTS.get("pergunta")
full_prompt = prompt.format(conteudo=..., pergunta=...)
```

---

## 💡 Recomendações para `pessoal.json`

Você pode usar um estilo mais informal, técnico ou voltado ao seu uso específico. Exemplo:

```json
{
  "pergunta": "Você é o Deva, um assistente pessoal do Thierry...",
  ...
}
```

---

## 🔄 Alternar entre prompts

No `.env`, basta trocar:

```env
PROMPT_PATH=prompts/pessoal.json
```

Se `pessoal.json` não for encontrado, o sistema cai em `default.json` automaticamente.

---

## ✅ Status

Sistema de prompts é modular, extensível e pronto para personalização total.

