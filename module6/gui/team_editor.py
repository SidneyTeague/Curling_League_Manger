import sys
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QListWidget, \
    QPushButton, QLabel, QLineEdit, QDialog, QInputDialog
from league.league_database import LeagueDatabase
from league.team import Team
from gui.league_editor import LeagueEditor
from league.team_member import TeamMember


class TeamEditor(QDialog):
    def __init__(self, team):
        super().__init__()

        self.league = None
        self.setWindowTitle("Curling League Manager")
        self.members_list = QListWidget()
        self.members_list.itemSelectionChanged.connect(self.enable_buttons)
        self.delete_member_button = QPushButton("Delete Member")
        self.delete_member_button.setEnabled(False)
        self.delete_member_button.clicked.connect(self.delete_member)

        self.add_member_button = QPushButton("Add Member")
        self.add_member_button.clicked.connect(self.add_member)

        self.edit_member_button = QPushButton("Edit Member")
        self.edit_member_button.setEnabled(False)
        self.edit_member_button.clicked.connect(self.edit_member)

        self.setFixedSize(QSize(500, 400))

        member_layout = QVBoxLayout()
        self.label = QLabel('Members on the Team', self)
        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        self.label.setFont(font)
        member_layout.addWidget(self.label)
        member_list_layout = QHBoxLayout()
        member_list_layout.addWidget(self.members_list)
        member_button_layout = QVBoxLayout()
        member_button_layout.addWidget(self.delete_member_button)
        member_button_layout.addWidget(self.add_member_button)
        member_button_layout.addWidget(self.edit_member_button)
        member_list_layout.addLayout(member_button_layout)
        member_layout.addLayout(member_list_layout)

        self.setLayout(member_layout)

        self.database = LeagueDatabase.instance()
        self.team = team
        self.update_members_list()

    def update_members_list(self):
        self.members_list.clear()
        for member in self.team.members:
            member_info = f"{member.name} ({member.email})"
            self.members_list.addItem(member_info)

    def enable_buttons(self):
        self.delete_member_button.setEnabled(True)
        self.edit_member_button.setEnabled(True)

    def delete_member(self):
        selected_item = self.members_list.currentItem()
        if selected_item:
            full_text = selected_item.text()
            member_name = full_text.split(' (')[0]  # Extract just the name part
            print(f"Member to delete: {member_name}")  # Debugging
            print(f"Members' names: {[m.name for m in self.team.members]}")  # Debugging
            print(f"Members before deletion: {[(member.name, member.email) for member in self.team.members]}")  # debugging
            member_to_delete = next((m for m in self.team.members if m.name == member_name), None)
            if member_to_delete:
                self.team.members.remove(member_to_delete)
                print(
                    f"Members after deletion: {[(member.name, member.email) for member in self.team.members]}")  # debugging
            else:
                print(f"No member found with name: {member_name}")  # Debugging
            self.update_members_list()

    def add_member(self):
        member_name, ok = QInputDialog.getText(self, 'Add Member', 'Enter member name:')
        member_email, ok2 = QInputDialog.getText(self, 'Add Member', 'Enter member email:')
        if ok and ok2:
            new_member = TeamMember(None, member_name, member_email)
            self.team.members.append(new_member)
            self.update_members_list()

    def edit_member(self):
        selected_item = self.members_list.currentItem()
        if selected_item:
            full_text = selected_item.text()
            member_name = full_text.split(' (')[0]  # Extract just the name
            member_to_update = next((m for m in self.team.members if m.name == member_name), None)
            if member_to_update:
                new_name, ok = QInputDialog.getText(self, 'Update Member', 'Enter new name:', QLineEdit.Normal,
                                                    member_name)
                new_email, ok2 = QInputDialog.getText(self, 'Update Member', 'Enter new email:', QLineEdit.Normal,
                                                      member_to_update.email)
                if ok and ok2:
                    member_to_update.name = new_name
                    member_to_update.email = new_email
            self.update_members_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    selected_team = LeagueEditor.teams_list.selectedItems()
    row_number = LeagueEditor.teams_list.row(selected_team)
    team_name = selected_team[0].text()
    team = Team(row_number, team_name)
    main_window = TeamEditor(team)
    main_window.show()
    sys.exit(app.exec_())
