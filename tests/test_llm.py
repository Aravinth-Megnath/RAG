from services.llm import LLM

llm = LLM.load()

response = llm.invoke("Who are you?")

print(response.content)