import csv
import socket
import time

try:
    import cwiid
    CWIID_ENABLED = True
except ImportError:
    CWIID_ENABLED = False

# 3 bytes per pixel
PIXEL_SIZE = 3
PIXEL_SIZE_SM16716 = 4

BLACK = bytearray(b'\x00\x00\x00')
AQUA = bytearray(b'\x00\xff\xff')
AQUAMARINE = bytearray(b'\x7f\xff\xd4')
AZURE = bytearray(b'\xf0\xff\xff')
BEIGE = bytearray(b'\xf5\xf5\xdc')
BISQUE = bytearray(b'\xff\xe4\xc4')
BLANCHEDALMOND = bytearray(b'\xff\xeb\xcd')
BLUE = bytearray(b'\x00\x00\xff')
BLUEVIOLET = bytearray(b'\x8a\x2b\xe2')
BROWN = bytearray(b'\xa5\x2a\x2a')
BURLYWOOD = bytearray(b'\xde\xb8\x87')
CADETBLUE = bytearray(b'\x5f\x9e\xa0')
CHARTREUSE = bytearray(b'\x7f\xff\x00')
CHOCOLATE = bytearray(b'\xd2\x69\x1e')
CORAL = bytearray(b'\xff\x7f\x50')
CORNFLOWERBLUE = bytearray(b'\x64\x95\xed')
CORNSILK = bytearray(b'\xff\xf8\xdc')
CRIMSON = bytearray(b'\xdc\x14\x3c')
CYAN = bytearray(b'\x00\xff\xff')
DARKBLUE = bytearray(b'\x00\x00\x8b')
DARKCYAN = bytearray(b'\x00\x8b\x8b')
DARKGOLDENROD = bytearray(b'\xb8\x86\x0b')
DARKGRAY = bytearray(b'\xa9\xa9\xa9')
DARKGREY = bytearray(b'\xa9\xa9\xa9')
DARKGREEN = bytearray(b'\x00\x64\x00')
DARKKHAKI = bytearray(b'\xbd\xb7\x6b')
DARKMAGENTA = bytearray(b'\x8b\x00\x8b')
DARKOLIVEGREEN = bytearray(b'\x55\x6b\x2f')
DARKORANGE = bytearray(b'\xff\x8c\x00')
DARKORCHID = bytearray(b'\x99\x32\xcc')
DARKRED = bytearray(b'\x8b\x00\x00')
DARKSALMON = bytearray(b'\xe9\x96\x7a')
DARKSEAGREEN = bytearray(b'\x8f\xbc\x8f')
DARKSLATEBLUE = bytearray(b'\x48\x3d\x8b')
DARKSLATEGRAY = bytearray(b'\x2f\x4f\x4f')
DARKSLATEGREY = bytearray(b'\x2f\x4f\x4f')
DARKTURQUOISE = bytearray(b'\x00\xce\xd1')
DARKVIOLET = bytearray(b'\x94\x00\xd3')
DEEPPINK = bytearray(b'\xff\x14\x93')
DEEPSKYBLUE = bytearray(b'\x00\xbf\xff')
DIMGRAY = bytearray(b'\x69\x69\x69')
DIMGREY = bytearray(b'\x69\x69\x69')
DODGERBLUE = bytearray(b'\x1e\x90\xff')
FIREBRICK = bytearray(b'\xb2\x22\x22')
FLORALWHITE = bytearray(b'\xff\xfa\xf0')
FORESTGREEN = bytearray(b'\x22\x8b\x22')
FUCHSIA = bytearray(b'\xff\x00\xff')
GAINSBORO = bytearray(b'\xdc\xdc\xdc')
GHOSTWHITE = bytearray(b'\xf8\xf8\xff')
GOLD = bytearray(b'\xff\xd7\x00')
GOLDENROD = bytearray(b'\xda\xa5\x20')
GRAY = bytearray(b'\x80\x80\x80')
GREY = bytearray(b'\x80\x80\x80')
GREEN = bytearray(b'\x00\x80\x00')
GREENYELLOW = bytearray(b'\xad\xff\x2f')
HONEYDEW = bytearray(b'\xf0\xff\xf0')
HOTPINK = bytearray(b'\xff\x69\xb4')
INDIANRED = bytearray(b'\xcd\x5c\x5c')
INDIGO = bytearray(b'\x4b\x00\x82')
IVORY = bytearray(b'\xff\xff\xf0')
KHAKI = bytearray(b'\xf0\xe6\x8c')
LAVENDER = bytearray(b'\xe6\xe6\xfa')
LAVENDERBLUSH = bytearray(b'\xff\xf0\xf5')
LAWNGREEN = bytearray(b'\x7c\xfc\x00')
LEMONCHIFFON = bytearray(b'\xff\xfa\xcd')
LIGHTBLUE = bytearray(b'\xad\xd8\xe6')
LIGHTCORAL = bytearray(b'\xf0\x80\x80')
LIGHTCYAN = bytearray(b'\xe0\xff\xff')
LIGHTGOLDENRODYELLOW = bytearray(b'\xfa\xfa\xd2')
LIGHTGRAY = bytearray(b'\xd3\xd3\xd3')
LIGHTGREY = bytearray(b'\xd3\xd3\xd3')
LIGHTGREEN = bytearray(b'\x90\xee\x90')
LIGHTPINK = bytearray(b'\xff\xb6\xc1')
LIGHTSALMON = bytearray(b'\xff\xa0\x7a')
LIGHTSEAGREEN = bytearray(b'\x20\xb2\xaa')
LIGHTSKYBLUE = bytearray(b'\x87\xce\xfa')
LIGHTSLATEGRAY = bytearray(b'\x77\x88\x99')
LIGHTSLATEGREY = bytearray(b'\x77\x88\x99')
LIGHTSTEELBLUE = bytearray(b'\xb0\xc4\xde')
LIGHTYELLOW = bytearray(b'\xff\xff\xe0')
LIME = bytearray(b'\x00\xff\x00')
LIMEGREEN = bytearray(b'\x32\xcd\x32')
LINEN = bytearray(b'\xfa\xf0\xe6')
MAGENTA = bytearray(b'\xff\x00\xff')
MAROON = bytearray(b'\x80\x00\x00')
MEDIUMAQUAMARINE = bytearray(b'\x66\xcd\xaa')
MEDIUMBLUE = bytearray(b'\x00\x00\xcd')
MEDIUMORCHID = bytearray(b'\xba\x55\xd3')
MEDIUMPURPLE = bytearray(b'\x93\x70\xd8')
MEDIUMSEAGREEN = bytearray(b'\x3c\xb3\x71')
MEDIUMSLATEBLUE = bytearray(b'\x7b\x68\xee')
MEDIUMSPRINGGREEN = bytearray(b'\x00\xfa\x9a')
MEDIUMTURQUOISE = bytearray(b'\x48\xd1\xcc')
MEDIUMVIOLETRED = bytearray(b'\xc7\x15\x85')
MIDNIGHTBLUE = bytearray(b'\x19\x19\x70')
MINTCREAM = bytearray(b'\xf5\xff\xfa')
MISTYROSE = bytearray(b'\xff\xe4\xe1')
MOCCASIN = bytearray(b'\xff\xe4\xb5')
NAVAJOWHITE = bytearray(b'\xff\xde\xad')
NAVY = bytearray(b'\x00\x00\x80')
OLDLACE = bytearray(b'\xfd\xf5\xe6')
OLIVE = bytearray(b'\x80\x80\x00')
OLIVEDRAB = bytearray(b'\x6b\x8e\x23')
ORANGE = bytearray(b'\xff\xa5\x00')
ORANGERED = bytearray(b'\xff\x45\x00')
ORCHID = bytearray(b'\xda\x70\xd6')
PALEGOLDENROD = bytearray(b'\xee\xe8\xaa')
PALEGREEN = bytearray(b'\x98\xfb\x98')
PALETURQUOISE = bytearray(b'\xaf\xee\xee')
PALEVIOLETRED = bytearray(b'\xd8\x70\x93')
PAPAYAWHIP = bytearray(b'\xff\xef\xd5')
PEACHPUFF = bytearray(b'\xff\xda\xb9')
PERU = bytearray(b'\xcd\x85\x3f')
PINK = bytearray(b'\xff\xc0\xcb')
PLUM = bytearray(b'\xdd\xa0\xdd')
POWDERBLUE = bytearray(b'\xb0\xe0\xe6')
PURPLE = bytearray(b'\x80\x00\x80')
RED = bytearray(b'\xff\x00\x00')
ROSYBROWN = bytearray(b'\xbc\x8f\x8f')
ROYALBLUE = bytearray(b'\x41\x69\xe1')
SADDLEBROWN = bytearray(b'\x8b\x45\x13')
SALMON = bytearray(b'\xfa\x80\x72')
SANDYBROWN = bytearray(b'\xf4\xa4\x60')
SEAGREEN = bytearray(b'\x2e\x8b\x57')
SEASHELL = bytearray(b'\xff\xf5\xee')
SIENNA = bytearray(b'\xa0\x52\x2d')
SILVER = bytearray(b'\xc0\xc0\xc0')
SKYBLUE = bytearray(b'\x87\xce\xeb')
SLATEBLUE = bytearray(b'\x6a\x5a\xcd')
SLATEGRAY = bytearray(b'\x70\x80\x90')
SLATEGREY = bytearray(b'\x70\x80\x90')
SNOW = bytearray(b'\xff\xfa\xfa')
SPRINGGREEN = bytearray(b'\x00\xff\x7f')
STEELBLUE = bytearray(b'\x46\x82\xb4')
TAN = bytearray(b'\xd2\xb4\x8c')
TEAL = bytearray(b'\x00\x80\x80')
THISTLE = bytearray(b'\xd8\xbf\xd8')
TOMATO = bytearray(b'\xff\x63\x47')
TURQUOISE = bytearray(b'\x40\xe0\xd0')
VIOLET = bytearray(b'\xee\x82\xee')
WHEAT = bytearray(b'\xf5\xde\xb3')
WHITE = bytearray(b'\xff\xff\xff')
WHITESMOKE = bytearray(b'\xf5\xf5\xf5')
YELLOW = bytearray(b'\xff\xff\x00')
YELLOWGREEN = bytearray(b'\x9a\xcd\x32')
RAINBOW = [AQUA, AQUAMARINE, AZURE, BEIGE, BISQUE, BLANCHEDALMOND, BLUE, BLUEVIOLET, BROWN, BURLYWOOD, CADETBLUE, CHARTREUSE, CHOCOLATE, CORAL, CORNFLOWERBLUE, CORNSILK, CRIMSON, CYAN, DARKBLUE, DARKCYAN, DARKGOLDENROD, DARKGRAY, DARKGREY, DARKGREEN, DARKKHAKI, DARKMAGENTA, DARKOLIVEGREEN, DARKORANGE, DARKORCHID, DARKRED, DARKSALMON, DARKSEAGREEN, DARKSLATEBLUE, DARKSLATEGRAY, DARKSLATEGREY, DARKTURQUOISE, DARKVIOLET, DEEPPINK, DEEPSKYBLUE, DIMGRAY, DIMGREY, DODGERBLUE, FIREBRICK, FLORALWHITE, FORESTGREEN, FUCHSIA, GAINSBORO, GHOSTWHITE, GOLD, GOLDENROD, GRAY, GREY, GREEN, GREENYELLOW, HONEYDEW, HOTPINK, INDIANRED, INDIGO, IVORY, KHAKI, LAVENDER, LAVENDERBLUSH, LAWNGREEN, LEMONCHIFFON, LIGHTBLUE, LIGHTCORAL, LIGHTCYAN, LIGHTGOLDENRODYELLOW, LIGHTGRAY, LIGHTGREY, LIGHTGREEN, LIGHTPINK, LIGHTSALMON, LIGHTSEAGREEN, LIGHTSKYBLUE, LIGHTSLATEGRAY, LIGHTSLATEGREY, LIGHTSTEELBLUE, LIGHTYELLOW, LIME, LIMEGREEN, LINEN, MAGENTA, MAROON, MEDIUMAQUAMARINE, MEDIUMBLUE, MEDIUMORCHID, MEDIUMPURPLE, MEDIUMSEAGREEN, MEDIUMSLATEBLUE, MEDIUMSPRINGGREEN, MEDIUMTURQUOISE, MEDIUMVIOLETRED, MIDNIGHTBLUE, MINTCREAM, MISTYROSE, MOCCASIN, NAVAJOWHITE, NAVY, OLDLACE, OLIVE, OLIVEDRAB, ORANGE, ORANGERED, ORCHID, PALEGOLDENROD, PALEGREEN, PALETURQUOISE, PALEVIOLETRED, PAPAYAWHIP, PEACHPUFF, PERU, PINK, PLUM, POWDERBLUE, PURPLE, RED, ROSYBROWN, ROYALBLUE, SADDLEBROWN, SALMON, SANDYBROWN, SEAGREEN, SEASHELL, SIENNA, SILVER, SKYBLUE, SLATEBLUE, SLATEGRAY, SLATEGREY, SNOW, SPRINGGREEN, STEELBLUE, TAN, TEAL, THISTLE, TOMATO, TURQUOISE, VIOLET, WHEAT, WHITE, WHITESMOKE, YELLOW, YELLOWGREEN, YELLOWGREEN]
#RAINBOW = [RED, GREEN, BLUE, YELLOW, VIOLET, ORANGE, GRAY, OLIVE, BROWN]



refresh_rate = 20
num_leds = 10
gamma = bytearray(256)
spi_dev_name = '/dev/spidev0.0'
spidev = file(spi_dev_name, "wb")

smile = 0 * PIXEL_SIZE
three = 4 * PIXEL_SIZE
two = 6 * PIXEL_SIZE
one = 8 * PIXEL_SIZE

pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)

for i in range(256):
        gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

def write_stream(pixels):
    spidev.write(pixels)
    return

def correct_pixel_brightness(pixel):
    corrected_pixel = bytearray(3)
    corrected_pixel[0] = int(pixel[0] / 1.1)
    corrected_pixel[1] = int(pixel[1] / 1.1)
    corrected_pixel[2] = int(pixel[2] / 1.3)
    return corrected_pixel

# Apply Gamma Correction and RGB / GRB reordering
# Optionally perform brightness adjustment
def filter_pixel(input_pixel, brightness):
    output_pixel = bytearray(PIXEL_SIZE_SM16716)

    input_pixel[0] = int(brightness * input_pixel[0])
    input_pixel[1] = int(brightness * input_pixel[1])
    input_pixel[2] = int(brightness * input_pixel[2])

    output_pixel[0] = gamma[input_pixel[0]]
    output_pixel[1] = gamma[input_pixel[1]]
    output_pixel[2] = gamma[input_pixel[2]]
    return output_pixel


def fade():

    pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)
    current_color = bytearray(PIXEL_SIZE)
    print "Displaying..."

    while True:
        for color in RAINBOW:
            for brightness in [x * 0.01 for x in range(0, 100)]:
                current_color[:] = filter_pixel(color[:], brightness)

                for pixel_offset in [(x * 3) for x in range(num_leds)]:
                   pixel_output[pixel_offset:] = current_color[:]

                write_stream(pixel_output)
                spidev.flush()
                time.sleep((refresh_rate) / 1000.0)
            for brightness in [x * 0.01 for x in range(100, 0, -1)]:
                current_color[:] = filter_pixel(color[:], brightness)

                for pixel_offset in [(x * 3) for x in range(num_leds)]:
                    pixel_output[pixel_offset:] = current_color[:]

                write_stream(pixel_output)
                spidev.flush()
                time.sleep((refresh_rate) / 1000.0)


def smile_led(color):
    pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)

    for pixel_offset in [(x * 3) for x in range(num_leds)]:

                    if pixel_offset >= smile and pixel_offset < three:
                          pixel_output[pixel_offset:] = color
                    else:
                          pixel_output[pixel_offset:] = BLACK

    write_stream(pixel_output)
    spidev.flush()

def three_led(color):
    pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)

    for pixel_offset in [(x * 3) for x in range(num_leds)]:

                    if pixel_offset >= three and pixel_offset < two:
                          pixel_output[pixel_offset:] = color
                    else:
                          pixel_output[pixel_offset:] = BLACK
    write_stream(pixel_output)
    spidev.flush()

def two_led(color):
    pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)

    for pixel_offset in [(x * 3) for x in range(num_leds)]:

                    if pixel_offset >= two and pixel_offset < one:
                          pixel_output[pixel_offset:] = color
                    else:
                          pixel_output[pixel_offset:] = BLACK
    write_stream(pixel_output)
    spidev.flush()

def one_led(color):
    pixel_output = bytearray(num_leds * PIXEL_SIZE + 3)

    for pixel_offset in [(x * 3) for x in range(num_leds)]:

                    if pixel_offset >= one:
                          pixel_output[pixel_offset:] = color
                    else:
                          pixel_output[pixel_offset:] = BLACK
    write_stream(pixel_output)
    spidev.flush()

for pixel_offset in [(x * 3) for x in range(num_leds)]:

                pixel_output[pixel_offset:] = bytearray(b'\x32\xcd\x32')

                write_stream(pixel_output)
                spidev.flush()


time.sleep(1)



for pixel_offset in [(x * 3) for x in range(num_leds)]:


          if pixel_offset >= three and pixel_offset < two:
                pixel_output[pixel_offset:] = GREEN
          else:
                pixel_output[pixel_offset:] = GREY

write_stream(pixel_output)
spidev.flush()

time.sleep(1)

for pixel_offset in [(x * 3) for x in range(num_leds)]:


          if pixel_offset >= three and pixel_offset < one:
                pixel_output[pixel_offset:] = GREEN
          else:
                pixel_output[pixel_offset:] = GREY

write_stream(pixel_output)
spidev.flush()

time.sleep(1)

for pixel_offset in [(x * 3) for x in range(num_leds)]:


          if pixel_offset >= three:
                pixel_output[pixel_offset:] = GREEN
          else:
                pixel_output[pixel_offset:] = GREY

write_stream(pixel_output)
spidev.flush()

time.sleep(1)

for pixel_offset in [(x * 3) for x in range(num_leds)]:


         pixel_output[pixel_offset:] = DARKRED

write_stream(pixel_output)
spidev.flush()

time.sleep(5)

smile_led(RED)
time.sleep(1)

one_led(GREEN)
time.sleep(1)

two_led(BLUE)
time.sleep(1)

three_led(YELLOW)
time.sleep(1)

smile_led(PAPAYAWHIP)
time.sleep(1)

fade()
