import csv
import sys

#Extracts the following features from the last five games
HOME_NO_WINS = 0
HOME_NO_DRAWS = 1
HOME_NO_LOSSES = 2
HOME_GOALS_SCORED = 3
HOME_GOALS_CONCEDED = 4
HOME_SHOTS_FOR = 5
HOME_SHOTS_AGAINST = 6
HOME_SHOTS_TARGET_FOR = 7
HOME_SHOTS_TARGET_AGAINST = 8
AWAY_NO_WINS = 9
AWAY_NO_DRAWS = 10
AWAY_NO_LOSSES = 11
AWAY_GOALS_SCORED = 12
AWAY_GOALS_CONCEDED = 13
AWAY_SHOTS_FOR = 14
AWAY_SHOTS_AGAINST = 15
AWAY_SHOTS_TARGET_FOR = 16
AWAY_SHOTS_TARGET_AGAINST = 17
BET365HOME_WIN = 18
BET365DRAW = 19
BET365AWAY_WIN = 20
BETWAYHOME_WIN = 21
BETWAY_DRAW = 22
BETWAY_AWAY_WIN = 23
ACTUAL_RESULT = 24
ACTUAL_HOME_GOALS = 25
ACTUAL_AWAY_GOALS = 26

#The number of matches being considered
NO_MATCHES_CONSIDERED = 5

f = open(sys.argv[1])
reader = csv.reader(f)

encountered_matches = {}

i = 0
for row in reader:
    if i != 0:
        if row[2] not in encountered_matches:
            encountered_matches[row[2]] = []
        if row[3] not in encountered_matches:
            encountered_matches[row[3]] = []
        encountered_matches[row[2]].append(row)
        encountered_matches[row[3]].append(row)
    i += 1
f.close()
f = open(sys.argv[1])
reader = csv.reader(f)

data_struct = []
j = 0
for row in reader:
    home_last_five_matches = []
    if j != 0:
        i = 0
        while encountered_matches[row[2]][i][3] != row[3]:
            i += 1
        if i > NO_MATCHES_CONSIDERED:
            for x in range(NO_MATCHES_CONSIDERED):
                home_last_five_matches.append(encountered_matches[row[2]][i - 1 - x])

            away_last_five_matches = []

            i = 0
            while encountered_matches[row[3]][i][2] != row[2]:
                i += 1
            if i > NO_MATCHES_CONSIDERED:
                for x in range(NO_MATCHES_CONSIDERED):
                    away_last_five_matches.append(encountered_matches[row[3]][i - 1 - x])

                home_team = row[2]
                away_team = row[3]

                home_no_wins = 0
                home_no_draws = 0
                home_no_losses = 0
                home_goals_scored = 0
                home_goals_conceded = 0
                home_shots_for = 0
                home_shots_against = 0
                home_shots_target_for = 0
                home_shots_target_against = 0

                for match in home_last_five_matches:
                    if match[2] == home_team:
                        if (match[6] == 'H'):
                            home_no_wins += 1
                        elif (match[6] == 'D'):
                            home_no_draws += 1
                        elif (match[6] == 'A'):
                            home_no_losses += 1
                        else:
                            raise Exception('Invalid result')
                        home_goals_scored += int(match[4])
                        home_goals_conceded += int(match[5])
                        home_shots_for += int(match[11])
                        home_shots_against += int(match[12])
                        home_shots_target_for += int(match[13])
                        home_shots_target_against += int(match[14])
                    elif match[3] == home_team:
                        if (match[6] == 'H'):
                            home_no_losses += 1
                        elif (match[6] == 'D'):
                            home_no_draws += 1
                        elif (match[6] == 'A'):
                            home_no_wins += 1
                        else:
                            raise Exception('Invalid result')
                        home_goals_scored += int(match[5])
                        home_goals_conceded += int(match[4])
                        home_shots_for += int(match[12])
                        home_shots_against += int(match[11])
                        home_shots_target_for += int(match[14])
                        home_shots_target_against += int(match[13])

                    else:
                        raise Exception('Team not found')

                away_no_wins = 0
                away_no_draws = 0
                away_no_losses = 0
                away_goals_scored = 0
                away_goals_conceded = 0
                away_shots_for = 0
                away_shots_against = 0
                away_shots_target_for = 0
                away_shots_target_against = 0

                for match in away_last_five_matches:
                    if match[2] == away_team:
                        if (match[6] == 'H'):
                            away_no_wins += 1
                        elif (match[6] == 'D'):
                            away_no_draws += 1
                        elif (match[6] == 'A'):
                            away_no_losses += 1
                        else:
                            raise Exception('Invalid result')
                        away_goals_scored += int(match[4])
                        away_goals_conceded += int(match[5])
                        away_shots_for += int(match[11])
                        away_shots_against += int(match[12])
                        away_shots_target_for += int(match[13])
                        away_shots_target_against += int(match[14])
                    elif match[3] == away_team:
                        if (match[6] == 'H'):
                            away_no_losses += 1
                        elif (match[6] == 'D'):
                            away_no_draws += 1
                        elif (match[6] == 'A'):
                            away_no_wins += 1
                        else:
                            raise Exception('Invalid result')
                        away_goals_scored += int(match[5])
                        away_goals_conceded += int(match[4])
                        away_shots_for += int(match[12])
                        away_shots_against += int(match[11])
                        away_shots_target_for += int(match[14])
                        away_shots_target_against += int(match[13])

                    else:
                        raise Exception('Team not found')
                for i in range(23, 29):
                    if row[i] == "":
                        row[i] = "2.5"
                entry = [home_no_wins, home_no_losses, home_no_draws, home_goals_scored, \
                home_goals_conceded, home_shots_for, home_shots_against, home_shots_target_for, \
                home_shots_target_against, away_no_wins, away_no_draws, away_no_losses, \
                away_goals_scored, away_goals_conceded, away_shots_for, away_shots_against, \
                away_shots_target_for, away_shots_target_against, int(float(row[23]) * 100),
                int(float(row[24]) * 100), int(float(row[25]) * 100), int(float(row[26]) * 100),
                int(float(row[27]) * 100), int(float(row[28]) * 100), row[6], int(row[4]), int(row[5])]

                data_struct.append(entry)
    j += 1
f.close()

print(data_struct)
