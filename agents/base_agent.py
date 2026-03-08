"""Base agent class with common functionality."""

from openai import OpenAI
import os


class BaseAgent:
    """Base class for all AI agents."""
    
    def __init__(self, role: str, model: str = "gpt-4o-mini"):
        self.role = role
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def execute(self, prompt: str, context: dict = None) -> str:
        """Execute the agent's task with given prompt and context."""
        system_prompt = self._get_system_prompt()
        user_message = self._build_user_message(prompt, context)
        
        print(f"🤖 {self.role} is working...")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        print(f"✓ {self.role} completed\n")
        
        return result
    
    def _get_system_prompt(self) -> str:
        """Override in subclasses to define agent-specific behavior."""
        raise NotImplementedError
    
    def _build_user_message(self, prompt: str, context: dict = None) -> str:
        """Build the user message with context."""
        message = prompt
        
        if context:
            message += "\n\n## Context from Previous Agents:\n"
            for key, value in context.items():
                if value:
                    message += f"\n### {key}:\n{value}\n"
        
        return message
