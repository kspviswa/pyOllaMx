import ollama

res = ollama.chat(
	model="llava:7b",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['assets/icon.png']
		}
	]
)

print(res['message']['content'])