@startuml
class Card{
    question: str
    answer_options: str
    is_true_option(option: str)
}

class Deck{
    __cards: list[Card]
    get_card(index: int) -> Card
}

class User{
    id: int
    question_id: int
}

class UserDB{
    __users: list[User]
    get_quiz_index(self, user_index: int) -> None
    update_quiz_index(self, user_index: int, quest_index: int) -> None
}

class UI{
    greet() -> None
    ask_question(question: str) -> None
    suggest_answers(options: list[str]) -> None
    get_answer(options: list[str]) -> str
}

class QuizApp{
    start_main_loop() -> None
}

Deck o-- Card
UserDB o-- User

QuizApp ..> Deck
QuizApp ..> UserDB
QuizApp ..> UI
QuizApp ..> Card
QuizApp ..> User
@enduml