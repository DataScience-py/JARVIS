"""core logic for JARVIS."""

import requests

class Core:
    """Main class for Jarvis."""

    def cli(self, text: str) -> None:
        """CLI for Jarvis."""
        print(text)

    def stt(self, text: str) -> None:
        """Speech to text for Jarvis."""
        print(text)
        self.llm("What is your name?")

    def llm(self, request: str) -> None:
        """Language model for Jarvis."""
        response = requests.post(
            url="http://localhost:1234/v1/chat/completions",
            json={
                "model": "deepseek/deepseek-r1-0528-qwen3-8b",
                "messages": [
                { "role": "system", "content": "Always answer in rhymes. \
                 Today is Thursday" },
                { "role": "user", "content": request }
                ],}
        )

        print(response.json()["choices"][0]["message"]["content"])

core = Core()
