# 📚 SecondBrain AI (com Deva)

Um sistema de IA local integrado ao seu Second Brain no Obsidian. Permite buscas semânticas e interações via terminal ou API usando um modelo personalizado (via Ollama + embeddings).

---

## 🚀 Funcionalidades

- 🔍 **Busca semântica** com FAISS + Sentence Transformers
- 🧠 **Assistente local** (LLM via Ollama) com prompt personalizado
- 📦 **Indexação inteligente** das suas notas em Markdown (com hash incremental)
- 💬 **Interface via terminal** e também via **API HTTP** (FastAPI)
- 📝 **Correção automática de notas** com o LLM (formatação ortográfica e estilística)

---

## 🧱 Estrutura do Projeto

```bash
📦 secondbrain_ai/
├── config/            # Configurações (env, modelo, caminhos)
├── core/              # Núcleo do sistema (embeddings, parser, LLM, indexação)
├── server/            # API com FastAPI e schemas de entrada
├── prompts/           # Prompts default (e pessoais ignorados)
├── scripts/           # Entradas executáveis (CLI, atualizador, testes)
├── utils/             # Utilitários como hash de arquivos
├── data/              # Índice embeddado (ignorado no Git)
├── .env.example       # Exemplo de variáveis de ambiente
├── Modelfile.example  # Exemplo de modelfile para Ollama
├── requirements.txt   # Dependências do projeto
└── README.md
```

---

## ⚙️ Requisitos

- Python 3.10+
- [Ollama](https://ollama.com) instalado localmente

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/secondbrain_ai.git
cd secondbrain_ai
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure seu ambiente:

```bash
cp .env.example .env
# edite o .env conforme necessário
```

4. Crie um modelo no Ollama com base no seu `Modelfile`:

```bash
ollama create deva -f Modelfile
```

> Dica: use o `Modelfile.example` como base e crie sua versão pessoal.

---

## 🧪 Como usar

### Terminal (CLI)

```bash
python scripts/cli_main.py
```

Digite perguntas com base nas suas notas. O sistema buscará trechos relevantes e responderá com o LLM.

### Reindexar completamente:

```bash
python scripts/cli_main.py --reindexar
```

### Rodar em modo escuta (atualização automática):

```bash
python scripts/cli_main.py --escutar
```

### API (FastAPI)

```bash
uvicorn server.api:app --reload
```

- `POST /query`: envia pergunta
- `POST /formatar-nota`: corrige ortografia/estilo de uma nota Markdown

---

## 🧠 Sobre os prompts

Os prompts usados pelo modelo são externos e configuráveis em JSON:

- `prompts/default.json`: prompts genéricos, versionados
- `prompts/pessoal.json`: **sua versão customizada** (é ignorada pelo Git)

Você pode mudar o caminho no `.env` com:

```env
PROMPT_PATH=prompts/pessoal.json
```

Os campos aceitos são:

- `pergunta`
- `formatar`
- `revisar`
- `resumir`

> Veja [docs/prompts.md](docs/prompts.md) para detalhes sobre como personalizar e organizar seus prompts.

---

## 🔐 Segurança

- Nenhuma nota é enviada online — tudo roda **100% localmente**
- O diretório `vault/` e `data/` são ignorados via `.gitignore`
- Você pode controlar tudo pelo seu terminal

---

## 🧩 Modelfile

O projeto usa modelos personalizados via `Ollama`. Um exemplo de `Modelfile` está incluído no repositório.

Se quiser manter um `Modelfile` pessoal com instruções específicas (ex: "Você é o Deva..."), mantenha isso em `Modelfile` e ignore no Git:

```
Modelfile*
!Modelfile.example
```

Você pode criar outros arquivos de documentação, como:

- `docs/prompts.md`
- `docs/modelfiles.md`

> Veja [docs/modelfiles.md](docs/modelfiles.md) para entender como personalizar o comportamento do seu assistente local via prompt base.

---

## 🧹 Para manter o repositório limpo

Certifique-se de que seu `.gitignore` contém:

```gitignore
.env
__pycache__/
*.pyc
data/
vault/
prompts/pessoal.json
Modelfile*
!Modelfile.example
```

---

## ✨ Créditos e inspiração

Este projeto foi idealizado como um Second Brain integrado com IA, focando em produtividade e organização pessoal com máxima privacidade e controle.

---

## ✅ Status

Projeto ainda em andamento, ainda ah muito para evoluir.

---

