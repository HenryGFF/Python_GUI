from PySide6.QtWidgets import QBoxLayout, QPushButton


def gui_responsivity(main_widget):
    largura = main_widget.width()

    if largura < 800:
        main_widget.content.selection_box.option_box.layout().setDirection(QBoxLayout.TopToBottom)

    else:
        main_widget.content.selection_box.option_box.layout().setDirection(QBoxLayout.LeftToRight)