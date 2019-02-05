from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


class EditableInlineKeyboardMarkup(InlineKeyboardMarkup):
    def set_callback_data(self, callback_data, row=0, column=0):
        self.inline_keyboard[row][column].callback_data = callback_data

    def set_url(self, url, row=0, column=0):
        self.inline_keyboard[row][column].url = url

    @property
    def callback_data(self):
        return self.inline_keyboard[0][0].callback_data

    @callback_data.setter
    def callback_data(self, value):
        self.set_callback_data(value)

    @property
    def url(self):
        return self.inline_keyboard[0][0].url

    @url.setter
    def url(self, value):
        self.set_url(value)


class InlineKeyboard:
    MORE_HELP = EditableInlineKeyboardMarkup(
        [[InlineKeyboardButton('più info', callback_data='morehelp')]]
    )
    REDUCE_HELP = EditableInlineKeyboardMarkup(
        [[InlineKeyboardButton('indietro', callback_data='lesshelp')]]
    )
