import os

from openAIAPI.open_aiapi import GenAIAPI


def test_genai_api():
    print(os.environ)
    api_key = os.getenv("GENAI_API_KEY", "")
    base_url = os.getenv("GENAI_BASE_URL", "https://api.genai.com")
    genai = GenAIAPI(api_key, base_url)

    # Test data transformation
    transformed = genai.transform_data("Testing the improved API class", task="summarize")
    assert transformed is not None, "Transformation failed"
    print("Transformed Data:", transformed)

    # Test embeddings generation
    embeddings = genai.generate_embeddings("Testing embeddings")
    assert embeddings, "Embeddings generation failed"
    print("Embeddings:", embeddings)

    # Test classification
    classification = genai.classify_data("Classify this text", labels=["Label1", "Label2"])
    assert classification is not None, "Classification failed"
    print("Classification:", classification)

if __name__ == "__main__":
    test_genai_api()
