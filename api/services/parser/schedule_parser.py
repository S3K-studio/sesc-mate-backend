import requests
from typing import NoReturn, Dict, List, Set


class LessonJson:
    """Representation of the lesson"""
    number: int
    subject: str
    subgroup: int
    auditory: int
    teacher: str
    replaced: bool

    def __init__(self, number: int, subject: str, subgroup: int, auditory: int, teacher: str, replaced: bool):
        """Initializing the lesson"""
        self.number = number
        self.subject = subject
        self.subgroup = subgroup
        self.auditory = auditory
        self.teacher = teacher
        self.replaced = replaced

    def serialize(self):
        """Serializing the lesson"""
        return {
            "number": self.number,
            "subject": self.subject,
            "subgroup": self.subgroup,
            "auditory": self.auditory,
            "teacher": self.teacher,
            "replaced": self.replaced
        }


class ScheduleParser:
    """Class for getting schedule from SESC URFU server"""

    def __init__(self, json: Dict):
        """Initializing an object"""
        self.__json = json  # JSON from SESC UrFU server
        self.__lessons_list: List[LessonJson] = []  # List for lessons for the day
        self.__difference = []  # List for schedule changes

    def _parse_api(self) -> Dict:
        """Getting json from SESC UrFU server"""
        return self.__json

    def _analyze_lessons(self) -> NoReturn:
        """Очищаем JSON для последующей обработки"""
        response: Dict = self._parse_api()
        # Getting schedule changes
        self.__difference: Dict[List] = response["diffs"]
        # Getting raw list of lessons for the day
        raw_lessons: Dict[List] = response["lessons"]

        # List filling with lesson objects
        self.__forming_lessons_list(raw_lessons)

    def _sort_lessons(self) -> NoReturn:
        """Sorting lessons by lesson number"""
        try:
            self.__lessons_list.sort(key=lambda lesson: lesson.subgroup)
            self.__lessons_list.sort(key=lambda lesson: lesson.number)
        except:
            print("Error while sorting lessons")

    def __forming_lessons_list(self, raw_lessons: List, is_replaced: bool = False) -> NoReturn:
        """Function for lessons list forming
        :param raw_lessons lessons that should be updated in the main list of lessons
        :param is_replaced if lessons are replaced
        """
        for index in range(len(raw_lessons)):
            # Forming lesson object
            lesson: LessonJson = LessonJson(
                number=raw_lessons[index]["number"],
                subject=raw_lessons[index]["subject"],
                subgroup=raw_lessons[index]["subgroup"],
                auditory=raw_lessons[index]["auditory"],
                teacher=raw_lessons[index]["teacher"],
                replaced=is_replaced
            )
            # Adding lesson to lessons list
            self.__lessons_list.append(lesson)

    def _check_for_difference(self) -> NoReturn:
        """Checking difference in schedule"""
        self.__forming_lessons_list(self.__difference, True)

        diffs_info: Dict[int, List] = {}  # Dict for lessons info {lesson number: [subgroups to change]}
        diffs_numbers: List[int] = list(set(map(lambda x: x["number"], self.__difference)))

        # A list of lessons numbers, that were changed
        for index in range(len(diffs_numbers)):
            diffs_info[diffs_numbers[index]] = []

        # Filling diffs_info with information about schedule changes
        for index in range(len(self.__difference)):
            diffs_info[self.__difference[index]["number"]].append(self.__difference[index]["subgroup"])

        self.__lessons_list = list(
            set(self.__lessons_list) -
            set(filter(
                lambda x: x.number in diffs_info.keys()
                          and not x.replaced
                          and (x.subgroup == 0 or diffs_info[x.number][0] == 0 or (x.subgroup in diffs_info[x.number])),
                self.__lessons_list
            ))
        )

    def _delete_empty_lessons(self):
        """Deleting empty lessons from lessons list"""
        self.__lessons_list = list(filter(
            lambda lesson: lesson.subject != "Нет",
            self.__lessons_list
        ))

    def _serialize_json(self) -> List:
        """Serializing the schedule"""
        # Analyzing, checking for difference and sorting lessons list
        self._analyze_lessons()
        self._check_for_difference()
        self._delete_empty_lessons()
        self._sort_lessons()

        # Forming final JSON
        final_json: List = []
        # Number of lessons. This number is required for the loop
        lessons_number: List[int] = list(set([lesson.number for lesson in self.__lessons_list]))
        # Serializing lessons, forming final JSON
        for index in lessons_number:
            # Filtering lessons by current lesson number. Current lesson number = current loop iteration
            lesson: List[LessonJson] = list(filter(lambda lesson: lesson.number == index, self.__lessons_list))
            # Filtering lessons by subgroups
            subgroups_lesson: List[LessonJson] = list(filter(lambda lesson: lesson.subgroup != 0, lesson))
            if subgroups_lesson:
                # If there are lessons in subgroups, adding a list with subgroups lessons
                final_json.append(list(map(
                    lambda lesson: lesson.serialize(), subgroups_lesson)
                ))
            else:
                if lesson:
                    # If there are no subgroups lessons
                    final_json.append(
                        lesson[0].serialize()
                    )
        return final_json

    def get_lessons(self) -> Dict[str, List]:
        """Getting schedule for the day"""
        return self._serialize_json()


"""Block for tests"""


def get_schedule(day, group):
    return requests.get("https://lyceum.urfu.ru/?type=11&scheduleType=group&weekday={0}&group={1}".format(
        day, group
    )).json()


if __name__ == "__main__":
    a = ScheduleParser(get_schedule(4, 11))
    print(a.get_lessons())
