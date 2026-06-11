"""
claude_agents.py
----------------
Connect to the Anthropic API and interact with named Claude agents.

Setup:
    pip install anthropic python-dotenv

    Set your API key in one of two ways:
      Option A - .env file:  ANTHROPIC_API_KEY=sk-ant-...
      Option B - shell:      export ANTHROPIC_API_KEY=sk-ant-...
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# ── Load env vars (no-op if you set the key in your shell) ──────────────────
load_dotenv()

# ── Client ───────────────────────────────────────────────────────────────────
client = Anthropic()          # Reads ANTHROPIC_API_KEY from environment
DEFAULT_MODEL = "claude-sonnet-4-6"


# ── Agent registry ───────────────────────────────────────────────────────────
# Each agent is a dict with a name, model, system prompt, and optional config.
# Add, edit, or remove agents here to fit your use case.

AGENTS: dict[str, dict] = {
    "general": {
        "name": "General Assistant",
        "model": DEFAULT_MODEL,
        "system": "You are a helpful, concise assistant.",
        "max_tokens": 1024,
    },
    "coder": {
        "name": "Coding Assistant",
        "model": DEFAULT_MODEL,
        "system": (
            "You are an expert software engineer. "
            "Respond with clean, well-commented code and brief explanations."
        ),
        "max_tokens": 2048,
    },
    "analyst": {
        "name": "Data Analyst",
        "model": DEFAULT_MODEL,
        "system": (
            "You are a senior data analyst. "
            "Provide structured, evidence-based insights and flag any assumptions."
        ),
        "max_tokens": 1024,
    },
}


# ── Core functions ────────────────────────────────────────────────────────────

def list_agents() -> list[dict]:
    """
    Return a list of all registered agents with their key, name, and model.

    Returns:
        List of dicts: [{"key": ..., "name": ..., "model": ...}, ...]

    Example:
        for agent in list_agents():
            print(agent["key"], "-", agent["name"])
    """
    return [
        {"key": key, "name": cfg["name"], "model": cfg["model"]}
        for key, cfg in AGENTS.items()
    ]


def ask_agent(
    agent_key: str,
    question: str,
    conversation_history: list[dict] | None = None,
) -> str:
    """
    Send a question to a named agent and return its text response.

    Args:
        agent_key:            Key from the AGENTS registry (e.g. "coder").
        question:             The user's message / prompt.
        conversation_history: Optional list of prior {"role", "content"} turns
                              for multi-turn conversations. Pass the list you
                              get back from ask_agent_with_history() to
                              continue a thread.

    Returns:
        The agent's response as a plain string.

    Raises:
        KeyError:  If agent_key is not in AGENTS.
        Exception: Propagates any Anthropic API errors.

    Example:
        reply = ask_agent("coder", "Write a Python hello-world script.")
        print(reply)
    """
    if agent_key not in AGENTS:
        raise KeyError(
            f"Agent '{agent_key}' not found. "
            f"Available agents: {list(AGENTS.keys())}"
        )

    cfg = AGENTS[agent_key]
    messages = list(conversation_history or [])
    messages.append({"role": "user", "content": question})

    response = client.messages.create(
        model=cfg["model"],
        max_tokens=cfg["max_tokens"],
        system=cfg["system"],
        messages=messages,
    )

    return response.content[0].text


def ask_agent_with_history(
    agent_key: str,
    question: str,
    conversation_history: list[dict] | None = None,
) -> tuple[str, list[dict]]:
    """
    Like ask_agent(), but also returns the updated conversation history
    so you can continue a multi-turn thread on the next call.

    Args:
        agent_key:            Key from the AGENTS registry.
        question:             The user's message / prompt.
        conversation_history: Prior turns (start with None or [] for a new thread).

    Returns:
        Tuple of (reply_text, updated_history).

    Example:
        reply, history = ask_agent_with_history("analyst", "Summarize my sales data.")
        reply, history = ask_agent_with_history("analyst", "Which region grew fastest?", history)
    """
    reply = ask_agent(agent_key, question, conversation_history)

    updated_history = list(conversation_history or [])
    updated_history.append({"role": "user", "content": question})
    updated_history.append({"role": "assistant", "content": reply})

    return reply, updated_history


def add_agent(
    key: str,
    name: str,
    system_prompt: str,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
) -> None:
    """
    Register a new agent at runtime (not persisted between runs).

    Args:
        key:           Short identifier used to call the agent (e.g. "summarizer").
        name:          Human-readable display name.
        system_prompt: The system instruction that shapes the agent's behavior.
        model:         Anthropic model string. Defaults to DEFAULT_MODEL.
        max_tokens:    Max tokens in the response. Defaults to 1024.

    Example:
        add_agent(
            key="summarizer",
            name="Summarization Agent",
            system_prompt="You summarize text into three bullet points.",
        )
        print(ask_agent("summarizer", "Summarize the history of the Roman Empire."))
    """
    AGENTS[key] = {
        "name": name,
        "model": model,
        "system": system_prompt,
        "max_tokens": max_tokens,
    }


# ── Quick demo (runs only when executed directly) ─────────────────────────────

if __name__ == "__main__":
    # 1. List all registered agents
    print("=== Registered Agents ===")
    for agent in list_agents():
        print(f"  [{agent['key']}]  {agent['name']}  ({agent['model']})")

    print()

    # 2. Ask the general agent a one-off question
    print("=== Single-turn example ===")
    reply = ask_agent("general", "What is the capital of Brazil?")
    print(f"General: {reply}")

    print()

    # 3. Multi-turn conversation with the coder agent
    print("=== Multi-turn example ===")
    reply, history = ask_agent_with_history("coder", "Write a Python function that reverses a string.")
    print(f"Coder: {reply}")

    reply, history = ask_agent_with_history("coder", "Now add type hints and a docstring.", history)
    print(f"Coder (follow-up): {reply}")

    print()

    # 4. Register a new agent at runtime and use it
    print("=== Dynamic agent example ===")
    add_agent(
        key="haiku_poet",
        name="Haiku Poet",
        system_prompt="You only respond in haiku format (5-7-5 syllables).",
    )
    print("Agents after add_agent():")
    for agent in list_agents():
        print(f"  [{agent['key']}]  {agent['name']}")

    reply = ask_agent("haiku_poet", "Write a haiku about coding.")
    print(f"\nHaiku Poet: {reply}")
