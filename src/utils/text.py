from typing import Literal

import pygame as pg

pg.init()


def draw_line(
    surface: pg.Surface,
    pos: tuple[float, float] | pg.Vector2,
    font: pg.font.Font,
    line: str,
    color: tuple[int, int, int],
    *,
    alignment: Literal['left', 'centered', 'right'] = 'left',
) -> None:
    """Draws a line of text on a surface.

    Args:
        surface (pg.Surface): The surface to draw text onto.
        pos (pg.Vector2): The position of the text.
        font (pg.font.Font): The font object used to render each line.
        line (list[str]): The string to draw.
        color (tuple[int, int, int]): The color of the text.
        alignment (Literal['left', 'centered', 'right']): The alignment of the \
        text at the provided position.
    """
    pos = pg.Vector2(pos)
    surf = font.render(line, True, color)

    if alignment == 'centered':
        pos.x -= surf.get_width() / 2
    elif alignment == 'right':
        pos.x -= surf.get_width()

    surface.blit(surf, pos)


def draw_lines(
    surface: pg.Surface,
    start_pos: tuple[float, float] | pg.Vector2,
    font: pg.font.Font,
    lines: list[str],
    color: tuple[int, int, int],
    margin: float = 2,
    *,
    alignment: Literal['left', 'centered', 'right'] = 'left',
) -> None:
    """Draws multiple lines of text on a surface.

    Args:
        surface (pg.Surface): The surface to blit onto.
        start_pos (pg.Vector2): The position of the text.
        font (pg.font.Font): The font object used to render each line.
        lines (list[str]): A list of strings to draw. No \\n escape sequences are \
        needed.
        color (tuple[int, int, int]): The color of the text.
        alignment (Literal['left', 'centered', 'right']): The alignment of the \
        text at the provided position.
        margin (float, optional): Margin between each line. Defaults to 2px.
    """
    current_pos = pg.Vector2(start_pos)

    for line in lines:
        draw_line(surface, current_pos.copy(), font, line, color, alignment=alignment)

        current_pos.y += font.get_linesize() + margin
