import token_handling
import recommendation
import users_class


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

        while password_chosen == False:

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

        user_answer = input(
            """What would you like to do? \n 
        Enter 1 to go to the watchlists home screen \n
        2 to see your films \n
        3 to add a friend \n
        4 to see your notifications \n
        5 to log a film \n
        6 to see your 5 most recently watched films"""
        )
        options = ["1", "2", "3", "4", "5", "6"]
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
        if user_answer == "6":
            print(f"Your five most recently watched films are:")
            recently_watched = self.user.get_recently_watched_films()
            for film in recently_watched:
                print(film.title)

            self.homepage()

    def watchlist_home(self):
        print("Your available watchlists:")
        watchlist_options = []
        indexes = []
        options = []
        j = 1
        for i in range(len(self.user.watchlists)):
            if self.user.watchlist_invites[i] == False:
                print(f"{str(j)}. {self.user.watchlists[i].name}")
                watchlist_options.append(self.user.watchlists[i])
                indexes.append(i)
                j += 1

        if j == 1:
            "You are not in any watchlists"

        user_answer = input(
            """What would you like to do? \n
        Enter 1 to choose a watchlist to view or edit \n
        Enter 2 to create a watchlist \n
        Enter 3 to return home \n"""
        )
        while user_answer not in ["1", "2", "3"] or (user_answer == "1" and j == 1):
            if user_answer == "1" and j == 1:
                user_answer = input(
                    "You are not in any watchlists, please choose another option: "
                )
            else:
                user_answer = input("Please enter one of the options")

        if user_answer == "1":
            user_answer = input(
                "Which watchlist would you like to view or edit? Enter the number that it was displayed with: "
            )
            options = range(1, j)
            for i in range(len(options)):
                options[i] = str(options[i])
            while user_answer not in options:
                user_answer = input("Please enter one of the options")

            user_choice = watchlist_options[indexes[int(user_answer) - 1]]
            self.view_watchlist(user_choice)
        if user_answer == "2":
            self.create_watchlist()
        if user_answer == "3":
            self.homepage()

    def view_watchlist(self, watchlist):
        print("The films in your watchlist are:")
        for film in watchlist.films:
            print(film.title)

        user_answer = input(
            """What would you like to do? \n
        Enter 1 to add a film to the watchlist \n
        Enter 2 to invite a user to the watchlist \n
        Enter 3 to get a recommendation for a film from the watchlist \n
        Enter 4 to get a random film from the watchlist \n
        Enter 5 to choose a different watchlist \n
        Enter 6 to go back to homepage"""
        )

        options = ["1", "2", "3", "4", "5", "6"]
        while user_answer not in options:
            user_answer = input("Please enter one of the options: ")

        if user_answer == "1":
            self.add_watchlist_film(watchlist)
        if user_answer == "2":
            self.watchlist_invite(watchlist)
        if user_answer == "3":
            print(f"Try {recommendation.recommend_film(self.user, watchlist).title}")
            self.view_watchlist(watchlist)
        if user_answer == "4":
            print(f"Try {watchlist.get_random_film().title}")
        if user_answer == "5":
            self.watchlist_home()
        if user_answer == "6":
            self.homepage()

    def add_watchlist_film(self, watchlist):
        pass

    def log_film(self):
        pass

    def films_seen(self):
        pass

    def find_friend(self):
        friend_chosen = False
        friend_username = ""
        while friend_chosen == False:
            friend_username = input(
                "What is the username of the person you would like to add? "
            )
            if token_handling.check_username_available(friend_username):
                "user does not exist"
            else:
                friend_chosen = True

        friend = users_class.User(friend_username, self.user.token)

        result = self.user.add_friend(friend)

        if result == "friend added":
            print("friend request sent")
        else:
            print("You have already requested to be or are friends with this user")

        user_answer = input(
            "Enter 1 to return to your homepage or 2 to add a friend again"
        )

        while user_answer not in ["1", "2"]:
            user_answer = input("Please enter one of the options: ")

        if user_answer == "1":
            self.homepage()
        if user_answer == "2":
            self.find_friend()

    def notifications(self):
        user_answer = input(
            "Enter 1 to see your watchlist notifications and 2 to see your friendship notifications: "
        )
        while user_answer not in ["1", "2"]:
            user_answer = input("Please enter one of the options: ")

        if user_answer == "1":
            self.watchlist_notifications()
        if user_answer == "2":
            self.friendship_notifications()

    def watchlist_notifications(self):
        print("Your watchlist invites:")
        watchlist_options = []
        indexes = []
        options = []
        j = 1
        for i in range(len(self.user.watchlists)):
            if self.user.watchlist_invites[i]:
                print(f"{str(j)}. {self.user.watchlists[i].name}")
                watchlist_options.append(self.user.watchlists[i])
                indexes.append(i)
                j += 1

        if j == 1:
            "You have no invites"
            self.homepage()

        user_answer = input(
            "Which watchlist would you like to join? Enter the number that it was displayed with or enter nothing to return to the homepage: "
        )
        options = range(1, j)
        for i in range(len(options)):
            options[i] = str(options[i])
        while user_answer not in options:
            if user_answer == "":
                self.homepage()
            user_answer = input("Please enter one of the options")

        user_choice = watchlist_options[indexes[int(user_answer) - 1]]
        self.user.join_watchlist(user_choice)
        print("Watchlist joined")
        self.homepage()

    def friendship_notifications(self):
        print("You have friend requests from:")
        friend_options = []

        for i in range(len(self.user.friends)):
            if self.user.friend_statuses[i][0] == "Request":
                print(self.user.friends[i].username)
                friend_options.append(self.user.friends[i].username)

        user_answer = input(
            "Which request would you like to accept? Enter their username or enter nothing to return to the homepage"
        )
        while user_answer not in friend_options:
            if user_answer == "":
                self.homepage()
            user_answer = input("You do not have a friend request from that user")

        self.user.accept_friend(users_class.User(user_answer, self.user.token))
        print("Friend added")
        self.homepage()

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
            input(
                "Enter 1 to return to the main homepage, 2 to return to the watchlist homepage, or 3 to view the new watchlist"
            )

        if user_answer == "1":
            self.homepage()
        if user_answer == "2":
            self.watchlist_home()
        if user_answer == "3":
            self.view_watchlist(new_watchlist)
