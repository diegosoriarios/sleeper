import tkinter as tk
from tkinter import ttk, messagebox
import os
import platform
import subprocess

class ShutdownTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Shutdown/Sleep Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="PC Timer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Time input
        ttk.Label(main_frame, text="Minutes:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.time_var = tk.StringVar(value="30")
        time_spinbox = ttk.Spinbox(main_frame, from_=1, to=1440, textvariable=self.time_var, width=15)
        time_spinbox.grid(row=1, column=1, sticky=tk.W, pady=10)
        
        # Action selection
        ttk.Label(main_frame, text="Action:", font=("Arial", 11)).grid(row=2, column=0, sticky=tk.W, pady=10)
        self.action_var = tk.StringVar(value="shutdown")
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=2, column=1, sticky=tk.W, pady=10)
        
        ttk.Radiobutton(action_frame, text="Shutdown", variable=self.action_var, value="shutdown").pack(anchor=tk.W)
        ttk.Radiobutton(action_frame, text="Sleep", variable=self.action_var, value="sleep").pack(anchor=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Start Timer", command=self.start_timer, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel Timer", command=self.cancel_timer, width=15).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="No timer set", font=("Arial", 10), foreground="gray")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
    def start_timer(self):
        try:
            minutes = int(self.time_var.get())
            if minutes <= 0:
                messagebox.showerror("Error", "Please enter a positive number of minutes")
                return
            
            seconds = minutes * 60
            action = self.action_var.get()
            system = platform.system()
            
            if system == "Windows":
                if action == "shutdown":
                    os.system(f"shutdown /s /t {seconds}")
                    self.status_label.config(text=f"Shutdown scheduled in {minutes} minutes", foreground="green")
                else:  # sleep
                    # Schedule sleep using task scheduler
                    os.system(f"shutdown /h /t {seconds}")
                    self.status_label.config(text=f"Hibernate scheduled in {minutes} minutes", foreground="green")
            
            elif system == "Linux":
                if action == "shutdown":
                    os.system(f"shutdown -h +{minutes}")
                    self.status_label.config(text=f"Shutdown scheduled in {minutes} minutes", foreground="green")
                else:  # sleep
                    os.system(f"sleep {seconds} && systemctl suspend")
                    self.status_label.config(text=f"Sleep scheduled in {minutes} minutes", foreground="green")
            
            elif system == "Darwin":  # macOS
                if action == "shutdown":
                    os.system(f"sudo shutdown -h +{minutes}")
                    self.status_label.config(text=f"Shutdown scheduled in {minutes} minutes", foreground="green")
                else:  # sleep
                    os.system(f"sleep {seconds} && pmset sleepnow")
                    self.status_label.config(text=f"Sleep scheduled in {minutes} minutes", foreground="green")
            
            messagebox.showinfo("Success", f"{action.capitalize()} timer set for {minutes} minutes")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
    
    def cancel_timer(self):
        system = platform.system()
        
        try:
            if system == "Windows":
                os.system("shutdown /a")
            elif system == "Linux":
                os.system("shutdown -c")
            elif system == "Darwin":  # macOS
                os.system("sudo killall shutdown")
            
            self.status_label.config(text="Timer cancelled", foreground="red")
            messagebox.showinfo("Cancelled", "Timer has been cancelled")
        except:
            messagebox.showerror("Error", "Failed to cancel timer")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownTimerApp(root)
    root.mainloop()