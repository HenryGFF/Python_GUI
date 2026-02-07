from PySide6.QtGui import QColor, QTextCharFormat, QPainter
from PySide6.QtWidgets import QFrame, QWidget, QLabel, QVBoxLayout, QSizePolicy, QDateEdit, QHBoxLayout, QCalendarWidget
from PySide6.QtCore import Qt, QDate, Signal

class CustomCalendar(QCalendarWidget):
    def __init__(self, min_date: QDate, max_date: QDate):
        super().__init__()
        self.min_date = min_date
        self.max_date = max_date

    def paintCell(self, painter: QPainter, rect, date: QDate):
        super().paintCell(painter, rect, date)

        if date < self.min_date or date > self.max_date:
            painter.fillRect(rect, QColor("#E0E6EB"))
            painter.setPen(QColor("#CFCFCF"))
            painter.drawText(rect, Qt.AlignCenter, str(date.day()))


class NoWheelDateEdit(QDateEdit):
    def wheelEvent(self, event):
        event.ignore()

class FormBox(QFrame):
    max_files_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setFixedHeight(170)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.setObjectName('FormBox')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(10)

        self.invalid_fmt = QTextCharFormat()
        self.invalid_fmt.setForeground(QColor("#9AA0A6"))
        self.invalid_fmt.setBackground(QColor("#FCE8E6"))

        self.normal_fmt = QTextCharFormat()


class FormA(FormBox):
    def __init__(self):
        super().__init__()

        title = QLabel("Selecione uma data")
        title.setObjectName("input_title")

        layout = self.layout()
        layout.addWidget(title)

        self.date_input = NoWheelDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dddd, dd MMMM yyyy")
        self.date_input.setMaximumDate(QDate.currentDate())
        self.date_input.setMinimumDate(QDate(2020, 1, 1))
        self.date_input.setDate(QDate(2020, 1, 1))
        self.date_input.setSpecialValueText("Escolha uma data")

        calendar = CustomCalendar(
            min_date=self.date_input.minimumDate(),
            max_date=self.date_input.maximumDate()
        )
        self.date_input.setCalendarWidget(calendar)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        self.date_input.dateChanged.connect(self._on_date_changed)

        layout.addWidget(self.date_input, alignment=Qt.AlignLeft)

    def _on_date_changed(self, date: QDate):
        if date == QDate(1, 1, 1):
            self.max_files_changed.emit(0)
        else:
            self.max_files_changed.emit(1)




class FormB(FormBox):
    def __init__(self):
        super().__init__()

        title = QLabel("Defina um período")
        title.setObjectName("input_title")

        layout = self.layout()
        layout.addWidget(title)

        self.date_box = QWidget()
        self.date_layout = QHBoxLayout(self.date_box)
        self.date_layout.setContentsMargins(0, 0, 0, 0)
        self.date_layout.setSpacing(10)

        self.first_date_input = NoWheelDateEdit()
        self.first_date_input.setCalendarPopup(True)
        self.first_date_input.setDisplayFormat("dd/MM/yyyy")
        self.first_date_input.setMaximumDate(QDate.currentDate())
        self.first_date_input.setMinimumDate(QDate(2020, 1, 1))
        self.first_date_input.setDate(QDate(2020, 1, 1))


        first_calendar = CustomCalendar(
            min_date=self.first_date_input.minimumDate(),
            max_date=self.first_date_input.maximumDate()
        )
        self.first_date_input.setCalendarWidget(first_calendar)
        first_calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        first_label = QLabel()
        first_label.setText('Data inicial:')
        first_label.setObjectName('first_label')
        first_input_box = QWidget()
        first_layout = QHBoxLayout(first_input_box)
        first_layout.setContentsMargins(0, 0, 0, 0)
        first_layout.setSpacing(0)
        first_layout.addWidget(first_label)
        first_layout.addWidget(self.first_date_input)

        self.date_layout.addWidget(first_input_box, alignment=Qt.AlignLeft)



        self.last_date_input = NoWheelDateEdit()
        self.last_date_input.setCalendarPopup(True)
        self.last_date_input.setDisplayFormat("dd/MM/yyyy")
        self.last_date_input.setMinimumDate(self.first_date_input.date())
        self.last_date_input.setMaximumDate(QDate.currentDate())
        self.last_date_input.setMinimumDate(QDate(2020, 1, 1))
        self.last_date_input.setDate(QDate(2020, 1, 1))

        last_calendar = CustomCalendar(
            min_date=self.last_date_input.minimumDate(),
            max_date=self.last_date_input.maximumDate()
        )
        self.last_date_input.setCalendarWidget(last_calendar)
        last_calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        self.last_date_input.dateChanged.connect(self.last_date_changed)
        self.first_date_input.dateChanged.connect(self.first_date_changed)

        last_label = QLabel()
        last_label.setText('Data final:')
        last_label.setObjectName('last_label')
        last_input_box = QWidget()
        last_layout = QHBoxLayout(last_input_box)
        last_layout.setContentsMargins(0, 0, 0, 0)
        last_layout.setSpacing(0)
        last_layout.addWidget(last_label)
        last_layout.addWidget(self.last_date_input)
        self.date_layout.addWidget(last_input_box, alignment=Qt.AlignLeft)

        layout.addWidget(self.date_box)

    def update_invalid_dates(self):
        first_cal = self.first_date_input.calendarWidget()
        last_cal = self.last_date_input.calendarWidget()

        first_cal.min_date = self.first_date_input.minimumDate()
        first_cal.max_date = self.last_date_input.date()

        last_cal.min_date = self.first_date_input.date()
        last_cal.max_date = self.last_date_input.maximumDate()

        first_cal.update()
        last_cal.update()

    def first_date_changed(self):
        self.last_date_input.setMinimumDate(self.first_date_input.date())
        if self.last_date_input.date() < self.first_date_input.date():
            self.last_date_input.setDate(self.first_date_input.date())

        self.update_invalid_dates()

        self.last_date_input.dateChanged.connect(self._on_dates_changed)

    def last_date_changed(self):
        self.first_date_input.setMaximumDate(self.last_date_input.date())
        if self.first_date_input.date() > self.last_date_input.date():
            self.first_date_input.setDate(self.last_date_input.date())

        self.update_invalid_dates()

        self.first_date_input.dateChanged.connect(self._on_dates_changed)

    def _on_dates_changed(self):
        start = self.first_date_input.date()
        end = self.last_date_input.date()

        if start == QDate(2000, 1, 1) or end == QDate(2000, 1, 1):
            self.max_files_changed.emit(0)
            return

        if end < start:
            self.max_files_changed.emit(0)
            return

        days = start.daysTo(end) + 1
        self.max_files_changed.emit(days)

        self.last_date_input.setMinimumDate(start)
