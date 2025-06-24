import random
import tkinter as tk
from tkinter import messagebox, ttk
import pygame
import threading
import os

# Sound file names
SOUND_WIN = "win.mp3"
SOUND_LOSE = "lose.mp3"
SOUND_TIE = "tie.mp3"
SCORE_FILE = "scores.txt"

class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock-Paper-Scissors Deluxe")
        self.root.geometry("500x500")
        self.root.resizable(False, False)
        self.is_dark = False

        # Initialize sound engine
        pygame.mixer.init()

        self.setup_start_screen()

    def setup_start_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Enter Your Name:", font=("Arial", 14)).pack(pady=10)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.name_entry.pack()

        tk.Label(self.root, text="Choose Match Type (Best of):", font=("Arial", 14)).pack(pady=10)
        self.round_var = tk.StringVar(value="5")
        ttk.Combobox(self.root, textvariable=self.round_var, values=["3", "5", "7"], state="readonly").pack()

        self.dark_mode_var = tk.BooleanVar()
        tk.Checkbutton(self.root, text="Enable Dark Mode", variable=self.dark_mode_var, font=("Arial", 12)).pack(pady=5)

        tk.Button(self.root, text="Start Game", command=self.start_game, font=("Arial", 13), bg="green", fg="white").pack(pady=20)

    def start_game(self):
        self.name = self.name_entry.get().strip() or "Player"
        self.total_rounds = int(self.round_var.get())
        self.enable_dark_mode(self.dark_mode_var.get())

        self.current_round = 1
        self.player_score = 0
        self.computer_score = 0
        self.history = []

        self.choices = ["rock", "paper", "scissor"]

        self.clear_window()
        self.create_game_screen()

    def create_game_screen(self):
        self.header = tk.Label(self.root, text=f"Round {self.current_round} of {self.total_rounds}", font=("Arial", 14))
        self.header.pack(pady=10)

        self.result_label = tk.Label(self.root, text="Make your choice:", font=("Arial", 12))
        self.result_label.pack()

        self.score_label = tk.Label(self.root, text=f"{self.name}: 0 | Computer: 0", font=("Arial", 12))
        self.score_label.pack(pady=5)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        for choice in self.choices:
            tk.Button(self.button_frame, text=choice.capitalize(), width=10, font=("Arial", 11),
                      command=lambda c=choice: self.play_round(c)).pack(side=tk.LEFT, padx=8)

        self.history_label = tk.Label(self.root, text="History", font=("Arial", 12, "underline"))
        self.history_label.pack(pady=5)
        self.history_box = tk.Text(self.root, height=8, width=50, font=("Arial", 10))
        self.history_box.pack()

        tk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_dark_mode, font=("Arial", 10)).pack(pady=5)

    def play_round(self, player_choice):
        computer_choice = random.choice(self.choices)

        if player_choice == computer_choice:
            result = "Tie"
            self.play_sound(SOUND_TIE)
        elif (player_choice == "rock" and computer_choice == "scissor") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissor" and computer_choice == "paper"):
            result = "Win"
            self.player_score += 1
            self.play_sound(SOUND_WIN)
        else:
            result = "Lose"
            self.computer_score += 1
            self.play_sound(SOUND_LOSE)

        round_result = f"Round {self.current_round}: {self.name} chose {player_choice}, Computer chose {computer_choice} ➤ {result}"
        self.history.append(round_result)
        self.history_box.insert(tk.END, round_result + "\n")
        self.result_label.config(text=round_result)
        self.score_label.config(text=f"{self.name}: {self.player_score} | Computer: {self.computer_score}")
        self.current_round += 1

        if self.current_round > self.total_rounds:
            self.end_game()
        else:
            self.header.config(text=f"Round {self.current_round} of {self.total_rounds}")

    def end_game(self):
        if self.player_score > self.computer_score:
            final_msg = f"🎉 {self.name}, you won the game!"
        elif self.computer_score > self.player_score:
            final_msg = f"😞 {self.name}, you lost the game."
        else:
            final_msg = f"🤝 It's a draw, {self.name}!"

        self.save_score()
        messagebox.showinfo("Game Over", f"{final_msg}\n\nFinal Score:\n{self.name}: {self.player_score}\nComputer: {self.computer_score}")

        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            self.setup_start_screen()
        else:
            self.root.quit()

    def toggle_dark_mode(self):
        self.is_dark = not self.is_dark
        self.enable_dark_mode(self.is_dark)

    def enable_dark_mode(self, enable):
        bg = "#1e1e1e" if enable else "white"
        fg = "white" if enable else "black"
        self.root.configure(bg=bg)

        for widget in self.root.winfo_children():
            try:
                widget.configure(bg=bg, fg=fg, insertbackground=fg)
            except:
                pass

    def play_sound(self, sound_file):
        if os.path.exists(sound_file):
            def _play():
                try:
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play()
                except Exception as e:
                    print("Sound error:", e)
            threading.Thread(target=_play, daemon=True).start()

    def save_score(self):
        try:
            with open(SCORE_FILE, "a") as file:
                file.write(f"{self.name} | {self.player_score}-{self.computer_score}\n")
        except:
            pass

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsApp(root)
    root.mainloop()
