import csv
from collections import defaultdict
from datetime import datetime, date


myImdbDates = list()
imdbMovieDateSets = defaultdict(set)

# Get my imdb entries dates (+ all dates for each movie for later)
with open('imdb-3.csv') as imdbfile:
    imdbrows = csv.reader(imdbfile, delimiter=',', quotechar='"', skipinitialspace=True)
    for row in imdbrows:
        date = datetime.strptime(row[2], "%d/%m/%y").date().toordinal()
        imdbMovieDateSets[row[1]].add(date)
        if(row[0] != "andrea.piccione@epfl.ch"):
            continue
        myImdbDates.append(date)

print(myImdbDates)

uhToDates = defaultdict(list)
# Read com402 entries dates per user hash
with open('com402-3.csv') as comfile:
    comrows = csv.reader(comfile, delimiter=',', quotechar='"', skipinitialspace=True)
    for row in comrows:
        user = row[0]
        date = datetime.strptime(row[2], "%d/%m/%y").date().toordinal()
        uhToDates[user].append(date)

# Filter user hashes to find myself
for d in myImdbDates:
    possibilities = {d + x for x in range(-13,14)}
    uhToDates = dict((
        (h, ds)
        for h, ds in uhToDates.items()
        if not possibilities.isdisjoint(ds)
    ))
myHash = list(uhToDates)[0]

print(uhToDates)

myMH = set()

# Get my movies hashes from com402
with open('com402-3.csv') as comfile:
    comrows = csv.reader(comfile, delimiter=',', quotechar='"', skipinitialspace=True)
    for row in comrows:
        if(row[0] != myHash):
            continue
        myMH.add(row[1])

moviesHDates = defaultdict(set)
# Get dates for movie hashes that I've seen
with open('com402-3.csv') as comfile:
    comrows = csv.reader(comfile, delimiter=',', quotechar='"', skipinitialspace=True)
    for row in comrows:
        m = row[1]
        if(m not in myMH):
            continue
        date = datetime.strptime(row[2], "%d/%m/%y").date().toordinal()
        for i in range(-13,14):
            moviesHDates[m].add(date + i)

myMovies = list()

# Get the movies names using subset checks
for mh in myMH:
    for m, s in imdbMovieDateSets.items():
        if s <= moviesHDates[mh]:
            myMovies.append(m)
            break

with open('ex1c-movies.txt', 'w') as out:
    out.writelines("\n".join(myMovies))
