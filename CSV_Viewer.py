import sys
import pandas as pd
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, 
                             QPushButton, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QFileDialog)

class csvViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV Viewer')
        #set widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        #set text field
        self.layout = QVBoxLayout(self.central_widget)
        self.open_file = QLineEdit(self)
        self.layout.addWidget(self.open_file)
        #add the buttons
        button_layout = QHBoxLayout()

        self.open_button = QPushButton('Open File', self)
        button_layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_dialog_1)
        self.save_button = QPushButton('Save File',self)
        button_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_csv)

        self.layout.addLayout(button_layout)

        #add table
        self.table_entry = QTableWidget(self)
        self.layout.addWidget(self.table_entry)

    def open_dialog_1(self):
        #open file to select csv file
        fname, ok = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "CSV Files (*.csv)",
        ) 
        if fname:
            path = Path(fname)
            self.open_file.setText(str(path))
            #read csv file into pandas dataframe (df)
            df = pd.read_csv(fname)
            #set table dimensions
            self.table_entry.setRowCount(df.shape[0]) #set rows
            self.table_entry.setColumnCount(df.shape[1]) #set columns
            self.table_entry.setHorizontalHeaderLabels(df.columns) #set column headers
            
            # Populate table with CSV data
            for row_idx in range(df.shape[0]):
                for col_idx in range(df.shape[1]):
                    cell_value = str(df.iloc[row_idx, col_idx]) #convert value to string
                    self.table_entry.setItem(row_idx, col_idx, QTableWidgetItem(cell_value))


    def save_csv(self):
        # Open file dialog to save CSV
        fname, ok = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")

        if fname:
            # Extract data from table
            row_count = self.table_entry.rowCount()
            col_count = self.table_entry.columnCount()
            headers = [self.table_entry.horizontalHeaderItem(i).text() for i in range(col_count)]

            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = self.table_entry.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # Create a DataFrame and save it as CSV
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(fname, index=False)

if __name__=='__main__':
    app = QApplication(sys.argv)
    main_window = csvViewer()
    main_window.show()
    sys.exit(app.exec())