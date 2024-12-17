#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   local_ai_communicator.py
@Time    :   17/12/2024 11:33:18
@Author  :   Uras Ayanoglu
@Version :   1.0
@Contact :   uras@ayanoglu.org
@GitHub  :   https://github.com/urasayanoglu
@License :   (C)Copyright 2024, Uras Ayanoglu
@Desc    :   This script facilitates real-time communication with an AI server running on a local network (via Tailscale).
'''

import requests
import json
from inventory.models import InventoryItem

# AI Server URL (Tailscale IP - Tailscale service is used with the Local-AI server when connecting from outside the local network)
# Replace with your Local-AI server IP address
API_URL = "http://100.113.165.114:8080/v1/chat/completions"
LocalAI_API_Key = "your_localai_api_key_here"  # Replace with your actual API Key
MODELS = [
    "codestral-22b-v0.1",
    "gpt-4",
    "gpt-4-vision-preview",
    "jina-reranker-v1-base-en",
    "meta-llama-3.1-8b-instruct",
    "stablediffusion",
    "text-embedding-ada-002",
    "tts-1",
    "whisper-1",
    "llava-v1.6-7b-mmproj-f16.gguf",]


def search_inventory_by_keywords(keywords):
    """
    This function searches the inventory based on provided keywords
    in both name and category fields (following ForeignKey relationships).
    """
    # Search for matches in the name field (direct CharField)
    name_matches = InventoryItem.objects.filter(name__icontains=keywords)

    # Search for matches in the related category name (ForeignKey relationship)
    category_matches = InventoryItem.objects.filter(
        category__name__icontains=keywords)

    # Combine both querysets (name_matches and category_matches) using union
    return name_matches.union(category_matches)


# Function to send a message and get a response
def chat_with_ai(message, model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LocalAI_API_Key}"
    }

    # The payload is the message and model you are using
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    # Sending the request to the server
    response = requests.post(API_URL, headers=headers,
                             data=json.dumps(payload))

    # Check if the response status code is OK (200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        ai_response = data['choices'][0]['message']['content']

        # Check if the user's message or AI response is related to the inventory
        # Keywords related to the inventory can be modified or expanded
        # Or totally a different approach can be implemented based on the requirements
        inventory_related_keywords = [
            "inventory", "circuit", "resistor", "oscilloscope", "PicoScope", "LED", "capacitor",
            "multimeter", "power supply", "soldering iron", "solder", "breadboard", "microcontroller",
            "Arduino", "Raspberry Pi", "sensor"]

        # Find specific keywords present in the user's message
        matched_keywords = [
            keyword for keyword in inventory_related_keywords if keyword.lower() in message.lower()]

        if matched_keywords:
            # Initialize an empty set to avoid duplicates
            inventory_items_set = set()

            # Search the inventory only for matched keywords
            for keyword in matched_keywords:
                items = search_inventory_by_keywords(keyword)
                inventory_items_set.update(items)

            # If any items were found, format the inventory response
            if inventory_items_set:
                inventory_response = ""
                for index, item in enumerate(inventory_items_set, start=1):
                    location = item.location if item.location else "location unknown"
                    inventory_response += f"{index}. {
                        item.name} located at {location}\n"

                return f"{ai_response}\n\nIn the Embedded Lab inventory, I found:\n\n{inventory_response.strip()}"

        # If no inventory items are found or the message isn't relevant, just return the AI response
        return ai_response

    else:
        return f"Error: {response.status_code}, {response.text}"


# Function to handle model selection
def select_model():
    print("\nAvailable Models: ")
    for i, model in enumerate(MODELS):
        print(f"{i+1}. {model}")

    # Validate user input for model selection
    while True:
        try:
            user_model = int(
                input("\nSelect your AI Model by entering corresponding model number (1-10): "))
            if 1 <= user_model <= len(MODELS):
                return MODELS[user_model - 1]
            else:
                print("Please enter a valid number between 1 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")


# Main chat loop
def main():
    print("Welcome to LocalAI Chat! Type 'exit' to quit.")

    # Select the model
    model = select_model()

    while True:
        # Get user input
        user_message = input("Your Message: ")

        if user_message.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        # Send the message to the AI server
        ai_response = chat_with_ai(user_message, model)

        # Print AI's response
        print(f"AI: {ai_response}")


if __name__ == "__main__":
    main()
