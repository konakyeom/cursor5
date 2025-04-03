import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path


class PhotoAlbum:
    def __init__(self, root):
        self.root = root
        self.root.title("사진 앨범")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 이미지 관련 변수
        self.current_image = None
        self.prev_preview = None
        self.next_preview = None
        self.image_list = []
        self.current_index = -1
        self.image_directory = None
        
        # 메인 프레임
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # 상단 버튼 프레임
        self.top_button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.top_button_frame.pack(fill='x', pady=(0, 10))
        
        # 폴더 선택 버튼
        self.folder_button = tk.Button(
            self.top_button_frame,
            text="폴더 선택",
            command=self.select_folder,
            font=('Segoe UI', 10),
            bg='#0078d7',
            fg='white',
            relief='flat',
            padx=20,
            pady=5
        )
        self.folder_button.pack(side='left', padx=5)
        
        # 이미지 표시 영역
        self.image_frame = tk.Frame(
            self.main_frame,
            bg='white',
            width=700,
            height=450
        )
        self.image_frame.pack(expand=True, fill='both')
        self.image_frame.pack_propagate(False)
        
        # 이미지 레이블
        self.image_label = tk.Label(
            self.image_frame,
            bg='white',
            text="이미지를 선택하세요"
        )
        self.image_label.pack(expand=True)
        
        # 프리뷰 프레임
        self.preview_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.preview_frame.pack(fill='x', pady=5)
        
        # 이전 이미지 프리뷰
        self.prev_preview_label = tk.Label(
            self.preview_frame,
            bg='#f0f0f0',
            text="이전 이미지"
        )
        self.prev_preview_label.pack(side='left', padx=5)
        
        # 다음 이미지 프리뷰
        self.next_preview_label = tk.Label(
            self.preview_frame,
            bg='#f0f0f0',
            text="다음 이미지"
        )
        self.next_preview_label.pack(side='right', padx=5)
        
        # 하단 버튼 프레임
        self.bottom_button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.bottom_button_frame.pack(fill='x', pady=10)
        
        # 이전 버튼
        self.prev_button = tk.Button(
            self.bottom_button_frame,
            text="이전",
            command=self.show_previous,
            font=('Segoe UI', 10),
            bg='#e0e0e0',
            relief='flat',
            padx=20,
            pady=5,
            state='disabled'
        )
        self.prev_button.pack(side='left', padx=5)
        
        # 다음 버튼
        self.next_button = tk.Button(
            self.bottom_button_frame,
            text="다음",
            command=self.show_next,
            font=('Segoe UI', 10),
            bg='#e0e0e0',
            relief='flat',
            padx=20,
            pady=5,
            state='disabled'
        )
        self.next_button.pack(side='left', padx=5)
        
        # 상태 레이블
        self.status_label = tk.Label(
            self.bottom_button_frame,
            text="",
            bg='#f0f0f0',
            font=('Segoe UI', 10)
        )
        self.status_label.pack(side='right', padx=5)
        
        # 지원하는 이미지 형식
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        
        # 프리뷰 이미지 크기
        self.preview_size = (150, 100)
    
    def select_folder(self):
        """이미지가 있는 폴더를 선택합니다."""
        folder = filedialog.askdirectory()
        if folder:
            self.image_directory = folder
            self.load_images()
    
    def load_images(self):
        """선택된 폴더에서 이미지 파일들을 로드합니다."""
        if not self.image_directory:
            return
            
        self.image_list = []
        for file in os.listdir(self.image_directory):
            if Path(file).suffix.lower() in self.supported_formats:
                self.image_list.append(file)
        
        if self.image_list:
            self.current_index = 0
            self.show_current_image()
            self.update_previews()
            self.update_buttons()
            self.update_status()
        else:
            messagebox.showinfo(
                "알림",
                "선택한 폴더에 지원되는 이미지 파일이 없습니다."
            )
    
    def show_current_image(self):
        """현재 이미지를 표시합니다."""
        if not self.image_list or self.current_index < 0:
            return
            
        try:
            image_path = os.path.join(
                self.image_directory,
                self.image_list[self.current_index]
            )
            image = Image.open(image_path)
            
            # 이미지 크기 조정
            display_size = (700, 450)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # 이미지 표시
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.configure(image=self.current_image)
            
        except Exception as e:
            messagebox.showerror("오류", f"이미지를 불러오는 중 오류가 발생했습니다: {str(e)}")
    
    def update_previews(self):
        """이전과 다음 이미지 프리뷰를 업데이트합니다."""
        # 이전 이미지 프리뷰
        if self.current_index > 0:
            try:
                prev_path = os.path.join(
                    self.image_directory,
                    self.image_list[self.current_index - 1]
                )
                prev_image = Image.open(prev_path)
                prev_image.thumbnail(self.preview_size, Image.Resampling.LANCZOS)
                self.prev_preview = ImageTk.PhotoImage(prev_image)
                self.prev_preview_label.configure(image=self.prev_preview)
            except Exception as e:
                self.prev_preview_label.configure(image='')
        else:
            self.prev_preview_label.configure(image='')
        
        # 다음 이미지 프리뷰
        if self.current_index < len(self.image_list) - 1:
            try:
                next_path = os.path.join(
                    self.image_directory,
                    self.image_list[self.current_index + 1]
                )
                next_image = Image.open(next_path)
                next_image.thumbnail(self.preview_size, Image.Resampling.LANCZOS)
                self.next_preview = ImageTk.PhotoImage(next_image)
                self.next_preview_label.configure(image=self.next_preview)
            except Exception as e:
                self.next_preview_label.configure(image='')
        else:
            self.next_preview_label.configure(image='')
    
    def show_previous(self):
        """이전 이미지를 표시합니다."""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()
            self.update_previews()
            self.update_buttons()
            self.update_status()
    
    def show_next(self):
        """다음 이미지를 표시합니다."""
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.show_current_image()
            self.update_previews()
            self.update_buttons()
            self.update_status()
    
    def update_buttons(self):
        """버튼 상태를 업데이트합니다."""
        prev_state = 'normal' if self.current_index > 0 else 'disabled'
        next_state = 'normal' if self.current_index < len(self.image_list) - 1 else 'disabled'
        self.prev_button['state'] = prev_state
        self.next_button['state'] = next_state
    
    def update_status(self):
        """상태 레이블을 업데이트합니다."""
        if self.image_list:
            status_text = f"{self.current_index + 1} / {len(self.image_list)}"
            self.status_label['text'] = status_text
        else:
            self.status_label['text'] = ""


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoAlbum(root)
    root.mainloop() 