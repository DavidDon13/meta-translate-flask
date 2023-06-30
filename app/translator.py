import logging
import time
from custom_language_detector import CustomLanguageDetector
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from collections import defaultdict

checkpoint = "facebook/nllb-200-1.3B"
# checkpoint = "facebook/nllb-200-distilled-600M"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model_path = "./models/transformers/"


class Translator:
    def __init__(self):
        start_time = time.time()

        # to download the model, only first time
        logger.info("Downloading model...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
        self.model.save_pretrained(model_path)

        # to use local files
        # logger.info("Loading local model...")
        # self.model = AutoModelForSeq2SeqLM.from_pretrained(
        #     model_path, local_files_only=True
        # )

        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.detector = CustomLanguageDetector()
        self.target_lang = "eng_Latn"
        self.max_length = 2000
        self.translation_cache = defaultdict(str)
        self.current_src_lang = None
        self.translator = None
        end_time = time.time()
        logger.info(f"Model loaded in {end_time - start_time} seconds.")

    def translate(self, messages):
        start_time = time.time()

        translated_messages = []
        duplicate_count = 0

        for text in messages:
            if text in self.translation_cache:
                translated_text = self.translation_cache[text]
                duplicate_count += 1
            else:
                input_lang = self.detector.predict(text)

                # Instantiate the translator pipeline only if the source language has changed
                if input_lang != self.current_src_lang:
                    self.translator = pipeline(
                        "translation",
                        model=self.model,
                        tokenizer=self.tokenizer,
                        src_lang=input_lang,
                        tgt_lang=self.target_lang,
                        max_length=self.max_length,
                    )
                    self.current_src_lang = input_lang

                output = self.translator(text)
                translated_text = output[0]["translation_text"]
                self.translation_cache[text] = translated_text

            translated_messages.append(
                {
                    "original_text": text,
                    "translated_text": translated_text,
                }
            )

        end_time = time.time()

        logger.info(
            f"Translated {len(messages)} messages in {end_time - start_time} seconds."
        )
        logger.info(f"Found {duplicate_count} duplicate messages.")

        return translated_messages
