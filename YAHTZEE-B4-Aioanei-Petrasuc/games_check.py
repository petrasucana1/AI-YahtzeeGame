def Ones(dices):
    sum=0
    for dice in dices[1]:
        if dice==1:
            sum=sum+1

    return sum


def Twos(dices):
    sum = 0
    for dice in dices[1]:
        if dice == 2:
            sum = sum + 2

    return sum


def Threes(dices):
    sum = 0
    for dice in dices[1]:
        if dice == 3:
            sum = sum + 3

    return sum


def Fours(dices):
    sum = 0
    for dice in dices[1]:
        if dice == 4:
            sum = sum + 4

    return sum


def Fives(dices):
    sum = 0
    for dice in dices[1]:
        if dice == 5:
            sum = sum + 5

    return sum


def Sixes(dices):
    sum = 0
    for dice in dices[1]:
        if dice == 6:
            sum = sum + 6

    return sum


def Three_of_a_kind(dices):
    sum=0
    counts = {}

    for dice in dices[1]:
        if dice in counts:
            counts[dice] += 1
        else:
            counts[dice] = 1
        sum=sum+dice

    for count in counts.values():
        if count >= 3:
           return sum
    return 0

def Four_of_a_kind(dices):
    sum=0
    counts = {}

    for dice in dices[1]:
        if dice in counts:
            counts[dice] += 1
        else:
            counts[dice] = 1
        sum=sum+dice

    for count in counts.values():
        if count == 4:
           return sum
    return 0


def Full_House(dices):
    counts = {}

    for dice in dices[1]:
        if dice in counts:
            counts[dice] += 1
        else:
            counts[dice] = 1

    has_three_of_a_kind = False
    has_pair = False

    for count in counts.values():
        if count == 3:
            has_three_of_a_kind = True
        elif count == 2:
            has_pair = True

    if has_three_of_a_kind and has_pair:
        return 25
    else:
        return 0


def Small_Straight(dices):
    check_ss = sorted(set(dices[1]))

    for i in range(len(check_ss) - 3):
        if (check_ss[i] + 1 == check_ss[i + 1] and
                check_ss[i] + 2 == check_ss[i + 2] and
                check_ss[i] + 3 == check_ss[i + 3]):
            return 30

    return 0

def Large_Straight(dices):
    check_ls = sorted(set(dices[1]))

    for i in range(len(check_ls) - 4):
        if (check_ls[i] + 1 == check_ls[i + 1] and
                check_ls[i] + 2 == check_ls[i + 2] and
                check_ls[i] + 3 == check_ls[i + 3] and
                check_ls[i] + 4 == check_ls[i + 4]):
            return 40

    return 0

def Chance(dices):
    sum=0

    for dice in dices[1]:
        sum=sum+dice

    return sum

def YAHTZEE(dices):
    counts = {}

    for dice in dices[1]:
        if dice in counts:
            counts[dice] += 1
        else:
            counts[dice] = 1

    for count in counts.values():
        if count ==5 and dices[1][0]!=0 :
            return 50
    return 0

game_functions = {
    "Ones": Ones,
    "Twos": Twos,
    "Threes": Threes,
    "Fours": Fours,
    "Fives": Fives,
    "Sixes": Sixes,
    "Three of a kind": Three_of_a_kind,
    "Four of a kind": Four_of_a_kind,
    "Full House": Full_House,
    "Small Straight": Small_Straight,
    "Large Straight": Large_Straight,
    "Chance": Chance,
    "YAHTZEE": YAHTZEE
}

game_numbers = {
    "Ones": 1,
    "Twos": 2,
    "Threes": 3,
    "Fours": 4,
    "Fives": 5,
    "Sixes": 6,
    "Three of a kind": 7,
    "Four of a kind": 8,
    "Full House": 9,
    "Small Straight": 10,
    "Large Straight": 11,
    "Chance": 12,
    "YAHTZEE": 13
}

index_to_game_name = {
    1: "Ones",
    2: "Twos",
    3: "Threes",
    4: "Fours",
    5: "Fives",
    6: "Sixes",
    7: "Three of a kind",
    8: "Four of a kind",
    9: "Full House",
    10: "Small Straight",
    11: "Large Straight",
    12: "Chance",
    13: "YAHTZEE"
}

max_scores = {
    "Ones": 5 * 1, "Twos": 5 * 2, "Threes": 5 * 3,
    "Fours": 5 * 4, "Fives": 5 * 5, "Sixes": 5 * 6,
    "Three of a kind": 30, "Four of a kind": 30, "Full House": 25,
    "Small Straight": 30, "Large Straight": 40, "Chance": 30, "YAHTZEE": 50
}