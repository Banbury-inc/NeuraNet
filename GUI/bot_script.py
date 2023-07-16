import sys

# Read user input from standard input
user_input = sys.stdin.readline().rstrip()

# Echo the user's input as the bot's response
bot_response = f"You said: {user_input}"

# Write the bot's response to standard output
sys.stdout.write(bot_response)
sys.stdout.flush()
