from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QPushButton, QLabel, QMessageBox
from datetime import timedelta, date

class DateRangeSelector(QWidget):
    def __init__(self, file_name):  # Add file_name as an argument
        super().__init__()

        self.setWindowTitle("Date Range Selector")
        self.setGeometry(100, 100, 400, 300)

        self.start_calendar_widget = QCalendarWidget(self)
        self.start_calendar_widget.setGridVisible(True)
        self.start_calendar_widget.selectionChanged.connect(self.update_date_range_label)

        self.end_calendar_widget = QCalendarWidget(self)
        self.end_calendar_widget.setGridVisible(True)
        self.end_calendar_widget.selectionChanged.connect(self.update_end_date)

        self.date_range_label = QLabel("Please select start and end dates", self)

        self.list_dates_button = QPushButton("List Dates", self)
        self.list_dates_button.clicked.connect(self.list_dates)

        self.start_date_selected = False
        self.end_date_selected = False

        self.file_name = file_name  # Store the file_name

        layout = QVBoxLayout()
        layout.addWidget(self.start_calendar_widget)
        layout.addWidget(self.end_calendar_widget)
        layout.addWidget(self.date_range_label)
        layout.addWidget(self.list_dates_button)

        self.setLayout(layout)

    def update_date_range_label(self):
        start_date = self.start_calendar_widget.selectedDate().toPyDate()
        if start_date != date.today():
            self.start_date_selected = True
            self.date_range_label.setText(f"Start Date: {start_date.strftime('%m/%d/%Y')}")

    def update_end_date(self):
        end_date = self.end_calendar_widget.selectedDate().toPyDate()
        if end_date != date.today():
            self.end_date_selected = True
            self.date_range_label.setText(f"Date Range: {self.start_calendar_widget.selectedDate().toPyDate().strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')}")

    def list_dates(self):
        if not self.start_date_selected and not self.end_date_selected:
            QMessageBox.critical(self, "Error", "Please select both start and end dates")
        elif not self.start_date_selected:
            QMessageBox.critical(self, "Error", "Please select a start date")
        elif not self.end_date_selected:
            QMessageBox.critical(self, "Error", "Please select an end date")
        else:
            start_date = self.start_calendar_widget.selectedDate().toPyDate()
            end_date = self.end_calendar_widget.selectedDate().toPyDate()

            if start_date > end_date:
                QMessageBox.critical(self, "Error", "Start date cannot be greater than end date")
            else:
                dates = []
                current_date = start_date

                while current_date <= end_date:
                    dates.append(current_date)
                    current_date += timedelta(days=1)

                with open(self.file_name, 'w') as f:  # Open the file in write mode
                    for date in dates:
                        f.write(str(date) + '\n')  # Write each date to the file

                print(dates)

if __name__ == "__main__":
    app = QApplication([])
    window = DateRangeSelector("my_file.txt")  # Pass the file_name when creating an instance
    window.show()
    app.exec()