"""core logic for JARVIS."""

import json
from typing import Any

import requests
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
)


def search_wikipedia(query: str) -> Any:
    """Выполняет поиск по Википедии и возвращает краткое содержание статьи."""
    try:
        print("Start use this item")
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": 1,
            },
        )
        data = response.json()

        if not data["query"]["search"]:
            return f"No article found for '{query}'."

        title = data["query"]["search"][0]["title"]

        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "titles": title,
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
            },
        )
        data = response.json()

        page_id = list(data["query"]["pages"].keys())[0]
        content = data["query"]["pages"][page_id]["extract"]
        print(content)
        return f"Wikipedia article for '{title}':\n{content}"

    except Exception as e:
        return f"An error occurred: {e}"


WIKI_TOOL: ChatCompletionFunctionToolParam = {
    "type": "function",
    "function": {
        "name": "search_wikipedia",
        "description": "Search Wikipedia and fetch the introduction. You MUST use English for the search query, as the Wikipedia API returns more accurate results for English queries.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for the Wikipedia article.",
                },
            },
            "required": ["query"],
        },
    },
}


class Core:
    """Main class for Jarvis."""

    def __init__(self) -> None:
        self.client = OpenAI(
            base_url="http://localhost:1234/v1", api_key="Not"
        )
        self.messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the 'search_wikipedia' tool to answer factual questions.",
            },
        ]

    def cli(self, text: str) -> None:
        """CLI for Jarvis."""
        self.llm(text)

    def stt(self, text: str) -> None:
        """Speech to text for Jarvis."""
        self.llm(text)

    def llm(self, request: str) -> None:
        """Language model for Jarvis."""
        print(f"You: {request}")
        self.messages.append({"role": "user", "content": request})

        try:
            response = self.client.chat.completions.create(
                model="mistralai/devstral-small-2507",  # Replace with a tool-enabled model
                messages=self.messages,
                tools=[WIKI_TOOL],
                tool_choice="auto",
            )

            # Check for tool calls first
            if response.choices[0].message.tool_calls:
                tool_calls = response.choices[0].message.tool_calls
                print("Assistant: Processing tool calls...")

                # Add the assistant's message with tool calls to history
                self.messages.append(response.choices[0].message.model_dump())

                tool_outputs: list[ChatCompletionToolMessageParam] = []

                for tool_call in tool_calls:
                    # Check the tool type before accessing the function attribute
                    if tool_call.type == "function":
                        function_name = tool_call.function.name
                        arguments = json.loads(tool_call.function.arguments)

                        print(
                            f"  - Calling '{function_name}' with query: '{arguments.get('query', 'N/A')}'"
                        )

                        result = search_wikipedia(query=arguments["query"])

                        tool_outputs.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "content": result,
                            }
                        )

                print("Sending results back to the model...")
                self.messages.extend(tool_outputs)

                final_response = self.client.chat.completions.create(
                    model="mistralai/devstral-small-2507",  # Use the same model
                    messages=self.messages,
                )

                print(
                    "\nAssistant:", final_response.choices[0].message.content
                )
                self.messages.append(
                    final_response.choices[0].message.model_dump()
                )
            elif "[TOOL_CALLS]" in response.choices[0].message.content:
                print(
                    "Assistant: Processing custom tool calls from content..."
                )

                # Извлекаем имя функции и аргументы
                content = response.choices[0].message.content
                match = re.search(r"\[TOOL_CALLS\](.*?)\[ARGS\](.*)", content)

                if match:
                    function_name = match.group(1)
                    arguments_str = match.group(2)

                    try:
                        arguments = json.loads(arguments_str)
                        print(
                            f"  - Calling '{function_name}' with arguments: {arguments}"
                        )

                        # Вызываем функцию по имени, используя if/elif или словарь
                        if function_name == "search_wikipedia":
                            result = search_wikipedia(
                                query=arguments["query"]
                            )  # Убедитесь, что ключ "query" верен
                            tool_outputs = [
                                {
                                    "tool_call_id": "custom-id-123",  # Используйте уникальный ID
                                    "role": "tool",
                                    "content": result,
                                }
                            ]

                            self.messages.append(
                                {"role": "assistant", "content": content}
                            )
                            self.messages.extend(tool_outputs)

                            # Повторный запрос к модели
                            final_response = (
                                self.client.chat.completions.create(
                                    model="openai/gpt-oss-20b",
                                    messages=self.messages,
                                )
                            )
                            print(
                                "\nAssistant:",
                                final_response.choices[0].message.content,
                            )
                            self.messages.append(
                                final_response.choices[0].message.model_dump()
                            )

                        else:
                            print(f"Unknown tool: {function_name}")
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error parsing tool call: {e}")
                    else:
                        # Normal text response
                        print(
                            "Assistant: \n\n",
                            response.choices[0].message.content,
                        )
                        self.messages.append(
                            response.choices[0].message.model_dump()
                        )

        except Exception as e:
            print(f"An error occurred with the LLM call: {e}")

        print("\n--- Current Message History ---")
        print(json.dumps(self.messages, indent=2))
        print("-------------------------------")


core = Core()
