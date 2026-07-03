import os
from .BaseController import BaseController
from fastapi import UploadFile
from models.enums.ResponseEnym import ResponseSignal
from .ProjectController import ProjectController
import re

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  

    def validate_file(self, file: UploadFile):
        _, file_extension = os.path.splitext(file.filename.lower())
        allowed_extensions = [ext.strip() for ext in self.settings.FILE_ALLOWED_TYPES.split(",")]
        
        if file_extension not in allowed_extensions:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
            
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > self.settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filepath(self, original_filename: str, project_id: int):
        random_file_name = self.generate_random_string(8) 
        project_path = ProjectController().get_project_Path(project_id=project_id)
        cleaned_filename = self.get_cleaned_filename(original_filename)
        
        new_file_path = os.path.join(project_path, f"{random_file_name}_{cleaned_filename}")
        while os.path.exists(new_file_path):
            random_file_name = self.generate_random_string(8)
            new_file_path = os.path.join(project_path, f"{random_file_name}_{cleaned_filename}")
            
        return new_file_path , random_file_name+"_"+cleaned_filename

    def get_cleaned_filename(self, original_filename: str):
        """Remove special characters from the filename."""
        cleaned_filename = ''.join(e for e in original_filename if e.isalnum() or e in (' ', '.', '_')).rstrip()
        return cleaned_filename