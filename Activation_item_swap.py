import json as js

MESSAGE = """
Insert the identifier of the item to be used as the new trigger (example: minecraft:sparkler).
Make sure it's an item you can hold in your offhand.
Otherwise, you can input a number to reference one item from the list above.

"""
OFFHAND_ITEM_LIST = [
    "minecraft:shield",
    "minecraft:arrow",
    "minecraft:firework_rocket",
    "minecraft:totem_of_undying",
    "minecraft:empty_map",
    "minecraft:filled_map",
    "minecraft:nautilus_shell"
    ]
offHandItemListStr = str(   [ f"{i}:  {x}" for i, x in enumerate(OFFHAND_ITEM_LIST) ]  )
offHandItemListStr = offHandItemListStr.replace("', '", '\n')
offHandItemListStr = offHandItemListStr.strip("[] '")


with open("entity/player.entity.json") as f:
    data = js.load(f)                           # Open the file and load it as a dictionary

while True:
    # Acquire the new item to be used as trigger
    print(offHandItemListStr)
    new_trigger = input(MESSAGE)

    if new_trigger.isdigit():                               # If it is a number (an option from the list)
        new_trigger = int(new_trigger)                      # Cast to int
        if new_trigger < len(OFFHAND_ITEM_LIST):            # Check if out of bounds
            new_trigger = OFFHAND_ITEM_LIST[new_trigger]    # Assign the value from the list
            break                                           # Exit the loop
        else:
            print("Number is too high! Try again.")         # If the number's too high, warn the user
    else:
        new_trigger = new_trigger.replace(' ', "")      # Remove eventual spaces from the string
        new_trigger = new_trigger.strip('''"' ''')      # Remove eventual spaces or quotes at the beginning or ending of the string
        if not new_trigger.startswith("minecraft:"):    # Check that the input starts with the "minecraft:" prefix. If not, acquire it again
            print('Identifiers start with "minecraft:". Make sure to include it and to write it correctly')
        else:
            break   # Exit the loop

# Loop exit
# Create the new molang expression
new_molang = f"variable.render_chunk = q.is_item_name_any('slot.weapon.offhand', 0, '{new_trigger}') && !(q.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:crossbow') || q.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:bow')) && !q.is_in_ui && !v.is_first_person;"

# Write the new molang in the file
for i, j in enumerate(data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"]):
    if j.startswith("variable.render_chunk"):  
        data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"][i] = new_molang      # Find the old molang expression and replace it with the new one
        break
else:
    data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"].append(new_molang)       # If the molang expression is not present, add it

with open("entity/player.entity.json", 'w') as f:       # Open the file again and write the new json
    js.dump(data, f, indent=4)

print("Done! For more advanced configurations, I suggest you edit the json file yourself :D")