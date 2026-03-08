from crewai import Agent, Task, Crew, Process

agent1 = Agent(role="A1", goal="Say hi", backstory="say hi",
               llm="gpt-3.5-turbo") # don't actually need real LLM to check structure
task1 = Task(description="Say hi", agent=agent1, expected_output="hi")

crew1 = Crew(agents=[agent1], tasks=[task1])
print("crew1 setup ok")

agent2 = Agent(role="A2", goal="Say bye", backstory="say bye")
task1_new = Task(description="Say hi", agent=agent1, expected_output="hi")
task2 = Task(description="Say bye", agent=agent2, expected_output="bye", context=[task1_new])

crew2 = Crew(agents=[agent2], tasks=[task2])
print("crew2 setup ok, task2 context:", task2.context)
