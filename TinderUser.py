import json
import re
import requests

POPULAR_USER = 'sprinkle'
USER_WHO_LIKE_YOU = 'promoted_ml'


class TinderUser:
    def __init__(self, userData):
        self._userData = userData

    @property
    def userDetails(self):
        return self._userData['user']

    @property
    def bio(self):
        return self.userDetails['bio']

    @property
    def jobs(self):
        return self.userDetails['jobs']

    @property
    def name(self):
        return self.userDetails['name']

    @property
    def s_number(self):
        return self._userData['s_number']

    @property
    def id(self):
        return self.userDetails['_id']

    @property
    def user_type(self):
        return self._userData['rec_type']

    @property
    def experiment_info(self):
        return 'experiment_info' in self.userDetails and self.userDetails['experiment_info']

    def user_has_keywords(self, keyword):
        if keyword == None:
            return False

        data_to_check = f'{self.bio} {self.jobs and self.jobs} {self.experiment_info}'
        test = re.search(keyword, data_to_check, flags=re.IGNORECASE)
        return test and test.group()

    def did_user_like_you(self):
        return self.user_type == USER_WHO_LIKE_YOU

    def is_popular_user(self):
        return self.user_type == POPULAR_USER

    def popular_user_log(self):
        return f'\nSwiping right with popular user: {self.name}\n{self.bio}\n{self.jobs}'

    def user_who_like_you_log(self):
        return f'\nSwiping right with someone who likes you: {self.name}\n{self.bio}\n{self.jobs}'

    def like_user_with_keyword_log(self):
        return f'\nSwiping user with matched keywords: {self.name}\n{self.bio}\n{self.jobs}'

    def __str__(self):
        return str(self.__class__) + ": " + json.dumps(self.__dict__, indent=2)
