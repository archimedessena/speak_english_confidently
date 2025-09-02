class DialogManager:
    def __init__(self):
        self.conversation_topics = [
            "Daily routine", "Hobbies", "Travel", "Food", "Work", "Family"
        ]
    def get_topic_suggestion(self):
        import random
        return random.choice(self.conversation_topics)
