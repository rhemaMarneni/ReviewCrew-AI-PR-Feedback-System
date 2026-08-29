import gradio as gr
from dotenv import load_dotenv

class ReviewCrewApp:
    def __init__(self):
        self.app = gr.Interface(
            fn=self.review_crew,
            inputs=[
                gr.Textbox(
                    lines=1,
                    placeholder="https://github.com/owner/repository/pull/123",
                    label="GitHub Pull Request URL",
                ),
            ],
            outputs=gr.Markdown(),
            title="ReviewCrew",
            description="Enter a GitHub Pull Request URL to run an AI-assisted code review.",
        )

    def review_crew(self, pr_url: str, auth_token: str):
        return f"Review requested for: {pr_url}"

    def launch(self):
        self.app.launch()


if __name__ == "__main__":
    load_dotenv()
    ReviewCrewApp().launch()
