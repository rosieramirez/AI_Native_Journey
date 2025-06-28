# This script greets the user and calculates a lucky number
name = input("What's your name? ")
favorite_number = 7
lucky_number = favorite_number * 2
print(f"Nice to meet you, {name}!")
print(f"Your lucky number is: {lucky_number}")
print("Have a great day!")

# Add a pause so we can see the output
print("\nPress Enter to exit...", end='', flush=True)
input()