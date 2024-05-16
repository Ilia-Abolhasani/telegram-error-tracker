import asyncio
import traceback
from telegram import Bot
from telegram.error import TelegramError


class Telelog:
    def __init__(self, token, chat_id, verbose=False):
        self.verbose = verbose
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.log_file = "telelog.log"

    def _log(self, text):
        if self.verbose:
            print(text)
        with open(self.log_file, "a") as file:
            file.write(text + "\n")

    def send_traceback(self, error_message, reply_to_message_id=None):
        error_traceback = traceback.format_exc()
        message = f"Error: {error_message}\n\nTraceback:\n{error_traceback}"
        try:
            message_sent = asyncio.run(
                self.bot.send_message(chat_id=self.chat_id, text=message, reply_to_message_id=reply_to_message_id)
            )
            if message_sent:
                self._log("Error message sent successfully.")
            else:
                self._log("Error sending message: Unknown error")
        except TelegramError as e:
            self._log(f"Error sending message: {e}")
