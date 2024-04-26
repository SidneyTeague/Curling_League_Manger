import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QListWidget, \
    QPushButton, QLabel, QDialog, QFileDialog, QInputDialog, QMessageBox
from league.league import League
from main_window import MainWindow
from league.league_database import LeagueDatabase
from league.team import Team


class LeagueEditor(QDialog):
    def __init__(self, league):
        super().__init__()

        self.team_editor = None
        self.setWindowTitle("Curling League Manager")
        self.teams_list = QListWidget()
        self.import_button = QPushButton("Import Teams")
        self.import_button.clicked.connect(self.import_team)

        self.export_button = QPushButton("Export Teams")
        self.export_button.clicked.connect(self.export_team)

        self.delete_team_button = QPushButton("Delete Team")
        self.delete_team_button.setEnabled(False)
        self.delete_team_button.clicked.connect(self.delete_team)

        self.add_team_button = QPushButton("Add Team")
        self.add_team_button.clicked.connect(self.add_team)

        self.edit_team_button = QPushButton("Edit Team")
        self.edit_team_button.setEnabled(False)
        self.edit_team_button.clicked.connect(self.openTeamEditor)
        self.teams_list.itemSelectionChanged.connect(self.enable_buttons)
        self.setFixedSize(QSize(500, 400))

        team_layout = QVBoxLayout()
        self.label = QLabel('Teams in League', self)
        font = QFont()
        font.setBold(True)
        font.setPointSize(15)
        self.label.setFont(font)
        team_layout.addWidget(self.label)
        team_list_layout = QHBoxLayout()
        team_list_layout.addWidget(self.teams_list)
        team_button_layout = QVBoxLayout()
        team_button_layout.addWidget(self.import_button)
        team_button_layout.addWidget(self.export_button)
        team_button_layout.addWidget(self.delete_team_button)
        team_button_layout.addWidget(self.add_team_button)
        team_button_layout.addWidget(self.edit_team_button)
        team_list_layout.addLayout(team_button_layout)
        team_layout.addLayout(team_list_layout)

        self.setLayout(team_layout)

        self.main_window = MainWindow()  # create an instance of MainWindow (hidden by default)

        self.database = LeagueDatabase.instance()
        self.league = league

    def openTeamEditor(self):
        from gui.team_editor import TeamEditor
        selected_team = self.teams_list.selectedItems()
        selected_team = next(iter(selected_team), None)
        if selected_team:
            team_name = selected_team.text()
            team = self.league.team_named(team_name)
            self.hide()  # hide the LeagueEditor
            self.team_editor = TeamEditor(team)  # Now passing Team object itself
            self.team_editor.show()  # show the TeamEditor
            print(self.team_editor)
        else:
            QMessageBox.warning(self, 'Warning', 'No Team Selected')

    def import_team(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Import Teams', '',
                                                   'CSV Files (*.csv)', options=options)
        if file_name:
            self.database.import_league_teams(self.league, file_name)
            self.update_teams_list()
        else:  # No file was selected
            QMessageBox.information(self, "Information", "No file selected.")

    def export_team(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Export Teams', '',
                                                   'CSV Files (*.csv)', options=options)
        if file_name:
            self.database.export_league_teams(self.league, file_name)

    def update_teams_list(self):
        self.teams_list.clear()
        team_name = [team.name for team in self.league.teams]
        for name in team_name:
            self.teams_list.addItem(name)

    def add_team(self):
        team_name, ok = QInputDialog.getText(self, 'Add Team', 'Enter team name:')
        if ok:
            max_oid = max([team.oid for team in self.league.teams]) if self.league.teams else -1
            next_oid = max_oid + 1
            team = Team(next_oid, team_name)
            self.league.add_team(team)
            self.database.import_league_teams(next_oid, team.name)
            self.update_teams_list()

    def delete_team(self):
        selected_item = self.teams_list.currentItem()
        if selected_item:
            team_name = selected_item.text()
            team_to_remove = next((team for team in self.league.teams if team.name == team_name), None)
            if team_to_remove:
                self.league.remove_team(team_to_remove)
                self.update_teams_list()

    def enable_buttons(self):
        should_enable = self.teams_list.currentItem() is not None
        self.delete_team_button.setEnabled(should_enable)
        self.edit_team_button.setEnabled(should_enable)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selected_league = MainWindow.leagues_list.selectedItems()
    row_number = MainWindow.leagues_list.row(selected_league)
    league_name = selected_league.text()
    league = League(row_number, league_name)
    main_window = LeagueEditor(league)
    main_window.show()
    sys.exit(app.exec_())
