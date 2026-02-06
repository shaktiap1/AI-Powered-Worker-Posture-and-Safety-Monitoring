from unstructured.partition.pdf import partition_pdf
from pathlib import Path
 
 # Loader :- This reads the PDF and extracts structured elements (titles, paragraphs, lists, etc.)
 # using unstructured's partition_pdf function with a specific chunking strategy based on titles. 
 # The load_pdf_elements function takes the path to a PDF file and returns a list of extracted elements, 
 # which will be used for further processing in the RAG pipeline to create chunks of text for embedding and retrieval.

def load_pdf_elements(pdf_path: str): # this function reads a PDF file from the specified path and uses the unstructured library's partition_pdf function to extract structured elements from the PDF, such as titles, paragraphs, and lists. 
                                      # The partitioning strategy is set to "by_title", which means that the PDF will be divided into chunks based on the presence of titles, allowing for more meaningful segmentation of the content for use in the RAG pipeline.
                                      # The resulting list of elements is returned for further processing.
    """
    Uses unstructured to extract structured elements
    (titles, paragraphs, lists, etc.)
    """

    elements = partition_pdf(
        filename=pdf_path,
        strategy="fast",
        chunking_strategy="by_title",   # ⭐ important
        infer_table_structure=True
    )

    return elements # this will return a list of elements extracted from the PDF, which can include various types of content such as titles, paragraphs, and lists, depending on the structure of the PDF and the effectiveness of the partitioning strategy used. 
                    # These elements will then be processed further in the RAG pipeline to create chunks of text for embedding and retrieval based on user queries.


if __name__ == "__main__":
    pdf = Path("../data/Data_Science_from_Scratch.pdf")
    els = load_pdf_elements(str(pdf))
    print(f"Loaded {len(els)} elements")

# THANKYOU JI FOR REVIEWING MY CODE HOPING TO CONNECT WITH U FOR THE NEXT ROUND OF INTERVIEW :) SHAKTESH
