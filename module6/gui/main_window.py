import sys
import csv
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, \
    QPushButton, QLabel, QFileDialog, QInputDialog, QMessageBox
from league.league_database import LeagueDatabase
from league.league import League


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.league_editor = None
        self.setWindowTitle("Curling League Manager")

        self.leagues_list = QListWidget()
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.open_file_dialog)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file_dialog)

        self.leagues_list.itemSelectionChanged.connect(self.enable_button)
        self.delete_league_button = QPushButton("Delete League")
        self.delete_league_button.setEnabled(False)
        self.delete_league_button.clicked.connect(self.delete_item)

        self.add_league_button = QPushButton("Add League")
        self.add_league_button.clicked.connect(self.add_item)

        self.leagues_list.itemSelectionChanged.connect(self.enable_button)
        self.edit_league_button = QPushButton("Edit League")
        self.edit_league_button.setEnabled(False)
        self.edit_league_button.clicked.connect(self.openLeagueEditor)

        self.setFixedSize(QSize(500, 400))

        layout = QVBoxLayout()
        self.label = QLabel('List of Curling Leagues', self)
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.label.setFont(font)
        layout.addWidget(self.label)
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.leagues_list)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_league_button)
        button_layout.addWidget(self.add_league_button)
        button_layout.addWidget(self.edit_league_button)

        list_layout.addLayout(button_layout)
        layout.addLayout(list_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.database = LeagueDatabase.instance()

    def openLeagueEditor(self):
        from gui.league_editor import LeagueEditor
        selected_league = self.leagues_list.selectedItems()
        selected_league = next(iter(selected_league), None)
        if selected_league:
            league_name = selected_league.text()
            self.hide()  # hide the MainWindow
            selected_league = self.database.league_named(league_name)
            self.league_editor = LeagueEditor(selected_league)  # Now passing League object itself
            self.league_editor.show()  # show the LeagueEditor
        else:
            QMessageBox.warning(self, 'Warning', 'No League Selected')

    def update_league_list(self):
        self.leagues_list.clear()
        league_names = [league.name for league in self.database.leagues]
        self.leagues_list.addItems(league_names)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Load File', '', 'CSV Files (*.csv)', options=options)
        if not file_name:
            QMessageBox.information(self, "Information", "No file selected.")
            return
        with open(file_name, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for league in reader:
                self.league = League(LeagueDatabase.next_oid(), league[0])
                self.database.add_league(self.league)
                self.update_league_list()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV Files (*.csv)', options=options)
        if file_name:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['League Name'])
                for i in range(self.leagues_list.count()):
                    item_text = self.leagues_list.item(i).text()
                    writer.writerow([item_text])

    def enable_button(self):
        should_enable = self.leagues_list.currentItem() is not None
        self.delete_league_button.setEnabled(should_enable)
        self.edit_league_button.setEnabled(should_enable)

    def delete_item(self):
        current_item = self.leagues_list.currentItem()
        if current_item:
            league_name = current_item.text()
            league = self.database.league_named(league_name)
            if league:
                self.database.remove_league(league)
                self.update_league_list()
                self.enable_button()  # verify if any item is selected after deletion

    def add_item(self):
        league_name, ok = QInputDialog.getText(self, 'Add League', 'Enter league name:')
        if ok and league_name:
            self.leagues_list.addItem(league_name)
            self.league = League(LeagueDatabase.next_oid(), league_name)
            self.database.add_league(self.league)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
