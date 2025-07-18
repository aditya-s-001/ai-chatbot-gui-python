from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import emoji

# GUI Setup
root = Tk()
root.title("AI Chatbot")
root.geometry("600x800")
root.resizable(True, True)

# Colors and Fonts
BG_COLOR = "#1e1e2f"
TEXT_COLOR = "#ffffff"
USER_COLOR = "#70e1f5"
BOT_COLOR = "#f57070"
FONT = ("Helvetica", 14)
FONT_BOLD = ("Helvetica", 13, "bold")

# Initialize speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Knowledge Base with suggestions
knowledge_base = {
    ("hello", "hi", "hlo", "hii", "hiiii"): "Hi there, how can I help you?",
    ("how are you",): "I'm fine! And you?",
    ("fine", "i am good", "i am doing good"): "Great! How can I assist you today?",
    ("thanks", "thank you", "now its my time"): "My pleasure!",
    ("what do you sell", "what kinds of items are there", "have you something"): "We have coffee and tea.",
    ("tell me a joke", "tell me something funny", "crack a funny line"): "Why did the developer go broke? Because he used up all his cache! 😄",
    ("tell me about your self", "say few lines about your self"): "Hello! I'm AIBot, created in 2023 to assist and chat with awesome users like you.",
    ("goodbye", "see you later", "see yaa"): "Goodbye! Have a great day!",
    ("who made you", "who is your developer", "developer name", "creator name"): "I was developed by Aditya Shukla.",
    ("when were you created", "when you build", "your build year", "when were you built"): "I was built in 2023."
}

suggestion_buttons = []

def clear_suggestions():
    for btn in suggestion_buttons:
        btn.destroy()
    suggestion_buttons.clear()

def show_suggestions(suggestions):
    clear_suggestions()
    for suggestion in suggestions:
        btn = Button(suggestion_frame, text=suggestion, font=("Helvetica", 10), bg="#4CAF50", fg="white",
                     command=lambda s=suggestion: autofill_and_send(s))
        btn.pack(side=LEFT, padx=5, pady=5)
        suggestion_buttons.append(btn)

def autofill_and_send(suggestion):
    e.delete(0, END)
    e.insert(0, suggestion)
    send()

def send(event=None):
    user_input = e.get().strip().lower()
    if user_input == "":
        return

    txt.insert(END, f"\nYou: {user_input}", ("user",))

    response = None
    suggestion_list = []
    for keys, value in knowledge_base.items():
        for key in keys:
            if key in user_input:
                response = value
                break
            elif key.startswith(user_input):
                suggestion_list.append(key)
        if response:
            break

    if response:
        txt.insert(END, f"\nBot: {response}", ("bot",))
        speak(response)
        clear_suggestions()
    elif suggestion_list:
        txt.insert(END, f"\nBot: Did you mean:", ("bot",))
        show_suggestions(suggestion_list)
    else:
        txt.insert(END, "\nBot: Sorry, I didn't understand that.", ("bot",))
        speak("Sorry, I didn't understand that.")
        clear_suggestions()

    e.delete(0, END)

def record_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Listening", "Speak Now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            e.delete(0, END)
            e.insert(0, text)
            send()
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, I could not understand the audio.")
        except sr.RequestError:
            messagebox.showerror("Error", "Request failed. Check internet connection.")
        except sr.WaitTimeoutError:
            messagebox.showerror("Timeout", "Listening timed out.")

def insert_emoji():
    def add_selected(emoji_char):
        e.insert(END, emoji_char)
        emoji_window.destroy()

    emoji_window = Toplevel(root)
    emoji_window.title("Choose Emoji")
    emoji_window.geometry("250x150")
    emoji_window.configure(bg="white")

    emoji_list = ["😊", "😂", "😢", "😎", "👍", "🙏", "❤️", "🔥", "🥳", "🤔"]

    for idx, emo in enumerate(emoji_list):
        btn = Button(emoji_window, text=emo, font=("Segoe UI Emoji", 18), width=2, command=lambda c=emo: add_selected(c))
        btn.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)

# Top Label
header = Label(root, text="🤖 AIBuddy ", font=("Helvetica", 20, "bold"), bg=BG_COLOR, fg=TEXT_COLOR, pady=10)
header.pack(fill=X)

# Chat Frame
chat_frame = Frame(root, bg=BG_COLOR)
chat_frame.pack(pady=10, fill=BOTH, expand=True)

# Text Widget
txt = Text(chat_frame, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, wrap=WORD, padx=10, pady=10)
txt.pack(side=LEFT, fill=BOTH, expand=True)
txt.tag_config("user", foreground=USER_COLOR)
txt.tag_config("bot", foreground=BOT_COLOR)

# Scrollbar
scrollbar = Scrollbar(chat_frame, command=txt.yview)
scrollbar.pack(side=RIGHT, fill=Y)
txt.config(yscrollcommand=scrollbar.set)

# Suggestion Frame
suggestion_frame = Frame(root, bg=BG_COLOR)
suggestion_frame.pack(fill=X, pady=5)

# Bottom Frame
bottom_frame = Frame(root, bg=BG_COLOR)
bottom_frame.pack(fill=X, pady=10)

e = Entry(bottom_frame, font=FONT, width=40, bg="#2C3E50", fg=TEXT_COLOR)
e.pack(side=LEFT, padx=(10, 5), pady=10, ipady=6)
e.focus()
e.bind("<Return>", send)

send_btn = Button(bottom_frame, text="Send", font=FONT_BOLD, bg="#4CAF50", fg="white", padx=10, pady=5, command=send)
send_btn.pack(side=LEFT, padx=5)

mic_btn = Button(bottom_frame, text="🎤", font=("Arial", 14), bg="#2196F3", fg="white", padx=10, pady=5, command=record_voice)
mic_btn.pack(side=LEFT, padx=5)

emoji_btn = Button(bottom_frame, text="😊", font=("Segoe UI Emoji", 14), bg="#9C27B0", fg="white", padx=10, pady=5, command=insert_emoji)
emoji_btn.pack(side=LEFT, padx=5)

root.mainloop()
