from pathlib import Path

from model.pull_photo import Pull
from model.dto import Photo, Session, Source, Target
from model.connect_db import SqlConnector
from model.move_photo import Mover


class Service:
    def __init__(self,
                 name_default_session: str,
                 sql_connect: SqlConnector,
                 mover: Mover,
                 pull=None,
                 ):
        self.name_default_session = name_default_session
        self._sql_connect = sql_connect
        self._session = self._get_session()
        self.mover = mover
        self._pull = Pull(self._session.get_photos())


    def get_current_link_photo(self) -> str:
        return self._get_current_photo().name

    def get_next_link_photo(self) -> str:
        return self._get_next_photo().name

    def get_previous_link_photo(self) -> str:
        return self._get_previous_photo().name

    def get_short_targets_dict_on_session(self) -> list[dict[int, str]]:
        """[{'id': int, 'name': str(name last in path),}, ...]"""
        # session updated to have actual targets
        self._session = self._get_session(self._session.name)
        return list({'id':target.id, 'name': Path(target.name).name} for target in self._session.targets)

    def get_full_targets_dict_on_session(self) -> list[dict[int, str]]:
        """[{'id': int, 'name': str(name last in path),}, ...]"""
        # session updated to have actual targets
        self._session = self._get_session(self._session.name)
        return list({'id':target.id, 'name': target.name} for target in self._session.targets)


    def get_targets_on_current_photo(self):
        return self._sql_connect.get_targets_id_by_photo(self._get_current_photo().id)

    def get_targets_name_by_photo_id(self, id_photo):
        return self._sql_connect.get_targets_name_by_photo(id_photo)

    def get_current_session_id(self) -> int:
        return self._session.id


    def get_current_session_name(self):
        return self._session.name


    def _get_next_photo(self):
        photo = self._pull.get_next_photo()
        self._sql_connect.update_flag_photo(photo.id)
        return photo

    def _get_previous_photo(self):
        photo = self._pull.get_previous_photo()
        self._sql_connect.update_flag_photo(photo.id)
        return photo

    def _get_current_photo(self):
        return self._pull.get_current_photo()


    def _search_actual_photos_by_source(self, folder: Source) -> list[Photo]:
        """finds the files that are in the source-folder at the moment"""
        list_actuals = []
        current_src = Path(folder.name).iterdir()
        for file in current_src:
            if file.is_file():
                list_actuals.append(Photo(name = str(file)))
        return list_actuals


    def _update_photos_dto_in_db(self, photos: list[Photo], id_source: int) -> list:
        """transforms data for sql sources
        to sources: [{'name_photo': _, 'id_source': _},...]
        from: [{'id_photo': _, 'name_photo': _, 'flag_photo': _ }]"""
        list_for_sql = list({ 'name_photo': ph.name, 'id_source': id_source} for ph in photos)
        answer_db = self._sql_connect.update_actuals_photo(list_for_sql)
        return list(Photo(id=ph['id_photo'], name=ph['name_photo'], flag_last=ph['flag_photo']) for ph in answer_db)

    def _get_session(self, name_session: str=None):
        """If the name_session is not passed, the last session will be loaded"""
        if  name_session:
            id_session = self._sql_connect.get_id_session_by_name(name_session)
        else:
            if self._sql_connect.exists_session_flag():
                id_session, name_session =  self._sql_connect.get_id_name_last_session().values()
            else:
                if self._sql_connect.exists_any_session():
                    id_session, name_session = self._sql_connect.get_any_session().values()
                else:
                    name_session = self.name_session = self.create_default_session()
                    id_session = self.get_id_session_by_name(name_session)
        session = Session(id=id_session,
                          name=name_session,
                          sources=self.get_sources_by_session_id(id_session),
                          targets=self._get_targets_by_session_id(id_session),
                          flag_last=True,
                          )
        self._sql_connect.update_flag_session(session.id)
        return session


    def get_sources_by_session_id(self, id_session: int) -> list[Source]:
        src_sql = self._sql_connect.get_all_source_folders_from_session(id_session)
        sources = list(Source(id=src['id_source'], name=src['name_source']) for src in src_sql)
        for src in sources:
            src.photos = self._update_photos_dto_in_db(self._search_actual_photos_by_source(src), src.id)
        return sources

    def _get_targets_by_session_id(self, id_session: int) -> list[Target]:
        sql_trg = self._sql_connect.get_targets_in_session(id_session)
        targets = list(Target( id=trg['id_target'], name=trg['name_target']) for trg in sql_trg)
        for trg in targets:
            trg.id_photos = self._sql_connect.get_id_photos_in_target(trg.id)
        return targets

    def deselect_target(self, id_target: int):
        id_photo = self._get_current_photo().id
        self._sql_connect.deselect_target(id_photo, id_target)

    def select_target(self, id_target: int):
        id_photo = self._get_current_photo().id
        self._sql_connect.select_target(id_photo, id_target)
        pass

    def add_new_source_folder(self, new_source_folder: str):
        self._sql_connect.add_source_folder_to_session(new_source_folder, self._session.id)
        self.update_service()
        # self._session.was_updated = True

    def delete_source(self, name_source):
        self._sql_connect.delete_source(name_source, self._session.id)
        self.update_service()

    def add_new_target_folder(self, new_target_folder: str):
        self._sql_connect.add_target_folder_to_session(new_target_folder, self._session.id)
        self._session = self._get_session()

    def delete_target(self, name_target):
        self._sql_connect.delete_target(name_target, self._session.id)
        pass

    def load_session_by_name(self, name_session :str=None):
        if name_session:
            self._session = self._get_session(name_session)
        else:
            self._session = self._get_session()
        self._pull = Pull(self._session.get_photos())

    def _load_session_if_dont_have_flag(self):
        name_session: str
        if dict_sessions := self.get_dict_sessions():
            name_session = list(n for n in dict_sessions.values())[0]
            self._sql_connect.update_flag_session(self._sql_connect.get_id_session_by_name(name_session))
        else:
            name_session = self.create_default_session()
        self._session = self._get_session(name_session)
        self._pull = Pull(self._session.get_photos())

    def create_default_session(self) -> str:
        """return name generated default session"""
        self._sql_connect.create_new_session(self.name_default_session)
        return self.name_default_session

    def create_new_session(self, name_session):
        self._sql_connect.create_new_session(name_session)
        self.load_session_by_name(name_session)

    def get_dict_sessions(self) -> dict:
        """{id:'name_session', ...}"""
        return self._sql_connect.get_all_sessions()

    def delete_session_by_id(self, id_session):
        self._sql_connect.delete_session_by_id(id_session)


    def get_id_session_by_name(self, name_session):
        return self._sql_connect.get_id_session_by_name(name_session)

    def update_service(self):
        self._session = self._get_session()
        self._pull = Pull(self._session.get_photos())

    def rename_session(self, new_name, last_name):
        self._sql_connect.rename_session(new_name, last_name)

    def rename_current_session(self, new_name):
        self.rename_session(new_name, self._session.name)

    def copy_photo(self, name_photo, name_target, new_name=None):
        self.mover.copy_one_to_one(name_photo, name_target, new_name)

    def copy_photo_without_exception_for_replace(self, name_photo, name_target):
        self.mover.copy_one_to_one_without_exception_for_replace(name_photo, name_target)

    def delete_photo(self, name_photo: str):
        self.mover.delete_photo_from_source(name_photo)
        self._sql_connect.delete_photo_by_name(name_photo)
        self.update_service()

    def get_dict_photos_in_session(self) -> list:
        """[{'id': _, 'name': _}]"""
        return list({'id': ph.id, 'name': ph.name} for ph in self._session.get_photos())

    def copy_photos_skip(self):
        pass

    def get_photo_by_name(self, name_photo) -> Photo:
        return list(ph for ph in self._session.get_photos() if ph.name == name_photo)[0]

    def generate_new_name(self, name_photo, name_target):
        return self.mover.generate_new_name(name_photo, name_target)

