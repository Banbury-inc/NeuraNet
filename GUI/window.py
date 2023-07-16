import tkinter as tk
from subprocess import Popen, PIPE

def send_message():
    user_message = user_input.get()

    display_message('User', user_message)
    display_message('Bot', 'Thinking...')
    
    # Pass user message to the Python script
    process = Popen(['python', 'Artificial_Intelligence\\conversation_mode_5.0.py'], stdin=PIPE, stdout=PIPE)
    output, _ = process.communicate(user_message.encode())
    bot_response = output.decode().strip()


    display_message('Bot', bot_response)

    user_input.delete(0, tk.END)

def display_message(sender, message):
    message_text = f"{sender}: {message}\n"
    chat_log.configure(state=tk.NORMAL)
    chat_log.insert(tk.END, message_text)
    chat_log.configure(state=tk.DISABLED)
    chat_log.see(tk.END)

def on_enter(event):
    send_button.invoke()

# Create the GUI window
window = tk.Tk()
window.title("Chatbot")
window.geometry("600x600")
window.configure(bg="#444444")

# Create the chat log area
chat_log = tk.Text(window, state=tk.DISABLED, bg="#333333", fg="white")
chat_log.pack(fill=tk.BOTH, expand=True)

# Create the user input area
user_input = tk.Entry(window, bg="white", fg="black", bd=0)
user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
user_input.bind("<Return>", on_enter)

# Create the send button
send_button = tk.Button(window, text="Send", command=send_message, bg="#666666", fg="white", bd=0, relief=tk.FLAT)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

window.mainloop()
