import c4d
from Fr import Fr
from Us import Us
from ..Const import Const as Const

class Text():
    """class who handle text in our program"""

    def __init__(self):
        self.set_language(self.__get_C4D_language_code())

    def __get_C4D_language_code(self):
        """
        Get the default C4D language
        :return: Const.General
        """
        i = 0
        language_data = c4d.GeGetLanguage(i)

        #Loop for each language until we get the default one
        while language_data:
            language_data = c4d.GeGetLanguage(i)
            if not language_data:
                break

            if language_data["default_language"]:
                break

            i += 1

        if not language_data:
            return Const.TEXT_US

        if language_data["extensions"] == "FR":
            return Const.TEXT_FR
        elif language_data["extensions"] == "US":
            return Const.TEXT_US

        return Const.TEXT_US

    def set_language(self, language_code):
        """
        Set the language of all text
        :param language_code: Const.General
        :return: None
        """
        if language_code == Const.TEXT_FR:
            self.ln_code = Const.TEXT_FR
            self.text = Fr()
        elif language_code == Const.TEXT_US:
            self.ln_code = Const.TEXT_US
            self.text = Us()
        else:
            self.ln_code = Const.TEXT_US
            self.text = Us()

    def get_language(self):
        """
        Get the default language code
        :return: Const.General
        """
        return self.ln_code

    def get(self, text_id):
        """
        Get a string.
        :param text_id: text_id
        :return: String value for the given text_id Can be empty str
        """
        if not self.text:
            self.set_language(self.__get_C4D_language_code())

        str_text_id = str(text_id)
        text_buffer = self.text.data.get(str_text_id, str())

        return text_buffer