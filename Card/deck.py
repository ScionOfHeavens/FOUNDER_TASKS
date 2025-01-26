from Card.card import Card

class Deck:
    __cards: dict[int, Card]
    def __init__(self):
        db = [
            {
                'question': 'Что такое Python?',
                'false_options': ['Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
                'true_option': 'Язык программирования'
            },
            {
                'question': 'Какой тип данных используется для хранения целых чисел?',
                'false_options': ['float', 'str', 'natural'],
                'true_option': 'int'
            },
        ]
        self.__cards = {i: Card(i,e) for i,e in zip(range(1, len(db)+1), db)}

    async def get_card(self, index: int) -> Card:
        return self.__cards[index]
    async def is_finish_card(self, card: Card) -> bool:
        return card.id == len(self.__cards)