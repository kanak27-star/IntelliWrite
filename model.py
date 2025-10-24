from textblob import TextBlob
import language_tool_python
from spellchecker import SpellChecker

# Optional: Add common irregular verbs
IRREGULAR_VERBS = {
    'knowed': 'knew',
    'has went': 'has gone',
    'do not knowed': 'does not know',
    'goed': 'went',
    'buyer': 'bought',
    'doed': 'did',
    'runned': 'ran',
    # Add more if needed
}

class SpellCheckerModule:
    def __init__(self):
        self.grammar_tool = language_tool_python.LanguageTool('en-US')
        self.spell = SpellChecker()

    def correct_spell(self, text):
        """
        Correct spelling using SpellChecker and TextBlob combined.
        """
        # First, use SpellChecker for word-level correction
        words = text.split()
        corrected_words = []
        for word in words:
            # Skip punctuation-only tokens
            if word.isalpha():
                corrected_word = self.spell.correction(word)
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        corrected_text = ' '.join(corrected_words)

        # Then use TextBlob for context-aware correction
        corrected_text = str(TextBlob(corrected_text).correct())
        return corrected_text

    def correct_irregular_verbs(self, text):
        """
        Replace common irregular verbs manually.
        """
        for wrong, right in IRREGULAR_VERBS.items():
            text = text.replace(wrong, right)
        return text

    def correct_grammar(self, text):
        """
        Correct grammar after spelling and irregular verbs correction.
        Returns corrected text, list of mistakes, and mistake count.
        """
        # Step 1: Correct spelling
        corrected_text = self.correct_spell(text)

        # Step 2: Correct irregular verbs
        corrected_text = self.correct_irregular_verbs(corrected_text)

        # Step 3: Correct grammar
        matches = self.grammar_tool.check(corrected_text)
        found_mistakes = [match.replacements[0] for match in matches if match.replacements]
        corrected_text = self.grammar_tool.correct(corrected_text)

        return corrected_text, found_mistakes, len(found_mistakes)


if __name__ == "__main__":
    obj = SpellCheckerModule()
    message = "Hello world. I has went to the market yesturday and buyed some apples, but it were too expensive."

    # Step 1: Spelling correction
    corrected_spelling = obj.correct_spell(message)
    print("Spell Correction:", corrected_spelling)

    # Step 2: Grammar correction
    corrected_text, mistakes, count = obj.correct_grammar(message)
    print("Grammar Correction:", corrected_text)
    print("Mistakes found:", mistakes, "Count:", count)
