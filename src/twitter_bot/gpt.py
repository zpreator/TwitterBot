from transformers import GPT2Tokenizer, GPT2LMHeadModel, AutoTokenizer, AutoModelForCausalLM
import torch

# tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
tokenizer = AutoTokenizer.from_pretrained('gpt2')
# model = GPT2LMHeadModel.from_pretrained('gpt2')
model = AutoModelForCausalLM.from_pretrained('gpt2')

# with open(r'C:\Users\zacha\PycharmProjects\TwitterBot\resources\datasets\laurarawra_archive2.txt', 'r', encoding="utf-8") as f:
#     text = f.read()
#
# def split_text(text, chunk_size):
#     return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

max_length = tokenizer.model_max_length

prompt = """
What is your name?
"""


input_ids = tokenizer.encode(prompt, return_tensors='pt', max_length=max_length, truncation=True)

outputs = []
for i in range(0, len(input_ids[0]), 50):
    input_chunk = input_ids[:, i:i+50]
    output_chunk = model(input_chunk)
    outputs.append(output_chunk[0])

output = torch.cat(outputs, dim=1)
print(tokenizer.decode(torch.argmax(output, dim=-1)[0]))