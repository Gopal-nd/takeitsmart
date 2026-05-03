from agents.summarizer import SummarizerAgent
from agents.sentiment import SentimentAgent
from agents.fact_checker import FactCheckerAgent

class Coordinator:
    def __init__(self):
        self.summarizer = SummarizerAgent()
        self.sentiment = SentimentAgent()
        self.fact_checker = FactCheckerAgent()

    def run_all(self, text):
        results = {}
        summary = self.summarizer.process(text)
        sentiment = self.sentiment.process(text)
        fact_check = self.fact_checker.process(text, context={"summary": summary})

        results[self.summarizer.name] = summary
        results[self.sentiment.name] = sentiment
        results[self.fact_checker.name] = fact_check

        return results