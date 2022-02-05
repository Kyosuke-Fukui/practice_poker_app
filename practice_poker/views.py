from django.shortcuts import render
import glob
import random

# Create your views here.


def index(request):
    if request.method == 'GET':
        return render(request, "html/home.html")

    else:
        files = glob.glob(
            r"static/history.txt")

        with open(files[0]) as fi:
            game = []
            data = []
            while True:
                line = fi.readline()

                if 'starts' in line:
                    if game:
                        data.append(game)
                    game = []

                if not line == '\n':
                    game.append(line.strip())
                if not line:
                    break

        # データ前処理の都合上、BB以外がbbを払っていることになっているものがあり、それをスキップ
        flag = True
        while flag:
            i = random.randint(0, len(data)-1)
            for line in data[i]:
                if 'BB posts big blind' in line:
                    flag = False
                    break

        output = []
        position = ''
        for line in data[i]:
            if 'wins' in line:
                position = line.split(' ')[0]

        output.append("<div>You are " + position + ".</div>")

        hand = []
        for line in data[i]:
            if position + " shows" in line:
                hand = map(lambda x: x[0:2], line.split(' ')[3:5])

        start = False
        className = ''
        flop = []
        turn = ''
        river = ''
        for line in data[i]:
            # print(line)

            if "is the button" in line:
                start = True

            if start:
                if "Dealing down cards" in line:
                    className = 'hist'
                elif "Dealing Flop" in line:
                    flop = map(lambda x: x[0:2], line.split(' ')[5:8])
                elif "Dealing Turn" in line:
                    turn = line.split(' ')[5][0:2]
                elif "Dealing River" in line:
                    river = line.split(' ')[5][0:2]

                if position in line:
                    if ("bets" in line) or ("checks" in line) or ("calls" in line) or ("raises" in line) or ("all-In" in line):
                        output.append(
                            '<div class="' + className +
                            '"><button value="' + line + '">Bet</button>\
                        <button value="' + line + '">Check</button>\
                        <button value="' + line + '">Call</button>\
                        <button value="' + line + '">Raise</button>\
                        <button value="' + line + '">All-In</button>\
                        <button value="' + line + '">Fold</button></div>')
                    else:
                        output.append('<div class="' + className +
                                      '">' + line + '</div>')

                # The time atを含む行と途中離脱、参加者のIDを含む行をスキップ
                elif ("The time at" not in line) and (max(map(lambda x: len(x), line.split())) < 20):
                    output.append('<div class="' + className +
                                  '">' + line + '</div>')
        return render(request, "html/home.html",
                      {"output": output,
                       "hand": hand,
                       "flop": flop,
                       "turn": turn,
                       "river": river})
