# Assignment 6: Create a PyQt5 interface for the Curling League Manager.  Your interface must include the following windows:
	 - Main window shows list of leagues in the current database. Has load/save menu items and/or buttons that raise Qt5 file dialogs to select the file to load/save.
	Has buttons to:
		Delete a league
		Add a league (the league name can be input directly in this window)
		Edit a league
	- League editor shows list of teams in the league being edited. Has import/export menu items or buttons that raise Qt5 dialogs to select files for import/exports.
 	Has buttons to:
		Delete a team
		Add a team (the team name can be input directly in this window)
		Edit a team
	- Team editor shows list of team members in the team being edited.
 	Has buttons to
		Delete a member
		Add a member (the member's name and email can be input directly in this window)
		Update a member (the member's name and email can be input directly in this window)

## Installation

1. Clone the repositroy:
```
git clone https://github.com/SidneyTeague/Curling_League_Manger.git
```
2. Install dependencies
```
pip install -r requirements.txt
```

## Usage
Run the application by executing 'main_window.py':
```
python main_window.py
```
	 
You will be greeted with a interface with 5 buttons on the left and an empty list on the right. You can either add a league or load a csv file [Leagues.csv](module6/league/tests/Leagues.csv). There is example league.csv you can use.
Once you have leagues in the list you will be able to save the list or delete a league. The edit league button will take you into a second window where you can edit teams within a league.
This team editor is very similar to the league editor interface, with 5 buttons on the left and an empty list on the right. You can either add a team name or import a csv file [Teams.csv](module6/league/tests/Teams.csv). There is example team.csv you can use.
Once you have teams in the list you will be able to export the list or delete a team. The edit team button will take you into a thrid window where you can edit teams members within a team.
This last editor only has 3 buttons on the left and an empty list on the right. You will be able to see, if you loaded your team using the included team.csv, team member including their email. There are edit and delete buttons
to remove a team member or if you need to edit any member information.

## Features

+ Manage curling league, teams, and team member
+ Import and export data from CSV files
	
