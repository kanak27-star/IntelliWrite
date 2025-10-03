from textblob import TextBlob
import language_tool_python

class SpellCheckerModule:
    def __init__(self):
        self.grammar_tool = language_tool_python.LanguageTool('en-US')

    def correct_spell(self, text):
        # Correct the entire text using TextBlob
        return str(TextBlob(text).correct())

    def correct_grammar(self, text):
        # First correct spelling
        spell_corrected_text = self.correct_spell(text)

        # Then check grammar on the corrected text
        matches = self.grammar_tool.check(spell_corrected_text)
        found_mistakes = [match.replacements[0] for match in matches if match.replacements]
        corrected_text = self.grammar_tool.correct(spell_corrected_text)

        return corrected_text, found_mistakes, len(found_mistakes)


if __name__ == "__main__":
    obj = SpellCheckerModule()
    message = "Hello world. I like mashine learning. appple. bananana"

    # Step 1: Spelling correction
    corrected_spelling = obj.correct_spell(message)
    print("Spell Correction:", corrected_spelling)

    # Step 2: Grammar correction
    mistakes, count = obj.correct_grammar(message)
  
    print("Mistakes found:", mistakes, "Count:", count)
