from model.dto import Photo

class Pull:
    def __init__(self, photos: list[Photo], last_photo :Photo=None):
        self._photos = photos
        self._current_index = self._get_current_index(self._photos)

    def _get_current_index(self, photos: list[Photo]) -> int:
        ind = 0
        for ph in photos:
            if ph.flag_last:
                return ind
            ind += 1
        return 0

    def get_current_photo(self):
        if len(self._photos):
            return self._photos[self._current_index]
        else:
            return Photo(0,"None")

    def get_next_photo(self):
        self._photos[self._current_index].flag_last = False
        self._current_index += 1
        if self._current_index > len(self._photos)-1:
            self._current_index = 0
        self._photos[self._current_index].flag_last = True
        return self._photos[self._current_index]

    def get_previous_photo(self):
        self._photos[self._current_index].flag_last = False
        self._current_index -= 1
        if self._current_index < 0:
            self._current_index = len(self._photos) - 1
        self._photos[self._current_index].flag_last = True
        return self._photos[self._current_index]

    def get_photos(self):
        pass
