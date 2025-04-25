import typing

from . import QtWidgets
from . import QtCore


class QHeaderView:
    @typing.overload
    @staticmethod
    def setSectionResizeMode(header: QtWidgets.QHeaderView, logicalIndex: int, mode: QtWidgets.QHeaderView.ResizeMode) -> None: ...
    @typing.overload
    @staticmethod
    def setSectionResizeMode(header: QtWidgets.QHeaderView, mode: QtWidgets.QHeaderView.ResizeMode) -> None: ...


def delete(obj: object) -> None: ...


def exec_(obj: object) -> int: ...


def getCppPointer(obj: object) -> typing.Tuple[int, ...]: ...


def isValid(obj: object) -> bool: ...


def loadUi(uifile: str, baseinstance: typing.Optional[None | QtWidgets.QWidget] = ...) -> QtWidgets.QWidget: ...


def load_ui(uifile: str, baseinstance: typing.Optional[None | QtWidgets.QWidget] = ...) -> QtWidgets.QWidget: ...


def translate(context: str, sourceText: str, *args: typing.Any) -> str: ...


def wrapInstance(address: int, qt_type: type) -> object | QtCore.QObject | QtWidgets.QWidget: ...
