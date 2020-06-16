import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode, ReplyKeyboardMarkup, Update


logger = logging.getLogger(__name__)

class Telegram:
        
    def __init__(self, config):

        self._config = config

        """Start the bot."""
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self._updater = Updater(config["telegram"]["token"], use_context=True)

        # Get the dispatcher to register handlers
        dp = self._updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help_command))
    
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, self.echo))

        # Start the Bot
        self._updater.start_polling(
            clean=True,
            bootstrap_retries=-1,
            timeout=30,
            read_latency=60,)

        self._sendMessage("starting the Volume bot!")

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi! from Volume Monitor!')


    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')


    def echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text(f"Echo Reply!:{update.message.text}")

    def _sendMessage(self, msg):

        keyboard = [['/help', '/start', '/value'],
                    ['/alerts']]
        reply_markup = ReplyKeyboardMarkup(keyboard)

        try:
            self._updater.bot.send_message(
                self._config['telegram']['chat_id'],
                text=msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        except Exception as network_err:
            # Sometimes the telegram server resets the current connection,
            # if this is the case we send the message again.
            logger.warning(
                'Telegram NetworkError: %s! Trying one more time.',
                network_err
            )
            self._updater.bot.send_message(
                self._config['telegram']['chat_id'],
                text=msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

