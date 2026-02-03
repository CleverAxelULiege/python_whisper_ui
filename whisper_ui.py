from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import traceback
from whisper_ui_input import WhisperUIInput, WHISPER_LANGUAGES
from pathlib import Path

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import librosa


# pyinstaller --name WhisperUITestConsole --onedir  whisper_ui.py
# pyinstaller --name WhisperUITestConsole --onedir --windowed  whisper_ui.py
class WhisperUI:
    def __init__(self):
        self.root = Tk()
        self.input = WhisperUIInput(self.root)

        self.progress_bar = ttk.Progressbar(master=self.root, mode="indeterminate")
        self.submit_button = Button()

        self.__init_root()
        self.__create_title()
        self.__file_name_and_location()
        self.__build_audio_selection()
        self.__build_language_selection()
        self.__submit_button()
        self.__place_progress_bar()
        self.__hide_progress_bar()
        self.__enable_submit_button()
    
    def __create_title(self):
        title = Label(self.root, text="~ WHISPER UI ᕕ( ᐛ )ᕗ", font=("Consolas", 22, "bold"))
        title.pack(
            side="top",
            anchor="nw",
            padx=10,
            pady=10
        )

        separator_title = Frame(
            self.root,
            height=3,
            bg="black"
        )
        separator_title.pack(fill="x", padx=10)

    def __disable_submit_button(self):
        self.submit_button["state"] = "disabled"


    def __enable_submit_button(self):
        self.submit_button["state"] = "enable"

    def __file_name_and_location(self):
        label_frame = LabelFrame(self.root, text=" • Nom et emplacement • ", font=("Arial", 12, "bold"))
        label_frame.pack(anchor="nw", fill="x", padx=5, pady=5)

        label_frame_grid = Frame(label_frame)
        label_frame_grid.pack(anchor="nw", fill="x")

        # Destination folder
        label = Label(label_frame_grid, text="Choisir le dossier de destination :", font=("Arial", 10, "italic"))
        label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")

        text_input = Entry(
            label_frame_grid,
            font=("Arial", 11),
            textvariable=self.input.save_directory_path
        )
        text_input.grid(row=1, column=0, sticky="ew", padx=5, pady=0)

        browse_button = Button(label_frame_grid, text="Choisir un dossier", command=self.__select_save_directory)
        browse_button.grid(row=1, column=1, pady=2, sticky="ew")

        # File name
        label = Label(label_frame_grid, text="Choisir le nom du fichier et l'extension du fichier :", font=("Arial", 10, "italic"))
        label.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="w")

        text_input = Entry(
            label_frame_grid,
            font=("Arial", 11),
            textvariable=self.input.save_filename
        )
        text_input.grid(row=3, column=0, sticky="ew", padx=5, pady=0)

        # file extension
        select_extension = ttk.Combobox(label_frame_grid, values=self.input.allowed_extensions, textvariable=self.input.save_file_extension, state="readonly")
        select_extension.grid(row=3, column=1, pady=2, sticky="ew")

        label_frame_grid.columnconfigure(0, weight=1)

        #Display future file full path :
        label = Label(label_frame, text="→ La future transcription sera enregistrée ici :", font=("Arial", 8, "italic"))
        label.pack(side="top", anchor="nw", expand=False, padx=2, pady=(5, 0))
        
        label = Label(label_frame, textvariable=self.input.save_transcript_file_full_path, font=("Arial", 8, "italic"), fg="red")
        label.pack(side="top", anchor="nw", expand=False, padx=2, pady=(0, 0))

    def __place_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.root, mode="indeterminate", length=300)
        self.__show_progress_bar()

    def __hide_progress_bar(self):
        self.progress_bar.pack_forget()

    def __show_progress_bar(self):
        self.progress_bar.pack()

    def __select_save_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.input.save_directory_path.set(path)

    def __build_audio_selection(self):
        label_frame = LabelFrame(self.root, text=" • Fichier audio • ", font=("Arial", 12, "bold"))        
        label_frame.pack(anchor="nw", fill="x", padx=5, pady=5)

        label_frame_grid = Frame(label_frame)
        label_frame_grid.pack(anchor="nw", fill="x")

        label = Label(label_frame_grid, text="Choisir le fichier audio :", font=("Arial", 10, "italic"))
        label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")

        text_input = Entry(
            label_frame_grid,
            font=("Arial", 11),
            textvariable=self.input.audio_file_path
        )
        text_input.grid(row=1, column=0, sticky="ew", padx=5, pady=0)

        browse_button = Button(label_frame_grid, text="Sélectionner un fichier", command=self.__select_audio_file)
        browse_button.grid(row=1, column=1, pady=2, sticky="ew")
        label_frame_grid.columnconfigure(0, weight=1)

    def __build_language_selection(self):
        label_frame = LabelFrame(self.root, text=" • Sélection de la langue • ", font=("Arial", 12, "bold"))        
        label_frame.pack(anchor="nw", fill="x", padx=5, pady=5)

        label_frame_grid = Frame(label_frame)
        label_frame_grid.pack(anchor="nw", fill="x")

        label = Label(label_frame_grid, text="Quel language est utilisé dans le fichier audio :", font=("Arial", 10, "italic"))
        label.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="w")

        select_language = ttk.Combobox(label_frame_grid, values=list(WHISPER_LANGUAGES.keys()), textvariable=self.input.language, state="readonly")
        select_language.set("Français")
        select_language.grid(row=0, column=1, pady=(10, 0), sticky="ew")


    def __select_audio_file(self):
        path = filedialog.askopenfilename(
        title="Sélectionner un fichier",
            filetypes=[
                ("Fichier audio", "*.wav *.mp3 *.m4a *.flac *.ogg *.aac *.wma"),
                # ("Fichier vidéo", "*.mp4 *.mkv *.webm"),
                # ("Tous les fichiers", "*.*")
            ]
        )
        if path:
            self.input.audio_file_path.set(path)

    def __submit_button(self):
        button_frame = Frame(self.root)
        button_frame.pack(anchor="nw", fill="x", padx=5, pady=5)
        self.submit_button = ttk.Button(button_frame, text="Transcrire le fichier audio", command=self.__on_submit_button)
        self.submit_button.pack(side="left", padx=5, pady=5, expand=True)

    def __on_submit_button(self):
        audio_path = Path(self.input.audio_file_path.get())
        save_directory_path = Path(self.input.save_directory_path.get())


        if(audio_path == Path(".") or not audio_path.exists()):
            messagebox.showerror(title="Fichier audio introuvable", message="Le fichier audio est introuvable, existe-t-il ?")
            return
        
        if(audio_path.is_dir()):
            messagebox.showerror(title="Le fichier n'est pas un fichier", message="Le chemin choisi n'est pas un fichier, il s'agit sans doute d'un dossier.")
            return
        
        if(save_directory_path == Path(".") or not save_directory_path.exists()):
            messagebox.showerror(title="Le dossier n'existe pas", message="Le dossier où doit être enregistré la transcription n'existe pas.")
            return

        self.__disable_submit_button()
        self.__show_progress_bar()
        self.progress_bar.start()
        # self.__transcribe()
        
    def __transcribe(self):
        try:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

            model_id = r"C:\Users\clever\Documents\python\tkinter_whisper\model\small"
            audio_file = r"C:\Users\clever\Documents\python\tkinter_whisper\audio.mp3"

            # Load model
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                model_id,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True
            )
            model.to(device)

            processor = AutoProcessor.from_pretrained(model_id)

            pipe = pipeline(
                "automatic-speech-recognition",
                model=model,
                tokenizer=processor.tokenizer,
                feature_extractor=processor.feature_extractor,
                batch_size=16,
                return_timestamps=True,
                dtype=torch_dtype,
                device=device,
                generate_kwargs={"language": "fr"}
            )

            # Load audio
            audio, sample_rate = librosa.load(audio_file, sr=16000, mono=True)

            # Transcribe
            result = pipe(audio)

            messagebox.showinfo("Transcription", result["text"][:300])

        except FileNotFoundError as e:
            messagebox.showerror(
                "File error",
                f"File not found:\n{e}"
            )

        except RuntimeError as e:
            messagebox.showerror(
                "Runtime error",
                f"A runtime error occurred (CUDA / model issue?):\n{e}"
            )

        except Exception as e:
            # Catch-all for anything else
            messagebox.showerror(
                "Unexpected error",
                f"{e}\n\n{traceback.format_exc()}"
            )


    def __init_root(self):
        self.root.title("Whisper UI")
        self.root.geometry("640x580")
        self.root.resizable(False, False)

    def start(self):
        self.root.mainloop()


ui = WhisperUI()
ui.start()
