import yfinance as yf
import tkinter as tk
from tkinter import messagebox, scrolledtext

def get_percentage_change(symbol):
    try:
        stock = yf.Ticker(symbol)
        today_data = stock.history(period="1d")
        if today_data.empty:
            return None
        today_close = today_data['Close'][0]
        prev_close = stock.history(period="2d")['Close'][0]
        return (today_close - prev_close) / prev_close * 100
    except Exception:
        return None

def calculate_average():
    user_input = text_var.get()
    div_input = div.get()
    symbols = [symbol.strip() for symbol in user_input.split(',')]
    changes = []

    log_text.delete(1.0, tk.END)
    
    for symbol in symbols:
        change = get_percentage_change(symbol)
        if change is not None:
            log_text.insert(tk.END, f"{symbol}: Change: {change:.2f}%\n")
            changes.append(change)
        else:
            log_text.insert(tk.END, f"{symbol}: Data not available\n")

    valid_changes = [change for change in changes if change is not None]

    if valid_changes:
        average_change = sum(valid_changes) / abs(div_input)
        result_var.set(f"Average Change: {average_change:.2f}%")
    else:
        result_var.set("No valid data available.")

    if is_updating:
        root.after(3000000, calculate_average)

def start_updates():
    global is_updating
    is_updating = True
    calculate_average()

def stop_updates():
    global is_updating
    is_updating = False

root = tk.Tk()
root.title("Stock Average Change Calculator")

default_symbols = "DJI, MSFT, TSLA, AAPL, META, GOOG, NVDA, AMZN"
is_updating = False

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="Enter Stock Tickers (comma separated):")
label.pack(pady=10)

text_var = tk.StringVar()
text_var.set(default_symbols)
entry = tk.Entry(frame, textvariable=text_var, width=50)
entry.pack(pady=10)

result_var = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_var)
result_label.pack(pady=10)


divlabel = tk.Label(frame, text="Enter divisor:")
divlabel.pack(pady=10)

div = tk.IntVar()
diventry = tk.Entry(frame, textvariable=div, width=10)
diventry.pack(pady=10)

log_text = scrolledtext.ScrolledText(frame, width=30, height=8)
log_text.pack(pady=10)

start_btn = tk.Button(frame, text="Start", command=start_updates)
start_btn.pack(side=tk.LEFT, padx=5)



root.mainloop()
