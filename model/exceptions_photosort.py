class SourceExists(Exception):
    """If this folder is exists like source in this or that session"""
    def __init__(self, name_folder):
        message = f"{name_folder} is exists like source in this or that session"
        super().__init__(message)


class PhotoExistsInTarget(Exception):
    def __init__(self, name_photo, target_folder):
        message = f"file with name [{name_photo}] already exists in [{target_folder}]"
        super().__init__(message)
        self.photo_name = name_photo
        self.target_folder = target_folder

