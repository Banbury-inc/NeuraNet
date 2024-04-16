import logging
from flask import Flask,request, jsonify
import sys
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import os
import socket
from dotenv import load_dotenv
import shutil
from receiver5 import send_profile_info, small_send_device_info

def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = "34.28.13.79" 
    RELAY_PORT = 443

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket


def change_first_name(first_name, last_name, username, email, password):
    print("Uploading file")
    print(first_name)

    directory_name = "BCloud"
    directory_path = os.path.expanduser(f"~/{directory_name}")

    # Use shutil to copy the file
    # shutil.copy(source, destination) will copy the file to the destination directory
    # If you want to keep the original filename, you can use os.path.basename(file_path)
    try:

        sender_socket = connect_to_relay_server() 

        send_profile_info(sender_socket, first_name, last_name, username, email, password)

        sender_socket.close()
        print("File uploaded to Cloud")
    except Exception as e:
        print(f"Error uploading to cloud: {e}")

    sys.stdout.flush()
def main():

    if len(sys.argv) > 1:
        first_name = sys.argv[1]
        last_name = sys.argv[2]
        username = sys.argv[3]
        email = sys.argv[4]
        password = sys.argv[5]
        print(f"Argument received: {first_name}")
        change_first_name(first_name, last_name, username, email, password)
    else:
        print("No argument received.")
        first_name = "Michael"
        last_name = "Mills"
        username = "mmills6060"
        email = "mmills6060@gmail.com"
        password = "test"
        change_first_name(first_name, last_name, username, email, password)


if __name__ == '__main__':
    main()




