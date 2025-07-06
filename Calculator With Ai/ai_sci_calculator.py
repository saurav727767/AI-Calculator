import tkinter as tk
from tkinter import messagebox
import math
import pyttsx3
import speech_recognition as sr

root = tk.Tk()
root.title("AI Scientific Calculator")
root.geometry("500x600")
root.resizable(False, False)

memory = 0
history = []
dark_mode = False
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def press(symbol):
    entry.insert(tk.END, str(symbol))

def clear():
    entry.delete(0, tk.END)

def equal():
    try:
        expression = entry.get().replace("^", "**")
        result = eval(expression, {"__builtins__": None}, math.__dict__)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        history.append(f"{expression} = {result}")
        update_history()
        speak(f"The result is {result}")
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        speak("There was an error")

def calculate_scientific(func):
    try:
        expression = entry.get()
        if not expression:
            entry.insert(tk.END, "Error")
            return
        value = float(eval(expression, {"__builtins__": None}, math.__dict__))

        if func == "sqrt":
            result = math.sqrt(value)
        elif func == "log":
            result = math.log10(value)
        elif func == "ln":
            result = math.log(value)
        elif func == "sin":
            result = math.sin(math.radians(value))
        elif func == "cos":
            result = math.cos(math.radians(value))
        elif func == "tan":
            result = math.tan(math.radians(value))
        else:
            result = "Error"

        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        history.append(f"{func}({value}) = {result}")
        update_history()
        speak(f"The result is {result}")
    except:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        speak("Invalid input")

def insert_pi():
    press(str(math.pi))

def memory_add():
    global memory
    try:
        memory += float(entry.get())
        speak("Added to memory")
    except:
        speak("Invalid number")

def memory_subtract():
    global memory
    try:
        memory -= float(entry.get())
        speak("Subtracted from memory")
    except:
        speak("Invalid number")

def memory_recall():
    entry.delete(0, tk.END)
    entry.insert(tk.END, str(memory))
    speak(f"Memory recalled: {memory}")

def memory_clear():
    global memory
    memory = 0
    speak("Memory cleared")

def update_history():
    history_text.delete("1.0", tk.END)
    for item in history[-10:]:
        history_text.insert(tk.END, item + "\n")

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2e2e2e" if dark_mode else "white"
    fg = "white" if dark_mode else "black"
    entry.config(bg=bg, fg=fg, insertbackground=fg)
    history_text.config(bg=bg, fg=fg)
    for btn in buttons:
        btn.config(bg=bg, fg=fg)

def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Speak now")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(tk.END, text)
            equal()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand")
        except sr.RequestError:
            speak("Could not connect to speech service")

# GUI Layout
entry = tk.Entry(root, font=("Arial", 20), bd=10, relief='sunken', justify='right')
entry.grid(row=0, column=0, columnspan=6, pady=10)

history_text = tk.Text(root, height=6, width=58)
history_text.grid(row=1, column=0, columnspan=6, padx=10, pady=5)

button_data = [
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('sqrt', 2, 4), ('M+', 2, 5),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('log', 3, 4), ('M-', 3, 5),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('ln', 4, 4), ('MR', 4, 5),
    ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3), ('π', 5, 4), ('MC', 5, 5),
    ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('^', 6, 3), ('C', 6, 4), ('🎤', 6, 5),
    ('🌙', 7, 0)
]

buttons = []
for (text, r, c) in button_data:
    if text in ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt']:
        cmd = lambda x=text: calculate_scientific(x)
    elif text == 'π':
        cmd = insert_pi
    elif text == 'C':
        cmd = clear
    elif text == '=':
        cmd = equal
    elif text == '^':
        cmd = lambda: press("**")
    elif text == 'M+':
        cmd = memory_add
    elif text == 'M-':
        cmd = memory_subtract
    elif text == 'MR':
        cmd = memory_recall
    elif text == 'MC':
        cmd = memory_clear
    elif text == '🎤':
        cmd = voice_input
    elif text == '🌙':
        cmd = toggle_dark_mode
    else:
        cmd = lambda x=text: press(x)

    btn = tk.Button(root, text=text, padx=15, pady=15, font=("Arial", 12), command=cmd)
    btn.grid(row=r, column=c, padx=2, pady=2)
    buttons.append(btn)

root.mainloop()
