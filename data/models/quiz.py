from typing import List


class Quiz:
    type: str = "quiz"

    def __init__(self, question, options, correct_option_id):
        self.question: str = question
        self.options: List[str] = [*options]
        self.correct_option_id: int = correct_option_id

    def __str__(self):
        return f"{self.question} {self.options}"
