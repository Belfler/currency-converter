from typing import Callable, Dict, Tuple, Any

__all__ = ['HandlerResponse', 'Handler']

HandlerResponse = Tuple[int, Dict[str, str], str]

Handler = Callable[[Dict[str, Any], Dict[str, str]], HandlerResponse]
