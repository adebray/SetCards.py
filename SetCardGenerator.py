#!/usr/bin/python

# I hope to eventually generate Set cards programatically as .png files. Of course this has been
# done before, but I want to try this style of art.

# I, uh, have no idea what I am doing.
# September 1, 2013 Arun Debray

import sys
import Image
import ImageFont
import ImageDraw

def color(n):
    return n/3 % 3
def number(n):
    return 1 + n % 3
def shading(n):
    return n/9 % 3
def shape(n):
    return n/27 % 3

# centers the rows on a 25-column grid by prepending whitespace
def center(strings):
    return [' '*((26 - len(s))/2) + s for s in strings]
# list comps for getting the right number of blobs on the card
def clone(strings, cardnum):
    return [' '.join([s] * number(cardnum)) for s in strings]
def get_shape(cardnum):
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

def text_of(cardnum):
    return center(clone(get_shape(cardnum), cardnum))
   #return ['0123456789012345678901234'] * 10  -- this is just for testing!
#    return center(clone(['  /\\  ',
#                         ' /%s\\ ' % (fill_char(cardnum) * 2),
#                         '/%s\\' % (fill_char(cardnum) * 4),
#                         '\\%s/' % (fill_char(cardnum) * 4),
#                         ' \\%s/ ' % (fill_char(cardnum) * 2),
#                         '  \\/  '], cardnum))
#
def fill_char(cardnum):
    #return ' -#'[shading(cardnum)] if shape(cardnum) != 1 else ' _#'[shading(cardnum)]
    return ' _#'[shading(cardnum)]
def fill_color(cardnum):
    return [(255, 0, 0), (0, 255, 0), (255, 0, 255)][color(cardnum)]

def offset(cardnum):
    return 20 if shape(cardnum) == 0 else 15

# The card number, from 0 to 80
def main(cardnum):
    image = Image.new('RGB', (150, 100))
#    draw_font = ImageFont.truetype("Menlo Regular.ttf", 16)
    drawer = ImageDraw.Draw(image)
    text_strings = text_of(cardnum)
    for i, line in enumerate(text_strings):
        drawer.text((0, offset(cardnum) + 10 * i), line, fill=fill_color(cardnum))#, font=draw_font)
    image.save('cards/%d.png' % cardnum)

if __name__ == '__main__':
#    if len(sys.argv) < 2:
    for i in range(81):
        main(i)
#        print 'Usage: ./SetCardGenerator.py number'
#        exit(1)
#    cardnum = int(sys.argv[1])
#    if 0 <= cardnum < 81:
#        main(cardnum)
#    else:
#        print 'Card number must be between 0 and 80, inclusive.'
#        exit(1)
