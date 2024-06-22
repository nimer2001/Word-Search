import tkinter as tk
from boggle_board_randomizer import*
from ex12_utils import*
import tkinter.messagebox

REMAINING = 10  # Last 10 seconds


class GUI:

    """ This class will execute boggle game """

    def __init__(self):
        self.root = tk.Tk()
        self.time_after = 0
        self.first_page()
        self.lst_of_words = []
        self.lst_of_index = []
        self.submit_flag = False
        self.delete_flag = False
        self.my_board = randomize_board()

    def first_page(self):

        """ This function will create the first page """

        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack()
        self.photo = tk.PhotoImage(file="photoforboggle.png")
        self.image = tk.Label(self.canvas, image=self.photo)
        self.image.pack()
        self.button = tk.Button(self.canvas, text="Start Game", width=10, height=2, command=self.second_page)
        self.button.place(x=460, y=370)

    def second_page(self):

        """This function will call to other helper functions that will create the game"""

        self.flag = False
        self.is_the_word_correct = False
        self.min = 3
        self.seconds = 0
        self.word = ""
        self.counter = 0
        self.finle_score = 0
        self.score= 0
        self.canvas.destroy()
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.photo = tk.PhotoImage(file="background.png")
        self.image = tk.Label(self.canvas, image=self.photo)
        self.image.pack()
        self.canvas.pack()
        self.build_text_box()
        self.build_board_words()
        self.cor_word_window()
        self.timer_box()
        self.score_box()
        self.submit_box()
        self.delete_word()
        self.exit_game()

    def build_text_box(self):

        """This function will create the box that save the words"""

        self.window = tk.Label(self.canvas, text="Words:", width=10, height=2, fg="black", bg="light yellow",
                               font=("Courier", 15))
        self.window.place(x=345, y=30)
        self.words_window = tk.Label(self.canvas, text="", width=20, height=2, font=("Courier", 15))
        self.words_window.place(x= 290, y= 80)

    def build_board_words(self):

        """This function will create the board"""

        self.board = tk.Frame(self.canvas, width=365, height=281, bg="sky blue")
        self.board.place(x=215, y=140)
        x = 1
        y = 1
        lst_ij = [None, None]
        for i in range(len(self.my_board)):
            for j in range(len(self.my_board[0])):
                lst_neighbors = find_neighbors(self.my_board, i, j)
                self.board_word = tk.Button(self.board, width=12, height=4, text=str(self.my_board[i][j])
                                       , command=self.add_words(i, j, lst_ij, lst_neighbors))
                self.board_word.place(x=x, y=y)
                x += 90
            y += 70
            x = 1

    def add_words(self, i, j, lst_ij, lst_neighbors):

        """This function will add the words to the window that build_text_box function create """

        def add_words_to_text():
            self.flag = True
            if self.submit_flag or (self.delete_flag and len(self.word) == 0):
                lst_ij[0], lst_ij[1] = None, None
            if (lst_ij[0] is None and lst_ij[1] is None) or (lst_ij[0], lst_ij[1]) in lst_neighbors and\
                    ((i, j) not in self.lst_of_index):
                self.lst_of_index.append((i, j))
                self.word += str(self.my_board[i][j])
                self.counter += 1
                self.words_window.configure(text=self.word)
                lst_ij[0] = i
                lst_ij[1] = j
                self.submit_flag, self.delete_flag = False, False
            else:
                self.error_massage()
        return add_words_to_text

    def cor_word_window(self):

        """This function will create the window that the correct words will appear in it"""

        self.window = tk.Label(self.canvas, text="Correct Words:", width=15, height=2, font=("Courier", 15))
        self.window.place(x=600, y=300)
        self.cor_window = tk.Label(self.canvas, text="",  font=("Courier", 15))
        self.cor_window.place(x=600, y=350)

    def submit_box(self):

        """This function create a button called submit, when the player press
         the button, the function will call correct_word_box func"""

        self.submit = tk.Button(self.canvas, text="Submit", width=10, height=2, bg="green", font=("Courier", 15),
                                command=self.correct_words_box)
        self.submit.place(x=215, y=420)

    def correct_words_box(self):

        """This function check if the word in the list of words, and updating the correct window """
        self.submit_flag = True

        self.lst_of_index = []
        with open("boggle_dict.txt", 'r') as f:
            flag = False
            for word in f:
                if self.word not in self.lst_of_words and self.word == word.strip():
                    self.is_the_word_correct = True
                    self.lst_of_words.append(self.word)
                    self.configure_words(self.lst_of_words)
                    self.add_to_score()
                    self.counter = 0
                    self.word = ""
                    self.words_window.configure(text="")
                    flag = True
                    self.error_massage()
                    self.is_the_word_correct = False
            if not flag:
                self.counter = 0
                self.error_massage()
                self.word = ""
                self.words_window.configure(text=self.word)

    def configure_words(self, lst_of_words):

        """This function add the correct word to the cor_window"""
        x = 7
        correct_words = ""
        for i in range(len(lst_of_words)):
            correct_words += (lst_of_words[i]).strip() + " "
            if len(correct_words) > x:
                correct_words += "\n"
                x += 7
        self.cor_window.configure(text=str(correct_words))


    def score_box(self):

        """This function create the score box"""

        self.add_score = tk.Label(self.canvas, text="Score:0 ", width=10, height=2,  font=("Courier", 15))
        self.add_score.place(x=30, y=150)

    def add_to_score(self):

        """This function will update the score """

        self.finle_score += self.counter**2
        self.add_score.configure(text="Score" + ":" + str(self.finle_score))

    def timer_box(self):

        """This function create the timer"""

        self.time = tk.Label(self.canvas, width=10, height=2, font=("Courier", 15))
        self.time.place(x=650, y=150)
        self.build_timer()

    def build_timer(self):

        """This function will let the timer work"""

        self.time.configure(text="Time" + ":" + "" + str(self.min) + ":" + str(self.seconds))
        if self.flag:
            if self.min == 0 and self.seconds == REMAINING:
                self.time.configure(text="Time" + ":" + "" + str(self.min) + ":" + str(self.seconds), fg="red")
            if self.seconds == 0 and self.min == 0:
                self.root.after_cancel(self.time_after)
                self.end_game()
                return
            if self.seconds == 0:
                self.min -= 1
                self.seconds = 59
            else:
                self.seconds -= 1
        self.time_after = self.root.after(1000, self.build_timer)

    def delete_word(self):

        """This function create delete button"""

        self.delete = tk.Button(self.canvas, text="Delete", width=8, height=2, font=("Courier", 15),
                                command=self.is_delete)
        self.delete.place(x=344, y=420)

    def is_delete(self):

        """This function delete the word if the user press the delete button """

        self.delete_flag = True
        self.word = self.word[0:-1]
        self.counter -= 1
        self.words_window.configure(text=self.word)

    def error_massage(self):

        """This function create the massage box and the error massage if their is something wrong"""

        self.massage = tk.Label(self.canvas, text="Massage:", width=10, height=2, font=("Courier", 15))
        self.massage.place(x=30, y=350)
        if self.is_the_word_correct:
            self.error = tk.Label(self.canvas, text="GOOD GOB!!",  width=14, height=2, bg="dark green", font=("Courier", 15))
            self.error.place(x=10, y=400)
            self.error.after(1000, lambda: self.error.config(text=""))
        else:
            self.error = tk.Label(self.canvas, text="ILLEGAL WORD!!",  width=14, height=2, bg="RED", font=("Courier", 15))
            self.error.place(x=10, y=400)
            self.error.after(1000, lambda: self.error.config(text=""))

    def exit_game(self):

        """This function create the exit button"""

        self.exit = tk.Button(self.canvas, text="Exit", width=10, height=2, bg="red", font=("Courier", 15), command=self.exit_helper)
        self.exit.place(x=450, y=420)

    def exit_helper(self):

        """This function asks the user if he want to exit the game"""

        yes_no_answer = tk.messagebox.askquestion("Game Over", "Do You Want To Exit?")
        if yes_no_answer == "yes":
            self.root.destroy()

    def end_game(self):

        """This function called when the timer is 0:0 and ask the user if he want to play again"""

        yes_no_answer = tk.messagebox.askquestion("Game Over", "The time end.Do you want to play again?")
        if yes_no_answer == "yes":
            self.second_page()
        else:
            self.root.destroy()

    def main_loop(self):

        """The main loop func"""

        self.root.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.main_loop()


