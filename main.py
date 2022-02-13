# This is a sample Python script.

import matplotlib.pyplot as plt
import time
import csv
import argparse

DEBUG = False

raw = {'Users': [], 'Hands': []}
user = {'ids': {}, 'Hands_played': {}}
Hand = 0
Money = {'ids': {}}

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help="Enter Filename to parse", required=True)
parser.add_argument('-o', '--onscreen', help="true or false, would you like the graph to be onscreen?", required=True)
parser.add_argument('--debug')
args = parser.parse_args()

filename = args.filename
onscreen = args.onscreen

if "true" in str(args.onscreen).lower():
    Onscreen = True
else:
    onscreen = False

with open(filename) as csv_file:
    csv_reader = reversed(list(csv.reader(csv_file, delimiter=',')))

    for row in csv_reader:
        if DEBUG:
            print(row)

        # Create a link between the players and each of their ids
        if "The admin approved the player" in row[0]:
            if DEBUG:
                print(row[0])
            raw['Users'].append(row)

        if "Player stacks" in row[0]:

            raw['Hands'].append(row)

            if DEBUG:
                print(row[0])

    if DEBUG:
        print("Printing the raw data")
        print(raw)

    # Create the list of users which we will then use to gather there round ending scores
    for raw_line in raw['Users']:
        if DEBUG:
            print(raw_line)

        User = raw_line[0].split('"')
        User = User[1].split('@')
        Real_Name = User[0].strip()
        User_Id = User[1].strip()

        if DEBUG:
            print(Real_Name)
            print(User_Id)

        user['ids'][Real_Name] = User_Id

        if DEBUG:
            print(user)

        for Poker_Player in user['ids']:
            if DEBUG:
                print(Poker_Player)

            Poker_Player_id = user['ids'][Poker_Player]
            if DEBUG:
                print(Poker_Player_id)

    for raw_line in raw['Hands']:
        Hand = Hand + 1

        print("Parsing information from hand: " + str(Hand))

        # Parse the lines which contain the scores and add then to a link
        Score_line = raw_line[0].split(':')
        Score_line = Score_line[1].split('|')

        print(Score_line)

        # print(row)
        print("Print Score Line: " + str(Score_line))

        for user_score_line in Score_line:
            if DEBUG:
                print(user_score_line)
            score_id = user_score_line.split("@")
            score_id = score_id[1].split('"')
            score_line_id = score_id[0].strip()
            score_value = score_id[1].strip().strip("(").strip(")")

            print("User ID: " + str(score_line_id))
            print("User Score: " + str(score_value))

            if score_line_id not in Money['ids']:
                Money['ids'][score_line_id] = {}
            Money['ids'][score_line_id][Hand] = {}
            Money['ids'][score_line_id][Hand] = int(score_value)

    print("The number of Hands played in this game where: " + str(Hand))

    if DEBUG:
        print(user)

    # Creating the initial graph from the users

    for users_in_game, user_in_game_id in user['ids'].items():
        print("Processing User: " + str(users_in_game) + " with id: " + str(user_in_game_id))

        user['Hands_played'][user_in_game_id] = len(Money['ids'][user_in_game_id])
        print("The number of Hands played for user: " + str(users_in_game) + " was " + str(
            user['Hands_played'][user_in_game_id]))

        x = list(Money['ids'][user_in_game_id].keys())
        y = list(Money['ids'][user_in_game_id].values())

        if DEBUG:
            print("Y Axis Data")
            print(y)

            print("x Axis Data")
            print(x)

        # plot lines
        plt.plot(x, y, label=users_in_game)

        # for score_per_round in Money['ids'][user_in_game_id]:
        #     print(Len)

    if DEBUG:
        print(Money['ids'])
        print(user['ids'])

    timestr = time.strftime("%Y%m%d-%H%M%S")
    timestr

    plt.legend()
    plt.draw()
    plt.grid()
    plt.savefig("Poker_Game-" + str(timestr) + ".png", format='png', dpi=1200)
    if onscreen:
        plt.show()
