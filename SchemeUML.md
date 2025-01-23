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
    quistion_id: int
}

class UserDB{
    __users: list[User]
    get_quiz_index(self, user_index: int) -> None
    update_quiz_index(self, user_index: int, quest_index: int) -> None
}

class UI{
    start_quiz() -> None
    take_answere(self, options: dict) -> str
    print_card(self, question_number, question, options) -> None
}

class Quiz{
    
}

Deck o-- Card
UserDB o-- User

@enduml