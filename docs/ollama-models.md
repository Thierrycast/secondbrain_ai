# 📄 Documentação: Modelfile

O projeto utiliza o Ollama como servidor local de modelos LLM. Para personalizar o comportamento do modelo, usamos arquivos chamados `Modelfile`, que servem como instruções de base para o modelo.

---

## 📦 Estrutura do Modelfile

```Dockerfile
FROM mistral

SYSTEM """
Você é um assistente pessoal de IA. Seu papel é auxiliar com clareza e utilidade...
"""
```

---

## 🔍 Onde fica

- `Modelfile.example` → Exemplo versionado
- `Modelfile` → Seu modelo pessoal (não versionado)

O padrão é chamar o modelo com:

```bash
ollama create deva -f Modelfile
```

Você também pode criar versões como:
```bash
ollama create deva-smart -f Modelfile.zephyr
```

---

## ✍️ Instruções personalizadas (SYSTEM)

A seção `SYSTEM` permite controlar completamente o comportamento do LLM. Exemplos:

### Neutro (default)
```Dockerfile
FROM mistral

SYSTEM """
Você é um assistente de IA. Responda com clareza, foco e sem devaneios.
"""
```

### Personalizado
```Dockerfile
FROM mistral

SYSTEM """
Você é o Deva, assistente pessoal de Thierry...
Seu papel é ser útil, direto e adaptável.
"""
```

### Comportamento avançado
- Define tom da resposta
- Reage a tipo de contexto (formal/informal)
- Pode restringir ou orientar o que o modelo nunca deve dizer

---

## 🛡️ Segurança

- O `Modelfile` NUNCA é enviado para servidores — ele é usado só na criação local do modelo Ollama
- Para manter privado, ignore no Git:

```gitignore
Modelfile*
!Modelfile.example
```

---

## ✅ Boas práticas

- Sempre use `SYSTEM` em blocos longos para controlar o comportamento
- Use `FROM mistral` ou `FROM zephyr` dependendo do estilo desejado
- Teste seu prompt base interativamente após gerar o modelo

---

## 🧠 Dica

Use o comando `ollama show NOME_DO_MODELO` para verificar detalhes do modelo localmente.

---

## ⚙️ Sobre desempenho

A performance do assistente dependerá fortemente de dois fatores:

- **Modelo base escolhido**: quanto mais recente e robusto o modelo, maior será a qualidade da resposta. Modelos maiores (como versões otimizadas ou com fine-tuning voltado para conversação) tendem a oferecer melhores resultados, mesmo que demandem mais recursos. O uso de modelos pequenos pode ser suficiente para tarefas simples, mas limitará a profundidade e fluidez das respostas.
- **Sua máquina**: quanto mais RAM, CPU ou GPU disponível, melhor será o desempenho. Computadores mais modestos podem apresentar lentidão ao inicializar o modelo ou gerar respostas longas.

---

## ✅ Status

Modelfile estruturado, pronto para ser customizado conforme sua necessidade pessoal, sem depender da nuvem.

