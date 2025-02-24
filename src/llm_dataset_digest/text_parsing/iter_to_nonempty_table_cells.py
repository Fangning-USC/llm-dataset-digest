"""Iterate a table through rows and columns."""
from country_named_entity_recognition import find_countries


def iter_to_nonempty_table_cells(
    tbl: object,
    text_len_threshold: int = 4,
    tbl_len_threshold: int = 6,
    font_size_threshold: int = 8,
) -> str:
    """This function iterate a table through rows and columns.

    Args:
        tbl: table object.
        text_len_threshold: Threshold of length of text string to be parsed.
                            Default = 4
        tbl_len_threshold: Threshold of row/col of table to be parsed. Only parse table
        with row/col smaller than this threshold.
                            Default = 6
        font_size_threshold: Threshold of font size in table to be parsed. Only parse
        the text with font size greater than this threshold.
                            Default = 8

    Returns:
        return iterator to non-empty rows.
    """
    if len(tbl.rows) < tbl_len_threshold or len(tbl.columns) < tbl_len_threshold:
        for ridx in range(sum(1 for _ in iter(tbl.rows))):
            for cidx in range(sum(1 for _ in iter(tbl.columns))):
                cell = tbl.cell(ridx, cidx)
                txt = str(cell.text)
                txt = txt.strip()
                if txt:
                    # find if country name exists
                    txt_with_countries = find_countries(txt)
                    # get the font size (not robust)
                    text_frame = cell.text_frame
                    paragraph = text_frame.paragraphs[0]
                    for run in paragraph.runs:
                        font = run.font
                        try:
                            # get font size (not robust)
                            font_size = font.size.pt
                        except:  # noqa
                            # if no font size info, set font_size = 0
                            font_size = 0

                    if (
                        txt_with_countries
                        or (
                            (len(txt.split(" ")) > text_len_threshold)
                            and (font_size > font_size_threshold)
                        )
                        or (txt[-1] in ".")
                    ):  # noqa
                        yield txt + "\n"
