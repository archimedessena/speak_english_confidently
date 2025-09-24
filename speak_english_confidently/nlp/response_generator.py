import openai
import os
class ResponseGenerator:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
    def generate_response(self, transcript, grammar_analysis, vocabulary_suggestions):
        try:
            prompt = f"""You are an English language coach. The student said: "{transcript}"
            Provide encouraging feedback and suggestions for improvement. Keep it friendly and helpful."""
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return "Great effort! Keep practicing your English speaking skills."
