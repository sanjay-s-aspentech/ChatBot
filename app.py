from flask import Flask, request, jsonify, render_template, session
import json
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import re
secret_key=os.urandom(24)
app = Flask(__name__)
app.secret_key = secret_key  # Replace with your secret key

# Load intents data
try:
    with open('intents.json') as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Error: intents.json file not found.")
    intents = {'intents': []}  # Fallback to an empty structure

# Load dynamic product data
try:
    with open('cleaned_products.json') as file:
        product_data = json.load(file)
except FileNotFoundError:
    print("Error: cleaned_products.json file not found.")
    product_data = []  # Fallback to an empty structure
# Load product descriptions
try:
    with open('product_descriptions.json') as file:
        product_descriptions = json.load(file)
except FileNotFoundError:
    print("Error: product_descriptions.json file not found.")
    product_descriptions = {} 
# Prepare data for intent recognition
patterns = []
tags = []
responses = {}

for intent in intents['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

# Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns)
y = np.array(tags)

# Train the model
model = MultinomialNB()
model.fit(X, y)

# Function to predict intent
def predict_intent(user_message):
    message_vector = vectorizer.transform([user_message])
    predicted_tag = model.predict(message_vector)[0]
    return predicted_tag

# Function to find products and categories
def find_product_info(user_message):
    user_message = user_message.lower()
    found_products = []
    found_category = None

    # Check for products in each category
    for category in product_data:
        for product in category['products']:
            if product.lower() in user_message:
                found_products.append(product)
                found_category = category['category']

    return found_products, found_category

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['message'].strip().lower()
    bot_response = None
    predicted_tag = None  

    # Check for product information first
    found_products, found_category = find_product_info(user_message)
    
    if found_products:
        descriptions = []
        for product in found_products:
            if product in product_descriptions:
                descriptions.append(product_descriptions[product])
        
        if descriptions:
            product_list = "\n• ".join(found_products)  # Format products with bullet points
            descriptions_text = "\n".join(descriptions)
            bot_response = f"\n• {product_list} is a part of {found_category.capitalize()} category:\n\nDescriptions:\n{descriptions_text}"
        else:
            product_list = "\n• ".join(found_products)  # Format products with bullet points
            bot_response = f"\n• {product_list} is a part of {found_category.capitalize()} category:\n\nI have no descriptions for these products."
    else:
        # Check for specific queries about categories
        if "how many categories" in user_message or "list all the categories" in user_message:
            num_categories = len(product_data)
            categories_list = "\n• ".join([product['category'] for product in product_data])  # Format categories with bullet points
            bot_response = f"There are {num_categories} categories:\n• {categories_list}"
        elif "how many products in" in user_message:
            category_name = user_message.split("how many products in")[-1].strip()
            category = next((cat for cat in product_data if cat['category'].lower() == category_name.lower()), None)
            if category:
                num_products = len(category['products'])
                products_list = "\n• ".join(category['products'])  # Format products with bullet points
                bot_response = f"There are {num_products} products in the {category_name} category:\n\n• {products_list}"
            else:
                bot_response = "Sorry, I couldn't find that category."
        else:
            # Retrieve response based on predicted intent
            if predicted_tag in responses:
                                # Check if a URL is associated with this tag
                url = next((intent.get("url", "") for intent in intents['intents'] if intent['tag'] == predicted_tag), None)
                if url:
                    bot_response =  f"Here is the link you requested: <a href='{url}' target='_blank'>{url}</a>"
                else:
                    bot_response = random.choice(responses[predicted_tag])
                # bot_response = random.choice(responses[predicted_tag])
            else:
                # Fallback to unknown tag response for unrecognized inputs
                bot_response = random.choice(responses['unknown'])

    # Store context in session only if predicted_tag is defined
    if predicted_tag is not None:
        session['last_intent'] = predicted_tag

    return jsonify({'response': bot_response})

@app.route('/feedback', methods=['POST'])
def feedback():
    user_feedback = request.form['feedback']
    last_intent = session.get('last_intent')

    # Store feedback (in a real application, you would save this to a database)
    print(f"User feedback for intent {last_intent}: {user_feedback}")

    return jsonify({'response': 'Thank you for your feedback!'})

if __name__ == "__main__":
    app.run(debug=True)