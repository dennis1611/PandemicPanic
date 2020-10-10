def choose_mode():
    """"Returns a boolean whether the user wants to play in visual mode (True) or terminal mode (False)"""
    print('Do you want to play in terminal mode ("t") or in visual mode ("v")?')
    while True:
        user_input = input()
        if user_input.lower()[0] == "t":
            print('You chose for terminal mode, the game will start now')
            return False
        elif user_input.lower()[0] == "v":
            print('You chose for visual mode, the game will start in a new window')
            return True
        else:
            print(f'Your input: {user_input}, is not recognised, please try')
