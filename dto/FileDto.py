import os
import shutil
import time
from pathlib import Path
from os.path import join, getsize

copy_files = False  # Remove once the copy logic is added

# Dto stands for Data Transfer Object meaning there should be no logic in the class, data only.
class FileDto:
    def __init__(self, parent, path: Path):
        self.create_time = time.ctime(os.path.getctime(path))  # save create time
        self.modified_time = time.ctime(os.path.getmtime(path))  # save modified time
        self.create_time_string = self.make_iso_date(self.create_time)
        self.modified_time_string = self.make_iso_date(self.modified_time)
        self.size = getsize(path)
        split_tup = os.path.splitext(path.name)
        self.file_name = split_tup[0]
        # self.file_extension = split_tup[1] if you want file_extension to start with '.'
        self.file_extension = split_tup[1][1:].lower()  # Ignores first character (the '.')
        self.parent = parent
        self.original_path = path
        self.complete_path = path.__fspath__()
        self.root = path.root
        self.image_meta_data = {}
        self.location = None
        self.new_path = ""  # New path can be calculated here, or later after array has been created


    def set_location(self, location):
        if self.image_meta_data:
            self.location = location

    def add_image_metadata(self, image_meta_data):
        self.image_meta_data = image_meta_data

    def copy(self):
        if copy_files:
            shutil.copy2(self.complete_path, self.new_path + "/" + self.file_name)
        self.print()

    def print(self):
        if self.image_meta_data:
            print (self.file_name+"."+self.file_extension, self.location, str(self.image_meta_data))
        # else:
        #     print(f"parent: {str(self.parent)} || file_name: {self.file_name} || file_extension: {self.file_extension} ||created: {self.create_time_string} || size: {self.size:,d} ")

    def make_new_path(self):
        a = 1
        # self.new_path = new_path # Compute new path from image metadata

    def make_iso_date(self, ctime):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(ctime))

    def get_size(self):
        return self.size
