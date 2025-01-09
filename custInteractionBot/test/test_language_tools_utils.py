import unittest
from custInteractionBot.utils.language_tools_utils import translate_text, detect_language

class TestLanguageToolsUtils(unittest.TestCase):

    def test_translate_text(self):
        input_text = "Hello, how are you?"
        target_language = "es"
        result = translate_text(input_text, target_language)
        self.assertIn("Translated to es", result)

    def test_detect_language(self):
        input_text = "Hola, ¿como estás?"
        result = detect_language(input_text)
        self.assertEqual(result, "en")  # Placeholder; modify as per actual implementation

if __name__ == "__main__":
    unittest.main()
