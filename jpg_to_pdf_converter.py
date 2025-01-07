import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
from pathlib import Path

class ModernJPGtoPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG to PDF Converter")
        self.root.geometry("800x600")
        
        # Warna tema dark mode
        self.colors = {
            "bg": "#202020",
            "secondary_bg": "#2D2D2D",
            "text": "#FFFFFF",
            "accent": "#60CDFF",
            "button_hover": "#3AA7DA",
            "success": "#6CCB5F",
            "error": "#FF6B6B"
        }
        
        # Konfigurasi tema
        self.root.configure(bg=self.colors["bg"])
        self.style = ttk.Style()
        self.style.configure(
            "Modern.TButton",
            padding=10,
            background=self.colors["accent"],
            foreground=self.colors["text"]
        )
        
        # Frame utama dengan padding
        main_frame = tk.Frame(root, bg=self.colors["bg"])
        main_frame.pack(pady=30, padx=40, fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        header_frame.pack(fill="x", pady=(0, 30))
        
        title_label = tk.Label(
            header_frame,
            text="JPG to PDF Converter",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        title_label.pack(side="left")
        
        # Container untuk input/output
        io_container = tk.Frame(main_frame, bg=self.colors["bg"])
        io_container.pack(fill="x", pady=(0, 20))
        
        # Frame untuk input folder
        input_frame = self.create_path_frame(io_container, "Input Folder", self.browse_input_folder)
        input_frame.pack(fill="x", pady=(0, 15))
        
        # Frame untuk output folder
        output_frame = self.create_path_frame(io_container, "Output Folder", self.browse_output_folder)
        output_frame.pack(fill="x")
        
        # Button konversi dengan efek hover
        convert_btn = tk.Button(
            main_frame,
            text="Konversi ke PDF",
            font=("Segoe UI", 11),
            command=self.start_conversion,
            bg=self.colors["accent"],
            fg=self.colors["text"],
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2"
        )
        convert_btn.pack(pady=30)
        convert_btn.bind("<Enter>", lambda e: e.widget.configure(bg=self.colors["button_hover"]))
        convert_btn.bind("<Leave>", lambda e: e.widget.configure(bg=self.colors["accent"]))
        
        # Frame untuk log
        log_frame = tk.Frame(main_frame, bg=self.colors["secondary_bg"], padx=15, pady=15)
        log_frame.pack(fill="both", expand=True)
        
        # Label untuk log
        log_label = tk.Label(
            log_frame,
            text="Log Proses",
            font=("Segoe UI", 11),
            bg=self.colors["secondary_bg"],
            fg=self.colors["text"]
        )
        log_label.pack(anchor="w", pady=(0, 10))
        
        # Text area untuk log dengan scrollbar
        self.log_text = tk.Text(
            log_frame,
            height=10,
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief="flat",
            padx=10,
            pady=10
        )
        self.log_text.pack(fill="both", expand=True)
        
        # Scrollbar untuk log
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
    def create_path_frame(self, parent, label_text, browse_command):
        frame = tk.Frame(parent, bg=self.colors["bg"])
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Segoe UI", 11),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        label.pack(anchor="w", pady=(0, 5))
        
        path_container = tk.Frame(frame, bg=self.colors["secondary_bg"], padx=2, pady=2)
        path_container.pack(fill="x")
        
        path_var = tk.StringVar()
        setattr(self, f"{label_text.lower().replace(' ', '_')}_path", path_var)
        
        entry = tk.Entry(
            path_container,
            textvariable=path_var,
            font=("Segoe UI", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            relief="flat",
            insertbackground=self.colors["text"]
        )
        entry.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        
        browse_btn = tk.Button(
            path_container,
            text="Browse",
            command=browse_command,
            font=("Segoe UI", 10),
            bg=self.colors["accent"],
            fg=self.colors["text"],
            relief="flat",
            padx=15,
            cursor="hand2"
        )
        browse_btn.pack(side="right", padx=2, pady=2)
        browse_btn.bind("<Enter>", lambda e: e.widget.configure(bg=self.colors["button_hover"]))
        browse_btn.bind("<Leave>", lambda e: e.widget.configure(bg=self.colors["accent"]))
        
        return frame

    def browse_input_folder(self):
        folder_path = filedialog.askdirectory(title="Pilih Folder Input")
        if folder_path:
            self.input_folder_path.set(folder_path)
            # Set default output folder
            if not self.output_folder_path.get():
                folder_name = os.path.basename(folder_path)
                parent_folder = os.path.dirname(folder_path)
                default_output = os.path.join(parent_folder, f"{folder_name} PDF")
                self.output_folder_path.set(default_output)
    
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(title="Pilih Folder Output")
        if folder_path:
            self.output_folder_path.set(folder_path)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
            
    def convert_jpg_to_pdf(self, input_folder, output_folder):
        # Membuat folder output jika belum ada
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        # Mencari semua file JPG dalam folder dan subfolder
        jpg_files = []
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg')):
                    jpg_files.append(os.path.join(root, file))
        
        if not jpg_files:
            self.log_message(f"Tidak ada file JPG ditemukan di folder {input_folder}")
            return
        
        # Proses setiap file JPG
        for jpg_file in jpg_files:
            try:
                # Mendapatkan struktur folder relatif
                rel_path = os.path.relpath(os.path.dirname(jpg_file), input_folder)
                if rel_path == ".":
                    output_subdir = output_folder
                else:
                    output_subdir = os.path.join(output_folder, rel_path)
                    
                # Membuat subfolder di output jika belum ada
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)
                
                # Buka gambar JPG
                image = Image.open(jpg_file)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Buat nama file PDF
                pdf_filename = os.path.splitext(os.path.basename(jpg_file))[0] + '.pdf'
                pdf_path = os.path.join(output_subdir, pdf_filename)
                
                # Simpan sebagai PDF
                image.save(pdf_path, 'PDF')
                self.log_message(f'Berhasil mengkonversi: {jpg_file} -> {pdf_path}')
                
            except Exception as e:
                self.log_message(f'Gagal mengkonversi {jpg_file}: {str(e)}')
    
    def start_conversion(self):
        input_folder = self.input_folder_path.get()
        output_folder = self.output_folder_path.get()
        
        if not input_folder or not output_folder:
            messagebox.showerror("Error", "Silakan pilih folder input dan output terlebih dahulu!")
            return
            
        self.log_text.delete(1.0, tk.END)
        self.log_message(f"Memulai konversi dari folder: {input_folder}")
        self.log_message(f"Hasil akan disimpan di: {output_folder}")
        self.convert_jpg_to_pdf(input_folder, output_folder)
        self.log_message("\nKonversi selesai!")
        messagebox.showinfo("Selesai", "Konversi file selesai!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernJPGtoPDFConverter(root)
    root.mainloop() 