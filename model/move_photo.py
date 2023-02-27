from pathlib import Path
from shutil import copyfile
import re
from model.exceptions_photosort import PhotoExistsInTarget

class Mover:
    def __init__(self):
        self.tuple_sufix = (" (copy)", " (another copy)")

    def _check_exists_file_in_target(self, short_name_photo, target) -> bool:
        return Path(target).joinpath(short_name_photo).exists()

    def copy_one_to_one(self, photo, target, new_name=None):
        if new_name:
            short_name_photo = new_name
        else:
            short_name_photo = Path(photo).name
        if self._check_exists_file_in_target(short_name_photo, target):
            raise PhotoExistsInTarget(photo, target)
        else:
            start = Path(photo)
            finish = Path(target).joinpath(short_name_photo)
            copyfile(start, finish)
            # print("copyed ",start, " to ", finish)

    def copy_one_to_one_without_exception_for_replace(self, photo, target):
        short_name_photo = Path(photo).name
        start = Path(photo)
        finish = Path(target).joinpath(short_name_photo)
        copyfile(start, finish)
        # print("replaced ",start, " to ", finish)


    def delete_photo_from_source(self, name):
        Path(name).unlink()


    def generate_new_name(self, name_photo, name_target):
        short_name = self.clean_short_name(Path(name_photo).name)
        name_ph_trg = Path(name_target).joinpath(short_name)
        ind = 0
        while True:
            sufix = "th"
            if ind == 2:
                sufix = "rd"
            elif ind > 2 and ind < 19:
                sufix = "th"
            elif ind > 18:
                modul = (ind+1) % 10
                if modul == 1:
                    sufix = "st"
                elif modul == 2:
                    sufix = "nd"
                elif modul == 3:
                    sufix = "rd"
            new_name = f"{str(name_ph_trg)} ({ind+1}{sufix} copy)"
            if ind < 2:
                new_name = f"{str(name_ph_trg)}{self.tuple_sufix[ind]}"

            if not Path(new_name).exists():
                return new_name
            ind += 1

    def clean_short_name(self, short_name_photo: str):
        """remove sufix like (copy), (another copy), (3rd copy) ..."""
        for sufix in self.tuple_sufix:
            if short_name_photo.endswith(sufix):
                ind_last = short_name_photo.index(sufix)
                return short_name_photo[:ind_last]
        pattern = r" \([\d]+[a-z]{2} copy\)$"
        match_result = re.search(pattern, short_name_photo)
        if match_result:
            sufix=match_result[0]
            ind_last = short_name_photo.index(sufix)
            return short_name_photo[:ind_last]
        return short_name_photo
