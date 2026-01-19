from gpt4all import GPT4All

# Load once (this may take a few seconds)
model = GPT4All("gpt4all-j-v1.3-groovy.ggml")  # path to your downloaded file

# Now you can generate multiple prompts without reloading
prompt1 = "Write a Python function to reverse a string"
print(model.generate(prompt1))

prompt2 = "Explain LangChain in simple words"
print(model.generate(prompt2))
