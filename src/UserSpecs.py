import os

FILE_PATH = 'userspecs.txt'


class UserSpecs:
    def __init__(self):
        if(os.path.exists(FILE_PATH)):
            file = open(FILE_PATH, 'r')
        else:
            file = open(FILE_PATH, 'a+')

        self._file = file
        if(file):
            file_dict = dict({})

            if(os.path.getsize(FILE_PATH) == 0):
                self._file_dict = file_dict
                return

            for line in file:
                [key, value] = line.split(':')
                file_dict[key] = value.replace('\n', '').strip()
            self._file_dict = file_dict

    @property
    def file(self):
        return self._file

    @property
    def file_dict(self):
        return self._file_dict or dict({})

    @property
    def user_token_key(self):
        return self.file_dict['token'] if 'token' in self._file_dict else ''

    @property
    def keyword(self):
        return self.file_dict['keyword'] if 'keyword' in self._file_dict else 'example|second traits|last'

    @property
    def time_to_run(self):
        return self.file_dict['time'] if 'time' in self._file_dict else 1

    @property
    def swipe_liked_user(self):
        return self.file_dict['swipeUserLike'] == 'True' if 'swipeUserLike' in self._file_dict else True

    @property
    def swipe_popular_user(self):
        return self.file_dict['swipePopUser'] == 'True'if 'swipePopUser' in self._file_dict else True
