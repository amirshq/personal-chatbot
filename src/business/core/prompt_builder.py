from typing import List
import yaml
from pathlib import Path

def _load_config() -> dict:
    """Load configuration from config.yml file."""
    # core/ -> business/ -> src/ -> config/config.yml
    config_path = Path(__file__).resolve().parents[2] / "config" / "config.yml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def _get_system_role() -> str:
    """Get LLM system role from config.yml."""
    config = _load_config()
    return config.get("llm_config", {}).get("llm_system_role", "You are a helpful assistant.")

class PromptBuilder:
    """
    Responsible for constructing prompts for the AI model.
    Sent to the LLM to generate responses based on user input and context in RAG pipeline.
    """

    def __init__(self, system_prompt: str = None):
        """
        Initialize PromptBuilder.

        Args:
            system_prompt: Custom system prompt. If None, uses llm_system_role from config.yml.
        """
        # Use config value if system_prompt not provided
        self.system_prompt = system_prompt or _get_system_role()

    def build_prompt_text(self, question: str, context: List[str]) -> str:
        """
        Constructs the full prompt (plain text) for completion-style models.
        """
        context_block = "\n\n".join(f"[Context {i+1}]: {ctx}" for i, ctx in enumerate(context))
        full_prompt = f"""
        {self.system_prompt}
        Use the following context to answer the question.
        {context_block}
        Question: {question}
        Rules:
        - Answer based only on the provided context.
        - If the answer is not in the context, respond with "I don't know."
        - Be concise and to the point.
        - Do not invent information.
        """
        return full_prompt.strip()

    def build_messages(self, question: str, context: List[str]):
        """
        Constructs chat messages for OpenAI Chat Completions API.
        """
        context_block = "\n\n".join(f"[Context {i+1}]: {ctx}" for i, ctx in enumerate(context))
        user_msg = (
            "Use the following context to answer the question.\n"
            f"{context_block}\n"
            f"Question: {question}\n"
            "Rules:\n"
            '- Answer based only on the provided context.\n'
            '- If the answer is not in the context, respond with "I don\'t know."\n'
            "- Be concise and to the point.\n"
            "- Do not invent information.\n"
        )
        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_msg},
        ]

    # Backwards compatibility
    def build_prompt(self, question: str, context: List[str]) -> str:
        return self.build_prompt_text(question, context)
        
