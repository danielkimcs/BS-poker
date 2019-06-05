from tkinter import *
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
BACK_OF_CARD_SCALE_FACTOR = 12
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
RANK_OPTIONS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "K", "A"]

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.master = master
        self.back_card_photo = PhotoImage(file=BACK_OF_CARD_PATH)
        self.back_card_photo = self.back_card_photo.subsample(BACK_OF_CARD_SCALE_FACTOR, BACK_OF_CARD_SCALE_FACTOR)
        self.claim_options = CLAIM_OPTIONS.copy()
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
        self.num_players_label.grid(row=1, column=1, columnspan=2, sticky=W)
        self.num_players_spinbox = Spinbox(self.welcome_frame,
                                           from_=MINIMUM_PLAYERS,
                                           to=MAXIMUM_PLAYERS,
                                           state='readonly',
                                           width=5)
        self.num_players_spinbox.grid(row=1, column=3)
        self.num_cards_label = Label(self.welcome_frame,
                                       text="Starting number of cards:",
                                       height=2)
        self.num_cards_label.grid(row=2, column=1, columnspan=2, sticky=W)
        self.num_cards_spinbox = Spinbox(self.welcome_frame,
                                         from_=MINIMUM_STARTING_CARDS,
                                         to=MAXIMUM_STARTING_CARDS,
                                         state='readonly',
                                         width=5)
        self.num_cards_spinbox.grid(row=2, column=3)
        self.start_btn = Button(self.welcome_frame,
                                text = "Play",
                                command = self.set_up_board)
        self.start_btn.config(font = ("Helvetica", 18), pady = 20)
        self.start_btn.grid(row = 3, column = 1, columnspan = 3)

    def set_up_board(self):
        self.welcome_frame.grid_forget()

        self.board_frame = Frame(self)
        self.board_frame.grid(row = 0)

        self.num_players = int(self.num_players_spinbox.get())
        self.starting_num_of_cards = int(self.num_cards_spinbox.get())

        self.table = Table(NUMBER_OF_STRIKES)
        for num in range(self.num_players):
            self.table.add_player(Player(NUMBER_OF_STRIKES))
        self.players = self.table.get_players()
        self.current_player = 0
        self.claim_cutoff = 0
        self.rank_cutoff = 0
        self.table.distribute_cards()
        self.player_frames = []

        # Show facing down cards of players
        for i in range(self.num_players):
            current_label = Label(self.board_frame,
                                  text = "Player " + str(i+1),
                                  padx = 20,
                                  pady = 20)
            card_frame = Frame(self.board_frame, width=200, height=self.back_card_photo.height()+15, padx=20)
            if i <= 3:
                current_label.grid(row = i, column = 0)
                card_frame.grid(row = i, column = 1)
            else:
                current_label.grid(row=i-4, column=2)
                card_frame.grid(row=i-4, column=3)
            self.player_frames.append(card_frame)
            self.display_back_cards(card_frame, self.starting_num_of_cards)

        self.options_frame = Frame(self)
        self.options_frame.grid(row=1)
        # self.get_player_turn()

    def display_back_cards(self, parent_frame, num_of_cards):
        interval = (parent_frame.winfo_reqwidth() - self.back_card_photo.width())/(parent_frame.winfo_reqwidth() * (MAXIMUM_STARTING_CARDS - 1))
        for i in range(num_of_cards):
            Label(parent_frame, image=self.back_card_photo).place(relx=i*interval)

    def get_player_turn(self):
        self.current_player_label = Label(self.options_frame,
                                          text = "Current turn: Player "+str(self.current_player))
        self.current_player_label.grid(row = 0)

        self.hand_label = Label(self.options_frame,
                                text = "Claim hand:")
        self.hand_label.grid(row = 1, column = 0)
        self.hand_menu_str = StringVar()
        self.hand_menu_str.set(self.claim_options[0])
        self.hand_menu = OptionMenu(self.options_frame, self.hand_menu_str, *self.claim_options)
        self.hand_menu.grid(row = 1, column = 1)
        self.options_choice_frame = Frame(self.options_frame)
        self.options_choice_frame.grid(row = 1, column = 2)
        # self.hand_menu_str.trace("w", self.handle_choice)

    # def handle_choice(self):
    #     choice = self.hand_menu_str.get()
    #     if choice in ["High card","Pair","Three of a kind","Four of a kind","Five of a kind","Six of a kind","Seven of a kind","Eight of a kind"]:
    #         question_label = Label(self.options_choice_frame,
    #                                text = "Specify the rank of the card:")
    #         question_label.grid(row = 0, column = 0)
    #         rank_menu = OptionMenu(self)
    #     elif choice == "Straight":


def main():
    root = Tk()
    root.title("BS Poker")
    # root.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT))
    app = Application(root).pack(fill = BOTH, expand=True)
    root.mainloop()

main()