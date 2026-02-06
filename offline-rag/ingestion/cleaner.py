import re
# this file contains helper functions for cleaning the extracted text from the PDF, such as removing excessive whitespace, page numbers, 
# and filtering out chunks that are too short to be useful for the RAG pipeline. The clean_text function takes a string of text as input and applies basic cleaning operations to it,
# while the is_valid_chunk function checks if a given chunk of text meets a minimum character length requirement to be considered valid for inclusion in the RAG pipeline.

def clean_text(text: str) -> str: # this function takes a string of text as input and applies basic cleaning operations to it, such as stripping leading and trailing whitespace, collapsing multiple consecutive whitespace characters into a single space, 
                                  # and removing page numbers that consist solely of digits. The cleaned text is then returned as output.
#Basic cleaning
    if not text:
        return ""

    text = text.strip()

    # remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # remove page numbers like "Page 23"
    text = re.sub(r"^\d+\s*$", "", text)

    return text


def is_valid_chunk(text: str, min_chars: int = 40) -> bool:
    """filter junk"""
    return len(text) >= min_chars

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH