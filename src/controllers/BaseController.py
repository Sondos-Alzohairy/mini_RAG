from helpers.config import get_settings, Settings
import os
import random 
import string

class BaseController:
    def __init__(self):
        self.settings = get_settings()
        current_file_path = os.path.abspath(__file__) 
        controllers_dir = os.path.dirname(current_file_path) 
        self.base_dir = os.path.dirname(controllers_dir) 
        self.file_dir = os.path.join(self.base_dir, "assets", "files")

    # طلعنا الدالة برة الـ __init__ وبقت ميثود تابعة للكلاس 👇
    def generate_random_string(self, length=8):
        """Generate a random string of fixed length."""
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for i in range(length))