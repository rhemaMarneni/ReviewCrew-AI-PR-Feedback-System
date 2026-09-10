from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ReviewCrew():
    """ReviewCrew crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def frontend_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_reviewer'],
            verbose=True
        )

    @agent
    def backend_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_reviewer'],
            verbose=True
        )

    @agent
    def security_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['security_reviewer'],
            verbose=True
        )

    @agent
    def test_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_reviewer'],
            verbose=True
        )

    @agent
    def lead_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_reviewer'],
            verbose=True
        )

    @task
    def frontend_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_review_task'],
            verbose=True
        )

    @task
    def backend_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_review_task'],
            verbose=True,
            output_file='output/backend_review.md'
        )

    @task
    def security_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_review_task'],
            verbose=True,
            output_file='output/security_review.md'
        )

    @task
    def test_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_review_task'],
            verbose=True,
            output_file='output/test_review.md'
        )

    @task
    def lead_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_review_task'],
                verbose=True,
            output_file='output/lead_review.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ReviewCrew crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,
        )
