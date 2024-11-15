from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import InferenceClient
import torch

class FalconAssistant:
    def __init__(self, model_name: str = "tiiuae/falcon-180b", api_token: str = None, use_api: bool = False, retriever = None):
        """
        Initializes the FalconAssistant class.

        :param model_name: The name of the model to use (default: Falcon 180B).
        :param api_token: Optional API token for Hugging Face Inference API.
        :param use_api: If True, use the Hugging Face Inference API; otherwise, run locally.
        """
        self.model_name = model_name
        self.use_api = use_api
        self.retriever = retriever
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.use_api:
            if not api_token:
                raise ValueError("API token is required for using the Hugging Face Inference API.")
            # Use InferenceClient instead of InferenceApi
            self.client = InferenceClient(model=self.model_name, token=api_token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16).cuda()

    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """
        Generates a response from the model based on the provided prompt.

        :param prompt: The input prompt for the model.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The sampling temperature for response variability.
        :return: The generated response as a string.
        """
        if self.use_api:
            # Use InferenceClient API call
            try:
                response = self.client.text_generation(prompt, max_new_tokens=max_tokens, temperature=temperature)
                return response
            except Exception as e:
                return f"API Error: {str(e)}"
        else:
            # Use local model
            try:
                inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
                outputs = self.model.generate(**inputs, max_new_tokens=max_tokens, temperature=temperature)
                response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                return response
            except Exception as e:
                return f"Local Model Error: {str(e)}"

    def set_model(self, model_name: str):
        """
        Updates the model being used.
        """
        self.model_name = model_name
        if not self.use_api:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16).cuda()

    def clear_cache(self):
        """
        Clears the GPU cache to free up memory.
        """
        torch.cuda.empty_cache()


if __name__ == "__main__":
    api_key = ""
    assistant = FalconAssistant(model_name="tiiuae/falcon-7b-instruct", api_token=api_key, use_api=True)
    response = assistant.generate_response("Explain how Chagu handles secure data transfer here : https://github.com/taimax13/Chagu")
    print("Falcon:" , response)