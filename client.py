import time
import pygame
import math
from network import Network
from game_config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    SCREEN_COLOR,
    SECONDARY_COLOR,
    PRIMARY_COLOR,
    PRIMARY_FONT,
    HEADER_HEIGHT,
    FOOTER_HEIGHT,
    SCORECARD_HEIGHT,
    SCORECARD_WIDTH,
    BORDER_WIDTH,
    TITLE_TEXT_SIZE,
    SUB_TITLE_TEXT_SIZE,
    BODY_TEXT_SIZE
)
from draw import draw_rect_with_text

DRAW_GUI = True
footer_credits = ["2024", "", "@vishuuwu"]



def draw_background(win):
    """
    Draw the background including header, scoreboard, and footer.

    Args:
        win (pygame.Surface): The window surface to draw on.
    """

    win.fill(SCREEN_COLOR)

    # Header
    draw_rect_with_text(
        text="COIN - BASE",
        font=PRIMARY_FONT,
        font_size=TITLE_TEXT_SIZE,
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
        font=PRIMARY_FONT,
        font_size=SUB_TITLE_TEXT_SIZE,
        rect_position=(0, 0),
        rect_width=SCORECARD_WIDTH,
        rect_height=HEADER_HEIGHT,
        color=SCREEN_COLOR,
        win=win,
        border_width=BORDER_WIDTH,
        padding_x=16,
    )
    align = "left"
    # Footer
    for i, credit in enumerate(footer_credits):
        if not credit: align= "right" 
        draw_rect_with_text(
            text=credit,
            font=PRIMARY_FONT,
            font_size=BODY_TEXT_SIZE,
            rect_position=(
                i * (math.ceil(SCREEN_WIDTH / len(footer_credits))),
                SCREEN_HEIGHT - FOOTER_HEIGHT,
            ),
            rect_width=SCREEN_WIDTH / len(footer_credits),
            rect_height=FOOTER_HEIGHT,
            color=SECONDARY_COLOR if i % 2 == 0 else PRIMARY_COLOR,
            win=win,
            border_width=BORDER_WIDTH,
            h_align=align,
            padding_x= 16
        )


def draw_scoreboard(player, opponents, win):
    """
    Draw the scoreboard displaying player and opponents' scores.

    Args:
        player (Player): The player object.
        opponents (dict): Dictionary containing opponent players.
        win (pygame.Surface): The window surface to draw on.
    """


    # Combine player and opponents' scores and sort them by score
    all_scores = [(player.name, player.score)] + [
        (opp.name, opp.score) for opp in opponents.values()
    ]
    all_scores.sort(key=lambda x: x[1], reverse=True)

    draw_rect_with_text(
        rect_position=(0, HEADER_HEIGHT + BORDER_WIDTH),
        rect_width=SCORECARD_WIDTH,
        rect_height=len(all_scores)*SCORECARD_HEIGHT,
        color=SCREEN_COLOR,
        win=win,
        draw_rect=True
    )
    # Draw scoreboard items for each player and opponent
    for i, (name, score) in enumerate(all_scores):

        draw_rect_with_text(
            text=name + "           " + str(round(score, 2)),
            font_size=BODY_TEXT_SIZE,
            rect_position=(
                0,
                HEADER_HEIGHT + BORDER_WIDTH + i * SCORECARD_HEIGHT,
            ),
            rect_width=SCORECARD_WIDTH,
            rect_height=SCORECARD_HEIGHT,
            color=PRIMARY_COLOR if name == player.name else SECONDARY_COLOR,
            win=win,
            border_width=BORDER_WIDTH,
            padding_x=18,
        )


def redraw_window(player, opponents, coins, win):
    """
    Redraw the game window with updated player, opponents, and coins.

    Args:
        player (Player): The player object.
        opponents (dict): Dictionary containing opponent players.
        coins (list): List containing coin tuples (position, multiplier).
        win (pygame.Surface): The window surface to draw on.
    """

    draw_rect_with_text(
        rect_position=(SCORECARD_WIDTH + BORDER_WIDTH, HEADER_HEIGHT + BORDER_WIDTH),
        rect_width=SCREEN_WIDTH - SCORECARD_WIDTH - 2 * BORDER_WIDTH,
        rect_height=SCREEN_HEIGHT - HEADER_HEIGHT - FOOTER_HEIGHT - 2 * BORDER_WIDTH,
        color=SCREEN_COLOR,
        win=win,
        draw_rect=True
    )
    draw_scoreboard(player, opponents, win)
    for coin in coins:
        coin.draw(win)
    for opp_id, opp in opponents.items():
        opp.draw(win)

    player.draw(win)

    pygame.display.update()


def handle_events():
    """Handle events such as quitting the game."""
    # global SCREEN_WIDTH, SCREEN_HEIGHT, SCORECARD_WIDTH
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        # elif event.type == pygame.VIDEORESIZE:
        #     # Update the screen dimensions if the window is resized
        #     SCREEN_WIDTH, SCREEN_HEIGHT = event.size
        #     # SCORECARD_WIDTH= SCREEN_WIDTH //6
        #     win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        #     draw_background(win)

        
    return True


def main():
    """Main function to run the game."""
    running = True
    n = Network()
    player = n.getPlayer()
    # print(player.get_player_details())
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
            font_size=SUB_TITLE_TEXT_SIZE,
            rect_position=(
                SCORECARD_WIDTH + BORDER_WIDTH,
                HEADER_HEIGHT + BORDER_WIDTH,
            ),
            rect_width=SCREEN_WIDTH - SCORECARD_WIDTH - 2 * BORDER_WIDTH,
            rect_height=SCREEN_HEIGHT
            - HEADER_HEIGHT
            - FOOTER_HEIGHT
            - 2 * BORDER_WIDTH,
            color=PRIMARY_COLOR if winner == player.name else SECONDARY_COLOR,
            win=win,
            border_width=BORDER_WIDTH,
            h_align="center",
        )
        pygame.display.update()
        time.sleep(5)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    # win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    draw_background(win)
    main()
