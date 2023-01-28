import os
import sys

from pathlib import Path
from dto import FileDto as fileDto
from util import Util_IO as defaultsIO
from util.ReadPictureMetaData import ReadPictureMetaData
from util.GeoLocator import GeoLocator

def compare(first: fileDto.FileDto, second: fileDto.FileDto):
    return first.size - second.size  # ascending size order (flip first and second to make it descending order)

if __name__ == '__main__':

    # Get defaults from json file in file system (it creates a default if not found)
    defaults = defaultsIO.Util_IO()

    picture_extensions = defaults.picture_extensions()

    start_path = defaults.start_path()  # Get start_path from json file
    if len(sys.argv) > 1:  # If 1st arg exists overwrite
        start_path = sys.argv[1]

    new_path = defaults.new_path()  # Get new_path from json file
    #  Example of getting arguments from the python cmd line
    if len(sys.argv) > 2:  # If 2nd arg exists overwrite
        new_path = sys.argv[2]

    saved_files = []  # Create empty array
    total_byte_size = 0
    # Loop through directories in file system starting from scanner.start_path and create the array of FileDto objects
    for root, dirs, files in os.walk(start_path):
        for file in files:
            path = Path(root + "/" + file)
            if path.is_symlink():  # A linux thing, should always be false in Windows
                continue
            file_dto = fileDto.FileDto(root, path)  # Create file object
            if file_dto.file_extension in picture_extensions:
                pass
                image_meta_data = ReadPictureMetaData(file_dto).read_image_metadata()
                file_dto.add_image_metadata(image_meta_data)  # Will be {} if no image metadata
                location = GeoLocator(file_dto).get_location()  # Will be None if no image metadata
                file_dto.set_location(location)

            saved_files.append(file_dto)  # Add file object to list

    # Possible, even likely that some kind of analysis loop that looks at all files will go here

    # Once finished, loop and copy
    for dto in saved_files:  # loop through saved_files list of FileDto objects
        # You may want to process all files, but process images files differently
        #  For now, this code ignores all non pictures files (as defined in the list picture_extensions
        total_byte_size += dto.get_size()
        dto.make_new_path()
        dto.copy()  # Will eventually actually copy, but it prints for now

    #  Sort saved_files by file size
    # sorted_l = sorted(saved_files, key=functools.cmp_to_key(compare))
    #
    # # If new_path was defined in scanner json, then loop through files and do something,
    # #   for now just add the new path and print
    # if new_path and new_path.strip():
    #     for dto in sorted_l:  # saved_files:
    #         total_byte_size += dto.get_size()
    #         metadata = ReadPictureMetaData(dto).readMeta()
    #         dto.make_new_path(metadata)
    #         dto.copy()  # Will eventually actually copy, but it prints for now
    # Print with commas in numbers
    print(f"Found {len(saved_files):,d}, files.  Total bytes {total_byte_size:,d}")
