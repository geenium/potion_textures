# potion_textures
Creates all potion textures from a small number of files
## Requirements
The potions_file folder and potions.py must be in the same folder.

All textures specified must be the same size.

# (If running the python script, rather than the exe):
potions.py requires pillow

    pip install pillow

## Specific Textures
You can specify a bottle texture or potion liquid texture for specific potion textures.

This can be:
* potion type ie wither, harm, nightVision
* bottle type ie drinkable, splash, lingering
* potion and bottle ie wither_drinkable, harm_splash, nightVision_lingering
* all.png - this is the default file if no other criteria match

These will be used if the situation is met ie bottle/wither_drinkable.png
This bottle texture will only be used for the wither_drinkable potion

If there is two or more textures which fulfill a situation the texture will be chosen in this order:
1. potion effect + bottle ie wither_drinkable, harm_splash, nightVision_lingering
2. potion effect ie wither, harm, nightVision
3. bottle ie drinkable, splash, lingering
4. all

## potion_colours.json
This is a json file containing a single compound containing keys which refer to a specific potion.

The same naming convention is applied to the keys in the json file ie "wither_splash", "wither", "splash", "all" are all valid keys for potion_colours.json

Each key has a value which is the colour to tint the potion colours located inside the liquids folder.

The key can be a hex value ie "2D5197" / "#2D5197" the # is optional or an rgb values list ie [45, 81, 151]

## Texture Output
After running the script a folder named output will be created in the same folder as potions.py, which will contain all the textures created.

## Potion Names
potions.py will only accept specific names for potion types.

They are as follows:

|Potion Type|potions.py name|
|-|-|
|strength|damageBoost|
|fire resistance|fireResistance|
|instant damage|harm|
|instant health|heal|
|invisibility|invisibility|
|jump boost|jump|
|slowness|moveSlowdown|
|swiftness|moveSpeed|
|night vision|nightVision|
|poison|poison|
|regeneration|regeneration|
|water breathing|waterBreathing|
|weakness|weakness|
|wither|wither|
|water / mundane / thick / awkward|water|
