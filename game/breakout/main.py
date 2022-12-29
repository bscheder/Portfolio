from classes.screen import Screen

Screen_ = Screen()

if __name__ == '__main__':
    Screen_.init_screen()

    while Screen_.game.is_running:
        Screen_.update_screen()
