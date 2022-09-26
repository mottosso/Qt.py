import typing
 
from . import QtWidgets
 
 
class QHeaderView:
    @typing.overload
    @staticmethod
    def setSectionResizeMode(header: QtWidgets.QHeaderView, logicalIndex: int, mode: QtWidgets.QHeaderView.ResizeMode) -> None: ...
    @typing.overload
    @staticmethod
    def setSectionResizeMode(header: QtWidgets.QHeaderView, mode: QtWidgets.QHeaderView.ResizeMode) -> None: ...

def translate(context: str, sourceText: str, *args: typing.Any) -> str: ...
