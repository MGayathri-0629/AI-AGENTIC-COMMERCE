# AI-Powered Product Recommendation and Sales Assistant

## Track
CODTECH - Track 1: AI Growth & Agentic Commerce

## Project Overview
This project is a web-based product recommendation and sales assistant. A user enters a requirement and optional budget/category. The recommendation engine analyzes the user's keywords against product information and ranks suitable products. A simple conversational assistant also helps users discover products.

## Problem Solved
Customers can find it difficult to choose products from many options. This application reduces that difficulty by giving personalized recommendations based on requirements, budget, and category.

## Technologies
- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript

## Main Features
1. Product catalog stored in a database.
2. Keyword-based recommendation engine.
3. Budget filtering.
4. Category filtering.
5. Simple conversational sales assistant.
6. Responsive web interface.

## How to Run

### 1. Open the project in VS Code
Open this folder in VS Code.

### 2. Create a virtual environment
Windows:
```bash
python -m venv venv
```

Activate it:
```bash
venv\Scripts\activate
```

### 3. Install Flask
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
Go to:
`http://127.0.0.1:5000`

The `products.db` SQLite database is created automatically when the application starts.

## Example Test
Requirement:
`I need something for coding under 3000`

Budget:
`3000`

The application will recommend products that match coding/computer-related keywords and are within the budget.

## Project Objectives
- Provide personalized product recommendations.
- Reduce the time customers spend searching for products.
- Use customer requirements and budget to rank products.
- Provide a simple conversational shopping experience.
- Demonstrate an AI-style recommendation workflow for commerce.

## Future Enhancements
- Add a real LLM API.
- Add user login and order history.
- Add payment gateway integration.
- Add product images and reviews.
- Add advanced machine-learning recommendation models.
