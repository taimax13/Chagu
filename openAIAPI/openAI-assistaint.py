import openai
from typing import List, Dict, Union

class OpenAIAssistant:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo-0125"):
        """
        Initializes the OpenAIAssistant with API key and model configuration.
        """
        self.api_key = api_key
        self.model = model
        self.history = []  # To maintain conversation history
        openai.api_key = self.api_key

    def send_message(self, message: str, user_id: str = "user") -> Dict:
        """
        Sends a message to the OpenAI model and retrieves the response.
        """
        self.history.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history,
                max_tokens=2000,
                temperature=0.7,
                user=user_id
            )
            # Extract the response content
            reply = response["choices"][0]["message"]["content"]
            # Append assistant's reply to the history
            self.history.append({"role": "assistant", "content": reply})
            return {"status": "success", "response": reply}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def stream_message(self, message: str, user_id: str = "user") -> str:
        """
        Sends a message with streaming enabled for real-time responses.
        """
        self.history.append({"role": "user", "content": message})
        try:
            stream = openai.ChatCompletion.create(
                model=self.model,
                messages=self.history,
                max_tokens=2000,
                temperature=0.7,
                user=user_id,
                stream=True
            )
            reply = ""
            for chunk in stream:
                if "choices" in chunk and "delta" in chunk["choices"][0]:
                    content = chunk["choices"][0]["delta"].get("content", "")
                    reply += content
                    print(content, end="", flush=True)  # Real-time print
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self) -> List[Dict[str, str]]:
        """
        Returns the conversation history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.history = []

    def set_model(self, model: str):
        """
        Updates the model being used for the chat.
        """
        self.model = model

    def set_temperature(self, temperature: float):
        """
        Adjusts the temperature for response variability.
        """
        self.temperature = temperature


if __name__ == "__main__":
    api_key = ""
    assistant = OpenAIAssistant(api_key)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        response = assistant.send_message(user_input)
        if response["status"] == "success":
            print(f"Assistant: {response['response']}")
        else:
            print(f"Error: {response['error']}")
