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
        pass

    def homepage(self):
        pass

    def view_watchlist(self):
        pass

    def log_film(self):
        pass

    def films_seen(self):
        pass

    def find_friend(self):
        pass

    def notifications(self):
        pass

    def watchlist_invite(self):
        pass

    def create_watchlist(self):
        pass