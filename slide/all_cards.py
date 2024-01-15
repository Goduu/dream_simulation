from classes.card import Card, CardAgent
from classes.backpack_item import Fish, FishType
from classes.card import CardPassiveTrigger, CardOnPlayReward


all_cards = [
    Card(
        short_name="BreakIceGainFish",
        cost=[(Fish(FishType.A), 1), (Fish(FishType.C), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When breaking an ice, get one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="BreakIceGainMove",
        cost=[(Fish(FishType.A), 2), (Fish(FishType.B), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.MOVEMENT: 1}},
        on_play_effects={},
        description="When breaking an ice, get one movement",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="GainFishOnCardPlay",
        cost=[(Fish(FishType.A), 2)],
        card_type="Fishing",
        passive_effect={CardPassiveTrigger.PLAY_CARD: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When playing a card to this penguin, get one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="BreakIceGainFishing",
        cost=[(Fish(FishType.C), 2)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When breaking an ice, get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="ChangeDirectionOnCollision",
        cost=[(Fish(FishType.C), 2)],
        card_type="Passive",
        passive_effect={
            CardPassiveTrigger.COLLIDE_PENGUIN: {CardOnPlayReward.MOVEMENT: 1}
        },
        on_play_effects={},
        description="When colliding with a penguin, change your penguin direction",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="LoseMoveGainIce",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.MOVEMENT: -1, CardOnPlayReward.ICE: 2}
        },
        description="Lose one movement to get two ice tokens",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="LoseIceGainFishing",
        cost=[(Fish(FishType.B), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.ICE: 2, CardOnPlayReward.FISHING: 1}
        },
        description="Lose two ice to get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="LoseMoveGainFishing",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.MOVEMENT: -1,
                CardOnPlayReward.FISHING: 1,
            }
        },
        description="Lose one movement to get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="LoseFishingGainMove",
        cost=[(Fish(FishType.B), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.FISHING: -1,
                CardOnPlayReward.MOVEMENT: 1,
            }
        },
        description="Lose one fishing to get one movement token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="ChangeDirection",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={},
        description="Change penguin direction",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="LoseIceGainFish",
        cost=[(Fish(FishType.A), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.ICE: -1, CardOnPlayReward.FISH: 1}
        },
        description="Lose one ice and get one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="IgnoreCollisionOnce",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={},
        description="You Ignore colliding once",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="PlaceIceOnPenguins",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.ALL: {CardOnPlayReward.ICE: 1}},
        description="Every player gets one ice token and needs to place it on one of its penguins",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="ChooseFishForYouAndOthers",
        cost=[(Fish(FishType.A), 2)],
        passive_effect={},
        card_type="Fishing",
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.FISH: 2},
            CardAgent.OTHERS: {CardOnPlayReward.FISH: 1},
        },
        description="Get two fish tokens of your choice, the other players get one of the same",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="DiscardFishForOthers",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.FISH: -1}},
        description="Every other player should discard a fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="GainMovesOnce",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.MOVEMENT: 2}},
        description="Get two movement tokens once",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="GainFishingOnce",
        cost=[(Fish(FishType.B), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.FISHING: 2}},
        description="Get two fishing tokens once",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="ExpandBackpack",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.BACKPACK: 2}},
        description="Expand its backpack slots by 2",
        points=1,
        quantity=1,
    ),
]


def get_all_cards():
    return all_cards
