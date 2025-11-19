from typing import Any, Iterator, Literal, Optional, Union


class NewType:
    letter_dict = dict[str, list[int]]
    ret_dict = dict[Literal["exception", "result"], Union[Optional[Exception], Any]]
    file_path = str
    iter_word = Iterator[str]
