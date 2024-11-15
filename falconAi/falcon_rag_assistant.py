from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import InferenceClient
import torch

class FalconRAGAssistant:
    def __init__(self, model_name: str = "tiiuae/falcon-7b-instruct", api_token: str = None, use_api: bool = False, retriever=None):
        """
        Initializes the FalconRAGAssistant class with RAG capabilities.

        :param model_name: The name of the model to use (default: Falcon 7B).
        :param api_token: Optional API token for Hugging Face Inference API.
        :param use_api: If True, use the Hugging Face Inference API; otherwise, run locally.
        :param retriever: A retrieval component (e.g., FAISS index or Elasticsearch client).
        """
        self.model_name = model_name
        self.use_api = use_api
        self.retriever = retriever
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        if self.use_api:
            if not api_token:
                raise ValueError("API token is required for using the Hugging Face Inference API.")
            self.client = InferenceClient(model=self.model_name, token=api_token)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16).to(self.device)

    def retrieve_context(self, query: str) -> str:
        """
        Retrieves relevant context from the knowledge base.

        :param query: The input query to search for relevant documents.
        :return: The retrieved context as a string.
        """
        if self.retriever:
            results = self.retriever.search(query)
            if results:
                return "\n".join([doc["content"] for doc in results])
        return ""

    def generate_response(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
        """
        Generates a response using the model, augmented with retrieved context.

        :param prompt: The input prompt for the model.
        :param max_tokens: The maximum number of tokens to generate.
        :param temperature: The sampling temperature for response variability.
        :return: The generated response as a string.
        """
        # Retrieve context from the knowledge base
        context = self.retrieve_context(prompt)
        if context:
            prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"

        if self.use_api:
            try:
                # Call the InferenceClient API
                response = self.client.text_generation(prompt, max_new_tokens=max_tokens, temperature=temperature)

                # Handle different response formats
                if isinstance(response, list):
                    # If response is a list, access the first element's 'generated_text'
                    return response[0].get('generated_text', "No response found")
                elif isinstance(response, dict):
                    # If response is a dictionary, check for 'text' key
                    return response.get('text', "No response found")
                else:
                    return "Unexpected response format"
            except Exception as e:
                return f"API Error: {str(e)}"
        else:
            try:
                inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
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
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16).to(self.device)

    def clear_cache(self):
        """
        Clears the GPU cache to free up memory.
        """
        torch.cuda.empty_cache()


if __name__ == "__main__":
    api_key = ""
    assistant = FalconRAGAssistant(model_name="tiiuae/falcon-7b-instruct", api_token=api_key, use_api=True)
    query = "Explain how ChaGu handles secure data transfer."
    response = assistant.generate_response(query)
    print("Chagu Assistant:", response)

