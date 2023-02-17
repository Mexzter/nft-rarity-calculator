import os
import json
import ctypes
import time


# Set the directory to search for JSON files


os.system('cls')

ctypes.windll.kernel32.SetConsoleTitleW('NFT Calc by Mexzter#0001')

banner = f'''
____ ____ ____ _ ___ _   _    ___ ____ ____ _    
|__/ |__| |__/ |  |   \_/      |  |  | |  | |    
|  \ |  | |  \ |  |    |       |  |__| |__| |___ 
                                                 
----------------> Mexzter#0001 <----------------

'''

print(banner)
dir_path = input('Path to json files -> ')

num_files = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
print(f'[!] Found {num_files} files\n\n')

file_name = input('What would you like to name the save file? -> ')



start = time.time()
# Define an object to store the rarity counts of each trait type and value
rarity_counts = {}

# Read the directory contents and filter for JSON files
with os.scandir(dir_path) as entries:
    json_files = [entry for entry in entries if entry.is_file() and entry.name.endswith('.json')]

    # Iterate over each JSON file and process its attributes
    for file in json_files:
        with open(file, 'r') as f:
            data = f.read()
            json_data = json.loads(data)
            attributes = json_data.get('attributes', [])
            if attributes:
                # Iterate over each trait map in the attributes list
                for trait_map in attributes:
                    # Iterate over each key-value pair in the trait map
                    for key, value in trait_map.items():
                        if key == 'trait_type':
                            # Extract the trait type
                            type = value

                            # Extract the trait value
                            trait_value = trait_map.get('value')

                            # Increment the rarity count for the trait type and value
                            if type not in rarity_counts:
                                rarity_counts[type] = {'count': 1, 'values': {trait_value: 1}}
                            else:
                                rarity_counts[type]['count'] += 1
                                if trait_value not in rarity_counts[type]['values']:
                                    rarity_counts[type]['values'][trait_value] = 1
                                else:
                                    rarity_counts[type]['values'][trait_value] += 1

# Write the rarity counts to a file after all JSON files have been processed
with open(f'{file_name}-attributes.json', 'w') as f:
    json.dump(rarity_counts, f, indent=2)

print(f'Found traits have been saved to {file_name}-attributes.json')

# Read the rarity counts from the file
with open(f'{file_name}-attributes.json', 'r') as f:
    rarity_counts = json.load(f)

# Define an array to store the calculated rarity values for each JSON file
calculated_rarity = []

# Read the directory contents and filter for JSON files
json_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith('.json')]

# Iterate over each JSON file and process its attributes
for file in json_files:
    with open(os.path.join(dir_path, file), 'r') as f:
        json_data = json.load(f)
        attributes = json_data.get('attributes', [])
        total_rarity = 1
        # Iterate over each trait map in the attributes list
        for trait_map in attributes:
            # Iterate over each key-value pair in the trait map
            for key, value in trait_map.items():
                if key == 'trait_type':
                    # Extract the trait type
                    trait_type = value

                    # Extract the trait value and its rarity count
                    trait_value = trait_map.get('value', '')
                    rarity = rarity_counts.get(trait_type, {}).get('values', {}).get(trait_value)

                    # Multiply the trait's rarity value with the running total
                    if rarity:
                        total_rarity *= rarity
        name_only = os.path.splitext(file)[0]
        calculated_rarity.append({'file': name_only, 'rarity': total_rarity})
calculated_rarity.sort(key=lambda item: item['rarity'])
top_256 = calculated_rarity[:num_files]
top_256_with_rank = [{'rank': i+1, 'file': item['file'], 'rarity': item['rarity']} for i, item in enumerate(top_256)]
with open(f'{file_name}.json', 'w') as f:
    json.dump(top_256_with_rank, f, indent=2)

os.system('cls')
ctypes.windll.kernel32.SetConsoleTitleW('NFT Calc by Mexzter#0001')
print(banner)
print('Top 10 list:')
# Display the top 100 list
top_100 = calculated_rarity[:10]
for i, item in enumerate(top_100):
    print(f'Rank #{i+1} - ID {item["file"]} - Rarity value {str(item["rarity"]/100000)[:5]}')
end = time.time()
print(f'\n\nOperation took -> {str(end - start)[:6]} ms to')
