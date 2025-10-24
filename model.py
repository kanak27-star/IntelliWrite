# model.py
from textblob import TextBlob
from spellchecker import SpellChecker
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Optional: Add common irregular verbs
IRREGULAR_VERBS = {
    'buyed': 'bought',
    'knowed': 'knew',
    'goed': 'went',
    'has went': 'has gone',
    'doed': 'did',
    'runned': 'ran',
    # Add more if needed
}

class SpellCheckerModule:
    def __init__(self):
        # Initialize SpellChecker for word-level spelling
        self.spell = SpellChecker()
        
        # Initialize transformer grammar model
        self.tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

    def correct_spell(self, text):
        """
        Correct spelling using SpellChecker and TextBlob combined.
        """
        # Step 1: SpellChecker (word-level)
        words = text.split()
        corrected_words = []
        for word in words:
            if word.isalpha():
                corrected_word = self.spell.correction(word)
                corrected_words.append(corrected_word)
            else:
                corrected_words.append(word)
        corrected_text = ' '.join(corrected_words)

        # Step 2: TextBlob for context-aware correction
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
        Correct grammar using transformer model after spelling and irregular verbs correction.
        Returns corrected text.
        """
        # Step 1: Correct spelling
        corrected_text = self.correct_spell(text)

        # Step 2: Correct irregular verbs
        corrected_text = self.correct_irregular_verbs(corrected_text)

        # Step 3: Transformer-based grammar correction
        inputs = self.tokenizer(corrected_text, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=512)
        grammar_corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        return grammar_corrected_text


if __name__ == "__main__":
    checker = SpellCheckerModule()
    message = "She do not knowed the answer, and their going to the park tomorow. I has went to the market yesturday and buyed some apples."

    # Step 1: Spelling correction
    corrected_spelling = checker.correct_spell(message)
    print("Spell Correction:", corrected_spelling)

    # Step 2: Grammar correction
    corrected_grammar = checker.correct_grammar(message)
    print("Grammar Correction:", corrected_grammar)
