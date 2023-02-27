class Photo:
    def __init__(self, name: str, id: int=None, flag_last: bool=False):
        self.id = id
        self.name = name
        self.flag_last = flag_last

    def __str__(self):
        return f" Photo id={self.id}, name={self.name}, flag={self.flag_last} "


class _Folder:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __str__(self):
        return f" Folder id={self.id}, name={self.name} "

class Source(_Folder):
    def __init__(self, id: int, name: str, photos: list=list[Photo]):
        super().__init__(id=id, name=name)
        self.photos = photos

    def __str__(self):
        return f"{super().__str__()}, photos={str(list(str(ph) for ph in self.photos))}"

class Target(_Folder):
    def __init__(self, id: int, name: str, id_photos: list = list[int]):
        super().__init__(id=id, name=name)
        self.id_photos = id_photos

    def __str__(self):
        return f"{super().__str__()}, id_photos={str(self.id_photos)}"


class Session:
    def __init__(self, id: int, name: str, sources: list[Source]=None, targets: list[Target]=None, flag_last: bool=False):
        self.id = id
        self.name = name
        self.sources = sources
        self.targets = targets
        self.flag_last = flag_last

    def __str__(self):
        return f"Session:\nid={self.id}\nname={self.name}\nsources={str(list(str(src) for src in self.sources))}\ntargets={str(list(str(trg) for trg in self.targets))}\nflag={self.flag_last} "

    def get_photos(self) -> list[Photo]:
        photos = []
        for src in self.sources:
            photos.extend(src.photos)
        return photos
