import token_handling

class ClientSession:
    def __init__(self):
        self.user = None

    def start_app(self):
        user_answer = 0
        while user_answer != 1 and user_answer != 2:
            user_answer = input("Enter 1 to log in or 2 to create an account: ")
        
        if user_answer == 1:
            self.log_in()
        else:
            self.create_account()

    def log_in(self):
        user = False
        user_answer = ""
        username = ""
        password = ""

        while user == False:
            user_answer = ""
            while user_answer == "":
                user_answer = input("Please enter your username: ")
            username = user_answer
            user_answer = ""
            while user_answer == "":
                user_answer = input("Please enter your password: ")
            password = user_answer

            user = token_handling.login(username, password)
            if user == False:
                print("Invalid username and password")
        
        self.user = user

        self.homepage()

    def create_account(self):
        username_chosen = False
        password_chosen = False
        username = ""
        password = ""
        user_answer = ""

        while username_chosen == False:
            user_answer = ""
            while user_answer == "":
                user_answer = input("Please enter your username: ")
            username = user_answer

            username_chosen = token_handling.check_username_available(username)
            if username_chosen == False:
                print("Username not available")

        while password_chosen = False:

            user_answer = ""
            while user_answer == "":
                user_answer = input("Please enter a password")

            password = user_answer

            user_answer = input("Please confirm your password")

            if password == user_answer:
                password_chosen = True

        user = token_handling.create_account(username, password)

        self.user = user

        self.homepage()

    def homepage(self):
        print(f"Hi, {self.user.username}")
        print(f"Your five most recently watched films are:")
        recently_watched = user.get_recently_watched_films()
        for film in recently_watched:
            print(film.title)


        user_answer = input("""What would you like to do? \n 
        Enter 1 to go to the watchlists home screen \n
        2 to see your films \n
        3 to add a friend \n
        4 to see your notifications \n
        5 to log a film""")
        options = ["1", "2", "3", "4", "5"]
        while user_answer not in options:
            user_answer = input("Please enter one of the options: ")
        
        if user_answer == "1":
            self.watchlist_home()
        if user_answer == "2":
            self.films_seen()
        if user_answer == "3":
            self.find_friend()
        if user_answer == "4":
            self.notifications()
        if user_answer == "5":
            self.log_film()


    def watchlist_home(self):
        pass

    def view_watchlist(self, watchlist):
        pass

    def add_watchlist_film(self, watchlist):
        pass

    def log_film(self):
        pass

    def films_seen(self):
        pass

    def find_friend(self):
        pass

    def notifications(self):
        pass

    def watchlist_invite(self, watchlist):
        user_chosen = False
        user_chosen = False
        while user_chosen == False:
            user_to_invite = input("Who would you like to invite? ")
            username_available = token_handling.check_username_available(user_to_invite)
            if username_available == False:
                user_chosen = True
            else:
                print("That user does not exist")
            
        result = self.user.invite_user_to_watchlist(user_to_invite, watchlist)
        if result == "user already invited/in watchlist":
            print("User already invited/in watchlist")
        else:
            print("User succesfully invited")

        self.view_watchlist(watchlist)

    def create_watchlist(self):
        user_answer = ""
        while user_answer == "" or len(user_answer) > 254:
            if len(user_answer) > 254:
                print("Name is too long")
            user_answer = input("What would you like to name your watchlist? ")
        
        new_watchlist = self.user.create_watchlist()
        
        user_answer = ""
        options = ["1", "2", "3"]
        while user_answer not in options:
            input("Enter 1 to return to the main homepage, 2 to return to the watchlist homepage, or 3 to view the new watchlist")

        if user_answer == "1":
            self.homepage()
        if user_answer == "2":
            self.watchlist_home()
        if user_answer == "3":
            self.view_watchlist(new_watchlist)