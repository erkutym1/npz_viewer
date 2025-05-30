import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class NPZViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NPZ Tıbbi Görüntüleyici")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")

        self.data = None
        self.image_buttons = []

        # Başlık
        title = tk.Label(root, text="NPZ Dosyası Görüntüleyici", font=("Arial", 16, "bold"), bg="#f5f5f5")
        title.pack(pady=10)

        # Dosya seç butonu
        self.select_button = ttk.Button(root, text="NPZ Dosyası Seç", command=self.load_npz_file)
        self.select_button.pack(pady=5)

        # Frame for buttons with scrollbar
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.canvas = tk.Canvas(self.button_frame, width=150, height=600)
        self.scrollbar = ttk.Scrollbar(self.button_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Görüntüyü göstereceğimiz frame
        self.image_frame = tk.Frame(root, bg="white", width=700, height=600)
        self.image_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Matplotlib Figure ve Canvas oluştur
        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.ax.axis('off')
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.image_frame)
        self.canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_npz_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("NPZ dosyaları", "*.npz")])
        if not file_path:
            return

        try:
            self.data = np.load(file_path, allow_pickle=True)

            # Temizle eski butonları
            for btn in self.image_buttons:
                btn.destroy()
            self.image_buttons.clear()

            # Sadece 'image' anahtarı varsa devam et
            if 'image' in self.data.files:
                images = self.data['image']
                # Butonları oluştur
                for i in range(len(images)):
                    btn = ttk.Button(self.scrollable_frame, text=f"Görüntü {i+1}", width=15,
                                     command=lambda idx=i: self.show_image(idx))
                    btn.pack(pady=2)
                    self.image_buttons.append(btn)

                self.ax.clear()
                self.ax.text(0.5, 0.5, "Bir görüntü seçin", ha='center', va='center', fontsize=16)
                self.ax.axis('off')
                self.canvas_fig.draw()
            else:
                messagebox.showinfo("Bilgi", "'image' anahtarı bulunamadı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenemedi:\n{e}")

    def show_image(self, index):
        try:
            img = self.data['image'][index]
            self.ax.clear()
            self.ax.imshow(img, cmap='gray')
            self.ax.axis('off')
            self.canvas_fig.draw()
        except Exception as e:
            messagebox.showerror("Hata", f"Görüntü yüklenemedi:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NPZViewerApp(root)
    root.mainloop()
