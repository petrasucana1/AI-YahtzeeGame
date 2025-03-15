from games_check import *
from training_alg import *
from chat import *
import pygame
import tkinter as tk
import random
import time
import json
import os



def InitialState():
    """Initializeaza starea initiala a jocului."""
    return (0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)


bonus_score_p0 = 0
bonus_score_p1 = 0
ok_p0 = 0
ok_p1 = 0
yahtzee_trainer = YahtzeeTraining()
Q_table = yahtzee_trainer.q_table
state = InitialState()

root = tk.Tk()
root.title("YAHTZEE")
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 650
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="green")

table_frame = tk.Frame(root, bg="black")
table_frame.pack(side=tk.RIGHT, padx=20, pady=20)

characters_frame = tk.Frame(root, bg="green")
characters_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

player2_frame = tk.Frame(characters_frame, bg="green")
player2_frame.pack(side=tk.TOP, pady=(5, 5), padx=(180, 0))
player2_label = tk.Label(player2_frame, text="😎", bg="green", fg="white", font=("Arial", 45))
player2_label.pack(anchor="center")
player2_text = tk.Label(player2_frame, text="Player 2", bg="green", fg="white", font=("Arial", 14, "bold"))
player2_text.pack(anchor="center")

spacer = tk.Frame(characters_frame, height=100, background="green")
spacer.pack()

player1_frame = tk.Frame(characters_frame, bg="green")
player1_frame.pack(side=tk.BOTTOM, pady=(10, 10), padx=(180, 0))
message_label = tk.Label(player1_frame, text="", bg="green", fg="yellow", font=("Arial", 14, "bold"))
message_label.pack()
player1_label = tk.Label(player1_frame, text="🙂", bg="green", fg="white", font=("Arial", 45))
player1_label.pack(anchor="center")
player1_text = tk.Label(player1_frame, text="Player 1", bg="green", fg="white", font=("Arial", 14, "bold"))
player1_text.pack(anchor="center")

dice_frame = tk.Frame(player1_frame, bg="green", width=300, height=70)
dice_frame.pack(side=tk.TOP, pady=(5, 10))
dice_frame.pack_propagate(False)

dice_frame_p2 = tk.Frame(player2_frame, bg="green", width=300, height=70)
dice_frame_p2.pack(side=tk.BOTTOM, pady=(5, 10))
dice_frame_p2.pack_propagate(False)

def play_sound():
    pygame.mixer.music.load('dice.wav')
    pygame.mixer.music.play()

pygame.init()

def get_recommendation():
    """Afișează o recomandare personalizată."""
    global dices
    custom_message_window = tk.Toplevel(root)
    custom_message_window.title("Custom Message")
    custom_message_window.geometry("400x200")

    games_played = [0 if game[1] == -1 else 1 for game in games_scores[:13]]
    dices_state = yahtzee_trainer.initialize_state(dices[1])
    available_games = [game for game in games_scores[:13] if game[1] == -1]
    if available_games:
        selected_game = yahtzee_trainer.choose_action(dices_state)
        games_not_disponible = []

        while games_played[selected_game] != 0:
            games_not_disponible.append(selected_game)
            selected_game = yahtzee_trainer.choose_next_action(dices_state, games_not_disponible)

        selected_game += 1
        game_name = index_to_game_name[selected_game]

    to_keep_dices = [[0] * 5, dices[1]]

    mess_dices=""
    DetermineHelpfulDicesT(game_name, to_keep_dices)
    for i in range(0,5):
        if to_keep_dices[0][i]==1:
            mess_dices=f"{to_keep_dices[1][i]}, "+mess_dices

    mess_dices = mess_dices.rstrip(", ")
    message = (f"Hint: Ai putea păstra zarurile cu valorile: {mess_dices}")
    if mess_dices=="":
        message = f"{game_name}"
    message_label = tk.Label(custom_message_window, text=message, font=("Arial", 14), padx=20, pady=20)
    message_label.pack(pady=20)

    close_button = tk.Button(custom_message_window, text="Close", font=("Arial", 12),
                             command=custom_message_window.destroy)
    close_button.pack(pady=10)

custom_button = tk.Button(root, text="HINT", bg="white", fg="black", font=("Arial", 14, "bold"), command=get_recommendation)
custom_button.pack(side=tk.TOP, pady=10)

def show_statistics():
    """Afișează statisticile jocurilor."""

    try:
        with open("scores.json", "r") as file:
            scores_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores_data = []

    total_games = len(scores_data)
    avg_p1 = sum(game["player1"] for game in scores_data) / total_games if total_games else 0
    avg_p2 = sum(game["player2"] for game in scores_data) / total_games if total_games else 0

    stats_window = tk.Toplevel(root)
    stats_window.title("User Statistics")
    stats_window.geometry("400x300")

    stats_text = f"Total Games: {total_games}\nAverage Score Player 1: {avg_p1:.2f}\nAverage Score Player 2: {avg_p2:.2f}"
    stats_label = tk.Label(stats_window, text=stats_text, font=("Arial", 14), padx=20, pady=20)
    stats_label.pack(pady=20)

def save_scores(player1_score, player2_score):
    """Salveaza punctajele fiecărui player într-un fișier JSON."""

    scores_data = []
    if os.path.exists("scores.json"):
        try:
            with open("scores.json", "r") as file:
                scores_data = json.load(file)
        except json.JSONDecodeError:
            print("Eroare la citirea fișierului scores.json. Se va crea unul nou.")

    scores_data.append({"player1": player1_score, "player2": player2_score})
    with open("scores.json", "w") as file:
        json.dump(scores_data, file, indent=4)

def show_end_game_popup(player1_score, player2_score, winner):
    """Afișează câștigătorul și generează feedback."""

    save_scores(player1_score, player2_score)
    feedback = "Este primul tău joc, nu există un scor anterior pentru comparație."
    if os.path.exists("scores.json"):
        try:
            with open("scores.json", "r") as file:
                scores_data = json.load(file)
                if len(scores_data) > 1:
                    last_score = scores_data[-2]["player1"]
                    if player1_score > last_score:
                        feedback = f"Ai obținut mai multe puncte decât data trecută! (+{player1_score - last_score})"
                    elif player1_score < last_score:
                        feedback = f"Ai obținut mai puține puncte decât data trecută. (-{last_score - player1_score})"
                    else:
                        feedback = "Ai obținut exact același scor ca data trecută."
        except json.JSONDecodeError:
            feedback = "Nu s-a putut citi istoricul scorurilor pentru comparație."

    end_game_window = tk.Toplevel(root)
    end_game_window.title("Game Over")
    end_game_window.geometry("600x500")

    result_text = (
        f"Game Over!\n\n"
        f"Player 1 Score: {player1_score}\n"
        f"Player 2 Score: {player2_score}\n\n"
        f"Winner: {winner}\n\n"
        f"{feedback}"
    )
    result_label = tk.Label(end_game_window, text=result_text, font=("Arial", 14), padx=20, pady=20)
    result_label.pack(pady=20)

    def exit_game():
        end_game_window.destroy()
        root.destroy()

    new_game_button = tk.Button(end_game_window, text="Exit Game", font=("Arial", 12), command=exit_game)
    new_game_button.pack(pady=20)



stats_button = tk.Button(root, text="Show Statistics", bg="white", fg="black", font=("Arial", 14, "bold"), command=show_statistics)
stats_button.pack(side=tk.TOP, pady=10)

def open_chat_window_box():
    """Creează o fereastră de chat pentru interacțiunea cu chatbot-ul."""

    chat_window = tk.Toplevel(root)
    chat_window.title("Chatbot Yahtzee")
    chat_window.geometry("500x600")

    chat_label = tk.Label(chat_window, text="Chat cu Bot-ul", font=("Arial", 16))
    chat_label.pack(pady=10)

    chat_text = tk.Text(chat_window, height=25, width=60, state=tk.DISABLED)
    chat_text.pack(pady=10)

    chat_entry = tk.Entry(chat_window, font=("Arial", 12))
    chat_entry.pack(pady=10)

    def handle_message():
        user_message = chat_entry.get()
        chat_entry.delete(0, tk.END)
        chat_text.config(state=tk.NORMAL)
        chat_text.insert(tk.END, f"Tu: {user_message}\n")
        response = get_chatbot_response(user_message)
        chat_text.insert(tk.END, f"Bot: {response}\n")
        chat_text.config(state=tk.DISABLED)

    send_button = tk.Button(chat_window, text="Trimite", font=("Arial", 12), command=handle_message)
    send_button.pack(pady=5)

def open_chat_window():
    """Deschide o fereastră nouă pentru reguli."""

    global chat_text
    chat_window = tk.Toplevel(root)
    chat_window.title("Chat")
    chat_window.geometry("500x600")

    chat_label = tk.Label(chat_window, text="Chat", font=("Arial", 16))
    chat_label.pack(pady=10)

    chat_text = tk.Text(chat_window, height=20, width=60, state=tk.DISABLED)
    chat_text.pack(pady=10)

    question_label = tk.Label(chat_window, text="Selectează o întrebare:\n1 - Reguli\n2 - Combinații secțiunea superioară\n3 - Combinații secțiunea inferioară\n4 - Strategii", font=("Arial", 12))
    question_label.pack(pady=10)

    button_frame = tk.Frame(chat_window)
    button_frame.pack()

    def show_response(option):
        """Afișează răspunsul în funcție de opțiunea aleasă."""

        global chat_text
        global dices
        responses = {
            1: (
                "Reguli: Obiectivul jocului YAHTZEE este să obții cât mai multe puncte prin aruncarea a cinci zaruri și realizarea unor combinații specifice de zaruri.\n "
                "Desfășurarea jocului: În fiecare tură, un jucător poate arunca zarurile de până la trei ori. Nu este necesar să arunce toate cele cinci zaruri la a doua și a treia aruncare dintr-o rundă;\n "
                "jucătorul poate pune deoparte câte zaruri dorește și să arunce doar pe cele care nu au numerele pe care încearcă să le obțină.\n "
                "De exemplu, un jucător aruncă zarurile și obține 1, 3, 3, 4, 6. Decide că dorește să încerce să obțină o combinație de „large straight” (1, 2, 3, 4, 5).\n "
                "Așadar, pune deoparte zarurile 1, 3 și 4 și aruncă din nou doar zarurile 3 și 6, sperând să obțină 2 și 5.\n "
                "În acest joc, trebuie să faci clic pe zarurile pe care vrei să le păstrezi. Acestea vor fi mutate în jos și nu vor fi aruncate data viitoare când apeși butonul „Roll Dice”.\n "
                "Dacă decizi, după a doua aruncare dintr-o tură, că nu vrei să păstrezi aceleași zaruri înainte de a treia aruncare, poți face clic din nou pe ele, iar acestea vor fi mutate înapoi pe masă și vor fi aruncate la a treia aruncare."),
            2: ("Combinații secțiunea superioară:\n "
                "- **Ones**: Obține cât mai multe zaruri cu valoarea 1.\n"
                "- **Twos**: Obține cât mai multe zaruri cu valoarea 2.\n"
                "- **Threes**: Obține cât mai multe zaruri cu valoarea 3.\n"
                "- **Fours**: Obține cât mai multe zaruri cu valoarea 4.\n"
                "- **Fives**: Obține cât mai multe zaruri cu valoarea 5.\n"
                "- **Sixes**: Obține cât mai multe zaruri cu valoarea 6."),
            3: ("Combinații secțiunea inferioară:\n "
                "- **Three of a kind**: Obține trei zaruri cu aceeași valoare. Punctele sunt suma tuturor zarurilor (nu doar a celor trei identice).\n"
                "- **Four of a kind**: Obține patru zaruri cu aceeași valoare. Punctele sunt suma tuturor zarurilor (nu doar a celor patru identice).\n"
                "- **Full House**: Obține trei zaruri cu aceeași valoare și o pereche, de exemplu, 1,1,3,3,3 sau 3,3,3,6,6. Valorează 25 de puncte.\n"
                "- **Small Straight**: Obține patru zaruri consecutive, de exemplu, 1,2,3,4 sau 2,3,4,5. Valorează 30 de puncte.\n"
                "- **Large Straight**: Obține cinci zaruri consecutive, de exemplu, 1,2,3,4,5 sau 2,3,4,5,6. Valorează 40 de puncte.\n"
                "- **Chance**: Poți pune orice combinație de zaruri aici. Este practic o soluție de rezervă când nu ai altă opțiune. Scorul este suma zarurilor.\n"
                "- **YAHTZEE**: Obține cinci zaruri identice. Valorează 50 de puncte. Poți obține mai multe Yahtzee-uri, dacă regulile permit."),
            4: ("Strategii: \n"
                "- Încearcă să obții bonusul completând secțiunea superioară.\n "
                "Concentrează-te pe aruncări bune cu cinciuri și șesari, astfel încât să nu conteze dacă ai punctaj zero la 1 sau 2.\n"
                "- Poți pune 0 la o combinație dacă nu o ai, chiar dacă ai o altă combinație. De exemplu, dacă ai 2,3,4,5,6 și singurele opțiuni rămase sunt Ones și Sixes, "
                "ar fi mai bine să pui 0 la Ones decât să pui doar 6 la Sixes.\n"
                "- Folosește „Chance” pentru a salva puncte când ai o aruncare slabă.\n\n"
                "Sper să te bucuri de joc!")
        }

        chat_text.config(state=tk.NORMAL)
        chat_text.delete(1.0, tk.END)

        chat_text.insert(tk.END, f"You selected: {option}\n")
        chat_text.insert(tk.END, f"{responses[option]}\n")
        chat_text.config(state=tk.DISABLED)

    button1 = tk.Button(button_frame, text="1", font=("Arial", 14), command=lambda: show_response(1))
    button1.pack(side=tk.LEFT, padx=5)

    button2 = tk.Button(button_frame, text="2", font=("Arial", 14), command=lambda: show_response(2))
    button2.pack(side=tk.LEFT, padx=5)

    button3 = tk.Button(button_frame, text="3", font=("Arial", 14), command=lambda: show_response(3))
    button3.pack(side=tk.LEFT, padx=5)

    button4 = tk.Button(button_frame, text="4", font=("Arial", 14), command=lambda: show_response(4))
    button4.pack(side=tk.LEFT, padx=5)

chat_button = tk.Button(root, text="Chat", bg="white", fg="black", font=("Arial", 14, "bold"), command=open_chat_window_box)
chat_button.pack(side=tk.TOP, pady=10)

chat_button = tk.Button(root, text="How to play", bg="white", fg="black", font=("Arial", 14, "bold"), command=open_chat_window)
chat_button.pack(side=tk.TOP, pady=10)


def draw_dice(frame, value, is_locked, index):
    """Desenează un zar pe ecran."""

    size = 50
    dot_size = 10
    bg_color = "red" if is_locked else "white"

    canvas = tk.Canvas(frame, width=size, height=size, bg=bg_color, highlightthickness=0)
    canvas.pack(side=tk.LEFT, padx=5)

    positions = {
        1: [(25, 25)],
        2: [(10, 10), (40, 40)],
        3: [(10, 10), (25, 25), (40, 40)],
        4: [(10, 10), (10, 40), (40, 10), (40, 40)],
        5: [(10, 10), (10, 40), (40, 10), (40, 40), (25, 25)],
        6: [(10, 10), (10, 25), (10, 40), (40, 10), (40, 25), (40, 40)],
    }

    for x, y in positions[value]:
        canvas.create_oval(
            x - dot_size // 2,
            y - dot_size // 2,
            x + dot_size // 2,
            y + dot_size // 2,
            fill="black"
        )

    canvas.bind("<Button-1>", lambda event: toggle_dice_by_click(index))

def toggle_dice_by_click(index):
    """Blochează sau deblochează un zar atunci când este apăsat."""

    global dices
    dices[0][index] = 1 - dices[0][index]
    update_dice_display(dices, dice_frame)


def display_characters(frame):
    """Afișează restul elementelor pentru a juca."""

    roll_button = tk.Button(player1_frame, text="Roll Dice", bg="white", fg="black", font=("Arial", 14, "bold"),
                            command=roll_dice_frontend)
    roll_button.pack(side=tk.TOP, pady=(5, 10))


def switch_dice_for_ai():
    """Schimbă zarurile pentru AI."""

    for widget in dice_frame.winfo_children():
        widget.destroy()


def switch_dice_for_human():
    """Schimbă zarurile pentru utilizator."""

    for widget in dice_frame_p2.winfo_children():
        widget.destroy()


def start_ai_turn():
    """Începe tura AI-ului."""

    global dices, game_selected, state
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    switch_dice_for_ai()
    game_selected = True
    game_name, score = ComputerChooseAI(games_scores)
    print(f"AI selected game: {game_name}, Score: {score}")
    display_table(table_frame, games_scores, dices, 0, interactive=False)
    message_label.config(text="Player2 alege jocul {game_name}")
    time.sleep(3)

    game_selected = False
    if not isFinalState(state):
        if Validation(state, state[0], game_numbers[game_name]):
            state = Transition(state, state[0], game_numbers[game_name], score)
    else:
        isFinalState(state)
    message_label.config(text="Este rândul tau. Poti sa dau cu zarurile!")
    start_new_turn()


game_selected = False

def display_table(frame, scores, dices, player, interactive=True):
    """Afișează tabelul de scor."""

    global game_selected

    def on_cell_click(event, game_name, col):
        global game_selected
        global state
        if interactive and not game_selected and scores[game_numbers[game_name] - 1][col] == -1:
            score = game_functions[game_name](dices)
            if score >= 0:
                game_selected = True
                UpdateScore(player, game_name, dices)
                if not isFinalState(state):
                    if Validation(state, state[0], game_numbers[game_name]):
                        state = Transition(state, state[0], game_numbers[game_name], score)
                display_table(frame, scores, dices, player, interactive=False)
                message_label.config(text="Este rândul Player-ului 2. Asteptati...")
                start_ai_turn()

    headers = ["Game", "Player 1", "Player 2"]
    for col, header in enumerate(headers):
        label = tk.Label(frame, text=header, bg="white", fg="black", height=2, borderwidth=1, relief="solid")
        label.grid(row=0, column=col, sticky="nsew")

    frame.grid_columnconfigure(0, weight=1, minsize=120)
    frame.grid_columnconfigure(1, weight=1, minsize=60)
    frame.grid_columnconfigure(2, weight=1, minsize=60)

    for row, game in enumerate(scores, start=1):
        game_name = game[0]
        potential_score = -1

        if game[player + 1] == -1:
            potential_score = game_functions[game_name](dices)

        for col, value in enumerate(game):
            fg_color = "red" if col == player + 1 and potential_score > 0 else "black"
            text = f"{value} (→ {potential_score})" if fg_color == "red" else str(value)
            label = tk.Label(frame, text=text, bg="white", fg=fg_color, height=2, borderwidth=1, relief="solid")
            label.grid(row=row, column=col, sticky="nsew")
            if col == player + 1 and game[col] == -1 and interactive and not game_selected:
                label.bind(
                    "<Button-1>",
                    lambda event, g_name=game_name, g_col=col: on_cell_click(event, g_name, g_col)
                )

reroll_counter = tk.IntVar(value=3)

def roll_dice_frontend():
    """Desenează zarurile."""

    global dices
    if reroll_counter.get() > 0:
        RollDice(dices)
        update_dice_display(dices, dice_frame)
        reroll_counter.set(reroll_counter.get() - 1)
        message_label.config(text=f"Reroll-uri rămase: {reroll_counter.get()}")
        display_table(table_frame, games_scores, dices, 0)
    else:
        message_label.config(text="Nu mai ai reroll-uri disponibile!")


def update_dice_display(dices, frame):
    """Redesenează zarurile."""

    for widget in frame.winfo_children():
        widget.destroy()

    for i, value in enumerate(dices[1]):
        draw_dice(frame, value, dices[0][i] == 1, i)


def toggle_dice(index):
    """Blochează un zar."""

    global dices
    dices[0][index] = keep_dice_vars[index].get()

def start_new_turn():
    """Începe o nouă tura a jucătorului 1."""

    global state
    if isFinalState(state):
        return
    global reroll_counter, dices, game_selected
    reroll_counter.set(2)
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    switch_dice_for_human()
    RollDice(dices)
    update_dice_display(dices, dice_frame)
    display_table(table_frame, games_scores, dices, 0, interactive=True)
    message_label.config(text="Este rândul tău. Alege un joc sau dă cu zarurile!")
    game_selected = False


def InitialGame():
    """Inițializează jocul."""

    yahtzee_trainer.train(episodes=1500000)
    games = [
        "Ones", "Twos", "Threes", "Fours", "Fives",
        "Sixes", "Three of a kind", "Four of a kind", "Full House", "Small Straight",
        "Large Straight", "Chance", "YAHTZEE"
    ]

    games_scores = [[game, -1, -1] for game in games]
    games_scores.append(["Bonus", 0, 0])
    games_scores.append(["Total", 0, 0])

    display_characters(characters_frame)
    display_table(table_frame, games_scores, dices, 0)
    return games_scores


def start_new_game():
    """Începe o nouă tura a jucătorului 1."""

    global state, games_scores, dices, reroll_counter, game_selected
    state = InitialState()
    games_scores = InitialGame()
    reroll_counter.set(3)
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    game_selected = False
    update_dice_display(dices, dice_frame)
    display_table(table_frame, games_scores, dices, 0)
    message_label.config(text="It's your turn. Roll the dice!")


def start_new_game_function():
    """Funcția care va fi apelată pentru a începe un joc nou."""

    global state
    state = InitialState()
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    for widget in dice_frame.winfo_children():
        widget.destroy()
    for widget in dice_frame_p2.winfo_children():
        widget.destroy()
    for widget in table_frame.winfo_children():
        widget.destroy()
    keep_dice_vars = [tk.IntVar(value=0) for _ in range(5)]
    games_scores = InitialGame()
    WelcomeGame(games_scores)

def isFinalState(state):
    """Verifică dacă jocul s-a încheiat și afișează pop-up-ul cu scorul și câștigătorul."""

    if all(s != -1 for s in state[:]):
        total_p0 = total(state, 0)
        total_p1 = total(state, 1)

        if total_p0 > total_p1:
            winner = "Player 1"
        elif total_p1 > total_p0:
            winner = "Player 2"
        else:
            winner = "It's a tie!"

        print("Player 1 score: ", total_p0)
        print("Player 2 score: ", total_p1)
        print(f"Winner: {winner}")

        show_end_game_popup(total_p0, total_p1, winner)
        return True
    return False


def RollDice(dices):
    """Generează random zarurile."""

    play_sound()
    for i in range(len(dices[0])):
        if dices[0][i] == 0:
            dices[1][i] = random.randint(1, 6)


def Transition(state, player, game_number, score):
    """Face tranziția de la o stare la următoarea."""

    state_list = list(state)
    state_list[13 * player + game_number] = score
    state_list[0] = int(not player)
    print(tuple(state_list))
    return tuple(state_list)


def Validation(state, player, game_number):
    """Verifică daca o nouă strae e corectă."""

    if state[13 * player + game_number] != -1:
        return False
    return True


def DiceValitation(dices, dices_to_let):
    """Verifică daca un zar este corect gestionat."""

    for dice in dices_to_let:
        if dices[0][dice] == 0:
            print("Invalid dice")
            return False
    return True


def UpdateScore(player, game_name, dices):
    """Actualizează scorul pentru fiecare joc."""

    global ok_p0
    global bonus_score_p0
    global ok_p1
    global bonus_score_p1
    if player == 0:
        game_index = game_numbers[game_name]
        score = game_functions[game_name](dices)
        games_scores[game_index - 1][1] = score
        if game_index <= 6:
            bonus_score_p0 += score
            if bonus_score_p0 >= 63 and ok_p0 == 0:
                games_scores[13][1] = 35
                games_scores[14][1] += 35
                ok_p0 = 1
        games_scores[14][1] += score
        return score
    else:
        game_index = game_numbers[game_name]
        score = game_functions[game_name](dices)
        games_scores[game_index - 1][2] = score
        if game_index <= 6:
            bonus_score_p1 += score
            if bonus_score_p1 >= 63 and ok_p1 == 0:
                games_scores[13][2] = 35
                games_scores[14][2] += 35
                ok_p1 = 1
        games_scores[14][2] += score
        return score


def state_to_index(state):
    """Convertește starea la index."""

    state_index = int("".join(map(str, state)), 2)
    return state_index


def DetermineHelpfulDices(game_name, dices):
    """Determină zarurile folositoare pentru un anumit joc."""

    dices[0] = [0, 0, 0, 0, 0]

    if game_name == "Ones":
        for i in range(5):
            if dices[1][i] == 1:
                dices[0][i] = 1

    elif game_name == "Twos":
        for i in range(5):
            if dices[1][i] == 2:
                dices[0][i] = 1

    elif game_name == "Threes":
        for i in range(5):
            if dices[1][i] == 3:
                dices[0][i] = 1

    elif game_name == "Fours":
        for i in range(5):
            if dices[1][i] == 4:
                dices[0][i] = 1

    elif game_name == "Fives":
        for i in range(5):
            if dices[1][i] == 5:
                dices[0][i] = 1

    elif game_name == "Sixes":
        for i in range(5):
            if dices[1][i] == 6:
                dices[0][i] = 1

    elif game_name == "Three of a kind":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 2:
                dices[0][i] = 1

    elif game_name == "Four of a kind":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 2:
                dices[0][i] = 1

    elif game_name == "Full House":
        counts = [dices[1].count(i) for i in range(1, 7)]
        pairs_or_more = [value for value, count in enumerate(counts, start=1) if count >= 2]

        if len(pairs_or_more) > 0:
            first_pair = pairs_or_more[0]
            for i in range(5):
                if dices[1][i] == first_pair:
                    dices[0][i] = 1

        if len(pairs_or_more) > 1:
            second_pair = pairs_or_more[1]
            for i in range(5):
                if dices[1][i] == second_pair:
                    dices[0][i] = 1

    elif game_name == "Small Straight":
        needed_values_sets = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        kept_values = set()
        best_sequence = set()
        for needed_values in needed_values_sets:
            current_sequence = needed_values.intersection(dices[1])
            if len(current_sequence) > len(best_sequence):
                best_sequence = current_sequence
        for i in range(5):
            if dices[1][i] in best_sequence and dices[1][i] not in kept_values:
                dices[0][i] = 1
                kept_values.add(dices[1][i])
            else:
                dices[0][i] = 0

    elif game_name == "Large Straight":
        needed_values = {1, 2, 3, 4, 5} if 6 not in dices[1] else {2, 3, 4, 5, 6}
        kept_values = set()

        for i in range(5):
            if dices[1][i] in needed_values and dices[1][i] not in kept_values:
                dices[0][i] = 1
                kept_values.add(dices[1][i])
            else:
                dices[0][i] = 0



    elif game_name == "YAHTZEE":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 3:
                dices[0][i] = 1


def DetermineHelpfulDicesT(game_name, dices_t):
    """Determină zarurile folositoare pentru un anumit joc."""

    dices_t[0] = [0, 0, 0, 0, 0]

    if game_name == "Ones":
        for i in range(5):
            if dices_t[1][i] == 1:
                dices_t[0][i] = 1

    elif game_name == "Twos":
        for i in range(5):
            if dices_t[1][i] == 2:
                dices_t[0][i] = 1

    elif game_name == "Threes":
        for i in range(5):
            if dices_t[1][i] == 3:
                dices_t[0][i] = 1

    elif game_name == "Fours":
        for i in range(5):
            if dices_t[1][i] == 4:
                dices_t[0][i] = 1

    elif game_name == "Fives":
        for i in range(5):
            if dices_t[1][i] == 5:
                dices_t[0][i] = 1

    elif game_name == "Sixes":
        for i in range(5):
            if dices_t[1][i] == 6:
                dices_t[0][i] = 1

    elif game_name == "Three of a kind":
        counts = [dices_t[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices_t[1][i] - 1] >= 2:
                dices_t[0][i] = 1

    elif game_name == "Four of a kind":
        counts = [dices_t[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices_t[1][i] - 1] >= 2:
                dices_t[0][i] = 1

    elif game_name == "Full House":
        counts = [dices_t[1].count(i) for i in range(1, 7)]
        pairs_or_more = [value for value, count in enumerate(counts, start=1) if count >= 2]

        if len(pairs_or_more) > 0:
            first_pair = pairs_or_more[0]
            for i in range(5):
                if dices_t[1][i] == first_pair:
                    dices_t[0][i] = 1

        if len(pairs_or_more) > 1:
            second_pair = pairs_or_more[1]
            for i in range(5):
                if dices_t[1][i] == second_pair:
                    dices_t[0][i] = 1

    elif game_name == "Small Straight":
        needed_values_sets = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        kept_values = set()
        best_sequence = set()
        for needed_values in needed_values_sets:
            current_sequence = needed_values.intersection(dices_t[1])
            if len(current_sequence) > len(best_sequence):
                best_sequence = current_sequence
        for i in range(5):
            if dices_t[1][i] in best_sequence and dices_t[1][i] not in kept_values:
                dices_t[0][i] = 1
                kept_values.add(dices_t[1][i])
            else:
                dices_t[0][i] = 0

    elif game_name == "Large Straight":
        needed_values = {1, 2, 3, 4, 5} if 6 not in dices_t[1] else {2, 3, 4, 5, 6}
        kept_values = set()

        for i in range(5):
            if dices_t[1][i] in needed_values and dices_t[1][i] not in kept_values:
                dices_t[0][i] = 1
                kept_values.add(dices_t[1][i])
            else:
                dices_t[0][i] = 0



    elif game_name == "YAHTZEE":
        counts = [dices_t[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices_t[1][i] - 1] >= 3:
                dices_t[0][i] = 1



def total(state, player):
    """Calculează scorul total pentru un player."""

    sum_player = 0
    if player == 0:
        for i in range(1, 14):
            sum_player = sum_player + state[i]
    else:
        for i in range(14, 27):
            sum_player = sum_player + state[i]

    return sum_player


def ComputerChooseAI(games_scores):
    """Funcție care folosește metoda QLearning pentru a gestiona mutările player-ului 2."""

    count = 0
    games_played = [0 if game[2] == -1 else 1 for game in games_scores[:13]]
    while count < 3:

        RollDice(dices)
        update_dice_display(dices, dice_frame_p2)
        root.update()
        time.sleep(2)
        dices_state = yahtzee_trainer.initialize_state(dices[1])
        print(f"Computer rolls: {dices[1]}")

        if count == 0:
            available_games = [game for game in games_scores[:13] if game[2] == -1]
            if available_games:
                selected_game = yahtzee_trainer.choose_action(dices_state)
                games_not_disponible = []

                while games_played[selected_game] != 0:
                    games_not_disponible.append(selected_game)
                    selected_game = yahtzee_trainer.choose_next_action(dices_state, games_not_disponible)

                selected_game += 1
                game_name = index_to_game_name[selected_game]

                print(f"Computer chooses the game {game_name} based on Q-table.")
                DetermineHelpfulDices(game_name, dices)
                update_dice_display(dices, dice_frame_p2)
                root.update()
                time.sleep(1)

                if all(die == 1 for die in dices[0]):
                    count = 3


        else:
            selected_game = yahtzee_trainer.choose_action(dices_state)
            games_not_disponible = []

            while games_played[selected_game] != 0:
                games_not_disponible.append(selected_game)
                selected_game = yahtzee_trainer.choose_next_action(dices_state, games_not_disponible)

            selected_game += 1
            game_name = index_to_game_name[selected_game]
            DetermineHelpfulDices(game_name, dices)
            update_dice_display(dices, dice_frame_p2)
            root.update()
            time.sleep(1)

            if all(die == 1 for die in dices[0]):
                count = 3
            else:
                print(f"Computer continues with kept dices for {game_name}: {dices[0]}")

        count += 1

    score = UpdateScore(1, game_name, dices)
    return game_name, score

def WelcomeGame(games_scores):
    root.mainloop()


if __name__ == "__main__":
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    keep_dice_vars = [tk.IntVar(value=0) for _ in range(5)]
    games_scores = InitialGame()
    WelcomeGame(games_scores)
