import datetime
import telebot

# Replace TOKEN with your bot's token
bot = telebot.TeleBot("5989533371:AAFUFFAwyHjteNnMpYPOJGK5AkssHkCn6Xk")

def calculate_date_difference(year, message):
    # Get the last day of the year
    last_day_of_year = datetime.date(year, 12, 31)

    # Get the input date from the message text
    input_date_str = message.text

    # Split the input string into its component parts (day, month, input_year)
    if "/" in input_date_str:
        day, month, input_year = input_date_str.split("/")
    elif "." in input_date_str:
        day, month, input_year = input_date_str.split(".")

    # Convert the strings to integers
    day = int(day)
    month = int(month)
    input_year = int(input_year)

    # Create a `datetime` object for the input date
    input_date = datetime.date(input_year, month, day)

    # Calculate the difference between the two dates
    date_difference = last_day_of_year - input_date

    # Finally, we can check if the difference is less than 183 days
    if date_difference.days < 183:
        # The difference is less than 183 days
        # Do something here
        days_count = date_difference.days
        bot.send_message(message.chat.id, f"В {year} году вы были вне России всего {days_count} дней. Это значит, что за {year} год вы остаётесь налоговым резидентом РФ, а ставка НДФЛ на доходы за {year} остаётся в размере 13%. При этом за {year} в российскую казну вам нужно будет уплатить налог на доходы зарубежом. В деталях  можно почитать в материале https://vc.ru/legal/555011-nalogovoe-nerezidentstvo-pt-2-izuchaem-zhizn-petra-i-ego-nalogi ")
    else:
        # The difference is 183 days or more
        # Do something else here
        days_count = date_difference.days
        bot.send_message(message.chat.id, f"В {year} году вы находились вне России {days_count} дней и, соответственно, меньше 183 дней в самой России. За {year} год вы теряете налоговое резидентство РФ, а ставка НДФЛ на ваши доходы в {year} году поднимается до 30%. При этом за {year} в России вам не придётся платить налог на доходы, полученные зарубежом. Все детали с примерами можно почитать в материале https://vc.ru/legal/555011-nalogovoe-nerezidentstvo-pt-2-izuchaem-zhizn-petra-i-ego-nalogi ")

# Add the start function as a handler for the /start command, handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    # Send a message to the user
    bot.send_message(message.chat.id, "Привет! За какой год вы хотите посчитать своё налогое резидентство в России? Укажите только год.")
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    try:
        year = int(message.text)
        if year < 100:
            year += 2000
        bot.send_message(message.chat.id, f"Спасибо! Теперь напишите дату выезда из России в формате 01.01.2022")
        bot.register_next_step_handler(message, lambda message: calculate_date_difference(year, message))
    except Exception as e:
        bot.send_message(message.chat.id, "Я могу подсказать, нужно ли вам платить больше налогов или не нужно. Можете, пожалуйста, указать год, в котором мне это нужно посчитать?")
        bot.register_next_step_handler(message, get_year)

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Calculate the date difference
    bot.send_message(message.chat.id, "Я могу подсказать, нужно ли вам платить больше налогов или не нужно. Можете, пожалуйста, указать год, в котором мне это нужно посчитать?")
    bot.register_next_step_handler(message, get_year)

# Start the bot
bot.polling()