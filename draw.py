from os import listdir
import pygame
from os.path import join, isfile
from game_config import PRIMARY_FONT, SECONDARY_FONT, TERTIARY_COLOR, DRAW_GUI


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
    border_color=TERTIARY_COLOR,
    draw=True,
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
    if not draw:
        return

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
        return pygame.font.SysFont(SECONDARY_FONT, font_size)


def draw_text(
    text,
    font_size,
    color,
    position,
    win,
    h_align="left",
    v_align="top",
    font=SECONDARY_FONT,
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


def draw_rect_with_text(
    text=None,
    font=PRIMARY_FONT,
    font_size=None,
    rect_position=None,
    rect_width=None,
    rect_height=None,
    color=None,
    win=None,
    border_width=0,
    border_color=TERTIARY_COLOR,
    h_align="left",
    v_align="center",
    padding_x=0,
    padding_y=0,
    draw_rect=DRAW_GUI,
):
    """
    Draw a rectangle with optional text inside, supporting alignment and padding.

    Args:
        text (str, optional): The text to be drawn (default is None).
        font (str, optional): The font to be used for the text (default is None).
        font_size (int, optional): The size of the font (default is None).
        rect_position (tuple, optional): The position of the rectangle (top-left corner) (default is None).
        rect_width (int, optional): The width of the rectangle (default is None).
        rect_height (int, optional): The height of the rectangle (default is None).
        color (tuple, optional): The color of the rectangle (default is None).
        win (pygame.Surface): The window surface to draw on (default is None).
        border_width (int): The width of the rectangle border (default is 0).
        border_color (tuple, optional): The color of the rectangle border (optional, default is black).
        h_align (str, optional): Horizontal alignment of the text within the rectangle ('left', 'center', or 'right') (default is "left").
        v_align (str, optional): Vertical alignment of the text within the rectangle ('top', 'center', or 'bottom') (default is "top").
        padding_x (int, optional): Padding on the x-axis for the text (default is 0).
        padding_y (int, optional): Padding on the y-axis for the text (default is 0).
    """
    # Draw rectangle with border
    if draw_rect:
        if border_width:
            # Update position and size for border
            border_x, border_y = rect_position
            border_width_scaled = 2 * border_width
            border_x -= border_width
            border_y -= border_width
            width, height = rect_width, rect_height
            width += border_width_scaled
            height += border_width_scaled
            rect = pygame.Rect(border_x, border_y, width, height)

            # Adjust horizontal and vertical positions
            horizontal_position, vertical_position = rect_position
            horizontal_position -= border_width
            vertical_position -= border_width

            pygame.draw.rect(win, border_color, rect, border_width)
            inner_rect = rect.inflate(-border_width_scaled, -border_width_scaled)
            pygame.draw.rect(win, color, inner_rect)
        else:
            rect = pygame.Rect(rect_position, (rect_width, rect_height))
            pygame.draw.rect(win, color, rect)

    if text:
        # Draw text if text and font are provided
        # Calculate position for the text
        text_x = rect_position[0] + padding_x
        text_y = rect_position[1] + padding_y
        if h_align == "center":
            text_x += (rect_width - 2 * padding_x) / 2
        elif h_align == "right":
            text_x += rect_width - 2 * padding_x

        if v_align == "center":
            text_y += (rect_height - 2 * padding_y) / 2 - font_size / 2
        elif v_align == "bottom":
            text_y += rect_height - 2 * padding_y - font_size

        # Draw text
        draw_text(
            text,
            font_size,
            TERTIARY_COLOR,
            (text_x, text_y),
            win,
            font=font,
            h_align=h_align,
        )
