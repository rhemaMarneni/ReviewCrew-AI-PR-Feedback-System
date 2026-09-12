import gradio as gr
from dotenv import load_dotenv

load_dotenv()

from review_crew.main import run

class ReviewCrewApp:
    def __init__(self):
        self.app = gr.Interface(
            fn=self.review_crew,
            inputs=[
                gr.Textbox(
                    lines=1,
                    placeholder="ReviewCrew",
                    label="Enter Project Name",
                ),
                gr.Textbox(
                    lines=1,
                    placeholder="https://github.com/owner/repository/pull/123",
                    label="GitHub Pull Request URL",
                ),
                gr.Textbox(
                    lines=5,
                    placeholder="The project is a web application that allows users to review code...",
                    label="Give a small Project description for which this review is being done.",
                ),
            ],
            outputs=gr.Markdown(),
            title="ReviewCrew",
            description="Enter a GitHub Pull Request URL to run an AI-assisted code review.",
        )

    def review_crew(self, project_name: str, pr_url: str, project_description: str):
        result = run(pr_url, project_name, project_description)
        return result.raw

    def launch(self):
        self.app.launch()


if __name__ == "__main__":
    ReviewCrewApp().launch()
