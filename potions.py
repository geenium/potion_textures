from json import loads as jsonLoads
from PIL import Image
from os import path, mkdir
from shutil import copy2


# Re-colours the greyscale potion image, and returns the new tinted image
def blend_multiply(greyscale, colour):
    # Colour can be a hex value or an rgb list
    # Larger than 3 means it's a hex value so the rgb values \
    # have to be extracted from the hex
    if len(colour) > 3:
        red, green, blue = [int(colour[-6:-4], 16), int(colour[-4:-2], 16),
                            int(colour[-2:], 16)]
    # If not a hex value it is a list as in - [r, g, b]
    else:
        red, green, blue = colour

    # Creates a new image which will be saved as the potion texture
    tinted = Image.new("RGBA", greyscale.size)

    # Gets the width and height of the greyscale potion texture
    width, height = greyscale.size

    # Loads the images for pixel access
    potion_pixels = greyscale.load()
    tinted_pixels = tinted.load()
    for x in range(width):
        for y in range(height):
            # If the alpha value of the pixel is greater than 0 \
            # it needs to be re-coloured
            if potion_pixels[x, y][3] > 0:
                tinted_pixels[x, y] = (round(potion_pixels[x, y][0] * red /
                                            255),
                                      round(potion_pixels[x, y][1] * green /
                                            255),
                                      round(potion_pixels[x, y][2] * blue /
                                            255),
                                      potion_pixels[x, y][3])
    return tinted


# Opens a texture depending on the variables given
def get_texture(item, effect, bottle):
    # Quickly changes the 'item' variable to the correct folder name
    folder_dict = {"bottle": "bottles", "potion": "liquids"}
    folder = "potion_files/" + folder_dict[item] + "/"
    # Nested try except statements quickly check for the highest precedent
    # file name to use for the specific texture needed
    # <effect>_<bottle>.png has the highest precedent ie wither_splash.png
    try:
        texture = Image.open(folder + effect + "_" + bottle + ".png")
    except FileNotFoundError:
        # <effect>.png is the next highest ie wither.png
        try:
            return Image.open(folder + effect + ".png")
        except FileNotFoundError:
            # <bottle>.png is checked next ie splash.png
            try:
                return Image.open(folder + bottle + ".png")
            except FileNotFoundError:
                # all.png is the default file used if none else are there
                try:
                    return Image.open(folder + "all.png")
                # If all.png is not there a texture cannot be produced
                except FileNotFoundError:
                    print(effect, item, "texture not available!\n")
                    # If no texture is found False is returned
                    # This value is checked for later on
                    return False


# Gets the colour from the dictionary of colours
def get_colour(effect, bottle):
    # Nested try except statements quickly check for the highest precedent
    # colour definition to use for the specific potion needed
    # "<effect>_<bottle>" has the highest precedent ie "wither_splash": "..."
    try:
        colour = potion_colours[effect + "_" + bottle]
    except KeyError:
        # "<effect>" is the next highest ie "wither": "..."
        try:
            return potion_colours[effect]
        except KeyError:
            # "<bottle>" is checked next ie "splash": "..."
            try:
                return potion_colours[bottle]
            except KeyError:
                # "all" is the default key used if none else are there
                try:
                    return potion_colours["all"]
                # If "all" is not there a tint cannot be applied
                except KeyError:
                    print(bottle, "potion of", effect, "no tint found!\n\
Using default potion colour.\n")
                    # Just white is used if no other colour is found
                    return [255, 255, 255]

# These are the only potion textures actually used in game
potion_list = ["damageBoost", "fireResistance", "harm", "heal", "invisibility",
               "jump", "moveSlowdown", "moveSpeed", "nightVision", "poison",
               "regeneration", "waterBreathing", "weakness", "wither", ""]

bottle_list = ["drinkable", "lingering", "splash"]

# Gets the colours for the potions from the json file
with open("potion_files/potion_colours.json", "r") as f:
    potion_colours = jsonLoads(f.read())

# Changes "water" to "" as this is used as the texture name
try:
    potion_colours[""] = potion_colours.pop("water")
    potion_colours["_drinkable"] = potion_colours.pop("water_drinkable")
    potion_colours["_splash"] = potion_colours.pop("water_splash")
    potion_colours["_lingering"] = potion_colours.pop("water_lingering")
except KeyError:
    # If the key does not exist nothing needs to happen
    pass

# Checks if the directory exists, if it doesn't it creates it
if not path.isdir("output"):
    mkdir("output")

# Creates all the potion textures
for effect in potion_list:
    for bottle in bottle_list:
        bottle_texture = get_texture("bottle", effect, bottle)
        potion_texture = blend_multiply(get_texture("potion", effect, bottle),
                                        get_colour(effect, bottle))
        # If the two images are not the same size
        # alpha_composite cannot be used
        if bottle_texture.size != potion_texture.size:
            print("Bottle texture and potion greyscale need to be the same \
size.\nUnable to create", bottle, "potion of", effect, "texture.\n")
            continue

        # Checks if either of the textures has returned "False"
        if bottle_texture and potion_texture:
            bottle = "_" + bottle
            if effect != "":
                if bottle == "_drinkable":
                    bottle = ""
                bottle += "_"
            save_name = "output/potion_bottle" + bottle + effect + ".png"
            new_potion = Image.new("RGBA", bottle_texture.size)
            new_potion = Image.alpha_composite(potion_texture, bottle_texture)
            new_potion.save(save_name)

empty_bottle = "output/potion_bottle_empty.png"
bottle_path = "potion_files/bottles/"
# Copies the empty drinkable bottle texture to use as the empty bottle texture
try:
    copy2(bottle_path + "drinkable.png", empty_bottle)
except FileNotFoundError:
    # If the empty drinakble bottle doesn't exist bottles/all.png will be used
    try:
        copy2(bottle_path + "all.png", empty_bottle)
    except FileNotFoundError:
        # If no file is found then it cannot create an empty bottle texture
        print("Cannot find empty drinkable bottle.\nNo empty bottle texture \
              produced!")

input("Potion files created.\nPress Enter to exit\n>> ")
