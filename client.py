import pygame
from network import Network
from game_config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    COIN_RADIUS,
    COIN_COLOR,
    SCREEN_COLOR,
    ACCENT_PINK,
    ACCENT_YELLLOW,
    HEADER_HEIGHT,
    FOOTER_HEIGHT,
    SCORECARD_HEIGHT,
    SCORECARD_WIDTH

)
from os import listdir
from os.path import join, isfile



footer_credits = ["ASHISH KUMAR", "VINAY PRAKASH", "VISHAL KASHYAP"]


def flip_sprite(sprite):
    return pygame.transform.flip(sprite, True, False)


def load_character_sprites(direction=False):
    """
    Load character sprites from the assets folder.

    Args:
        direction (bool): Whether to load sprites for both directions.

    Returns:
        dict: Dictionary containing character sprites.
    """
    dir = "characters"
    path = join("assets", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    character_sprites = {}

    for image in images:
        sprite = pygame.image.load(join(path, image)).convert_alpha()

        if direction:
            character_sprites[image.replace(".png", "") + "_right"] = sprite
            character_sprites[image.replace(".png", "") + "_left"] = flip_sprite(sprite)
        else:
            character_sprites[image.replace(".png", "")] = sprite
    return character_sprites


# --------------------------------------------------------
"""
TypeError: cannot pickle 'pygame.surface.Surface' object` 

pickle cant serialize (or i am not able to serialize..) pygame.surface object
"""

# def draw(player, win, SPRITES):
#     """
#         Draw the player on the window.

#         Args:
#             win (pygame.Surface): The window surface to draw the player on.
#     """
#     player.sprite = SPRITES[player.char + "_" + player.direction]
#     win.blit(player.sprite, (player.x, player.y))

# def redraw_window(win, player, opponents):
#     """
#     Redraw the window with a white background and the player.

#     Args:
#         win (pygame.Surface): The window surface to draw on.
#         player (Player): The player object to draw.
#     """
#     win.fill((255, 255, 255))
#     draw(player,win, SPRITES)
#     for opp_id, opp in opponents.items():
#         draw(opp,win, SPRITES)

#     pygame.display.update()

# --------------------------------------------------------


def draw(player, win):
    """
    Draw the player on the window.

    Args:
        player (Player): The player object to draw.
        win (pygame.Surface): The window surface to draw on.
    """
    pygame.draw.rect(win, player.color, player.rect)


def draw_coin(coin, win):
    """
    Draw a coin on the window.

    Args:
        coin (tuple): The coin object containing position and radius information.
                Format: (center_x, center_y, radius)
        win (pygame.Surface): The window surface to draw on.
    """
    (center_x, center_y), multiplier = coin
    pygame.draw.circle(win, COIN_COLOR, (center_x, center_y), COIN_RADIUS * multiplier)


def align_shape(shape, position, h_align="left", v_align="top"):
    """
    Align a shape (text or rectangle) to a specified position based on horizontal and vertical alignment.

    Args:
        shape (pygame.Rect or tuple): The shape to be aligned, represented as a pygame.Rect object or a tuple (width, height).
        position (tuple): The position to align the shape to (top-left corner).
        h_align (str): Horizontal alignment of the shape ('left', 'center', or 'right').
        v_align (str): Vertical alignment of the shape ('top', 'center', or 'bottom').

    Returns:
        pygame.Rect: The aligned shape as a pygame.Rect object.
    """
    # Convert shape to a pygame.Rect if it's not already one
    if not isinstance(shape, pygame.Rect):
        width, height = shape
        shape = pygame.Rect(position[0], position[1], width, height)

    # Adjust horizontal alignment
    if h_align == "center":
        shape.centerx = position[0]
    elif h_align == "right":
        shape.right = position[0]
    else:
        shape.left = position[0]

    # Adjust vertical alignment
    if v_align == "center":
        shape.centery = position[1]
    elif v_align == "bottom":
        shape.bottom = position[1]
    else:
        shape.top = position[1]

    return shape


def draw_rectangle(
    size,
    color,
    position,
    win,
    h_align="left",
    v_align="top",
    border_width=0,
    border_color=(0, 0, 0),
):
    """
    Draw a rectangle on the window with support for horizontal and vertical alignment.

    Args:
        size (tuple): The size of the rectangle (width, height).
        color (tuple): The color of the rectangle.
        position (tuple): The position to draw the rectangle (top-left corner).
        win (pygame.Surface): The window surface to draw on.
        h_align (str): Horizontal alignment of the rectangle ('left', 'center', or 'right').
        v_align (str): Vertical alignment of the rectangle ('top', 'center', or 'bottom').
        border_width (int): The width of the rectangle border (default is 0, no border).
        border_color (tuple): The color of the rectangle border (optional, default is None).
    """
    rect = pygame.Rect(0, 0, *size)
    rect = align_shape(rect, position, h_align, v_align)

    if border_width:
        # Update position and size for border
        border_x, border_y = rect.topleft
        border_width_scaled = 2 * border_width
        border_x -= border_width
        border_y -= border_width
        width, height = size
        width += border_width_scaled
        height += border_width_scaled
        rect = pygame.Rect(border_x, border_y, width, height)

        # Adjust horizontal and vertical positions
        horizontal_position, vertical_position = position
        horizontal_position -= border_width
        vertical_position -= border_width

        pygame.draw.rect(win, border_color, rect, border_width)
        inner_rect = rect.inflate(-border_width_scaled, -border_width_scaled)
        pygame.draw.rect(win, color, inner_rect)
    else:
        pygame.draw.rect(win, color, rect)


def load_font(font_name, font_size):
    """
    Load a font from the assets/fonts directory.

    Args:
        font_name (str): The name of the font file without extension.
        font_size (int): The size of the font.

    Returns:
        pygame.font.Font: The loaded font object, or "Roboto" font if the specified font is not found.
    """
    dir = "fonts"
    path = join("assets", dir)
    font_path = join(path, f"{font_name}.ttf")

    try:
        return pygame.font.Font(font_path, font_size)
    except pygame.error:
        # Return "Roboto" font if specified font is not found
        return pygame.font.SysFont("Roboto", font_size)


def draw_text(
    text, font_size, color, position, win, h_align="left", v_align="top", font="ROBOTO"
):
    """
    Draw text on the window with support for horizontal and vertical alignment.

    Args:
        text (str): The text to be drawn.
        font_size (int): The size of the font.
        color (tuple): The color of the text.
        position (tuple): The position to draw the text (top-left corner).
        win (pygame.Surface): The window surface to draw on.
        h_align (str): Horizontal alignment of the text ('left', 'center', or 'right').
        v_align (str): Vertical alignment of the text ('top', 'center', or 'bottom').
        font (str): The font to be used for the text.
    """
    font_style = load_font(font, font_size)
    rendered_text = font_style.render(text, True, color)
    text_rect = rendered_text.get_rect()

    # Align the text rectangle
    text_rect = align_shape(text_rect, position, h_align, v_align)

    win.blit(rendered_text, text_rect.topleft)


def draw_footer_item(text, rect_color, text_color, font_size, font, position, win):
    """
    Draw a rectangle and text item in the footer.

    Args:
        text (str): The text to be drawn.
        rect_color (tuple): The color of the rectangle.
        text_color (tuple): The color of the text.
        font_size (int): The size of the font.
        font (str): The font to be used for the text.
        position (tuple): The position to draw the item (center of the text).
        win (pygame.Surface): The window surface to draw on.
    """
    adjust = 12  # Adjustment for text position
    draw_rectangle(
        (SCREEN_WIDTH / len(footer_credits), FOOTER_HEIGHT),
        rect_color,
        (
            position[0] - (SCREEN_WIDTH / len(footer_credits)) / 2,
            SCREEN_HEIGHT - FOOTER_HEIGHT,
        ),
        win,
        h_align="left",
        v_align="top",
        border_width=1,
        border_color=(0, 0, 0),
    )
    draw_text(
        text,
        font_size,
        text_color,
        position,
        win,
        font=font,
        h_align="center",
        v_align="top",
    )



def draw_background(win):

    win.fill(SCREEN_COLOR)

    # header
    draw_rectangle(
        (SCREEN_WIDTH, HEADER_HEIGHT),
        SCREEN_COLOR,
        (SCREEN_WIDTH / 2, 0),
        win,
        h_align="center",
        v_align="top",
        border_width=1,
        border_color=(0, 0, 0),
    )
    draw_text(
        "COIN - BASE",
        48,
        (0, 0, 0),
        (SCREEN_WIDTH / 2, 0),
        win,
        font="NixieOne-Regular",
        h_align="center",
    )

    # SCORECARD
    draw_rectangle(
        (SCORECARD_WIDTH, SCREEN_HEIGHT),
        SCREEN_COLOR,
        (0, 0),
        win,
        h_align="left",
        v_align="top",
        border_width=1,
        border_color=(0, 0, 0),
    )
    draw_rectangle(
        (SCORECARD_WIDTH, HEADER_HEIGHT),
        SCREEN_COLOR,
        (0, 0),
        win,
        h_align="left",
        v_align="top",
        border_width=1,
        border_color=(0, 0, 0),
    )
    draw_text(
        "scoreboard",
        18,
        (0, 0, 0),
        (SCREEN_WIDTH / 12, 18),
        win,
        font="MabryPro-Regular",
        h_align="center",
    )

    # footer
    adjust = 12
    for i, credit in enumerate(footer_credits):
        draw_footer_item(
            text=credit,
            rect_color=ACCENT_PINK if i % 2 == 0 else ACCENT_YELLLOW,
            text_color=(0, 0, 0),
            font_size=14,
            font="MabryPro-Regular",
            position=(
                i * (SCREEN_WIDTH / len(footer_credits))
                + (SCREEN_WIDTH / len(footer_credits)) / 2,
                SCREEN_HEIGHT - FOOTER_HEIGHT + adjust,
            ),
            win=win,
        )


def draw_scoreboard(player, opponents, win):
    for opp_id, opp in opponents.items():
        continue


def redraw_window(player, opponents, coins, win):
    """
    Redraw the window with a white background and the players.

    Args:
        win (pygame.Surface): The window surface to draw on.
        player (Player): The player object to draw.
        opponents (dict): Dictionary containing opponent players.
        coins (dict): Dictionary containing coin positions and multipliers.
    """
    
    draw_background(win)
    draw(player, win)
    for coin_id, coin in coins.items():
        draw_coin(coin, win)
    for opp_id, opp in opponents.items():
        draw(opp, win)

    draw(player, win)

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
        coins = response["coins"]

        running = handle_events()
        if not running:
            print("Disconnected")
            n.disconnect()

        player.move()
        redraw_window(player, opponents, coins, win)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Client")
    # draw_background(win) optimise this shit 
    main()
