import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from TinderUser import TinderUser
from TinderRequest import TinderRequest
from UserSpecs import UserSpecs


class TinderGUI:
    def __init__(self):
        self._userSpecs = UserSpecs()
        self.win = tk.Tk()
        self.win.resizable(True, True)
        self.win.title("WING'S TINDER GUI")
        self.create_widgets()
        self.win.mainloop()

    def create_widgets(self):
        self.packDisclaimer()
        self.packTokenKey()
        self.packLoopsField()
        self.packKeywordField()
        self.packSwipePopularUser()
        self.swipeUserWhoLikeYou()
        self.packRunButton()
        self.packScrollTextDisplay()

    def packDisclaimer(self):
        disclaimerText = "Don't leave the keywords empty. If tinder detects you are running bots, you might get banned.\nSimilarly, don't run the loop for too many times."
        disclaimerFrame = ttk.Frame(self.win)
        disclaimer_lbl = ttk.Label(disclaimerFrame, text=disclaimerText)
        disclaimer_lbl.pack(side=tk.LEFT)
        disclaimerFrame.grid(column=0, row=0, columnspan=2,
                             sticky='WE', padx=5, pady=5)

    def packTokenKey(self):
        inputDataFrame = ttk.Frame(self.win)
        p1_lbl = ttk.Label(
            inputDataFrame, text="Token key that will identify yourself (copy x-auth-token):")
        p1_lbl.pack(side=tk.LEFT)
        self.tokenValue = tk.StringVar(value=self._userSpecs.user_token_key)
        self.tokenEntry = ttk.Entry(
            inputDataFrame, width=40, textvariable=self.tokenValue)
        self.tokenEntry.pack(side=tk.LEFT)
        inputDataFrame.grid(column=0, row=1, columnspan=2,
                            sticky='WE', padx=5, pady=5)

    def packLoopsField(self):
        inputDataFrame = ttk.Frame(self.win)
        p1_lbl = ttk.Label(
            inputDataFrame, text="No. of times to run (each run is 34 users):")
        p1_lbl.pack(side=tk.LEFT)
        self.runValues = tk.IntVar(value=self._userSpecs.time_to_run)
        self.runEntry = ttk.Entry(
            inputDataFrame, width=10, textvariable=self.runValues)
        self.runEntry.pack(side=tk.LEFT)
        inputDataFrame.grid(column=0, row=2, columnspan=2,
                            sticky='WE', padx=5, pady=5)

    def packKeywordField(self):
        inputDataFrame = ttk.Frame(self.win)
        p1_lbl = ttk.Label(
            inputDataFrame, text="Keywords (put in | separated: e.g. finance|invest|money):")
        p1_lbl.pack(side=tk.LEFT)
        self.keywordValue = tk.StringVar(value=self._userSpecs.keyword)
        self.keywordEntry = ttk.Entry(
            inputDataFrame, width=80, textvariable=self.keywordValue)
        self.keywordEntry.pack(side=tk.LEFT)
        inputDataFrame.grid(column=0, row=3, columnspan=2,
                            sticky='WE', padx=5, pady=5)

    def packSwipePopularUser(self):
        self.popUserState = tk.BooleanVar()
        self.popUserState.set(self._userSpecs.swipe_popular_user)
        chk = ttk.Checkbutton(
            self.win, text="Swipe on popular user", var=self.popUserState)
        chk.grid(column=0, row=4, columnspan=2, sticky="W", padx=5, pady=5)

    def swipeUserWhoLikeYou(self):
        self.likeUserState = tk.BooleanVar()
        self.likeUserState.set(self._userSpecs.swipe_liked_user)
        chk = ttk.Checkbutton(
            self.win, text="Swipe on users who like you", var=self.likeUserState)
        chk.grid(column=1, row=4, columnspan=1, sticky="W", padx=5, pady=5)

    def packRunButton(self):
        actionFrame = ttk.Frame(self.win)
        actionFrame.grid(column=0, row=5, columnspan=1,
                         sticky="W", padx=5, pady=5)
        self.run_btn = ttk.Button(
            actionFrame, text="Run Tinder Automate", command=self.run_tinder_automate)
        self.run_btn.config()
        self.run_btn.pack()

    def packScrollTextDisplay(self):
        outputFrame = ttk.Frame(self.win)
        outputFrame.grid(column=0, row=6, columnspan=2)
        self.output = ScrolledText(
            outputFrame, width=100, height=20, wrap=tk.WORD)
        self.output.config(state=tk.DISABLED)
        self.output.grid(column=0, row=0, sticky='WE')

    def handleSingleUser(self, potential, keyword, req):
        user = TinderUser(potential)
        if(self.likeUserState.get() and user.did_user_like_you()):
            log = req.send_and_log_user_like(
                user, user.user_who_like_you_log())
            return log

        elif(self.popUserState.get() and user.is_popular_user()):
            log = req.send_and_log_user_like(
                user, user.popular_user_log())
            return log

        elif(user.user_has_keywords(keyword)):
            log = req.send_and_log_user_like(
                user, user.like_user_with_keyword_log())
            return log

        else:
            return 'nah, just swiping left'

    def run_tinder_automate(self):
        self.log_user_input()
        self.display('Starting tinder automation ...')
        req = TinderRequest(self.tokenValue.get())
        keyword = self.keywordValue.get()

        try:
            runs = self.runValues.get() or 0
            no_of_profile = 0
            user_log = ''

            for i in range(int(runs)):
                self.display(f'Running {i+1} time(s)')
                response = req.get_user_list()
                print(response)
                human = response.json()['data']['results']

                for potential in human:
                    no_of_profile += 1
                    user_log += f'{self.handleSingleUser(potential, keyword, req)}\n'

                self.display(user_log)
                self.display(f'finish checking {no_of_profile}')

        except Exception as e:
            self.display(f'Error encounter:  {e}')

    def log_user_input(self):
        tokenValue = self.tokenValue.get()
        keyword = self.keywordValue.get()
        timeToRun = self.runValues.get()
        isUserLikeValue = self.likeUserState.get()
        isSwipePopUser = self.popUserState.get()
        f = open("userspecs.txt", "w")

        f.write(
            f"""token: {tokenValue}\nkeyword: {keyword}\ntime: {timeToRun}\nswipeUserLike: {isUserLikeValue}\nswipePopUser:{isSwipePopUser}""")
        f.close()

    def display(self, msg=''):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, msg + '\n')
        self.output.config(state=tk.DISABLED)
