from bot_core import Chatbot
bot = Chatbot(base_dir=".")
print(bot.get_answer("pip install numpy"))
print(bot.get_answer("How do I create a virtual environment in Python?"))
print(bot.get_answer("scikit learn"))
