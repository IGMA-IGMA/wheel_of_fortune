from typing import Union, Optional, Literal, Any

class NewType:
    letter_dict = dict[str, list[int]]
    
    ret_dict = dict[
        Literal["exception", "result"], 
        Union[Optional[Exception], Any]
    ]

