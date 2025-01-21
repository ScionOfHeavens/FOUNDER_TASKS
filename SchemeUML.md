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

class Quiz{
    
}

Deck o-- Card

@enduml