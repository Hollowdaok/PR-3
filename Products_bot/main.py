import telebot
import sqlite3
# Ініціалізація бота з токеном
bot = telebot.TeleBot('7899158320:AAEpw7sQE7lNVtlGnpcVYTSxg88V0v8rO20')

cart = {}
# Обробник команди /start та /help
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    conn=sqlite3.connect('products.db')
    
    bot.send_message(message.chat.id, f"""\
Привіт {message.from_user.first_name}, я допоможу тобі з вибором продуктів.
""")
    
    markup = telebot.types.InlineKeyboardMarkup()
    
    markup.add(telebot.types.InlineKeyboardButton(text='🧀 Сир', callback_data='cheese'))
    markup.add(telebot.types.InlineKeyboardButton(text='🥩 Ковбаса', callback_data='sausage'))
    markup.add(telebot.types.InlineKeyboardButton(text='🍬 Цукерки', callback_data='candies'))
    
    bot.send_message(message.chat.id, 'Вибери категорію товару:', reply_markup=markup)
# Функція для відображення товарів певної категорії
def send_products_list(chat_id, category):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, weight, price, image_url FROM products WHERE category = ?", (category,))
    products = cursor.fetchall()
    conn.close()

    bot.send_message(chat_id, "🛍 Вот такі є товари в цій категорії:")

    total_products = len(products)

    for index, product in enumerate(products):
        name, weight, price, image_url = product

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="🛒 Додати в кошик", callback_data=f"add_{name}"))

        bot.send_photo(chat_id, image_url, caption=f"🔹 Назва: {name}\n📦 Вага: {weight}\n💰 Ціна: {price} грн.", reply_markup=markup)

        if index == total_products - 1:
            bot.send_message(chat_id, "Також ви можете перейти одразу до інших категорій ввівши відповідні команди:/cheese, /sausage, /candies. Щоб перейти до кошика, введіть команду /cart.")
# Обробник команд /cheese, /sausage, /candies
@bot.message_handler(commands=['cheese', 'sausage', 'candies'])
def handle_category_command(message):

    category = message.text[1:]
    send_products_list(message.chat.id, category)
# Обробник натискання кнопок категорій
@bot.callback_query_handler(func=lambda call: call.data in ["cheese", "sausage", "candies"])
def handle_callback_query(call):
    send_products_list(call.message.chat.id, call.data)
    
# Обробник додавання товару в кошик
@bot.callback_query_handler(func=lambda call: call.data.startswith("add_"))
def handle_add_to_cart(call):
    user_id = call.from_user.id
    product_name = call.data[4:]
    
    if user_id not in cart:
        cart[user_id] = {}

    if product_name in cart[user_id]:
        cart[user_id][product_name] += 1
    else:
        cart[user_id][product_name] = 1
    
    bot.answer_callback_query(call.id, text=f"Продукт {product_name} додано до кошика (x{cart[user_id][product_name]}).")

# Обробник команди /cart для перегляду кошика
@bot.message_handler(commands=['cart'])
def view_cart(message):
    user_id = message.chat.id
    
    if user_id not in cart or not cart[user_id]:
        bot.send_message(user_id, "🛒 Ваш кошик порожній.")
    else:
        cart_items = "\n".join([f"🔹 {item} {count} шт." for item, count in cart[user_id].items()])
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="🛍 Оформити замовлення", callback_data="order"))
        markup.add(telebot.types.InlineKeyboardButton(text="🗑 Очистити кошик", callback_data="clear_cart"))
        
        bot.send_message(user_id, f"🛒 Ваш кошик:\n\n{cart_items}", reply_markup=markup)

# Обробник оформлення замовлення
@bot.callback_query_handler(func=lambda call: call.data == "order")
def order_cart(call):
    user_id = call.message.chat.id
    
    if user_id not in cart or not cart[user_id]:
        bot.answer_callback_query(call.id, text="Ваш кошик порожній!")
        return
    
    cart_summary = "\n".join([f"🔹 {item} {count} шт." for item, count in cart[user_id].items()])
    bot.send_message(user_id, f"✅ Замовлення оформлене! Дякую за покупку!\n\nВаше замовлення:\n{cart_summary}")
    
    cart[user_id] = {}

# Обробник очищення кошика
@bot.callback_query_handler(func=lambda call: call.data == "clear_cart")
def clear_cart(call):
    user_id = call.message.chat.id

    bot.answer_callback_query(call.id, text="🗑 Кошик очищено!")
    if user_id in cart:
        cart[user_id] = {}

    bot.send_message(user_id, "Ваш кошик порожній.")

    
bot.infinity_polling()