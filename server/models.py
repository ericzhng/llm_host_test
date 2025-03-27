
from transformers import AutoModelForCausalLM, AutoTokenizer

class LLMModel:
    def __init__(self, model_name: str = "gpt2"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.model.eval()
            # Set pad_token_id to eos_token_id if not already set (for GPT-2 compatibility)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def generate(self, text: str, max_length: int = 200) -> str:
        # Tokenize input with padding and attention mask
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]
        outputs = self.model.generate(
            inputs["input_ids"],
            attention_mask=attention_mask, 
            max_length=max_length, 
            num_return_sequences=1,
            pad_token_id=self.tokenizer.pad_token_id  # Explicitly set pad_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# Singleton instance
llm = LLMModel(model_name="gpt2")  # Change model_name to swap models
