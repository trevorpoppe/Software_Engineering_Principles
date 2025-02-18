# Smart Home API Project

This repository contains four different API files: device_API, house_API, rooms_API, and user_API. Each of these files/folders contains the JSON structure code that is organized in CRUD format (create[POST], read[GET], update[PUT], delete[DELETE]).

# Device_API

This folder contains two .py files: devices_api.py and devices_unit_test.py. The first file is the function code formatted using the CRUD design. With the help of ChatGPT, the recommendation to utilize the FastAPI application for this code was incorporated.

  - Create: @app.post("/devices", response_model=Device)
      - The function generates a "device id" by incrementing a device_id_counter variable by one when a new device is added to the smart home system.
  - Read: @app.get("/devices/{id}", response_model=Device)
      - This function returns an existing device by prompting the user to input the device id.
      - If the device is not found, a 404 error will appear with the message "Device not found"
  - Update: @app.put("/devices/{id}", response_model=Device)
    - The function allows the user to update the device_id to any integer.
    - If the original device is not found, a 404 error will appear with the message "Device not found"
  - Delete: @app.delete("/devices/{id}")
    - The function allows the user to delete an existing device.
    - Once the device is deleted, the message "Device deleted successfully" displays
    - If the device the user wishes to delete is not recognized, a 404 error will be prompted with the message "Device not found"
   
# House_API

This JSON formatted file contains the input and expected responses for creating and modifying the houses the user wishes to include in their smart home network.

  - Create House:
    - The user is prompted to enter the house name, address, gps coordinates, owner id, and occupant id.
    - The output will generate a unique id for the house the user wishes to add.
  - Read House:
    - This function allows the user to retrieve information about an existing house with a house id.
  - Update House:
    - When updating a house, the user must first retrieve the house they wish to update.
    - In this input-output example, the user is able to update any of the original fields that were used to create the home.
  - Delete House:
    - The user can choose to delete an existing house with a house id.
    - When the user deletes the home, the message "House deleted successfully will appear.
  - Finally, there is a handy function that allows the user to list the existing houses on their account.

# Rooms_API

This JSON formatted file contains the input and expected responses for creating and modifying the rooms the user wishes to include in their smart home network.

  - Create Room:
      - The user is prompted to enter the room name, floor, size, house id, and type of room.
      - The output will generate a unique id for the room the user wishes to add.
    - Read Room:
      - This function allows the user to retrieve information about an existing room with a room id.
    - Update Room:
      - When updating a room, the user must first retrieve the room they wish to update.
      - In this input-output example, the user is able to update any of the original fields that were used to create the room.
    - Delete Room:
      - The user can choose to delete an existing room with a room id.
      - When the user deletes the room, the message "Room deleted successfully will appear.
    - Finally, there is a handy function that allows the user to list the existing rooms on their account.

# User_API

This JSON formatted file contains the input and expected responses for creating and modifying the users the user wishes to include in their smart home network.

  - Create User:
      - The user is prompted to enter the user name, username, phone number, and email.
      - The output will generate a unique id for the user the user wishes to add.
    - Read User:
      - This function allows the user to retrieve information about an existing user with a user id.
    - Update User:
      - When updating a user, the user must first retrieve the user they wish to update.
      - In this input-output example, the user is able to update any of the original fields that were used to create the user.
    - Delete User:
      - The user can choose to delete an existing user with a user id.
      - When the user deletes the user, the message "User deleted successfully will appear.

