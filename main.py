
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import time
from pathlib import Path

root = tk.Tk()
root.title("Whispery boi")
root.geometry("640x360")
root.resizable(False, False)


directory_transcript_path = tk.StringVar(value=Path.home())


main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_label = tk.Label(main_frame, text="♫ WHISPER UI", font=("Consolas 22 bold"))
main_label.pack(
    side="top",
    anchor="nw",
    padx=10,
    pady=10
)

separator_title = tk.Frame(
    main_frame,
    height=3,
    bg="black"
)
separator_title.pack(fill="x", padx=10)



######################### DIRECTORY ###############################
def browse_dir():
    path = filedialog.askdirectory()
    if path:
        directory_transcript_path.set(path)
        pathObject = Path(directory_transcript_path.get() + "/" + transcript_filename.get().replace(" ", "_") + ".txt")

        file_full_path.set(pathObject.resolve())

directory_label_transcript = tk.Label(
    main_frame,
    text="•Où enregistrer la retranscription:",
    font=("Consolas", 12, "bold")
)
directory_label_transcript.pack(anchor="nw", padx=10, pady=(10, 2))


directory_input_container = tk.Frame(
    main_frame
)
directory_input_container.pack(fill="x", expand=False, side="top", anchor="nw")


directory_input_transcript = tk.Entry(
    directory_input_container,
    font=("Consolas", 11),
    textvariable=directory_transcript_path
)
directory_input_transcript.pack(side="left", anchor="nw", fill="x", expand=True, padx=5, pady=5)

directory_button_transcript = tk.Button (
    directory_input_container,
    text="Choisir un dossier",
    command=browse_dir
)
directory_button_transcript.pack(side="right", anchor="ne", expand=False, padx=5)

separator_selected_dir = tk.Frame(
    main_frame,
    height=1,
    bg="gray"
)
separator_selected_dir.pack(
    fill="x",
    padx=10,
    pady=10,
    side="top",
    anchor="nw"
)

######################### FIN DIRECTORY ###############################
######################### NOM FICHIER #################################
def on_filename_change(*args):
        pathObject = Path(directory_transcript_path.get() + "/" + transcript_filename.get().replace(" ", "_") + ".txt")
        file_full_path.set(pathObject.resolve())

file_full_path = tk.StringVar()

transcript_filename = tk.StringVar(value=str(int(time.time())))
transcript_filename.trace_add("write", on_filename_change)
file_full_path.set(directory_transcript_path.get() + "/" + transcript_filename.get().replace(" ", "_") + ".txt")

filename_container = tk.Frame(
    main_frame
)
filename_container.pack(fill="x", expand=False, side="top", anchor="nw")



filename_label = tk.Label(
    filename_container,
    text="•Donnez un nom à la retranscription :",
    font=("Consolas", 12, "bold")
)
filename_label.pack(expand=False, side="left", anchor="nw", padx=5, pady=5)



filename_input = tk.Entry(
    filename_container,
    font=("Consolas", 11),
    textvariable=transcript_filename
)
filename_input.pack(side="right", anchor="nw", fill="x", expand=True, padx=5, pady=5)

saved_as_label = tk.Label(
    main_frame,
    text="Le fichier sera enregistré ici en tant que :",
    padx=5,
    font=("Consolas", 8),
)
saved_as_label.pack(expand=False, side="top", anchor="nw")


file_fullpath_label = tk.Label(
    main_frame,
    textvariable=file_full_path,
    fg="#cf1717",
    font=("Consolas", 8, "italic"),
    padx=5
)
file_fullpath_label.pack(expand=False, side="top", anchor="nw")

separator_input_filename = tk.Frame(
    main_frame,
    height=3,
    bg="black"
)
separator_input_filename.pack(
    fill="x",
    padx=10,
    pady=10,
    side="top",
    anchor="nw"
)
####################################################################################
##################################AUDIO#############################################
audio_file_path = tk.StringVar()
def browse_dir():
    path = filedialog.askopenfilename(
        title="Sélectionner un fichier",
        filetypes=[
            ("Fichier audio", "*.wav *.mp3 *.m4a *.flac *.ogg *.aac *.wma"),
            # ("Fichier vidéo", "*.mp4 *.mkv *.webm"),
            ("Tous les fichiers", "*.*")
        ]
    )
    if path:
        audio_file_path.set(path)

audio_label = tk.Label(
    main_frame,
    text="•Sélectionnez le fichier audio à retranscrire:",
    font=("Consolas", 12, "bold")
)
audio_label.pack(anchor="nw", padx=10, pady=(10, 2))


audio_input_container = tk.Frame(
    main_frame
)
audio_input_container.pack(fill="x", expand=False, side="top", anchor="nw")


audio_input = tk.Entry(
    audio_input_container,
    font=("Consolas", 11),
    textvariable=audio_file_path
)
audio_input.pack(side="left", anchor="nw", fill="x", expand=True, padx=5, pady=5)

audio_button = tk.Button (
    audio_input_container,
    text="Choisir le fichier",
    command=browse_dir
)
audio_button.pack(side="right", anchor="ne", expand=False, padx=5)




root.mainloop()