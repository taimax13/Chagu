import requests
import json
import os
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GenAIAPI:
    """
    GenAIAPI class for integrating Generative AI capabilities into the Chagu project.
    This class handles API calls and processes responses for data transformation.
    """

    def __init__(self, api_key: str, base_url: str, timeout: int = 10, retries: int = 3, verify_ssl: bool = True, proxies: dict = None):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.proxies = proxies

        # Set up session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _request(self, method: str, endpoint: str, payload: dict):
        """
        Helper function to make an API request.

        Args:
            method (str): HTTP method (e.g., 'POST').
            endpoint (str): API endpoint.
            payload (dict): Request payload.

        Returns:
            dict: JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug(f"Request URL: {url}")
            logger.debug(f"Request Payload: {json.dumps(payload, indent=2)}")

            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                verify=self.verify_ssl,
                proxies=self.proxies
            )
            response.raise_for_status()
            result = response.json()
            logger.debug(f"Response: {json.dumps(result, indent=2)}")
            return result
        except requests.RequestException as e:
            logger.error(f"Error calling GenAI API: {e}")
            return {"error": str(e)}

    def generate_text(self, prompt: str, max_tokens: int = 150, temperature: float = 0.7,
                      model: str = "text-davinci-003"):
        """
        Sends a prompt to the Generative AI API and retrieves the generated text response.

        Args:
            prompt (str): Input text prompt for the model.
            max_tokens (int): Maximum number of tokens in the response.
            temperature (float): Sampling temperature for response creativity.
            model (str): Model name (default is 'text-davinci-003').

        Returns:
            str: The generated text response from the API.
        """
        endpoint = f"{self.base_url}/v1/completions"
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = self.session.post(endpoint, headers=self.headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result.get("choices", [{}])[0].get("text", "").strip()
        except requests.RequestException as e:
            logger.error(f"Error calling GenAI API: {e}")
            return {"error": str(e)}

    def transform_data(self, data: str, task: str = "summarize"):
        """
        Transforms input data using the Generative AI API based on the specified task.

        Args:
            data (str): The input data to be transformed.
            task (str): The type of task to perform (e.g., "summarize", "analyze", "translate").

        Returns:
            str: Transformed data or a processed response from the API.
        """
        prompt = f"Perform the following task: {task} on the data: {data}"
        return self.generate_text(prompt)

    def generate_embeddings(self, text: str):
        """
        Retrieves embeddings for the input text using the Generative AI API.

        Args:
            text (str): Input text for which embeddings are generated.

        Returns:
            List[float]: A list of embeddings (vector representation of the text).
        """
        payload = {"input": text}
        result = self._request("POST", "/v1/embeddings", payload)
        return result.get("data", [{}])[0].get("embedding", [])

    def classify_data(self, text: str, labels: list):
        """
        Classifies the input text based on the provided labels using the Generative AI API.

        Args:
            text (str): Input text to classify.
            labels (list): List of labels to use for classification.

        Returns:
            str: The label assigned to the input text.
        """
        prompt = f"Classify the following text: '{text}' into one of these labels: {', '.join(labels)}"
        return self.generate_text(prompt)



if __name__ == "__main__":
    api_key = ""
    base_url = os.getenv("GENAI_BASE_URL", "https://api.openai.com")

    genai = GenAIAPI(api_key, base_url, retries=5, verify_ssl=True)

    # Test generate_text
    response = genai.generate_text("What is the capital of France?", max_tokens=50)
    print("Generated Text:", response)

    # Test transform_data
    summary = genai.transform_data("This is a long text that needs summarizing.", task="summarize")
    print("Summary:", summary)

    # Test generate_embeddings
    embeddings = genai.generate_embeddings("Artificial Intelligence is transforming the world.")
    print("Embeddings:", embeddings)

    # Test classify_data
    classification = genai.classify_data("This is a positive review.", labels=["Positive", "Negative", "Neutral"])
    print("Classification:", classification)
