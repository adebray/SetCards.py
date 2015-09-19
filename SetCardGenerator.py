#!/usr/bin/env python3.4

# A program for generating SET cards as .png files, using Pillow.
# This particular design represents them as ASCII art, but I'm happy
# to try other designs.

# The type annotations here don't do anything yet,
# but I might use them in the future.

# Some TODOs, in no particular order:
	# 1. clean up the code a little bit, and ensure it works in multiple versions of Python
	# 2. Generate cards with a lighter background
	# 3. Maybe fiddle with the design?

from PIL import (
	Image,
	ImageDraw,
	ImageFont
)

def color(n: int) -> int:
	return n // 3 % 3
def number(n: int) -> int:
	return 1 + n % 3
def shading(n: int) -> int:
	return n // 9 % 3
def shape(n: int) -> int:
	return n // 27 % 3

# Respectively, empty, shaded, filled depending on the shadng
def fill_char(cardnum: int) -> str:
	return ' _#'[shading(cardnum)]

# Returns the color of the ASCII art for the card
def fill_color(cardnum: int) -> (int, int, int):
	return [(255, 0, 0), (0, 255, 0), (255, 0, 255)][color(cardnum)]

# Given a list of strings, centers each string in a 25-character string by adding
# whitespace on both ends.
# This will fail if given strings of more than 25 characters.
def center(strings: [str]) -> (str): # actually returns a generator
	return (' '*((26 - len(s)) // 2) + s for s in strings)

# Given the shape of the blob on the SET card and the card number,
# clones the shame to appear that number of times on the card.
def clone(strings: [str], cardnum: int) -> (str): # actually returns a generator
	return (' '.join([s] * number(cardnum)) for s in strings)

# Uses the card's shading and shape attributes to return the shape and filling of
# of the blob for that card, which is processed into the fill card.
def get_shape(cardnum: int) -> [str]:
	if shape(cardnum) == 0:
		return ['  /\\  ',
				' /%s\\ ' % (fill_char(cardnum) * 2),
				'/%s\\' % (fill_char(cardnum) * 4),
				'\\%s/' % (fill_char(cardnum) * 4),
				' \\%s/ ' % (fill_char(cardnum) * 2),
				'  \\/  ']
	elif shape(cardnum) == 1:
		return ['  __  ',
				' /%s\\ ' % (fill_char(cardnum) * 2),
				'|%s|' % (fill_char(cardnum) * 4),
				'|%s|' % (fill_char(cardnum) * 4),
				'|%s|' % (fill_char(cardnum) * 4),
				' \\%s/ ' % (fill_char(cardnum) * 2 if shading(cardnum) != 0 else '__')]
	else:
		return [' ____ ',
				'/%s/ ' % (fill_char(cardnum) * 3),
				'\\%s\\ ' % (fill_char(cardnum) * 3),
				' \\%s\\' % (fill_char(cardnum) * 3),
				' /%s/' % (fill_char(cardnum) * 3),
				'/___/ ' if shading(cardnum) == 0 else '/%s/ ' % (fill_char(cardnum) * 3)]

# Uses the above functions to return the complete ASCII art image of the card
def text_of(cardnum: int) -> (str): # returns a generator
	return center(clone(get_shape(cardnum), cardnum))

# Given a card number, from 0 to 80, produces the card
def make_card(cardnum: int, color: (int, int, int), directory: str) -> None:
	image = Image.new('RGB', (150, 100), color=color)
	drawer = ImageDraw.Draw(image)
	offset = 20 if shape(cardnum) == 0 else 15
	for i, line in enumerate(text_of(cardnum)):
		drawer.text((0, offset + 10 * i), line, fill=fill_color(cardnum))
	image.save(directory + '/%d.png' % cardnum)

if __name__ == '__main__':
	for i in range(81):
		# produces one card with a black background, and one with a lighter gray background
		make_card(i, (0, 0, 0), 'cards')
		make_card(i, (85, 85, 85), 'cards_gray')
