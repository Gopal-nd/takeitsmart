from transformers import pipeline
from .base_agent import BaseAgent

class SummarizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Summarizer")
        self.summarizer = pipeline("summarization")

    def process(self, text, context=None):
        return self.summarizer(text, max_length=100, min_length=30, do_sample=False)[0]['summary_text']