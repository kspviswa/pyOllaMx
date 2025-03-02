from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Phi-4-mini-instruct-8bit")

prompt="Hi how are you?"

if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template is not None:
    messages = [{"role": "user", "content": prompt}]
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

response = generate(model, tokenizer, prompt=prompt, verbose=True)
print(response)
