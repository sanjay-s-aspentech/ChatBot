# Chatbot Project

This project implements a simple chatbot using Flask, which can provide information about products and their descriptions. The chatbot utilizes machine learning for intent recognition and can respond to user queries regarding product categories and details.

## Project Structure


### 1. `app.py`

This is the main application file that contains the Flask web server and the chatbot logic. It handles user input, predicts intents, and retrieves product information and descriptions. Key functionalities include:

- Loading intents and product data from JSON files.
- Predicting user intent using a Naive Bayes classifier.
- Finding products and categories based on user queries.
- Responding with product descriptions or default messages.

### 2. `cleaned_products.json`

This JSON file contains structured data about products and their respective categories. It should be formatted as a list of categories, where each category contains a list of products. Example structure:

```json
[
        {
        "category": "Exchanger Design & Rating",
        "products": [
            "Aspen Air Cooled Exchanger",
            "Aspen Fired Heater",
            "Aspen Plate Exchanger",
            "Aspen Plate Fin Exchanger",
            "Aspen Shell & Tube Exchanger",
            "Aspen Shell & Tube Mechanical",
            "Aspen Coil Wound Exchanger"
        ]
    },
    {
        "category": "Concurrent FEED",
        "products": [
            "Aspen Capital Cost Estimator",
            "Aspen In-Plant Cost Estimator",
            "Aspen Process Economic Analyzer",
            "Aspen OptiPlant 3D Layout",
            "Aspen OptiRouter",
            "Aspen Basic Engineering"
        ]
    },
]
```
### 3. intents.json
```json
{
    "intents": [
        {
            "tag": "greeting",
            "patterns": ["Hi", "Hello", "How are you?"],
            "responses": ["Hello!", "Hi there!", "How can I help you?"]
        },
        {
            "tag": "goodbye",
            "patterns": ["Bye", "See you later", "Goodbye"],
            "responses": ["Goodbye!", "See you later!", "Have a great day!"]
        }
    ]
}
```
### 4. products descriptions
```json
{
    "Aspen HYSYS": "AspenHYSYS is a process simulation software used for modeling and optimizing chemical processes.",
    "Aspen HYSYS Crude": "Aspen HYSYS Crude is designed for modeling crude oil processing.",
    "Acid Gas Cleaning": "Acid Gas Cleaning is a technology used to remove acid gases like H2S and CO2 from natural gas.",
}
```

# How to Run the Chatbot
## Step-1: Clone the Repository
        ```
        git clone <https://github.com/your-username/chatbot.git>
        ```
## Step-2: Install dependencies
         ```
         pip install -r requirements.txt
         ```
## Step-3: Run the chatbot using the command 
        ```
        python chatbot.py
        ```
## Step-4: Access the chatbot
Open a web browser and navigate to `http://localhost:5000/` to interact with it ....

## Author

**Sanjay S**  
Sanjay.S@aspentech.com

## Copyright

© 2024 [Sanjay S].
