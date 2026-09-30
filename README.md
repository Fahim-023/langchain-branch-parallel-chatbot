# LangChain Chatbot using RunnableBranch & RunnableParallel

An AI chatbot built with LangChain that demonstrates conditional routing (`RunnableBranch`), simultaneous multi-output generation (`RunnableParallel`), and schema-validated responses (Pydantic structured output), wrapped in a Streamlit chat interface.

## Project Overview

This project routes user questions to one of four specialized prompt pipelines based on the content of the question, generates a structured, schema-validated answer alongside an independently generated follow-up question suggestion, and displays everything through an interactive Streamlit chat UI.

The chatbot is powered by Groq's `openai/gpt-oss-20b` model via the `langchain-groq` integration, chosen for its speed and native support for structured outputs.

## Features

- **Four-way conditional routing** via `RunnableBranch` — Programming, Mathematics, English, and General queries each get a specialized prompt.
- **Parallel output generation** via `RunnableParallel` — the main structured answer and a follow-up question suggestion are generated independently from the same input.
- **Schema-validated responses** via Pydantic (`with_structured_output`) — every main answer includes an answer, summary, confidence score, category, and keywords, all type-checked.
- **Streamlit chat interface** — persistent chat history, a live "Thinking…" spinner, an expandable follow-up section, and a Clear Chat button.
- **Secure API key handling** — the Groq API key is loaded from a `.env` file and never hardcoded or committed.

## RunnableBranch Implementation

Four condition functions inspect the incoming question for keywords (e.g. `"python"`, `"function"` for programming; `"algebra"`, `"calculus"` for math; `"grammar"`, `"essay"` for English). `RunnableBranch` evaluates these conditions in order and routes the question to the matching prompt-and-model chain. If no keywords match, the question falls through to a General Assistant chain by default.

```python
branch = RunnableBranch(
    (is_programming, programming_chain),
    (is_math, math_chain),
    (is_english, english_chain),
    general_chain  # default fallback
)
```

This satisfies FR-4: different prompt pipelines are executed depending on user input, with custom branching logic (a 4th English branch was added beyond the PRS's three suggested categories).

## RunnableParallel Implementation

`RunnableParallel` runs two independent chains on the same user question simultaneously:

- `answer` — the routed, schema-validated response from `branch`
- `summary` — a plain-text, independently generated follow-up/summary output

```python
chat_parallel = RunnableParallel(
    answer=branch,
    summary=summary_chain
)
```

Both chains execute off the identical input dictionary (`{"question": ...}`) but produce separate, unrelated outputs in a single `.invoke()` call, satisfying FR-5.

## Pydantic Structured Output Implementation

A `ResponseSchema` class defines the exact shape every main answer must conform to:

```python
class ResponseSchema(BaseModel):
    answer: str
    summary: str
    confidence: int
    category: str
    keywords: List[str]
```

The LLM is bound to this schema using `llm.with_structured_output(ResponseSchema)`, so every branch chain returns a validated `ResponseSchema` object instead of raw text — satisfying FR-3. `StrOutputParser` alone is not used anywhere in the response pipeline, per the assignment's requirement.

## Project Structure

```
project/
│
├── app.py              # Streamlit UI
├── chatbot.py           # RunnableBranch, RunnableParallel, structured output wiring
├── prompts.py            # PromptTemplates for each branch
├── schemas.py            # Pydantic response schema
├── requirements.txt
├── .env.example
└── README.md
```

## Installation Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Fahim-023/langchain-branch-parallel-chatbot.git
   cd langchain-branch-parallel-chatbot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   - Copy `.env.example` to `.env`
   - Get a free API key from [console.groq.com](https://console.groq.com)
   - Add it to `.env`:
     ```
     GROQ_API_KEY=your_actual_key_here
     ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## Notes

- The `.env` file is excluded from version control via `.gitignore` and must never be committed.
- Model used: `openai/gpt-oss-20b` (via Groq), selected for native support of structured outputs, tool use, and reasoning.
