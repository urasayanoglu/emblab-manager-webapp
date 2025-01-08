from django.shortcuts import render
from django.http import HttpResponse
from src.local_ai_communicator import chat_with_ai, MODELS

"""
chat_with_ai function that is used in the ai_server_view is implemented under src/local_ai_communicator. 
It is a function that takes a user message and a model name as input and returns the AI response.
"""

# AI Server Interaction
def ai_server_view(request):

    # Initialize ai_response to None or an empty string for GET requests
    ai_response = None

    if request.method == "POST":
        # Fecth the model and user input from the POST request
        model_name = request.POST.get("model")
        user_message = request.POST.get("input")

        if model_name not in MODELS:
            return HttpResponse("Invalid model selected!", status=400)

        # Get the AI response using the provided message and model
        ai_response = chat_with_ai(user_message, model_name)

    # Display the page with the available models
    return render(
        request, "aiserver/ai-server.html", {
            "models": MODELS, "ai_response": ai_response}
    )
