from .game import Game
import time
class Play(Game):
    baseTime = 0.1
    scoreCheckpoint = 200
    def __init__(self, stdscr, game_width, dino):
        super().__init__(stdscr, game_width, dino)
        self.y_pos = 0
        self.x_pos = 0
        self.jumping = False
        self.down = False
        self.collision = False
    
    def jump(self,key):
        if key == 32:
            if not self.jumping or self.down:
                self.jumping = True

        if self.jumping:
            self.y_pos += 1

            if self.y_pos == 7:
                self.down = True
                self.jumping = False
        if self.down:
            self.y_pos -= 1
            if self.y_pos <= 0:
                self.down = False

    def check_collision(self):
        dino_bottom_row = self.dino[-1]
        for i in range(min(self.game_width, len(dino_bottom_row))):
            if (dino_bottom_row[i] == '*' and i + self.x_pos < self.game_width and self.LineBuffer[i + self.x_pos] == '-' and self.y_pos < 1):
                self.collision = True
                

    def play(self):
        self.first_line(self.game_width)
        while not self.collision:
            start_time = time.time()

            self.stdscr.clear()

            self.draw_dino(self.y_pos, self.x_pos)
            self.draw_line_buffer()
            self.move_line_buffer()
            self.draw_obstacle()
            self.increment_score()
            self.display_score() 
            self.linBr += 1
            if self.score > Play.scoreCheckpoint:
                n = self.score // Play.scoreCheckpoint
                self.frame_time = Play.baseTime / n
            self.stdscr.refresh()
            if not self.down:
                key = self.stdscr.getch()
            self.jump(key)

            self.check_collision()

            elapsed_time = time.time() - start_time
            sleep_time = max(0, self.frame_time - elapsed_time)
            time.sleep(sleep_time)

        # Display game over message
        self.stdscr.addstr(self.height // 2, self.width // 2 - 5, "Game Over!")
        self.stdscr.addstr(self.height // 2+1, self.width // 2 - 5, f"Score: {self.score}")  
        self.stdscr.refresh()
        time.sleep(2)
        self.stdscr.getch()