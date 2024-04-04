import time
import pygame
from network import Network
from game_config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    SCREEN_COLOR,
    ACCENT_PINK,
    ACCENT_YELLOW,
    HEADER_HEIGHT,
    FOOTER_HEIGHT,
    SCORECARD_HEIGHT,
    SCORECARD_WIDTH,
)
from draw import (
    draw_rect_with_text,
    draw_coin,
    draw_character,
)


DRAW_GUI = True
BORDER_WIDTH = 1

footer_credits = ["VISHAL", "", "KASHYAP"]


def draw_background(win):

    win.fill(SCREEN_COLOR)

    # header
    draw_rect_with_text(
        text="COIN - BASE",
        font="MabryPro-Regular",
        font_size=48,
        rect_position=(0, 0),
        rect_width=SCREEN_WIDTH,
        rect_height=HEADER_HEIGHT,
        color=SCREEN_COLOR,
        win=win,
        border_width=BORDER_WIDTH,
        h_align="center",
    )

    # SCORECARD
    draw_rect_with_text(
        rect_position=(0, 0),
        rect_width=SCORECARD_WIDTH,
        rect_height=SCREEN_HEIGHT,
        color=SCREEN_COLOR,
        win=win,
        border_width=BORDER_WIDTH,
    )

    draw_rect_with_text(
        text="scoreboard",
        font_size=18,
        rect_position=(0, 0),
        rect_width=SCORECARD_WIDTH,
        rect_height=HEADER_HEIGHT,
        color=SCREEN_COLOR,
        win=win,
        border_width=BORDER_WIDTH,
        padding_x=16,
    )

    # footer
    for i, credit in enumerate(footer_credits):
        draw_rect_with_text(
            text=credit,
            font_size=14,
            rect_position=(
                i * (SCREEN_WIDTH / len(footer_credits)),
                SCREEN_HEIGHT - FOOTER_HEIGHT,
            ),
            rect_width=SCREEN_WIDTH / len(footer_credits),
            rect_height=FOOTER_HEIGHT,
            color=ACCENT_PINK if i % 2 == 0 else ACCENT_YELLOW,
            win=win,
            border_width=BORDER_WIDTH,
            h_align="center",
        )


def draw_scoreboard(player, opponents, win):
    draw_rect_with_text(
        rect_position=(0, HEADER_HEIGHT + BORDER_WIDTH),
        rect_width=SCORECARD_WIDTH,
        rect_height=SCREEN_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - 2 * BORDER_WIDTH,
        color=SCREEN_COLOR,
        win=win,
    )
    # Combine player and opponents' scores and sort them by score
    all_scores = [(player.name, player.score)] + [
        (opp.name, opp.score) for opp in opponents.values()
    ]
    all_scores.sort(key=lambda x: x[1], reverse=True)

    # Draw scoreboard items for each player and opponent
    for i, (name, score) in enumerate(all_scores):

        draw_rect_with_text(
            text=name + "           " + str(round(score, 2)),
            font_size=14,
            rect_position=(
                0,
                HEADER_HEIGHT + BORDER_WIDTH + i * SCORECARD_HEIGHT,
            ),
            rect_width=SCORECARD_WIDTH,
            rect_height=SCORECARD_HEIGHT,
            color=ACCENT_YELLOW if name == player.name else ACCENT_PINK,
            win=win,
            border_width=BORDER_WIDTH,
            padding_x=18,
        )


def redraw_window(player, opponents, coins, win):
    """
    Redraw the window with a white background and the players.

    Args:
        win (pygame.Surface): The window surface to draw on.
        player (Player): The player object to draw.
        opponents (dict): Dictionary containing opponent players.
        coins (list): List containing coin tuples (position, multiplier).
    """

    draw_rect_with_text(
        rect_position=(SCORECARD_WIDTH + BORDER_WIDTH, HEADER_HEIGHT + BORDER_WIDTH),
        rect_width=SCREEN_WIDTH - SCORECARD_WIDTH - 2 * BORDER_WIDTH,
        rect_height=SCREEN_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - 2 * BORDER_WIDTH,
        color=SCREEN_COLOR,
        win=win,
    )
    draw_scoreboard(player, opponents, win)
    for coin in coins:
        draw_coin(coin, win)
    for opp_id, opp in opponents.items():
        draw_character(opp, win)

    draw_character(player, win)

    pygame.display.update()


def handle_events():
    """Handle events such as quitting the game."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def main():
    """Main function to run the game."""
    running = True
    n = Network()
    player = n.getPlayer()
    print(player.get_player_details())
    print(player.name)
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        response = n.send(player)
        multiplier = response.get("multiplier", 0)
        if multiplier != 0:
            player.update_score(multiplier)
        opponents = response["opponents"]
        winner = response["winner"]
        # print("hi", winner)
        if winner:
            coins = {}
            break

        else:
            coins = response["coins"]
        running = handle_events()
        if not running:
            print("Disconnected")
            n.disconnect()

        player.move()
        redraw_window(player, opponents, coins, win)

    # Draw the rectangle and winner text

    if winner:

        draw_rect_with_text(
            text="Player " + winner + " WON!!!",
            font_size=18,
            rect_position=(
                SCORECARD_WIDTH + BORDER_WIDTH,
                HEADER_HEIGHT + BORDER_WIDTH,
            ),
            rect_width=SCREEN_WIDTH - SCORECARD_WIDTH - 2 * BORDER_WIDTH,
            rect_height=SCREEN_HEIGHT
            - HEADER_HEIGHT
            - FOOTER_HEIGHT
            - 2 * BORDER_WIDTH,
            color=ACCENT_YELLOW if winner == player.name else ACCENT_PINK,
            win=win,
            border_width=BORDER_WIDTH,
            h_align="center",
        )
        pygame.display.update()
        time.sleep(5)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    draw_background(win)  # optimise this shit
    main()
