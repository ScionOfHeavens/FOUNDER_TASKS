import json
from Card.card import Card

class Deck:
    __cards: dict[int, Card]

    def __init__(self):
        data: str
        with open(r"Card\deck.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        self.__cards = {i+1: Card(i+1,**e) for i,e in enumerate(data)}

    async def get_first_card(self) -> Card:
        return await self.get_card(1)

    async def get_next(self, card: Card) -> Card:
        if not await self.is_finish_card(card):
            return await self.get_card(card.id + 1)
        else:
            return await self.get_first_card()

    async def get_card(self, index: int) -> Card:
        return self.__cards.get(index)
    
    async def is_finish_card(self, card: Card) -> bool:
        return card.id == len(self.__cards)
    
    async def questions_amount(self) -> int:
        return len(self.__cards)