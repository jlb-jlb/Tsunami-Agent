from litellm import completion, embedding

def generate_text(prompt: str, model: str = "llama3.1") -> str:
    response = completion(
            model="ollama/llama3.1",
            messages = [{ "content": prompt, "role": "user"}],
            api_base="http://gpu1.mlsec.de:11434"
    )
    return response


def embed_text(text: str, model: str = "llama3.1") -> list[float]:
    response = embedding(model="ollama/llama3.1", input=[text], api_base="http://gpu1.mlsec.de:11434")
    return response


if __name__ == "__main__":
    # example for:
    # curl http://gpu1.mlsec.de:11434/api/generate -d '{ "model": "llama3.1", "prompt": "Hello, how are you?"}'
    print(generate_text("How are you today?"))
    print(embed_text("How are you today?"))
