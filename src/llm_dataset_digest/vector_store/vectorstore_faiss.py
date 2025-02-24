"""Create FAISS vector database."""
import os

from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from llm_dataset_digest.vector_store.load_jsonfile import load_jsonfile
from llm_dataset_digest.vector_store.tiktoken_len import tiktoken_len


def vectorstore_faiss(doc_dir: str, verbose: bool = False) -> object:
    r"""This function creates a FAISS vector database.

    Args:
        doc_dir: input document name or path.
        verbose: True to print the filenames.

    Returns:
        Faiss vector database object.
    """
    # Compile text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=["\n\n", "\n", " ", ""],
    )

    # compile embedding
    model_name = "text-embedding-ada-002"
    openai_api_key = os.environ["OPENAI_API_KEY"]

    embed = OpenAIEmbeddings(model=model_name, openai_api_key=openai_api_key)

    # load data recursively and store into a single list
    if verbose is True:
        print(r"""loading json files:\n""")
    data = load_jsonfile(root_dir=doc_dir, verbose=verbose)
    if verbose is True:
        print(r"""json files loading completed.""")

    # Text chuncking, embedding, and indexing
    docs = []
    for _i, record in enumerate(data):
        # first get metadata fields for this record
        metadata = {
            "doc_name": record["doc_name"],
            "doc_quarter": record["doc_quarter"],
            "doc_year": record["doc_year"],
            "page": record["page"],
            "text_type": record["text_type"],
        }

        # now we create chunks from the record text
        record_texts = text_splitter.split_text(record["text"])
        # create individual metadata dicts for each chunk
        record_metadatas = [
            {"chunk": j, **metadata} for j, text in enumerate(record_texts)
        ]

        # print(record_texts)
        # print(record_metadatas)

        # append chunk
        for record_text, record_metadata in zip(record_texts, record_metadatas):  # noqa
            # print(record_text,record_metadata)
            docs.append(Document(page_content=record_text, metadata=record_metadata))

    # create FAISS vector store
    return FAISS.from_documents(docs, embed)
