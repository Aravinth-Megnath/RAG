from services.agent import AgentService

agent = AgentService()

response =agent.run(
    "Book a Deluxe room from September 25, 2026 "
    "to September 27, 2026. "
    "My name is Aravinth and my email is "
    "aravinth.recruiting@gmail.com."
)
print(response)