import logging
from flask import Flask,request, jsonify
import sys
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import os
import socket
from dotenv import load_dotenv
import shutil
from receiver5 import small_send_device_info

def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = "34.28.13.79" 
    RELAY_PORT = 8002

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket


def upload_file(file_path):
    print("Uploading file")
    print(file_path)

    directory_name = "BCloud"
    directory_path = os.path.expanduser(f"~/{directory_name}")

    # Use shutil to copy the file
    # shutil.copy(source, destination) will copy the file to the destination directory
    # If you want to keep the original filename, you can use os.path.basename(file_path)
    try:
        shutil.copy(file_path, directory_path)
        print(f"File copied successfully to {directory_path}")
    except Exception as e:
        print(f"Error copying file: {e}")
    try:

        sender_socket = connect_to_relay_server() 
        small_send_device_info(sender_socket)

        sender_socket.close()
        print("File uploaded to Cloud")
    except Exception as e:
        print(f"Error uploading to cloud: {e}")

    sys.stdout.flush()
def main():

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Argument received: {file_path}")
    else:
        print("No argument received.")
        file_path = "sender3.py"

    upload_file(file_path)

if __name__ == '__main__':
    main()




