from classes.card import Card, CardAgent
from classes.backpack_item import Fish, FishType
from classes.card import CardPassiveTrigger, CardOnPlayReward


all_cards = [
    Card(
        short_name="[PA]DropIceGainFish",
        cost=[(Fish(FishType.B), 2), (Fish(FishType.C), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.DROP_ICE: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When dropping an ice, get one fish token from where you stand",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]BreakIceGainFish",
        cost=[(Fish(FishType.A), 1), (Fish(FishType.C), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When breaking an ice, get one fish token from where you stand",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]BreakIceGainFish",
        cost=[(Fish(FishType.A), 1), (Fish(FishType.C), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.FISH: 2}},
        on_play_effects={},
        description="When breaking an ice, get 2 fish tokens",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]BreakIceGainMove",
        cost=[(Fish(FishType.A), 2), (Fish(FishType.B), 1)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.MOVEMENT: 1}},
        on_play_effects={},
        description="When breaking an ice, get one movement",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]GainFishOnCardPlay",
        cost=[(Fish(FishType.A), 2)],
        card_type="Fishing",
        passive_effect={CardPassiveTrigger.PLAY_CARD: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When playing a card, this penguin gets one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]BreakIceGainFishing",
        cost=[(Fish(FishType.C), 2)],
        card_type="Passive",
        passive_effect={CardPassiveTrigger.BREAK_ICE: {CardOnPlayReward.FISH: 1}},
        on_play_effects={},
        description="When breaking an ice, get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]ChangeDirectionOnCollision",
        cost=[(Fish(FishType.C), 2)],
        card_type="Passive",
        passive_effect={
            CardPassiveTrigger.COLLIDE_PENGUIN: {CardOnPlayReward.FISH: 1}
        },
        on_play_effects={},
        description="When colliding with a penguin, gain one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[PA]ChangeDirectionOnCollision",
        cost=[(Fish(FishType.C), 2)],
        card_type="Passive",
        passive_effect={
            CardPassiveTrigger.COLLIDE_PENGUIN: {CardOnPlayReward.MOVEMENT: 1}
        },
        on_play_effects={},
        description="When colliding with a penguin, gain one movement",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]DiscardMoveGainIce",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.MOVEMENT: -1, CardOnPlayReward.ICE: 2}
        },
        description="Discard one movement to get two ice tokens",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard2IceGain1Fishing",
        cost=[(Fish(FishType.B), 2),(Fish(FishType.A), 1),(Fish(FishType.C), 1)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.ICE: 2, CardOnPlayReward.FISHING: 1}
        },
        description="Discard two ice to get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard1MoveGain2Fishing",
        cost=[(Fish(FishType.A), 2),(Fish(FishType.C), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.MOVEMENT: -1,
                CardOnPlayReward.FISHING: 2,
            }
        },
        description="Discard one movement to get 2 fishing tokens",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard1FishingGain2Move",
        cost=[(Fish(FishType.B), 2),(Fish(FishType.C), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.FISHING: -1,
                CardOnPlayReward.MOVEMENT: 2,
            }
        },
        description="Discard one fishing to get 2 movement tokens",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard1MoveGain1Fishing",
        cost=[(Fish(FishType.A), 2)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.MOVEMENT: -1,
                CardOnPlayReward.FISHING: 1,
            }
        },
        description="Discard one movement to get one fishing token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard1FishingGain1Move",
        cost=[(Fish(FishType.B), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {
                CardOnPlayReward.FISHING: -1,
                CardOnPlayReward.MOVEMENT: 1,
            }
        },
        description="Discard one fishing to get one movement token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Discard1IceGain1Fish",
        cost=[(Fish(FishType.A), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.ICE: -1, CardOnPlayReward.FISH: 1}
        },
        description="Discard one ice and get one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]PlaceIceOnPenguins",
        cost=[(Fish(FishType.B), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.ALL: {CardOnPlayReward.ICE: 1}},
        description="Every player chooses a penguin to get one ice token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]PlaceIceOnPenguins",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.ICE: 1}},
        description="Choose one of your penguins to get one ice token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Choose2FishForYouAnd1ForOthers",
        cost=[(Fish(FishType.C), 2)],
        passive_effect={},
        card_type="Fishing",
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.FISH: 2},
            CardAgent.OTHERS: {CardOnPlayReward.FISH: 1},
        },
        description="Choose one of your penguins and get two fish tokens \
            from a hexagon where it is, the other players do the same and \
            get one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Choose3FishForYouAnd2ForOthers",
        cost=[(Fish(FishType.A), 2),(Fish(FishType.B), 1)],
        passive_effect={},
        card_type="Fishing",
        on_play_effects={
            CardAgent.YOURSELF: {CardOnPlayReward.FISH: 3},
            CardAgent.OTHERS: {CardOnPlayReward.FISH: 2},
        },
        description="Choose one of your penguins and get 3 fish tokens \
            from a hexagon where it is, the other players do the same and \
            get 2 fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]DiscardFishForOthers",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.OTHERS: {CardOnPlayReward.FISH: -1}},
        description="Every other player should discard one fish token",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Gain2Moves",
        cost=[(Fish(FishType.A), 2),(Fish(FishType.C), 1)],
        card_type="Movement",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.MOVEMENT: 2}},
        description="One of your penguins get two movement tokens once",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Gain2Fishing",
        cost=[(Fish(FishType.A), 1),(Fish(FishType.B), 2)],
        card_type="Fishing",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.FISHING: 2}},
        description="One of your penguins get two fishing tokens once.",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Expand2Backpack",
        cost=[(Fish(FishType.A), 1),(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.BACKPACK: 2}},
        description="Expand a penguin's backpack slots by 2",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Expand1Backpack",
        cost=[(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.BACKPACK: 1}},
        description="Expand a penguin's backpack slots by 1",
        points=1,
        quantity=1,
    ),
    Card(
        short_name="[OP]Expand1Backpack",
        cost=[(Fish(FishType.A), 1),(Fish(FishType.B), 1),(Fish(FishType.C), 2)],
        card_type="Special",
        passive_effect={},
        on_play_effects={CardAgent.YOURSELF: {CardOnPlayReward.BACKPACK: 3}},
        description="Expand a penguin's backpack slots by 3",
        points=1,
        quantity=1,
    ),
]


def get_all_cards():
    return all_cards
