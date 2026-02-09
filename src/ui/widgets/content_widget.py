from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QParallelAnimationGroup
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QWidget, QSizePolicy, QLayout, QGraphicsOpacityEffect
from ui.components import SelectionBox, FormA, FormB, FinancialBasesUploadWidget, ControlBox
from ui.helpers import UserInput


class ContentSection(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.fileUploadWidget = None
        self.current_form = None
        self.control_box = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.section_header: QWidget = self.__init_sectionheader()

        self.center_wrapper = QWidget()
        self.center_wrapper.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Preferred
        )

        self.selection_box = SelectionBox()
        self.selection_box.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        self.center_layout = QVBoxLayout(self.center_wrapper)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(10)

        self.center_layout.addWidget(self.section_header)
        self.center_layout.addWidget(self.selection_box)

        section_layout: QVBoxLayout = QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(0)
        section_layout.addWidget(self.center_wrapper, alignment=Qt.AlignHCenter)

        self.setLayout(section_layout)
        self.setObjectName('ContentSection')
        self.selection_box.option_box.optionA.add_form_requested.connect(self.add_form)
        self.selection_box.option_box.optionB.add_form_requested.connect(self.add_form)

    def __init_sectionheader(self) -> QFrame:
        section_header: QFrame = QFrame()
        section_header.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        section_header.setObjectName('section_header')

        section_title: QLabel = QLabel()
        section_title.setText('Nova Conciliação')
        section_title.setObjectName('section_title')

        section_legend: QLabel = QLabel()
        section_legend.setText('Selecione o tipo de conciliação, o período desejado e importe as bases necessárias.')
        section_legend.setObjectName('section_legend')
        section_legend.setWordWrap(True)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(section_title)
        layout.addWidget(section_legend)

        section_header.setLayout(layout)
        return section_header

    def add_form(self, mapper, config, cache):
        target = config.form_type

        if target in cache:
            form = cache[target]
        else:
            form = FormA() if target == mapper.FormA else FormB()
            cache[target] = form

        if self.current_form is form:
            return

        if self.current_form:
            self.center_layout.removeWidget(self.current_form)
            self.current_form.setVisible(False)
            self.rm_file_inputs()

        self.current_form = form
        self.center_layout.addWidget(self.current_form)

        self.current_form.setVisible(True)

        # 🔑 conexão CORRETA
        self.current_form.max_files_changed.connect(self.on_max_files_changed)

        self.widget_status()

    def add_control_box(self):
        if self.layout_has_widget(self.layout(), self.control_box):
            return
        self.control_box = ControlBox()
        self.layout().addWidget(self.control_box)
        
        self.control_box.reset_content_widget.connect(self.reset_widget)
        self.control_box.send_content_data.connect(self.send_data)
        
    def reset_widget(self):
        self.center_layout.removeWidget(self.current_form)
        if self.fileUploadWidget is not None:
            self.center_layout.removeWidget(self.fileUploadWidget)
            self.fileUploadWidget = None

        self.layout().removeWidget(self.control_box)
        
    def send_data(self):
        try:
            self.control_box.status_bar.show_message("Processando...", "processing")

            if type(self.current_form).__name__ == 'FormA':
                date = self.current_form.date_input.date()
                info = UserInput(
                    form_type='FormA',
                    file_fields=self.fileUploadWidget.fields,
                    date=date
                )

            elif type(self.current_form).__name__ == 'FormB':
                start_date = self.current_form.first_date_input.date()
                end_date = self.current_form.last_date_input.date()
                info = UserInput(
                    form_type='FormB',
                    file_fields=self.fileUploadWidget.fields,
                    start_date=start_date,
                    end_date=end_date
                )

            print(info)
            self.control_box.status_bar.show_message("Concluído com sucesso!", "success")
        except Exception:
            self.control_box.status_bar.show_message("Algo deu errado!", "error")
            print(Exception)

    def update_send_button(self):
        counter: int = 0
        for field in self.fileUploadWidget.fields.values():
            if len(field.files) == field.max_files:
                counter += 1

        if counter == len(self.fileUploadWidget.fields):
            self.control_box.send_btn.setEnabled(True)
        else:
            self.control_box.send_btn.setEnabled(False)

    def add_file_inputs(self):
        if self.fileUploadWidget is None:
            self.fileUploadWidget = FinancialBasesUploadWidget()
            for field in self.fileUploadWidget.fields.values():
                field.activateSendBtn.connect(self.update_send_button)

            self.center_layout.addWidget(self.fileUploadWidget)

    def on_max_files_changed(self, n: int):
        self.add_file_inputs()  # garante que existe

        for upload in self.fileUploadWidget.fields.values():
            upload.set_max_files(n)

    def rm_file_inputs(self):
        if self.fileUploadWidget:
            self.center_layout.removeWidget(self.fileUploadWidget)
            self.fileUploadWidget.deleteLater()
            self.fileUploadWidget = None

    #funções auxiliares

    def widget_status(self):
        if self.layout_has_widget(self.center_layout, self.current_form):
            if not self.layout_has_widget(self.layout(), self.control_box):
                self.add_control_box()

    def layout_has_widget(self, layout: QLayout, widget: QWidget) -> bool:
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() is widget:
                return True
        return False