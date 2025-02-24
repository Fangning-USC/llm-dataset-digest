"""Command-line interface."""

import os

import click

from llm_dataset_digest.text_parsing.parse_ppt_one_page import parse_ppt_one_page
from llm_dataset_digest.text_parsing.ungroup_ppt import ungroup_ppt
from llm_dataset_digest.vector_store.vectorstore_faiss import vectorstore_faiss


@click.command()
@click.option(
    "--path",
    prompt="Provide the path to PowerPoints",
    help="The path to the dir that contains the PowerPoints.",
)
@click.option(
    "--db_storage_dir",
    prompt="Set the storage path to vector database",
    help="The storage path of the vector database.",
)
@click.option(
    "--vector_db_name",
    default="vectorstore",
    prompt="Set the name of the vector database",
    help="The name of the vector database.",
)
@click.option(
    "--verbose",
    default=True,
    prompt="Set False to not print the progress",
    help="Print the progress or not.",
)
@click.option(
    "--line_len_threshold",
    default=4,
    prompt="threshold of line numbers",
    help="Do not parse the page if line numbers of this page is smaller than the"
    "threshold.",
)
@click.option(
    "--text_len_threshold",
    default=4,
    prompt="threshold of text string length",
    help="Do not parse the string if string length is smaller than the threshold.",
)
def main(  # noqa
    path: str,
    db_storage_dir: str,
    vector_db_name: str,
    line_len_threshold: int = 4,
    text_len_threshold: int = 4,
    verbose: bool = True,
) -> None:
    """This function parse text, indexing and storing the outputs in a vector database.

    Args:
        path: The path to the dir that contains the PowerPoints.
        db_storage_dir: The storage path of the vector database.
        vector_db_name: The name of the vector database.
        line_len_threshold: Do not parse the page if line numbers of this page is
        smaller than the threshold.
            default = 4.
        text_len_threshold: Do not parse the string if string length is smaller than
        the threshold.
            default = 4.
        verbose: Print the progress (True) or not (False). Default is True.

    Returns:
        vector database.
    """
    # get all ppt files
    files = [x for x in os.listdir(path) if x.endswith(".pptx")]

    # ungrouping the grouped text frames
    for file in files:
        ungroup_ppt(
            input_file_path=path + "\\" + file,
            output_file_name=file,
            output_file_path=path + "\\ungrouped",
        )
        if verbose is True:
            print("ungroup processed: ", file)
            print("saved to: " + path + "\\ungrouped")

        # parse ppt and store text within one page
        folder_name = parse_ppt_one_page(
            ppt_file=file,
            ppt_path=path + "\\ungrouped",
            line_len_threshold=line_len_threshold,
            text_len_threshold=text_len_threshold,
        )
        if verbose is True:
            print("parsing processed, saved to: ", folder_name)

    # get vector database
    vector_db = vectorstore_faiss(doc_dir=path + "\\ungrouped", verbose=verbose)

    # save to the storage path
    os.chdir(db_storage_dir)
    vector_db.save_local(vector_db_name)
    if verbose is True:
        print(
            "Finalized. Vector database saved to: ",
            db_storage_dir + "\\" + vector_db_name,
        )
        print("-----------------------------------")


if __name__ == "__main__":
    main()
