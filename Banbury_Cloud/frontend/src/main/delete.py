import logging
from flask import Flask,request, jsonify
import sys
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import os
import socket
from dotenv import load_dotenv





def connect_to_relay_server():
    load_dotenv()
    RELAY_HOST = os.getenv("RELAY_HOST")
    RELAY_PORT = 8002

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((RELAY_HOST, RELAY_PORT))
    return sender_socket



def delete_file(files):


    file_path = files

    file_name = os.path.basename(f"~/BCloud/{file_path}")

    sender_socket = connect_to_relay_server()

    print(f"File Name: {file_name}")
    file_header = f"FILE_DELETE_REQUEST:{file_name}:"
    sender_socket.send(file_header.encode())
    sender_socket.send(b"END_OF_HEADER") # delimiter to notify the server that the header is done

    return


def request_file_test():
    # Log a debug message

    # Get the JSON data sent with the POST request
    data = request.get_json()

    # You can now access `files` sent in the request body
    files = data.get('files', [])

    # Perform your logic here with the received files list
    # For example, prepare the requested files for download

    # Respond back with a message or relevant data
    response = jsonify({'message': 'Requesting file...', 'receivedFiles': files})
    return response


def main():

    if len(sys.argv) > 1:
        files = sys.argv[1]
        print(f"Argument received: {files}")
    else:
        print("No argument received.")
        files = "chamonix.mp4"

    delete_file(files)

if __name__ == '__main__':
    main()

