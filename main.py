from tkinter import *
from Deck import Deck
from Card import Card
from Player import Player
from Table import Table

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
MINIMUM_PLAYERS = 2
MAXIMUM_PLAYERS = 8
MINIMUM_STARTING_CARDS = 1
MAXIMUM_STARTING_CARDS = 5
NUMBER_OF_STRIKES = 5
BACK_OF_CARD_PATH = "images/back_of_card.gif"
PLAYER_OUT_CARD_PATH = "images/player_out.gif"
CARD_SCALE_FACTOR = 5
PLAYER_DECK_FRAME_WIDTH = 250
CLAIM_OPTIONS = ["High card",
                 "Pair",
                 "Two pair",
                 "Three of a kind",
                 "Straight",
                 "Flush",
                 "Full house",
                 "Four of a kind",
                 "Five of a kind",
                 "Six of a kind",
                 "Straight flush",
                 "Royal flush",
                 "Seven of a kind",
                 "Eight of a kind"]
RANK_OPTIONS = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUIT_OPTIONS = ["Spades", "Hearts", "Clubs", "Diamonds"]


def get_index(choice, l):
    index = 0
    for item in l:
        if item == choice:
            return index
        index += 1
    return -1

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.master = master
        self.back_card_photo = PhotoImage(file=BACK_OF_CARD_PATH)
        self.back_card_photo = self.back_card_photo.subsample(CARD_SCALE_FACTOR, CARD_SCALE_FACTOR)
        self.player_out_photo = PhotoImage(file=PLAYER_OUT_CARD_PATH)
        self.player_out_photo = self.player_out_photo.subsample(CARD_SCALE_FACTOR, CARD_SCALE_FACTOR)
        self.ousted_players = []
        self.round = 0
        self.welcome()

    def welcome(self):
        self.welcome_frame = Frame(self)
        self.welcome_frame.grid()

        self.title = Label(self.welcome_frame,
              text = "BS Poker")
        self.title.config(font = ("Helvetica", 35))
        self.title.grid(row = 0, column = 0, columnspan = 5, padx = 25, pady = 20)
        self.num_players_label = Label(self.welcome_frame,
                                       text="Number of players:",
                                       height=2)
        self.num_players_label.config(wraplength = 100)
        self.num_players_label.grid(row=1, column=1, columnspan=2, sticky=W)
        self.num_players_spinbox = Spinbox(self.welcome_frame,
                                           from_=MINIMUM_PLAYERS,
                                           to=MAXIMUM_PLAYERS,
                                           state='readonly',
                                           width=5)
        self.num_players_spinbox.grid(row=1, column=3)
        # self.num_cards_label = Label(self.welcome_frame,
        #                                text="Starting number of cards:",
        #                                height=3)
        # self.num_cards_label.config(wraplength=70)
        # self.num_cards_label.grid(row=2, column=1, columnspan=2, sticky=W)
        # self.num_cards_spinbox = Spinbox(self.welcome_frame,
        #                                  from_=MINIMUM_STARTING_CARDS,
        #                                  to=MAXIMUM_STARTING_CARDS,
        #                                  state='readonly',
        #                                  width=5)
        # self.num_cards_spinbox.grid(row=2, column=3)
        self.start_btn = Button(self.welcome_frame,
                                text = "Play",
                                command = self.set_up_board)
        self.start_btn.config(font = ("Helvetica", 18), pady = 20)
        self.start_btn.grid(row = 3, column = 1, columnspan = 3)

    def set_up_board(self):
        self.welcome_frame.grid_forget()

        self.board_frame = Frame(self)
        self.board_frame.grid(row = 0)

        self.options_frame = Frame(self)
        self.options_frame.grid(row=1)

        self.num_players = int(self.num_players_spinbox.get())
        self.starting_num_of_cards = MINIMUM_STARTING_CARDS
        # self.starting_num_of_cards = int(self.num_cards_spinbox.get())

        self.table = Table(NUMBER_OF_STRIKES)
        for num in range(self.num_players):
            self.table.add_player(Player(self.starting_num_of_cards))
        self.begin_round()

    def get_first_player(self):
        cur = 0
        while cur in self.ousted_players:
            cur += 1
        return cur

    def get_next_player(self):
        cur = (self.current_player+1) % self.num_players
        while cur in self.ousted_players:
            cur = (cur+1) % self.num_players
        return cur

    def get_previous_player(self):
        cur = (self.current_player-1) % self.num_players
        while cur in self.ousted_players:
            cur = (cur-1) % self.num_players
        return cur

    def get_participating_players(self): # returns INDICES of players, not the actual Player objects themselves -- use the player index map to access their respective Player objects
        participating_players = []
        for i in range(self.num_players):
            if i not in self.ousted_players:
                participating_players.append(i)
        return participating_players

    def indices_map(self):
        return dict(zip(self.get_participating_players(), [x for x in range(len(self.players))]))

    def player_index_map(self):
        return dict(zip(self.get_participating_players(), self.players))

    def begin_round(self):
        self.round += 1
        self.clear_frame(self.board_frame)
        self.clear_frame(self.options_frame)
        round_label = Label(self.board_frame, text="Starting Round " + str(self.round) + ".")
        round_label.grid(row=0, column=0)
        round_btn = Button(self.board_frame, text="OK", command=self.start_game)
        round_btn.grid(row=0, column=1)

    def start_game(self):
        self.clear_frame(self.board_frame)

        self.players = self.table.get_players() # Not necessarily the same number of players in the beginning, since players will be out each round

        # Variables that will change during the game

        self.current_player = self.get_first_player() # Current player
        self.player_map = self.player_index_map() # Maps # of player (zero-indexed) to the Player object associated

        self.first_turn = True

        # The current stats that we compare
        self.current_claim = 0
        self.current_rank = -1
        self.current_suit = -1

        # Keep track of widgets
        self.selected_widgets = (None, None)

        # Begin
        self.table.distribute_cards()
        self.player_frames = []

        # Show facing down cards of players
        for i in range(self.num_players):
            current_label = Label(self.board_frame,
                                  text = "Player " + str(i+1),
                                  padx = 20,
                                  pady = 20)
            card_frame = Frame(self.board_frame, width=PLAYER_DECK_FRAME_WIDTH, height=self.back_card_photo.height()+25, padx=20)
            if i <= 3:
                current_label.grid(row = i, column = 0)
                card_frame.grid(row = i, column = 1)
            else:
                current_label.grid(row=i-4, column=2)
                card_frame.grid(row=i-4, column=3)
            self.player_frames.append(card_frame)
        #self.print_player_status()
        self.next_player_screen() # Begin player's turn

    def display_back_cards(self, parent_frame, num_of_cards):
        interval = (parent_frame.winfo_reqwidth() - self.back_card_photo.width())/(parent_frame.winfo_reqwidth() * (MAXIMUM_STARTING_CARDS - 1))
        for i in range(num_of_cards):
            Label(parent_frame, image=self.back_card_photo).place(relx=i*interval)

    def display_player_cards(self, player_num):
        parent_frame = self.player_frames[player_num]
        current_player = self.player_map[player_num]
        current_cards = current_player.get_cards()
        num_of_cards = len(current_cards)
        interval = (parent_frame.winfo_reqwidth() - self.back_card_photo.width())/(parent_frame.winfo_reqwidth() * (MAXIMUM_STARTING_CARDS - 1))
        for i in range(num_of_cards):
            current_card = current_cards[i]
            current_img = PhotoImage(file=self.get_image_url(current_card.get_rank(), current_card.get_suit()))
            current_img = current_img.subsample(CARD_SCALE_FACTOR, CARD_SCALE_FACTOR)
            current_img_label = Label(parent_frame, image=current_img)
            current_img_label.image = current_img
            current_img_label.place(relx=i*interval)

    def show_and_hide_cards(self, show=()):
        for i in range(len(self.player_frames)):
            self.clear_frame(self.player_frames[i])
            if i not in self.ousted_players:
                if i not in show:
                    self.display_back_cards(self.player_frames[i], len(self.player_map[i].get_cards()))
                else:
                    self.display_player_cards(i)
            else:
                Label(self.player_frames[i], image=self.player_out_photo).place(relx=0)

    def next_player_screen(self):
        self.show_and_hide_cards()
        self.clear_frame(self.options_frame)
        confirm_label = Label(self.options_frame, text="It is now Player " + str(self.current_player + 1) + "'s turn.")
        confirm_label.grid(row = 0, column = 0)
        confirm_btn = Button(self.options_frame, text="OK", command = self.get_player_turn)
        confirm_btn.grid(row = 0, column = 1)

    def get_player_turn(self):
        #self.print_status()
        self.show_and_hide_cards(show=(self.current_player,))
        self.clear_frame(self.options_frame)

        if self.first_turn:
            self.first_turn = False
        else: # If it's not the first turn
            claim_info = CLAIM_OPTIONS[self.current_claim]
            if self.current_rank == -1 and self.current_suit != -1:
                claim_info += ", " + SUIT_OPTIONS[self.current_suit]
            elif self.current_rank != -1 and self.current_suit == -1:
                claim_info += ", " + RANK_OPTIONS[self.current_rank]
            elif self.current_rank != -1 and self.current_suit != -1:
                claim_info += ", Rank: " + RANK_OPTIONS[self.current_rank] + ", Suit: " + SUIT_OPTIONS[self.current_suit]
            self.previous_claim_label = Label(self.options_frame,
                                              text="The previous player claimed: " + claim_info)
            self.previous_claim_label.grid(row=0, column=0)

            self.bs_btn = Button(self.options_frame,
                                 text = "Call BS",
                                 command = self.handle_bs)
            self.bs_btn.grid(row = 1, column = 1)

        self.current_player_label = Label(self.options_frame,
                                          text = "Current turn: Player "+str(self.current_player+1))
        self.current_player_label.grid(row = 1, column = 0)

        # If we have not exhausted all possible choices
        if not (self.current_claim == len(CLAIM_OPTIONS) - 1 and self.current_rank == len(RANK_OPTIONS) - 1):
            self.hand_label = Label(self.options_frame,
                                    text = "Claim hand:")
            self.hand_label.grid(row = 2, column = 0)
            self.hand_menu_str = StringVar()
            self.hand_menu_str.set("Select one")
            self.hand_menu = OptionMenu(self.options_frame, self.hand_menu_str, *CLAIM_OPTIONS[(self.current_claim+1):] if self.current_claim == 11 else (CLAIM_OPTIONS[self.current_claim:] if self.current_rank < len(RANK_OPTIONS) - 1 else CLAIM_OPTIONS[(self.current_claim+1):]))
            self.hand_menu.grid(row = 2, column = 1)
            self.options_choice_frame = Frame(self.options_frame)
            self.options_choice_frame.grid(row = 2, column = 2)
            self.hand_menu_str.trace("w", self.handle_choice)
            self.claim_btn = Button(self.options_frame,
                                    text = "Claim hand",
                                    command = self.handle_claim)
            self.claim_btn.grid(row = 1, column = 2)
        # else: Force the next player to BS it

    def handle_choice(self, *args):
        self.clear_frame(self.options_choice_frame)
        choice = self.hand_menu_str.get()

        if choice in ["Flush","Straight","Straight flush","Royal flush"]:
            if choice == "Flush" or choice == "Straight flush":
                question_label_rank = Label(self.options_choice_frame,
                                            text="Specify the rank of the highest card:")
                question_label_rank.grid(row=0, column=0)
                rank_str = StringVar()
                rank_str.set(RANK_OPTIONS[self.current_rank + 1] if choice == CLAIM_OPTIONS[self.current_claim] else (RANK_OPTIONS[0] if choice not in ["Flush","Straight","Straight flush"] else RANK_OPTIONS[3]))
                rank_menu = OptionMenu(self.options_choice_frame, rank_str, *RANK_OPTIONS[max(3,self.current_rank + 1):] if choice == CLAIM_OPTIONS[self.current_claim] else (RANK_OPTIONS if choice not in ["Straight","Flush","Straight flush"] else RANK_OPTIONS[3:]))
                rank_menu.grid(row=0, column=1)

                question_label_suit = Label(self.options_choice_frame,
                                            text="Specify the suit:")
                question_label_suit.grid(row=1, column=0)
                suit_str = StringVar()
                suit_str.set(SUIT_OPTIONS[0])
                suit_menu = OptionMenu(self.options_choice_frame, suit_str, *SUIT_OPTIONS)
                suit_menu.grid(row=1, column=1)
                self.selected_widgets = (rank_str, suit_str)
            elif choice == "Straight":
                question_label = Label(self.options_choice_frame,
                                       text="Specify the rank of the highest card:")
                question_label.grid(row=0, column=0)
                rank_str = StringVar()
                rank_str.set(RANK_OPTIONS[self.current_rank + 1] if choice == CLAIM_OPTIONS[self.current_claim] else (RANK_OPTIONS[0] if choice not in ["Flush","Straight","Straight flush"] else RANK_OPTIONS[3]))
                rank_menu = OptionMenu(self.options_choice_frame, rank_str, *RANK_OPTIONS[max(3,self.current_rank + 1):] if choice == CLAIM_OPTIONS[self.current_claim] else (RANK_OPTIONS if choice not in ["Straight","Flush","Straight flush"] else RANK_OPTIONS[3:]))
                rank_menu.grid(row=0, column=1)
                self.selected_widgets = (rank_str, None)
            elif choice == "Royal flush":
                question_label_suit = Label(self.options_choice_frame,
                                            text="Specify the suit:")
                question_label_suit.grid(row=0, column=0)
                suit_str = StringVar()
                suit_str.set(SUIT_OPTIONS[0])
                suit_menu = OptionMenu(self.options_choice_frame, suit_str, *SUIT_OPTIONS)
                suit_menu.grid(row=0, column=1)
                self.selected_widgets = (None, suit_str)
        else:
            question_label = Label(self.options_choice_frame,
                                   text="")
            question_label.grid(row=0, column=0)
            rank_str = StringVar()
            rank_str.set(RANK_OPTIONS[self.current_rank + 1] if choice == CLAIM_OPTIONS[self.current_claim] else RANK_OPTIONS[0])
            rank_menu = OptionMenu(self.options_choice_frame, rank_str, *RANK_OPTIONS[(self.current_rank + 1):] if choice == CLAIM_OPTIONS[self.current_claim] else RANK_OPTIONS)
            rank_menu.grid(row=0, column=1)
            self.selected_widgets = (rank_str, None)
            if choice in ["High card","Pair","Three of a kind","Four of a kind","Five of a kind","Six of a kind","Seven of a kind","Eight of a kind"]:
                question_label.configure(text = "Specify the rank of the card:")
            elif choice == "Two pair":
                question_label.configure(text="Specify the rank of the higher pair:")
            elif choice == "Full house":
                question_label.configure(text="Specify the rank of triple:")

    def print_player_status(self):
        print(self.ousted_players)
        for i in self.get_participating_players():
            print("Player "+str(i+1)+": "+str(self.player_map[i]))

    def handle_bs(self):
        self.show_and_hide_cards(show=tuple(self.get_participating_players()))
        if self.current_claim in [0,1,3,7,8,9,12,13]:
            hand_type = "single"
            if self.current_claim == 0: count_bound = 1
            elif self.current_claim == 1: count_bound = 2
            elif self.current_claim == 3: count_bound = 3
            elif self.current_claim == 7: count_bound = 4
            elif self.current_claim == 8: count_bound = 5
            elif self.current_claim == 9: count_bound = 6
            elif self.current_claim == 12: count_bound = 7
            else: count_bound = 8
        elif self.current_claim == 6:
            hand_type = "full house"
            count_bound = None
        elif self.current_claim == 2:
            hand_type = "two pair"
            count_bound = None
        else:
            hand_type = "five"
            count_bound = 5
        if self.current_rank != -1:
            if RANK_OPTIONS[self.current_rank] == "J": rank_bound = 11
            elif RANK_OPTIONS[self.current_rank] == "Q": rank_bound = 12
            elif RANK_OPTIONS[self.current_rank] == "K": rank_bound = 13
            elif RANK_OPTIONS[self.current_rank] == "A": rank_bound = 14
            else: rank_bound = int(RANK_OPTIONS[self.current_rank])
        else:
            rank_bound = 14
        rank_bound2 = rank_bound - 4
        if self.current_suit != -1:
            suit_bound = Deck.NUM_TO_SUIT[self.current_suit]
        else:
            suit_bound = None

        validate = self.table.contains(hand_type, rank_bound, rank_bound2, count_bound, suit_bound)
        self.table.collect_cards()
        if validate:
            losing_player = self.current_player
            losing_info = "BS Unsuccessful!"
        else:
            losing_player = self.get_previous_player()
            losing_info = "BS Successful!"

        self.clear_frame(self.options_frame)
        losing_label = Label(self.options_frame, text=losing_info)
        losing_label.grid(row=0, column=0)

        self.player_map[losing_player].increment_card_count()
        if self.player_map[losing_player].get_card_count() > NUMBER_OF_STRIKES:
            self.table.remove_player(self.indices_map()[losing_player])
            self.ousted_players.append(losing_player)
            if losing_player == self.current_player:
                out_info = "You are now out of the game."
            else:
                out_info = "Player " + str(losing_player+1) + " is now out of the game."
            out_label = Label(self.options_frame, text=out_info)
            out_label.grid(row = 0, column = 1)


        if len(self.get_participating_players()) == 1: # Only one person left
            win_label = Label(self.options_frame, text="Player " + str(self.get_participating_players()[0]+1) + " has won!")
            win_label.grid(row=1, column=1)
        else:
            losing_btn = Button(self.options_frame, text="Start next round", command=self.begin_round)
            losing_btn.grid(row=1, column=0)

    def handle_claim(self):
        user_choice = self.hand_menu_str.get()
        if user_choice != "Select one":
            self.current_claim = get_index(user_choice, CLAIM_OPTIONS)
            if user_choice in ["Flush","Straight flush"]:
                self.current_rank = get_index(self.selected_widgets[0].get(), RANK_OPTIONS)
                self.current_suit = get_index(self.selected_widgets[1].get(), SUIT_OPTIONS)
            elif user_choice == "Royal flush":
                self.current_rank = -1
                self.current_suit = get_index(self.selected_widgets[1].get(), SUIT_OPTIONS)
            else:
                self.current_rank = get_index(self.selected_widgets[0].get(), RANK_OPTIONS)
                self.current_suit = -1
            self.switch_player()

    def switch_player(self):
        self.current_player = self.get_next_player()
        self.next_player_screen()

    def get_image_url(self, rank, suit):
        assert rank in Card.RANKS
        assert suit in Card.SUITS

        if rank > 10:
            if rank == 11: url_rank = "jack"
            elif rank == 12: url_rank = "queen"
            elif rank == 13: url_rank = "king"
            else: url_rank = "ace"
        else:
            url_rank = str(rank)

        if suit == "S": url_suit = "spades"
        elif suit == "H": url_suit = "hearts"
        elif suit == "C": url_suit = "clubs"
        else: url_suit = "diamonds"

        return "images/"+url_rank + "_of_" + url_suit + ".gif"

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def print_status(self):
        print("Player "+str(self.current_player+1)+"'s turn:")
        print("current_claim: "+str(self.current_claim))
        print("current_rank: "+str(self.current_rank))
        print("current_suit: "+str(self.current_suit))

def main():
    root = Tk()
    root.title("BS Poker")
    # root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
    app = Application(root).pack(fill = BOTH, expand=True)
    root.mainloop()

main()
