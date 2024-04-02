# The transition from bcloud 1.0.0 to 1.0.1 

The transition will involve the transition from ipfs to just a typical relay server.
This will completely remove all functionality related to ipfs for the time being.
Implementing the relay server will involve changing a lot of the functions
so they use the relay server instead of tapping into ipfs api

# To Do

- Make the relay server absolutely bulletproof
- It just took 30 seconds to download a video. Print some sort of feedback to the client
so they are able to tell what is going on. 
    - feedback after each chunk is downloaded
- get the relay server to send out pings to all of the devices
- get the relay server to properly handle connections that are lost. remove them from the list
of client addresses.
- get the bcloud server to automatically launch the python file on startup


# Functions that need to be changed

- download_file
    - with this particular function, I need to change the logic so I am able to
    request a file from a specific device.
    - server looks through the database to see what device contains the file,
    send a request to the device to send the file, have the device send the file.
    All of this communication done through the relay server.
- upload_file 
- ping_device
- delete_file
    - right now delete file only removes it from the database.

# Threads for the BCloud Server
- Relay Server
- Ping Devices
- Website
- The BCloud Server can be its own device in the Bcloud
- Traffic Monitoring of how many people are hitting website, relay server, do analytics





