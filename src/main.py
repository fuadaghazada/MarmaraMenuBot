from bot import sendMessage, update_bot
from scraper import fetch_todays_menu, process_meal

'''
    Bot function
'''
def bot_func(text = '', chat_id = ''):
    if text == '/start' or text == '/help':
        sendMessage("Hello, I am Marmara Menu Bot!\n You can: \n\t/fix - For having today's fix menu \n\t/alt - For having today's alternative menu \n\n\nBon Apetite!", chat_id)
    elif text == '/fix':
        meal = fetch_todays_menu()['fix']
        sendMessage('*Fix Menu*\n___Lunch___\n\n' + meal['lunch'], chat_id)
        sendMessage('___Dinner___\n\n' + meal['dinner'], chat_id)
    elif text == '/alt':
        meal = fetch_todays_menu()['alt']
        sendMessage('*Alternative Menu*\n\n' + meal['lunch'], chat_id)
    else:
        sendMessage('I dont understand you :(\n', chat_id)

if __name__ == "__main__":
    update_bot(bot_func)
