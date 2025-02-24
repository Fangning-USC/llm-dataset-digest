"""token length function."""
import tiktoken


def tiktoken_len(text: str) -> int:
    r"""Output token length.

    Args:
        text: input text.

    Returns:
        length of the input text string.
    """
    tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokenizer = tiktoken.get_encoding("cl100k_base")

    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)
