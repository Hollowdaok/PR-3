# PR-3
This is a Telegram bot built using Python and the pyTelegramBotAPI library. The bot allows users to browse products from a SQLite database, add them to a cart, and place orders.

Features

Start with /start or /help command to get category selection.

Inline buttons for product categories: Cheese, Sausage, Candies.

Display available products in a selected category.

Add products to the cart with quantity tracking.

View the cart with /cart.

Clear the cart or place an order.

Direct access to categories using /cheese, /sausage, or /candies.

Requirements

Ensure you have the following installed:

Python 3.x

pyTelegramBotAPI library

SQLite3 for database management

Install dependencies:

pip install pyTelegramBotAPI

Setup

Create a Telegram bot using BotFather and get the bot token.

Update the bot = telebot.TeleBot('YOUR_BOT_TOKEN') line in the script with your bot token.

Ensure you have an SQLite database products.db with a table products containing columns: id, name, weight, price, image_url, category.

Running the Bot

Execute the script:

python main.py

The bot will start polling for messages.

Database Structure

The products.db SQLite database should have the following schema:

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    weight TEXT,
    price REAL,
    image_url TEXT,
    category TEXT NOT NULL
);

Ensure that each product entry has a corresponding category (cheese, sausage, candies).

Usage

Start the bot: /start

Select a category via buttons.

Browse products and add them to the cart.

View cart: /cart

Clear cart or place an order using inline buttons.
