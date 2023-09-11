import difflib
from collections import Counter

import requests

# define excluded families to be ignored
EXCLUDED_FAMILIES = {"None", "Unknown"}

# list of correctly spelled family names
CORRECT_FAMILIES = {
    "Baelish", "Baratheon", "Bolton", "Bronn", "Clegane", "Free Folk", "Greyjoy",
    "Lannister", "Lorath", "Mormont", "Naathi", "Naharis", "Qyburn", "Sand", "Seaworth",
    "Sparrow", "Stark", "Targaryen", "Tarly", "Tarth", "Tyrell", "Viper", "Worm"
}

# test the status code of a GET request
def test_get_request_status_code():
    response = requests.get("https://thronesapi.com/api/v2/Characters")
    if response.status_code == 200:
        print("Success! Status code is 200")
    else:
        print(f"Error! Status code is {response.status_code}")

# display character profiles
def character_profiles():
    response = requests.get("https://thronesapi.com/api/v2/Characters").json()
    for character in response:
        character_profile = (
            "ID:", character["id"],
            "FIRST NAME:", character["firstName"],
            "LAST NAME:", character["lastName"],
            "FULL NAME:", character["fullName"],
            "TITLE:", character["title"],
            "FAMILY:", character["family"],
            "IMAGE:", character["image"],
            "IMAGE URL:", character["imageUrl"]
        )
        print(character_profile)

# test data consistency based on character ID lookup
def test_data_consistency():
    characters_list = requests.get("https://thronesapi.com/api/v2/Characters").json()
    characters = {}

    for character in characters_list:
        character_id = character["id"]
        characters[character_id] = character

    for id in characters.keys():
        character_data = requests.get(f"https://thronesapi.com/api/v2/Characters/{id}").json()

        if character_data != characters[id]:
            print(f"Inconsistency in data for character with ID {id}")

    print("Data consistency check completed.")

# test character data
def test_character_data():
    character_data = requests.get("https://thronesapi.com/api/v2/Characters").json()

    for character_info in character_data:
        missing_data = []

        if "id" not in character_info or character_info["id"] is None:
            missing_data.append("ID")
        if not character_info.get("firstName"):
            missing_data.append("First Name")
        if not character_info.get("lastName"):
            missing_data.append("Last Name")
        if not character_info.get("fullName"):
            missing_data.append("Full Name")
        if not character_info.get("title"):
            missing_data.append("Title")
        if not character_info.get("family"):
            missing_data.append("Family")
        if not character_info.get("image"):
            missing_data.append("Image")
        if not character_info.get("imageUrl"):
            missing_data.append("Image URL")

        if missing_data:
            print(f"Character {character_info['id']} is missing data for: {', '.join(missing_data)}")
        else:
            print(f"Character {character_info['id']} has all data.")

# test character full names
def test_character_full_names():
    response = requests.get("https://thronesapi.com/api/v2/Characters").json()

    for character in response:
        first_name = character["firstName"].strip()
        last_name = character["lastName"].strip()
        full_name = character["fullName"].strip()

        if first_name and last_name and full_name != f"{first_name} {last_name}":
            print(f"ID: {character['id']}")
            print(f"First Name: {first_name}")
            print(f"Last Name: {last_name}")
            print(f"Full Name: {full_name}")
            print("Status: INCORRECT")
            print("-" * 30)

# helper function to format family names
def format_family_name(family):
    formatted_family = family.replace("House", "").strip()
    return formatted_family

# finding the closest correctly spelled family from the CORRECT_FAMILIES list
def find_closest_family(correct_family_name, CORRECRT_FAMILIES, EXCLUDED_FAMILIES):
    # the difflib library is used to find the closest match based on similarity.
    # the 'n' parameter is set to 1 to retrieve only the closest match.
    # the 'cutoff' parameter is set to 0.8, meaning that only matches with a similarity of 80% or higher are considered.
    closest_match = difflib.get_close_matches(correct_family_name, CORRECT_FAMILIES.union(EXCLUDED_FAMILIES), n=1, cutoff=0.8)
    
    if closest_match:
        return closest_match[0]
    else:
        # return the original family name if no close match is found
        return correct_family_name

def main():
    # fetch character data from the Thrones API
    response = requests.get("https://thronesapi.com/api/v2/Characters").json()

    # initialize counters and sets to track families
    family_counter = Counter()  # counter for counting occurrences of each family
    unique_families = set()      # set for storing unique formatted family names
    num_excluded_families = 0    # number of characters with excluded families
    characters_without_family = 0  # number of characters without a family

    # iterate through characters and analyze their family ties
    for character in response:
        family = character.get("family")
        if family and family.strip() != "":
            formatted_family = format_family_name(family)
            closest_correct_family = find_closest_family(formatted_family, CORRECT_FAMILIES, EXCLUDED_FAMILIES)

            if closest_correct_family:
                formatted_family_str = str(closest_correct_family)
                character["family"] = formatted_family_str

                if formatted_family_str not in EXCLUDED_FAMILIES:
                    family_counter[formatted_family_str] += 1
                    unique_families.add(formatted_family_str)
                else:
                    num_excluded_families += 1
            else:
                characters_without_family += 1
        else:
            characters_without_family += 1

    # helper function to print section headers
    def print_section_header(title):
        print("\n" + "=" * len(title))
        print(title)
        print("=" * len(title))

    # print section with a list of unique families and their statistics
    print_section_header("Families:")
    for index, family in enumerate(unique_families, start=1):
        print(f"{index}. {family}: {family_counter[family]}")

    # print section with character statistics
    print_section_header("Character Statistics:")
    total_characters = len(response)
    total_characters_without_family_or_excluded = characters_without_family + num_excluded_families
    total_characters_with_family = total_characters - total_characters_without_family_or_excluded

    print(f"Total characters: {total_characters}")
    print(f"Characters without a family: {characters_without_family}")
    print(f"Characters with excluded families: {num_excluded_families}")
    print(f"Total characters without a family or with excluded families: {total_characters_without_family_or_excluded}")
    print(f"Total characters with a family (excluding excluded families): {total_characters_with_family}")

    # print section with characters' family affiliations
    print_section_header("Character Family Affiliations:")
    for character in response:
        family = character.get("family")
        if family and family.strip() != "" and family not in EXCLUDED_FAMILIES:
            formatted_family = format_family_name(family)
            character["family"] = formatted_family
            if formatted_family in unique_families:
                print(f"{character['fullName']} belongs to the {formatted_family} family")
            else:
                print(f"{character['fullName']} has no family affiliation")
        else:
            print(f"{character['fullName']} has no family affiliation")

# test image paths
def test_image_paths():
    # fetch character data from the API
    character_data = requests.get("https://thronesapi.com/api/v2/Characters").json()

    for character_info in character_data:
        character_id = character_info["id"]
        image_path = character_info["imageUrl"]

        # check if the image path exists before sending a request
        if requests.head(image_path).status_code == 200:
            response = requests.get(image_path)

            if response.status_code == 200:
                print(f"Character ID: {character_id} - Image Path: {image_path} - Status Code: {response.status_code}")
            else:
                print(f"Character ID: {character_id} - Image Path: {image_path} - Status Code: {response.status_code} (Error)")
        else:
            print(f"Character ID: {character_id} - Image Path: {image_path} - Does not exist")

if __name__ == "__main__":
    print("\n")
    test_get_request_status_code()
    print("\n")
    character_profiles()
    print("\n")
    test_data_consistency()
    print("\n")
    test_character_data()
    print("\n")
    test_character_full_names()
    main()
    print("\n")
    test_image_paths()
    print("\n")