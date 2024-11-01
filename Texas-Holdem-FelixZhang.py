############################################## The following section is copied from AI ############################################################
from collections import Counter


def rank_to_value(rank):
    """Converts card rank to numerical value for easier comparison."""
    face_cards = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    if rank.isdigit():
        return int(rank)
    else:
        return face_cards.get(rank)


def hand_value(hand):
    """
    Evaluates the value of a poker hand.

    :param hand: List of Card objects.
    :return: Tuple with hand ranking and details.
    """
    # Sort cards by rank value
    sorted_hand = sorted(hand, key=lambda card: rank_to_value(card.rank), reverse=True)

    # Count the frequency of each rank
    rank_counts = Counter(card.rank for card in sorted_hand)

    # Check if all cards are of the same suit (flush)
    is_flush = len(set(card.suit for card in sorted_hand)) == 1

    # Check for straight (consecutive ranks)
    is_straight = len(set(rank_to_value(card.rank) for card in sorted_hand)) == 5 and \
                  (rank_to_value(sorted_hand[0].rank) - rank_to_value(sorted_hand[4].rank) == 4)

    # Check for special case of Ace-low straight (wheel), considering any suit
    is_wheel_straight = len(set(rank_to_value(card.rank) for card in sorted_hand)) == 5 and \
                        all(rank_to_value(card.rank) in [5, 4, 3, 2, 14] for card in sorted_hand)

    # Determine hand type and value
    if is_flush and (is_straight or is_wheel_straight):
        # Straight Flush / Royal Flush
        high_rank = rank_to_value(sorted_hand[0].rank)
        return (8, high_rank) if high_rank == 14 else (7, high_rank)  # Royal Flush (10 to Ace) or Straight Flush

    if len(rank_counts) == 2 and 4 in rank_counts.values():
        # Four of a Kind
        four_of_a_kind_rank = [rank for rank, count in rank_counts.items() if count == 4][0]
        kicker_rank = [rank for rank, count in rank_counts.items() if count == 1][0]
        return 6, rank_to_value(four_of_a_kind_rank), rank_to_value(kicker_rank)

    if len(rank_counts) == 2 and 3 in rank_counts.values() and 2 in rank_counts.values():
        # Full House
        three_of_a_kind_rank = [rank for rank, count in rank_counts.items() if count == 3][0]
        pair_rank = [rank for rank in rank_counts if rank_counts[rank] == 2][0]
        return 5, rank_to_value(three_of_a_kind_rank), rank_to_value(pair_rank)

    if is_flush:
        # Flush
        return 4, *[rank_to_value(card.rank) for card in sorted_hand]

    if is_straight or is_wheel_straight:
        # Straight
        return 3, rank_to_value(sorted_hand[0].rank)

    if len(rank_counts) == 3 and 3 in rank_counts.values():
        # Three of a Kind
        three_of_a_kind_rank = [rank for rank, count in rank_counts.items() if count == 3][0]
        kickers = sorted([rank_to_value(rank) for rank in rank_counts if rank_counts[rank] == 1], reverse=True)
        return 2, rank_to_value(three_of_a_kind_rank), *kickers
    else:
        pass

    if len(rank_counts) == 3 and 2 in rank_counts.values():
        # Two Pair
        pairs_ranks = [rank for rank, count in rank_counts.items() if count == 2]
        pairs_ranks_value = sorted([rank_to_value(rank) for rank in pairs_ranks], reverse=True)
        kicker_rank = [rank for rank in rank_counts if rank_counts[rank] == 1][0]
        return 1, pairs_ranks_value[0], pairs_ranks_value[1], rank_to_value(kicker_rank)

    if len(rank_counts) == 4 and 2 in rank_counts.values():
        # One Pair
        pair_rank = [rank for rank, count in rank_counts.items() if count == 2][0]
        kickers = sorted([rank_to_value(rank) for rank in rank_counts if rank_counts[rank] == 1], reverse=True)
        return 0, rank_to_value(pair_rank), *kickers

    # High Card
    return -1, *[rank_to_value(card.rank) for card in sorted_hand]


##########################################################################################################################################################
######################################## ALL Codes Below Are Written By Felix-Zhang ######################################################################
##########################################################################################################################################################
import time
import random
import textwrap

# how big the stake is for small blind
small_blind = 5
# the initial ship size each player possess
chipset = small_blind * 400
# initial chance that a computer player bluffs in first inter-rounds
bluff_chance = 0.2
# increase of bluff chance after a computer player decides to bluff
bluff_chance_increase = 0.1
# the maximum bluff chance for computer
bluff_chance_cap = 0.7
# the chance that a computer player bluffs AFTER the first inter-rounds
bluff_chance_after = 0.15
# the chance of calling no matter how big the stake is, after the computer already decides to bluff
bluff_chance_whatsoever = 0.2
# the indented space of outplay on screen terminal
indenture = 40


class Card:
    suits = ['♥', '♠', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def show(self):
        return f"{self.suit}{self.rank}"


class Pack:
    def __init__(self):
        self.cards = [Card(x, y) for x in Card.suits for y in Card.ranks]

    def wash(self):
        random.shuffle(self.cards)
        return

    def draw(self, n):
        cards_drawn = []
        for i in range(n):
            cards_drawn.append(self.cards.pop())
        return cards_drawn

    def rd_draw(self, n):
        cards_drawn = []
        for i in range(n):
            l = len(self.cards)
            j = random.randint(0, l - 1)
            cards_drawn.append(self.cards.pop(j))
        return cards_drawn


class Person:
    def __init__(self, name):
        self.name = name
        self.money = chipset
        self.playing = True
        self.is_allin = False
        self.ready = False
        self.stake = 0  ### this variable connects to the stakes in the game
        self.down = []
        self.hand = []
        self.bluff_chance = bluff_chance

    def fold(self):
        self.playing = False
        slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
        print(f"""{self.name} 弃牌...""")
        print(indenture * ' ', end='', flush=True)
        return

    def call(self):
        if self.stake == stake_ready():
            self.ready = True
            slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
            print(f"""{self.name} 过牌...""")
            print(indenture * ' ', end='', flush=True)
        elif self.money > (stake_ready() - self.stake):
            self.money -= (stake_ready() - self.stake)
            self.stake += (stake_ready() - self.stake)
            self.ready = True
            slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
            print(f"""{self.name} 跟注至 ¥{stake_ready()}...""")
            print(indenture * ' ', end='', flush=True)
        else:
            self.stake += self.money
            self.ready = True
            global is_someone_allin
            is_someone_allin = True
            slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
            print(f"""{self.name} 把仅剩的 ¥{self.money}筹码 ALL-IN 了 !""")
            print(indenture * ' ', end='', flush=True)
            self.money = 0
            self.is_allin = True
        return

    def rise(self, amount):
        if self.money > (stake_ready() - self.stake + amount):
            self.money -= (stake_ready() - self.stake + amount)
            self.stake += (stake_ready() - self.stake + amount)
            self.ready = True
            slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
            print(f"""{self.name} 加注了 ¥{amount}...""")
            print(indenture * ' ', end='', flush=True)
        else:
            self.stake += self.money
            self.ready = True
            global is_someone_allin
            is_someone_allin = True
            slow_print(f"{players.index(self) + 1} ", indent=0, ending='')
            print(f"""{self.name}把仅剩的 ¥{self.money}筹码 ALL-IN 了 !""")
            print(indenture * ' ', end='', flush=True)
            self.money = 0
            self.is_allin = True
        return

    def decide(self):  ### Algorithm for computer to decide Fold/Call/Rise
        print(f"{players.index(self) + 1}{self.name} 思考中...", end='', flush=True)
        if sum_player_stakes() < 20*small_blind:  # in case it's the blind-round, the odds would be too small at the beginning
            pot = 20*small_blind
        elif sum_player_stakes() < 40*small_blind:
            pot = 0.5 * sum_player_stakes() + 20*small_blind
        else:
            pot = sum_player_stakes()
        pot_tenth = 5 * int(pot / 50)
        odds = (stake_ready() - self.stake) / pot
        wins = winning_rate(self.down, cards_on_table)
        print('\r' + (20 + indenture) * ' ', flush=True)
        print(indenture * ' ', end='', flush=True)
        is_bluff = False

        def calculate():
            if wins < 0.5:  # the threshold for raising
                self.call()
            elif wins < 0.6:
                self.rise(pot_tenth * random.randint(1, 3))
            elif wins < 0.65:
                self.rise(pot_tenth * random.randint(1, 5))
            elif wins < 0.7:
                self.rise(pot_tenth * random.randint(1, 7))
            elif wins < 0.75:
                self.rise(pot_tenth * random.randint(1, 9))
            elif wins < 0.8:
                self.rise(pot_tenth * random.randint(1, 11))
            elif wins < 0.85:
                self.rise(pot_tenth * random.randint(1, 13))
            elif wins < 0.9:
                self.rise(pot_tenth * random.randint(1, 16))
            elif wins < 0.95:
                self.rise(pot_tenth * random.randint(1, 19))
            else:
                self.rise(pot_tenth * 10)
            return

        def bluff():
            if is_someone_allin:
                if random.random() < bluff_chance_whatsoever:
                    self.call()
                else:
                    if wins > odds or wins > 0.5:
                        self.call()
                    else:
                        self.fold()
            else:
                if random.random() < bluff_chance_whatsoever:
                    self.call()
                else:
                    if (stake_ready() - self.stake) <= 50 * small_blind:
                        self.rise(pot_tenth * random.randint(1, 10))  # how much to bluff...
                    elif (stake_ready() - self.stake) <= 100 * small_blind:
                        self.call()
                    elif (stake_ready() - self.stake) > 100 * small_blind:
                        if wins <= odds:
                            self.fold()
                        else:
                            self.call()
            return

        if (n_bet_round == 1 and random.random() < self.bluff_chance) or (
                n_bet_round > 1 and random.random() < bluff_chance_after):  # decide whether to bluff...
            is_bluff = True
            self.bluff_chance += bluff_chance_increase
            if self.bluff_chance > bluff_chance_cap:
                self.bluff_chance = bluff_chance_cap
        else:
            pass

        if is_bluff:
            bluff()
        elif not is_bluff:  # now the computer player will use monte-carlo simulation to decide...
            if wins >= odds:
                if is_someone_allin:
                    self.call()
                else:
                    calculate()
            elif wins < odds:
                if odds < 0.2:  # if odds are attractive, give it a try albeit low winning-rate
                    flip_a_coin = random.randint(0, 1)
                    if flip_a_coin == 1:
                        self.call()
                    else:
                        self.fold()
                else:
                    self.fold()
            else:
                print('出BUG了！！！')
        return

    def win(self):
        self.money += sum_player_stakes()
        time.sleep(2)
        print("""
              """)
        print(indenture * ' ' + '§(*￣▽￣*)§')
        print(indenture * ' ' + f"{self.name} 赢了!")
        print(indenture * ' ' + f"{self.name} 拿走了桌上所有的¥{sum_player_stakes()}筹码!")
        self.playing = False
        return


def slow_print(text, indent=indenture, delay=0.2, width=200, ending='\n'):
    wrapped_text = textwrap.fill(text, width=width)
    words = wrapped_text.split()
    space = indent * ' '
    print(space, end='', flush=True)
    for word in words:
        print('' + word, end='', flush=True)  # ' 'for English and '' for Chinese
        time.sleep(delay)
    print(ending, end='', flush=True)
    return


def best_5from7(down, table):
    best = table
    for j in range(7):
        for k in range(6):
            rand_5 = table + down  # reset the 7 cards
            rand_5.pop(j)
            rand_5.pop(k)
            if hand_value(rand_5) > hand_value(best):
                best = rand_5
    return best


def winning_rate(x_down, y_table_now, num_simulation=2000):
    wins = 0
    known_cards = x_down + y_table_now
    for i in range(num_simulation):
        pack2 = Pack()
        for j in range(len(known_cards)):  # remove the cards already-known to the computer player
            for k in range(len(pack2.cards)):
                if pack2.cards[k].suit == known_cards[j].suit and pack2.cards[k].rank == known_cards[j].rank:
                    pack2.cards.remove(pack2.cards[k])
                    break
        table_final = []
        if len(y_table_now) == 5:
            table_final = y_table_now
        else:
            table_final.extend(y_table_now)
            table_final.extend(pack2.rd_draw(5 - len(y_table_now)))  # draw the remaining cards for the table
        opponent_downs = []
        for j in range(5):
            opponent_downs.append(pack2.rd_draw(2))  # draw the down cards of 5 opponents.
        hand = best_5from7(x_down, table_final)  # find the best set the computer player has.
        hand_val = hand_value(hand)
        opponent_hands = [best_5from7(a, table_final) for a in
                          opponent_downs]  # find the best sets opponent players have
        opponent_values = [hand_value(b) for b in opponent_hands]
        oppo_max = max(opponent_values)
        if hand_val > oppo_max:  # compare to see if the computer player beats all opponents
            wins += 1
    return wins / num_simulation  # calculate and return the winning rate for the computer player.


def player_choose(i):
    print('')
    while True:
        command = input(f"'弃'/'跟'/'加'/'信息'>>>")

        if command == '弃':
            print(indenture * ' ', end='', flush=True)
            i.fold()
            break
        elif command == '跟':
            print(indenture * ' ', end='', flush=True)
            i.call()
            break
        elif command == '加' and (stake_ready() > i.stake or n_bet_round == 1):
            if is_someone_allin:
                print("已有玩家ALL IN，无法继续加注")
            else:
                while True:
                    message = input('您想加注多少¥ ? >>')
                    try:
                        a = float(message)
                        if a % 5 != 0:
                            print("输入有误!")
                        else:
                            break
                    except ValueError:
                        print("输入有误!")
                print(indenture * ' ', end='', flush=True)
                i.rise(int(message))
                break
        elif command == '信息':
            print(info())
        else:
            print("输入有误!")
    return


def go_on():
    print('')
    while True:
        message = input("请输入 '好' 来继续游戏>>")
        if message == '好':
            break
    print(indenture * ' ', end='', flush=True)
    return


def still_betting(n):
    is_still_betting = True
    still_players = [i for i in players if i.playing]

    if n == 0 and is_someone_allin:
        is_still_betting = False
    elif n != 0 and all((i.stake == stake_ready() or i.is_allin) for i in still_players):
        is_still_betting = False
    else:
        pass

    if len(still_players) == 1:
        is_still_betting = True

    if len(still_players) == 0:
        is_still_betting = False

    return is_still_betting


# define the six players that are about to start the game
players = []
# define YOU
player = Person("")


##################################### The program jumps here when the player starts a new game ##################################
def new_game():
    global player
    global players

    zhao = Person("赵金宝")
    sun = Person("孙广智")
    li = Person("李延寿")
    zhang = Person("张国强")
    wu = Person("吴家旺")
    myname = input("""请输入您的大名 >>""")
    player = Person(myname)
    players = [zhao, sun, li, zhang, wu, player]
    random.shuffle(players)  # randomly determine the order of playing

    slow_print(f"尊敬 的 {player.name} 您好！  欢迎 莅临 第八届 世界 德扑 大赛 总决赛 !!!")
    slow_print("Designed - and - Coded - by - FelixZhang - from - Shanghai - China - Oct/2024.")
    print(indenture * ' ', end='', flush=True)
    time.sleep(2)
    print('')
    slow_print("今天 我们 很荣幸 地 邀请 到了 本届 比赛 的 全球 6 强 选手，他们 是:")
    print('')
    print(indenture * ' ', end='', flush=True)
    for i in range(6):
        time.sleep(1)
        print(f"{players[i].name}  ", end='', flush=True)
    print("""
          """)
    go_on()
    print('')
    slow_print("以下 是 本次 比赛 的 简要 规则:")
    print('')
    slow_print(f"每位 选手 开局 均 持有 ¥ {chipset} 的 筹码。")
    slow_print(f"小 盲注 为 ¥ {small_blind}，大 盲注 为 ¥ {2*small_blind}。")
    print('')
    slow_print("上述 名单 顺序 即 为 比赛 时 各位 选手 的 下注 顺序， 每局 比赛 结束 后 将 往下 顺移 一位。")
    print('')
    slow_print("比 赛 开 始 后:")
    print(indenture * ' ' + "输入 '弃' - 弃牌离场。")
    print(indenture * ' ' + "输入 '跟' - 跟牌继续。")
    print(indenture * ' ' + "输入 '加' - 加注，并注明您想额外加注的¥数量。")
    print(
        indenture * ' ' + "输入 '信息' - 显示相关信息，如您的底牌、在场玩家数量、场内筹码规模、追平所需筹码、您所剩筹码等。")
    go_on()
    print("""
          """)
    print(indenture * ' ' + '<(￣︶￣)↗[GO!])> 比赛开始!')

    return


# how many inter-rounds have occurred for a certain street
n_bet_round = 0
# the public cards drawn and shown on the table
cards_on_table = []
# is someone all_in ?
is_someone_allin = False


def stake_ready():
    return max(p.stake for p in players)


def sum_player_stakes():
    return sum(p.stake for p in players)


def active_player_number():
    return sum(1 for p in players if p.playing)


def info():
    temp_info = f"""
  您的底牌 :{player.down[0].show()} {player.down[1].show()}
在场玩家数量: {active_player_number()}
场内所有筹码: ¥{sum_player_stakes()}
您的在场筹码: ¥{player.stake}
追平所需筹码: ¥{stake_ready() - player.stake}
您的所剩筹码: ¥{player.money}"""
    return temp_info


############################## the program jumps here when someone has won and goes to the next round ############################
def new_round():
    global players
    global player
    global cards_on_table
    global n_bet_round
    global is_someone_allin

    players = players[1:] + [players[0]]  # move order clockwise
    player_order = players.index(player)  # find YOUR order

    for i in players:  # initialize the game
        if i.money < 10:
            i.playing = False  # to see if a player is dead
        else:
            i.playing = True
        i.ready = False
        i.is_allin = False
        i.stake = 0
        i.down = []
        i.hand = []
        i.bluff_chance = bluff_chance

    cards_on_table = []  # clear the cards on table
    is_someone_allin = False  # clear all_in
    pack = Pack()  # get a new pack of cards
    pack.wash()  # then wash it

    for i in players:
        if i.playing:
            i.down.extend(pack.draw(1))  # get the first down-card for all active players

    for i in players:
        if i.playing:
            i.down.extend(pack.draw(1))  # get the second down-card

    print('')
    slow_print("玩 家 所 剩 筹 码： ")
    print((indenture - 30) * ' ', end='', flush=True)
    for i in players:
        print(f"{i.name} ¥{i.money}   ", end='', flush=True)  # inform of each player's remaining chip size

    print("""

          """)
    slow_print("您 抽 到 的 底 牌 是: ")
    print(indenture * " ", end='', flush=True)
    time.sleep(1.5)
    print(f"{player.down[0].show()}  ", end='', flush=True)
    time.sleep(1.5)
    print(f"{player.down[1].show()}")
    go_on()
    print("""                                           
          """)
    print(indenture * ' ' + '盲注轮开始下注!')

    print(indenture * ' ', end='', flush=True)  # set the cursor to the table center

    ################################################### Blind-Round ######################################################################
    bet0 = stake_ready()
    bet = 0
    n_bet_round = 0
    while still_betting(n_bet_round):
        n_bet_round += 1
        for i in players:
            if not i.playing:
                continue
            elif active_player_number() == 1:
                i.win()
                return
            elif i.is_allin:
                continue
            else:
                if sum_player_stakes() == 0:
                    i.stake = 5
                    i.money -= 5
                    i.ready = True
                    print(f"{players.index(i) + 1}", end='', flush=True)
                    print(f"""{i.name} 下小盲注¥{small_blind}...""")
                    print(indenture * ' ', end='', flush=True)
                elif sum_player_stakes() == 5:
                    i.stake = 10
                    i.money -= 10
                    i.ready = True
                    print(f"{players.index(i) + 1}", end='', flush=True)
                    print(f"""{i.name} 下大盲注¥{small_blind * 2}...""")
                    print(indenture * ' ', end='', flush=True)
                elif players.index(i) == player_order:
                    if stake_ready() == i.stake and bet > 0:
                        continue
                    else:
                        player_choose(i)
                else:
                    if stake_ready() > i.stake or (stake_ready() == i.stake and bet == 0):
                        i.decide()  ###the computer uses Monte-Carlo simulation to make an ultra-rational decision!
                    elif stake_ready() == i.stake and bet > 0:
                        continue

            bet = stake_ready() - bet0

    if len([i for i in players if i.playing]) == 0:
        return

    ######################################################## Flop-Round ########################################################################
    print("""
          """)
    slow_print('翻 牌 轮 开 始 下 注!')
    print("")

    cards_on_table.extend(pack.rd_draw(3))

    slow_print("本 次 抽 到 的 翻 牌 是: ")
    print(indenture * ' ', end='', flush=True)
    time.sleep(2)
    print(f"{cards_on_table[0].show()}  ", end='', flush=True)
    time.sleep(2)
    print(f"{cards_on_table[1].show()}  ", end='', flush=True)
    time.sleep(2)
    print(f"{cards_on_table[2].show()}")
    print(indenture * ' ', end='', flush=True)
    time.sleep(0.5)
    print(f"(您的底牌是: {player.down[0].show()}  {player.down[1].show()})")
    print(indenture * ' ', end='', flush=True)

    bet1 = stake_ready()
    bet = 0
    n_bet_round = 0
    while still_betting(n_bet_round):
        n_bet_round += 1
        for i in players:
            if not i.playing:
                continue
            elif active_player_number() == 1:
                i.win()
                return  # to end this round
            elif i.is_allin:
                continue
            else:
                if players.index(i) == player_order:
                    if stake_ready() == i.stake and bet > 0:
                        continue
                    else:
                        player_choose(i)
                else:
                    if stake_ready() > i.stake or (stake_ready() == i.stake and bet == 0):
                        i.decide()  ###the computer uses Monte-Carlo simulation to make an ultra-rational decision!
                    elif stake_ready() == i.stake and bet > 0:
                        continue

            bet = stake_ready() - bet1

    if len([i for i in players if i.playing]) == 0:
        return

    #############################################################Turn-Round###########################################################
    print("""                                                   
          """)
    slow_print('转 牌 轮 开 始 下 注！')
    print("")

    cards_on_table.extend(pack.rd_draw(1))

    slow_print("本 次 抽 到 的 转 牌 是:")
    print(indenture * ' ', end='', flush=True)
    print(f"{cards_on_table[0].show()}  {cards_on_table[1].show()}  {cards_on_table[2].show()}  ", end='', flush=True)
    time.sleep(2)
    print(f"{cards_on_table[3].show()}")
    print(indenture * ' ', end='', flush=True)
    time.sleep(0.5)
    print(f"(您的底牌是: {player.down[0].show()}  {player.down[1].show()})")
    print(indenture * ' ', end='', flush=True)

    bet2 = stake_ready()
    bet = 0
    n_bet_round = 0
    while still_betting(n_bet_round):
        n_bet_round += 1
        for i in players:
            if not i.playing:
                continue
            elif active_player_number() == 1:
                i.win()
                return  # to end this round
            elif i.is_allin:
                continue
            else:
                if players.index(i) == player_order:
                    if stake_ready() == i.stake and bet > 0:
                        continue
                    else:
                        player_choose(i)
                else:
                    if stake_ready() > i.stake or (stake_ready() == i.stake and bet == 0):
                        i.decide()  ###the computer uses Monte-Carlo simulation to make an ultra-rational decision!
                    elif stake_ready() == i.stake and bet > 0:
                        continue

            bet = stake_ready() - bet2

    if len([i for i in players if i.playing]) == 0:
        return

    ########################################################## River-Round ################################################################
    print("""  
          """)
    slow_print('河 牌 轮 开 始 下 注!')
    print("""  
          """)

    cards_on_table.extend(pack.rd_draw(1))

    slow_print("本 次 抽 到 的 河 牌 是:")
    print(
        indenture * ' ' + f"{cards_on_table[0].show()}  {cards_on_table[1].show()}  {cards_on_table[2].show()}  {cards_on_table[3].show()}  ",
        end='', flush=True)
    time.sleep(2)
    print(f"{cards_on_table[4].show()}")
    print(indenture * ' ', end='', flush=True)
    time.sleep(0.5)
    print(f"(您的底牌是: {player.down[0].show()}  {player.down[1].show()})")
    print(indenture * ' ', end='', flush=True)

    bet3 = stake_ready()
    bet = 0
    n_bet_round = 0
    while still_betting(n_bet_round):
        n_bet_round += 1
        for i in players:
            if not i.playing:
                continue
            elif active_player_number() == 1:
                i.win()
                return  # to end this round
            elif i.is_allin:
                continue
            else:
                if players.index(i) == player_order:
                    if stake_ready() == i.stake and bet > 0:
                        continue
                    else:
                        player_choose(i)
                else:
                    if stake_ready() > i.stake or (stake_ready() == i.stake and bet == 0):
                        i.decide()  ###the computer uses Monte-Carlo simulation to make an ultra-rational decision!
                    elif stake_ready() == i.stake and bet > 0:
                        continue

            bet = stake_ready() - bet3

    if len([i for i in players if i.playing]) == 0:
        return

    ########################################################### Show-Down #########################################################
    last_players = [i for i in players if i.playing]

    while True:
        print('')
        message = input("请输入'摊牌'来互看底牌并比大小>>")  # ready to showdown
        if message == '摊牌':
            print(indenture * ' ', end='', flush=True)
            break
        else:
            print("输入有误！")

    # Show the down-cards!
    print('')
    slow_print('场 上 公 共 牌 为:')
    print(
        indenture * ' ' + f"{cards_on_table[0].show()} {cards_on_table[1].show()} {cards_on_table[2].show()} {cards_on_table[3].show()} {cards_on_table[4].show()}")
    print('')
    print(indenture * ' ' + '在场玩家的底牌为:')
    print(indenture * ' ', end='', flush=True)
    for i in last_players:
        print(f"{i.name} :  ", end='', flush=True)
        time.sleep(1)
        print(f"{i.down[0].show()}  ", end='', flush=True)
        time.sleep(1)
        print(f"{i.down[1].show()}")
        print(indenture * ' ', end='', flush=True)
        time.sleep(1)

    # Find the best composition of 5 cards for each of the remaining players
    for i in players:
        if not i.playing:
            pass
        else:
            i.hand = best_5from7(i.down, cards_on_table)

    # Find the winner!
    last_players_values = [hand_value(i.hand) for i in last_players]
    max_value = max(last_players_values)
    winners = [i for i in last_players if hand_value(i.hand) == max_value]

    if len(winners) == 0 or len(winners) > 4:
        print('')
        print("出BUG了！！！")
    elif len(winners) == 1:
        print('')
        winners[0].win()
    else:
        divided_pot = round((sum_player_stakes() / len(winners)) / 5) * 5
        for i in range(len(winners)):
            winners[i].money += divided_pot

        time.sleep(2)
        print(f"""
               """)
        print(indenture * ' ' + '🎉🎉🎉🎉🎉🎉')
        print(f"""
               """)
        print(indenture * ' ', end='', flush=True)
        for i in range(len(winners)):
            print(f"{winners[i].name}  ", end='', flush=True)

        print(f"不相上下！平局！HolyShit")
        print(indenture * ' ' + f"他们{len(winners)}个人平分了桌上所有的¥{sum_player_stakes()}筹码!")

    return  # End this round of game


######################## The program starts here, all above are definition of classes/ functions/ variables ##################
new_game()

while True:

    new_round()  # play a round of game
    temp = players.copy()
    temp.remove(player)
    num_other_active_players = len([p for p in temp if p.money > 2 * small_blind])
    if player.money > 0 and num_other_active_players > 0:
        while True:
            msg = input("请输入 '继续' 来进入下一局游戏>>")
            if msg == '继续':
                break
            else:
                print("输入有误!")
    else:
        if player.money == 0:
            print(f"""

                   """)
            print(indenture * ' ' + "你输光了！！！")
        elif player.money > 0 and num_other_active_players == 0:

            print(f"""

                   """)
            print(indenture * ' ' + f"恭喜{player.name} 获得了本届比赛的总冠军！")
        while True:
            msg = input("请输入 '新游戏' 来启动新游戏>>")
            if msg == '新游戏':
                new_game()  ## go to start a new game
                break
            else:
                pass
