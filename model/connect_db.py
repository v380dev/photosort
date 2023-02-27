# SQL commands to create tables
CREATE_SESSIONS = """CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    flag_last_session BOOL DEFAULT FALSE,
                    flag_last_photo INT DEFAULT 0
                    );"""

CREATE_PRESCRIPTIONS = """CREATE TABLE IF NOT EXISTS prescriptions (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE);"""

CREATE_FOLDERS ="""CREATE TABLE IF NOT EXISTS folders (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    id_session INTEGER NOT NULL,
                    id_prescription INTEGER NOT NULL,
                    UNIQUE (name, id_session)  ON CONFLICT ABORT
                    FOREIGN KEY (id_session) REFERENCES sessions(id) ON DELETE CASCADE,
                    FOREIGN KEY (id_prescription) REFERENCES prescriptions(id) ON DELETE CASCADE);"""

CREATE_PHOTOS = """CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    id_source_folder INTEGER NOT NULL,
                    FOREIGN KEY (id_source_folder) REFERENCES folders(id) ON DELETE CASCADE);"""

CREATE_PHOTO_TARGET_FOLDER = """CREATE TABLE IF NOT EXISTS photo_target_folder (
                    id INTEGER PRIMARY KEY,
                    id_photo INTEGER,
                    id_folder INTEGER,
                    CONSTRAINT fk_photo
                    FOREIGN KEY (id_photo) REFERENCES photos(id) ON DELETE CASCADE,
                    CONSTRAINT fk_folder
                    FOREIGN KEY (id_folder) REFERENCES folders(id) ON DELETE CASCADE);"""

FILL_PRESCRIPTIONS = """INSERT INTO prescriptions (id, name) VALUES (1, "source"), (2, "target")"""


# SQL commands to add data
ADD_SESSION = """INSERT INTO sessions(name, flag_last_session) VALUES (?, TRUE);"""
# use before ADD_SESSION

ADD_SOURCE_FOLDER = """INSERT INTO folders (name, id_session, id_prescription) VALUES (?, ?, 1);"""
ADD_PHOTO = """INSERT INTO photos (name, id_source_folder) VALUES (?, ?);"""
ADD_TARGET_FOLDER = """INSERT INTO folders (name, id_session, id_prescription) VALUES (?, ?, 2);"""

# SQL commands to fixing selections
SELECT_TARGET = """INSERT INTO photo_target_folder (id_photo, id_folder) VALUES (?, ?);"""

DESELECT_TARGET = """DELETE FROM photo_target_folder WHERE id_photo=? AND id_folder=?;"""

# SQL commands getters
GET_ALL_SESSIONS = """SELECT id, name FROM sessions"""
GET_LAST_SESSION = """SELECT id, name FROM sessions WHERE flag_last_session=TRUE"""
GET_ANY_SESSION = """SELECT id, name FROM sessions LIMIT 1"""
EXISTS_ANY_SESSION_WITHOUT_FLAG = """SELECT EXISTS(SELECT 1 FROM sessions WHERE flag_last_session=0);"""
EXISTS_SESSION_WITH_FLAG = """SELECT EXISTS(SELECT 1 FROM sessions WHERE flag_last_session=1);"""
EXISTS_FOLDER_LIKE_SOUCE = """SELECT EXISTS(SELECT 1 FROM folders WHERE id_prescription=1 AND name=?);"""

GET_SESSION_ID_BY_NAME = """SELECT id FROM sessions WHERE name = ?;"""
GET_ALL_SOURCE_ON_SESSION = """SELECT f.id, f.name FROM folders AS f
                    JOIN prescriptions AS pr
                    ON f.id_prescription=pr.id
                    WHERE pr.id=1 AND f.id_session=?;"""
GET_ALL_TARGETS_ON_SESSION = """SELECT f.id, f.name FROM folders AS f
                    JOIN prescriptions AS pr
                    ON f.id_prescription=pr.id
                    WHERE pr.id=2 AND f.id_session=?;"""

SET_FLAG_SESSION_BY_ID = """UPDATE sessions SET flag_last_session=TRUE WHERE id =?;"""
CANCEL_SESSION_FLAGS = """UPDATE sessions SET flag_last_session=FALSE;"""
GET_ID_PHOTOS_IN_TARGET = """SELECT id_photo FROM photo_target_folder WHERE id_folder=?"""

GET_PHOTO_BY_NAME = """SELECT id FROM photos WHERE name = ?;"""
GET_LAST_PHOTO_CURRENT_SESSION = """SELECT flag_last_photo FROM sessions WHERE flag_last_session=1"""

SET_FLAG_PHOTO_BY_ID = """UPDATE sessions SET flag_last_photo=? WHERE flag_last_session=1;"""

GET_ID_TARGETS_BY_PHOTO_ID = """SELECT trg.id_folder FROM photo_target_folder AS trg
                    JOIN folders AS f ON trg.id_folder=f.id
                    JOIN sessions AS s ON f.id_session=s.id
                    WHERE trg.id_photo=? AND s.flag_last_session=1"""
GET_NAME_TARGETS_BY_PHOTO_ID = """SELECT f.name FROM folders AS f 
                    JOIN photo_target_folder AS trg ON f.id=trg.id_folder
                    JOIN sessions AS s ON f.id_session=s.id
                    WHERE trg.id_photo=? AND s.flag_last_session=1"""
GET_ID_TARGET_BY_NAME = """SELECT id FROM folders WHERE id_prescription=2 AND name=? AND id_session=?"""
GET_ID_SOURCE_BY_NAME = """SELECT id FROM folders WHERE id_prescription=1 AND name=? AND id_session=?"""

# SQL commands to remove data
# will cascade delete all related data
DELETE_SESSION_BY_ID = """DELETE FROM sessions WHERE id=?"""
# cascade will also delete from the table photo_target_folder
DELETE_TARGET_IN_SESSION_BY_NAME = """DELETE FROM folders WHERE id_prescription=2  AND name=? AND id_session=?"""
DELETE_SOURCE_IN_SESSION_BY_NAME = """DELETE FROM folders WHERE id_prescription=1 AND name=? AND id_session=?"""
DELETE_PHOTO_BY_NAME = """DELETE FROM photos WHERE name=?"""

RENAME_TARGET_FOLDER = """UPDATE folders SET name = ? WHERE id_prescription=2 AND id_session=? AND id = ?"""
RENAME_SESSION = """UPDATE sessions SET name = ? WHERE name=?;"""


import sqlite3
from pathlib import Path

from model.exceptions_photosort import SourceExists


class SqlConnector:
    def __init__(self, db_name):
        # name_db = Path(__file__).parent.resolve().joinpath(Path(db_name))
        # db_name = Path(__file__).parent.joinpath(Path(db_name)).resolve()
        db_name = Path.cwd().joinpath(Path(db_name)).resolve()
        # print("full db=", db_name)
        if not self._check_is_exists(db_name):
            self._create_db(db_name)
        # self.connect = sqlite3.connect(db_name)
        self.connect = sqlite3.connect(db_name)
        self.connect.execute('PRAGMA foreign_keys=ON').close()


    def _check_is_exists(self, db_name) -> bool:
        return Path(db_name).exists()

    def _create_db(self, db_name):
        connect = sqlite3.connect(db_name)
        cursor = connect.cursor()
        cursor.execute(CREATE_SESSIONS)
        cursor.execute(CREATE_PRESCRIPTIONS)
        cursor.execute(CREATE_FOLDERS)
        cursor.execute(CREATE_PHOTOS)
        cursor.execute(CREATE_PHOTO_TARGET_FOLDER)
        cursor.execute(FILL_PRESCRIPTIONS)
        connect.commit()
        connect.close()


    def create_new_session(self, name_session) -> int:
        print("---def create_new_session(self, name_session) -> int:---", name_session)
        with self.connect as connect:
            connect.execute(CANCEL_SESSION_FLAGS)
            connect.execute(ADD_SESSION, (name_session,))
            cursor = connect.execute(GET_SESSION_ID_BY_NAME, (name_session,))
            connect.commit()
        return int(list(id[0] for id in cursor)[0])


    def add_source_folder_to_session(self, name_source: str, id_session: int) -> int:
        """it is forbidden to add an already existing resource"""
        with self.connect as connect:
            cursor = connect.execute(EXISTS_FOLDER_LIKE_SOUCE, (name_source,))
            if cursor.fetchone()[0]:
                raise SourceExists(name_source)
            else:
                connect.execute(ADD_SOURCE_FOLDER, (name_source, id_session))
                cursor = connect.execute(GET_ID_SOURCE_BY_NAME, (name_source, id_session))
                connect.commit()
            return int(list(id[0] for id in cursor)[0])


    def get_all_sessions(self) -> dict:
        """{id:'name_session', ...}"""
        dict_sessions = {}
        with self.connect as connect:
            cursor = connect.execute(GET_ALL_SESSIONS)
            for session in cursor.fetchall():
                dict_sessions[session[0]]=session[1]
            return dict_sessions


    def get_all_source_folders_from_session(self, id_session: int) -> list:
        """return list of dictionaries:
        [ {'id_source': _ , 'name_source': _ }, ... ]"""
        with self.connect as connect:
            connect.execute(CANCEL_SESSION_FLAGS)
            connect.execute(SET_FLAG_SESSION_BY_ID, (id_session,))
            cursor = connect.execute(GET_ALL_SOURCE_ON_SESSION, (id_session, ))
            connect.commit()
            return list({'id_source':source[0], 'name_source':source[1]} for source in cursor)


    def get_id_name_last_session(self) -> dict:
        """return dict:
        {'id_session': _ , 'name_session': _ }"""
        with self.connect as connect:
            cursor = connect.execute(GET_LAST_SESSION)
            return list({'id_session':session[0], 'name_session':session[1]} for session in cursor)[0]


    def exists_session_flag(self) -> bool:
        with self.connect as connect:
            cursor = connect.execute(EXISTS_SESSION_WITH_FLAG)
            result = cursor.fetchone()[0]
            if result==1:
                return True
            return False


    def exists_any_session(self) -> bool:
        with self.connect as connect:
            cursor = connect.execute(EXISTS_ANY_SESSION_WITHOUT_FLAG)
            result = cursor.fetchone()[0]
            if result==1:
                return True
            return False


    def get_any_session(self):
        """return dict:
        {'id_session': _ , 'name_session': _ }"""
        with self.connect as connect:
            cursor = connect.execute(GET_ANY_SESSION)
            return list({'id_session':session[0], 'name_session':session[1]} for session in cursor)[0]


    def update_actuals_photo(self, actuals_photos) -> list:
        """
        required input [{'name_photo': _, 'id_source': _},...]
        return [{'id_photo': _, 'name_photo': _, 'flag_photo': _ }]
        """
        list_photos = []
        with self.connect as connect:
            for photo_source in actuals_photos:
                cursor = connect.execute(GET_LAST_PHOTO_CURRENT_SESSION)
                id_last_photo = cursor.fetchone()[0]
                cursor = connect.execute(GET_PHOTO_BY_NAME, (photo_source['name_photo'],))
                photo = cursor.fetchone()
                if not photo:
                    connect.execute(ADD_PHOTO, (photo_source['name_photo'], photo_source['id_source']))
                    cursor = connect.execute(GET_PHOTO_BY_NAME, (photo_source['name_photo'],))
                    photo = cursor.fetchone()
                flag_photo = 0
                if photo[0] == id_last_photo:
                    flag_photo = 1
                list_photos.append({'id_photo': photo[0],
                                    'name_photo': photo_source['name_photo'],
                                    'flag_photo': flag_photo},
                                   )
                flag_photo = 0
            connect.commit()
        return list_photos


    def get_targets_in_session(self, id_session):
        """return [{'id_target': _, 'name_target': _}, ... ]"""
        targets = []
        with self.connect as connect:
            cursor = connect.execute(GET_ALL_TARGETS_ON_SESSION, (id_session, ))
            sql_answer = cursor.fetchall()
            if len(sql_answer)>0:
                targets = list({'id_target': trg[0], 'name_target': trg[1]} for trg in sql_answer)
        return targets


    def get_id_photos_in_target(self, id_target):
        id_photos = []
        with self.connect as connect:
            cursor = connect.execute(GET_ID_PHOTOS_IN_TARGET, (id_target,))
            result = cursor.fetchall()
            if len(result)>0:
                id_photos = list(i[0] for i in result)
        return id_photos


    def update_flag_session(self, id_session):
        with self.connect as connect:
            connect.execute(CANCEL_SESSION_FLAGS)
            connect.execute(SET_FLAG_SESSION_BY_ID, (id_session,))
            connect.commit()


    def update_flag_photo(self, id_photo: int):
        with self.connect as connect:
            connect.execute(SET_FLAG_PHOTO_BY_ID, (id_photo,))
            connect.commit()


    def get_id_session_by_name(self, name_session: str) -> int:
        with self.connect as connect:
            cursor = connect.execute(GET_SESSION_ID_BY_NAME, (name_session,))
        return int(cursor.fetchone()[0])


    def deselect_target(self, id_photo, id_target):
        with self.connect as connect:
            connect.execute(DESELECT_TARGET, (id_photo, id_target))
            connect.commit()


    def select_target(self, id_photo, id_target):
        with self.connect as connect:
            connect.execute(SELECT_TARGET, (id_photo, id_target))
            connect.commit()


    def get_targets_id_by_photo(self, id_photo: int) -> list:
        with self.connect as connect:
            cursor = connect.execute(GET_ID_TARGETS_BY_PHOTO_ID, (id_photo,))
        return list(id[0] for id in cursor.fetchall())

    def get_targets_name_by_photo(self, id_photo: int) -> list:
        with self.connect as connect:
            cursor = connect.execute(GET_NAME_TARGETS_BY_PHOTO_ID, (id_photo,))
        return list(id[0] for id in cursor.fetchall())


    def delete_source(self, name_source: str, id_session: int):
        with self.connect as connect:
            connect.execute(DELETE_SOURCE_IN_SESSION_BY_NAME, (name_source, id_session))
            connect.commit()


    def add_target_folder_to_session(self, name_target_folder, id_session):
        with self.connect as connect:
            connect.execute(ADD_TARGET_FOLDER, (name_target_folder, id_session))
            cursor = connect.execute(GET_ID_TARGET_BY_NAME, (name_target_folder, id_session))
            connect.commit()
        return int(list(id[0] for id in cursor)[0])


    def delete_target(self, name_target, id_session):
        with self.connect as connect:
            connect.execute(DELETE_TARGET_IN_SESSION_BY_NAME, (name_target, id_session))
            connect.commit()


    def delete_session_by_id(self, id_session):
        with self.connect as connect:
            connect.execute(DELETE_SESSION_BY_ID, (id_session,))
            connect.commit()


    def rename_session(self, new_name, last_name):
        with self.connect as connect:
            connect.execute(RENAME_SESSION, (new_name, last_name))
            connect.commit()


    def delete_photo_by_name(self, name_photo):
        with self.connect as connect:
            connect.execute(DELETE_PHOTO_BY_NAME, (name_photo,))
            connect.commit()
