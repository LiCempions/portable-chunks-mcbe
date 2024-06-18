import json as js

with open("entity/player.entity.json") as f:
    data = js.load(f)                           # Open the file and load it as a dictionary

while True:
    # Acquire the new item to be used as trigger
    new_trigger = input("Insert the identifier of the item to be used as the new trigger (example: minecraft:firework_rocket). Make sure it's an item you can hold in your offhand.\n")
    new_trigger = new_trigger.strip('''"' ''')      # Remove eventual spaces or quotes at the beginning or ending of the string
    if not new_trigger.startswith("minecraft:"):    # Check that the input starts with the "minecraft:" prefix. If not, acquire it again
        print('Identifiers start with "minecraft:". Make sure to include it and to write it correctly')
    else:
        break

# Create the new molang expression
new_molang = f"variable.render_chunk = q.is_item_name_any('slot.weapon.offhand', 0, '{new_trigger}') && !(q.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:crossbow') || q.is_item_name_any('slot.weapon.mainhand', 0, 'minecraft:bow')) && !q.is_in_ui && !v.is_first_person;"

for i, j in enumerate(data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"]):
    if j.startswith("variable.render_chunk"):  
        data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"][i] = new_molang      # Find the old molang expression and replace it with the new one
        break
else:
    data["minecraft:client_entity"]["description"]["scripts"]["pre_animation"].append(new_molang)       # If the molang expression is not present, add it

with open("entity/player.entity.json", 'w') as f:       # Open the file again and write the new json
    js.dump(data, f, indent=4)

print("Done! For more advanced configurations, I suggest you edit the json file yourself :D")