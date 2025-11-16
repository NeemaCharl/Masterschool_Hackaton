import random
import wikipedia


items = [
    "Barack Obama",
    "French Revolution",
    "Marie Curie",
    "Apollo 11",
    "Leonardo da Vinci",
    "World War II",
    "Ada Lovelace",
    "Industrial Revolution"
]


# Select a random item from the list
chosen = random.choice(items)
print(f"Selected: {chosen}")

# Retrieve and print the Wikipedia summary for that item
summary = wikipedia.summary(chosen, sentences=2, auto_suggest=False)
summary = summary.replace(chosen, "__________")
print("Wikipedia summary:")
print(summary)
