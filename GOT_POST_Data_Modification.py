import requests

path = "https://thronesapi.com/api/v2/Characters"

data = {
    "id": "1",
    "firstName": "New_first_name",
    "lastName": "New_last_name",
    "fullName": "New_full_name",
    "title": "New_title",
    "family": "New_family",
    "image": "New_image",
    "imageUrl": "https://thronesapi.com/assets/images/new_image_path.jpg"
}

# sending a POST request with data
post_response = requests.post(path, json=data)  # Setting the request body in JSON format
print("\nThe status code of the POST request is:", post_response.status_code)

# checking the status code for the POST request
if post_response.status_code == 200:
    print("Data was added successfully via a POST request.")
else:
    print("POST request encountered an error with status code:", post_response.status_code)

# sending an empty POST request
empty_post_response = requests.post(path)
print("The status code of the empty POST request is:", empty_post_response.status_code)

# checking the status code for the empty POST request
if empty_post_response.status_code == 200:
    print("Empty POST request succeeded.")
else:
    print("Empty POST request encountered an error with status code:", empty_post_response.status_code)

# sending a GET request to retrieve data about the character with ID 1
get_response = requests.get(f"{path}/1")

# checking the status code for the GET request
if get_response.status_code == 200:
    print("Response to the GET request is:", get_response.json())

    # checking if the character data has been updated
    if get_response.json() == data:
        print("Data has been successfully updated.\n")
    else:
        print("Data has not been updated.\n")
else:
    print("GET request did not succeed.\n")