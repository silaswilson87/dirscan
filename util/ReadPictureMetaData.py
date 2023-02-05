from dto.FileDto import FileDto
from PIL import Image # pip3 install Pillow
from PIL.ExifTags import TAGS
from PIL import UnidentifiedImageError



class ReadPictureMetaData:
    def __init__(self, file_dto:FileDto):
        self.file_dto = file_dto

    def read_image_metadata(self):
        image_meta_data = {}

        try:
            image = Image.open(self.file_dto.complete_path)

            # extracting the exif metadata
            exifdata = image.getexif()

            for tagid in exifdata:
                # getting the tag name instead of tag id
                tagname = TAGS.get(tagid, tagid)

                # passing the tagid to get its respective value
                value = exifdata.get(tagid)

                # Some tagname values contain nulls so remove nulls
                if isinstance(value, str):
                    value = str(value).translate({
                        ord('\t'): None,
                        ord('\r'): None,
                        ord('\n'): None,
                        ord('\0'): None
                    })
                    # while value.__contains__('\x00'):
                    #     value = value.replace('\x00','')

                image_meta_data[tagname] = value

                # printing the final result
            # print(new_path)
        except UnidentifiedImageError as pe:
            print("Error reading metadata from "+self.file_dto.complete_path)
            return image_meta_data
        except Exception as e:
            print(self.full_stack())

        return image_meta_data

    def full_stack(self):
        import traceback, sys
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
        if exc is not None:  # i.e. an exception is present
            del stack[-1]  # remove call of full_stack, the printed exception
            # will contain the caught exception caller instead
        trc = 'Traceback (most recent call last):\n'
        stackstr = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stackstr += '  ' + traceback.format_exc().lstrip(trc)
        return stackstr

