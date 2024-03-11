from datetime import datetime


def greeting():
    current_time = datetime.now()
    if current_time.hour < 12:
        greeting_message = "Добро утро"
    elif current_time.hour < 17:
        greeting_message = "Добър ден"
    elif current_time.hour < 21:
        greeting_message = "Добър вечер"
    else:
        greeting_message = "Спокойна вечер"

    return greeting_message
