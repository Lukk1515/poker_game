import random
from typing import List, Tuple


def create_deck() -> list[str]:
    """
    Creates and returns a full deck of 52 playing cards.

    Each card has a value (2 through Ace) and a suit (Diamonds, Hearts, Spades, Clubs).

    Returns:
        A list of 52 card strings in the format "value suit".
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
    deck: list[str], num_players: int, cards_per_players=5
) -> list[list[str]]:
    """
    Shuffles the deck and deals a given number of cards to each player.

    Args:
        deck: A list of cards representing the deck.
        num_players: The number of players in the game.
        cards_per_players: The number of cards to deal to each player (default is 5).

    Returns:
        A list of hands, where each hand is a list of cards for one player.
    """
    random.shuffle(deck)
    hands = [[] for _ in range(num_players)]
    for _ in range(cards_per_players):
        for i in range(num_players):
            hands[i].append(deck.pop())
    return hands


def display_hands(hands: list[list[str]]):
    """
    Displays each player's hand in the console.

    Args:
        hands: A list of hands, where each hand is a list of card strings.
    """
    for i, hand in enumerate(hands, start=1):
        print(f"Player {i} hand: {', '.join(hand)}")


def evaluate_hands(hand: list[str]) -> tuple[str, int]:
    """
    Evaluates a player's hand and determines its poker ranking.

    Args:
        hand: A list of 5 cards, each in the format "value suit".

    Returns:
        A tuple containing:
            - The name of the poker hand (e.g., "One Pair", "Flush").
            - An integer representing the strength of the hand (1 = High Card, 9 = Straight Flush).
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


def announce_winner(hands: list[list[str]]) -> None:
    """
    Evaluates all players' hands and announces the winner based on hand strength.

    In case of a tie, it lists all players with the top-ranked hand.

    Args:
        hands: A list of hands, where each hand is a list of 5 cards.
    """
    evaluations = []

    for i, hand in enumerate(hands, start=1):
        hand_name, strength = evaluate_hands(hand)
        evaluations.append((i, hand_name, strength))
    evaluations.sort(key=lambda x: x[2], reverse=True)
    for eval in evaluations:
        print(f"Player {eval[0]}: {eval[1]} (Strength: {eval[2]})")

    top_strength = evaluations[0][2]
    winners = [eval for eval in evaluations if eval[2] == top_strength]

    if len(winners) > 1:
        winners_list = ", ".join(f"Player {winner[0]}" for winner in winners)
        print()
        print(f"It's a tie between: {winners_list} with the hand: {winners[0][1]}")
    else:
        print(
            f"\nWinner: Player {evaluations[0][0]} with the hand: {evaluations[0][1]}"
        )


def exchange_cards(hand: list[str], deck: list[str]) -> list[str]:
    """
    Allows the human player to exchange selected cards from their hand with new ones from the deck.

    Args:
        hand: The player's current hand as a list of card strings.
        deck: The remaining deck of cards.

    Returns:
        The updated hand after exchanging selected cards.
    """
    indexes_str = input(
        "Enter indexes of cards to exchange (separated by spaces) or press Enter to keep all "
    )
    if not indexes_str.strip():
        print("No cards exchanted.")
        return hand

    try:
        indexes = sorted({int(i) for i in indexes_str.split()}, reverse=True)
    except ValueError:
        print("No cards exchanged.")
        return hand

    for i in indexes:
        if 1 <= i <= len(hand):
            removed = hand.pop(i - 1)
            if deck:
                new_card = deck.pop()
                hand.insert(i - 1, new_card)
                print(f"Exchanged {removed} for {new_card}.")
            else:
                print("Deck is empty, can't draw more cards.")
        else:
            print(f"Index {i} is out range and was ignored.")

    return hand


def player_vs_computer() -> None:
    """
    Runs one round of poker against computer opponents.

    Prompts the user to select the number of bots, deals cards,
    allows card exchanges, and determines the winner.
    """
    while True:
        try:
            bots = int(input("How many computer opponents you want? (1-3): "))
            if 1 <= bots <= 3:
                break
            print("Please enter a number between 1 and 3.")
        except ValueError:
            print("That's not a valid number.")

    num_players = bots + 1
    human_index = 0

    deck = create_deck()
    hands = deal_cards(deck, num_players)

    print("\nYour hand:")
    display_hands([hands[human_index]])

    hands[human_index] = exchange_cards(hands[human_index], deck)

    print("\nFinal hands:")
    display_hands(hands)
    print()
    print("\nWinners list:")
    announce_winner(hands)
    print()


def test_game() -> None:
    """
    Runs a complete demonstration game of poker.

    This function initializes a new game, handles card dealing,
    displays all player hands, allows the human player to exchange cards,
    and announces the winner at the end.
    """
    player_vs_computer()


if __name__ == "__main__":
    test_game()
