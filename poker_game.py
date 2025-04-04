import random
from typing import List, Tuple


def create_deck() -> List[str]:
    """
    Creates and returns a full deck of 52 cards as a list of strings.

    Each card has a value (2-Ace) and a suit (Karo, Kier, Pik, Trefl).
    """
    colors = ["Karo", "Kier", "Pik", "Trefl"]
    values = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "As",
    ]
    deck = [f"{v} {c}" for v in values for c in colors]
    return deck


def deal_cards(
    deck: List[str], num_players: int, cards_per_players=5
) -> List[List[str]]:
    """
    Deals a specific number of cards to each player from the shuffled deck.

    Args:
        deck: A list of cards representing the deck.
        num_players: Number of players in the game.
        cards_per_player: Number of cards per player (default is 5).

    Returns:
        A list of hands, where each hand is a list of cards.
    """
    random.shuffle(deck)
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_players):
        for i in range(num_players):
            hands[i].append(deck.pop())
    return hands


def display_hands(hands: List[List[str]]):
    """
    Displays the cards of each player in the console.

    Args:
        hands: A list of hands, where each hand is a list of cards.
    """
    for i, hand in enumerate(hands, start=1):
        print(f"Player {i} hand: {', '.join(hand)}")


def evaluate_hands(hand: List[str]) -> Tuple[str, int]:
    """
    Evaluates a player's hand and determines its poker ranking.

    Args:
        hand: A list of 5 cards in the format "value suit".

    Returns:
        A tuple containing the name of the poker hand (e.g., "Pair") and its strength (e.g., 2).
    """
    value_order = {str(n): n for n in range(2, 11)}
    value_order.update({"Jack": 11, "Queen": 12, "King": 13, "As": 14})
    hand_values = []
    hand_colors = []

    for card in hand:
        value, color = card.split()
        hand_values.append(value_order[value])
        hand_colors.append(color)

    hand_values.sort()

    is_flush = len(set(hand_colors)) == 1

    is_straight = hand_values == list(
        range(hand_values[0], hand_values[0] + len(hand_values))
    )

    counts = {}
    for v in hand_values:
        counts[v] = counts.get(v, 0) + 1
    count_values = sorted(counts.values(), reverse=True)

    if is_flush and is_straight:
        return ("Poker", 9)
    if count_values[0] == 4:
        return ("Four of a Kind", 8)
    if count_values[0] == 3 and count_values[1] == 2:
        return ("Full House", 7)
    if is_flush:
        return ("Flush", 6)
    if is_straight:
        return ("Straight", 5)
    if count_values[0] == 3:
        return ("Three of a Kind", 4)
    if count_values[0] == 2 and count_values[1] == 2:
        return ("Two Pair", 3)
    if count_values[0] == 2:
        return ("One Pair", 2)
    return ("High Card", 1)

    # Poker          – Poker
    # Four of a Kind – Kareta
    # Full House     – Full
    # Flush          – Kolor
    # Straight       – Strit
    # Three of a Kind– Trójka
    # Two Pair       – Dwie pary
    # One Pair       – Para
    # High Card      – Wysoka karta


def announce_winner(hands: List[List[str]]) -> None:
    """
    Evaluates all hands and announces the winner based on the strongest hand.

    Args:
        hands: A list of player hands, where each hand is a list of 5 cards.
    """
    evaluations = []

    for i, hand in enumerate(hands, start=1):
        hand_name, strength = evaluate_hands(hand)
        evaluations.append((i, hand_name, strength))
    evaluations.sort(key=lambda x: x[2], reverse=True)
    for eval in evaluations:
        print(f"Player {eval[0]}: {eval[1]}")
    print(f"\nWinner: Player {evaluations[0][0]} with the hand: {evaluations[0][1]}")


def test_game() -> None:
    """
    Runs a full test game: creates a deck, deals cards, shows hands, and announces a winner.
    """
    deck = create_deck()
    num_players = 4
    hands = deal_cards(deck, num_players)
    display_hands(hands)
    announce_winner(hands)


if __name__ == "__main__":
    test_game()
