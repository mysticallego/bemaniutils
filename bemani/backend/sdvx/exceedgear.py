# vim: set fileencoding=utf-8
from typing import Any, Dict, List, Optional, Tuple
from typing_extensions import Final
from bemani.backend.ess import EventLogHandler
from bemani.backend.sdvx.base import SoundVoltexBase
from bemani.common import ID, Profile, VersionConstants, Time, BroadcastConstants
from bemani.data import UserID, Score
from bemani.protocol import Node


class SoundVoltexExceedGear(
    EventLogHandler,
    SoundVoltexBase,
):
    name: str = "SOUND VOLTEX VI EXCEED GEAR"
    version: int = VersionConstants.SDVX_EXCEED_GEAR

    GAME_LIMITED_LOCKED: Final[int] = 1
    GAME_LIMITED_UNLOCKABLE: Final[int] = 2
    GAME_LIMITED_UNLOCKED: Final[int] = 3

    GAME_CURRENCY_PACKETS: Final[int] = 0
    GAME_CURRENCY_BLOCKS: Final[int] = 1

    GAME_CATALOG_TYPE_SONG: Final[int] = 0
    GAME_CATALOG_TYPE_APPEAL_CARD: Final[int] = 1
    GAME_CATALOG_TYPE_CREW: Final[int] = 4

    GAME_CLEAR_TYPE_NO_PLAY: Final[int] = 0
    GAME_CLEAR_TYPE_FAILED: Final[int] = 1
    GAME_CLEAR_TYPE_CLEAR: Final[int] = 2
    GAME_CLEAR_TYPE_HARD_CLEAR: Final[int] = 3
    GAME_CLEAR_TYPE_ULTIMATE_CHAIN: Final[int] = 4
    GAME_CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: Final[int] = 5

    GAME_GRADE_NO_PLAY: Final[int] = 0
    GAME_GRADE_D: Final[int] = 1
    GAME_GRADE_C: Final[int] = 2
    GAME_GRADE_B: Final[int] = 3
    GAME_GRADE_A: Final[int] = 4
    GAME_GRADE_A_PLUS: Final[int] = 5
    GAME_GRADE_AA: Final[int] = 6
    GAME_GRADE_AA_PLUS: Final[int] = 7
    GAME_GRADE_AAA: Final[int] = 8
    GAME_GRADE_AAA_PLUS: Final[int] = 9
    GAME_GRADE_S: Final[int] = 10

    GAME_SKILL_NAME_ID_LV_01: Final[int] = 1
    GAME_SKILL_NAME_ID_LV_02: Final[int] = 2
    GAME_SKILL_NAME_ID_LV_03: Final[int] = 3
    GAME_SKILL_NAME_ID_LV_04: Final[int] = 4
    GAME_SKILL_NAME_ID_LV_05: Final[int] = 5
    GAME_SKILL_NAME_ID_LV_06: Final[int] = 6
    GAME_SKILL_NAME_ID_LV_07: Final[int] = 7
    GAME_SKILL_NAME_ID_LV_08: Final[int] = 8
    GAME_SKILL_NAME_ID_LV_09: Final[int] = 9
    GAME_SKILL_NAME_ID_LV_10: Final[int] = 10
    GAME_SKILL_NAME_ID_LV_11: Final[int] = 11
    GAME_SKILL_NAME_ID_LV_INF: Final[int] = 12
    GAME_SKILL_NAME_ID_BMK_2021: Final[int] = 13
    GAME_SKILL_NAME_ID_10TH_YEAR: Final[int] = 14

    extra_services: List[str] = [
        "userdata",
        "userid",
        "numbering",
        "local2",
        "lobby2",
        "netlog",
        "sidmgr",
        "globby",
    ]

    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """
        Return all of our front-end modifiably settings.
        """
        return {
            "bools": [
                {
                    "name": "Disable Online Matching",
                    "tip": "Disable online matching between games.",
                    "category": "game_config",
                    "setting": "disable_matching",
                },
                {
                    "name": "Force Song Unlock",
                    "tip": "Force unlock all songs.",
                    "category": "game_config",
                    "setting": "force_unlock_songs",
                },
                {
                    "name": "Force Appeal Card Unlock",
                    "tip": "Force unlock all appeal cards.",
                    "category": "game_config",
                    "setting": "force_unlock_cards",
                },
                {
                    "name": "Force Navigator Unlock",
                    "tip": "Force unlock all navigators.",
                    "category": "game_config",
                    "setting": "force_unlock_crew",
                },
                # {
                #     "name": "Use Information",
                #     "tip": "Enable the information section after entry.",
                #     "category": "game_config",
                #     "setting": "use_information",
                # },
                # {
                #     "name": "Use Asphyxia Gameover(???)",
                #     "tip": "Unknown",
                #     "category": "game_config",
                #     "setting": "use_asphyxia_gameover",
                # },
                {
                    "name": "Use Blasterpass",
                    "tip": "Enable Blaster Pass for VW and EG",
                    "category": "game_config",
                    "setting": "use_blasterpass",
                },
                {
                    "name": "Use New Year Special",
                    "tip": "Enable New Year Special BGM for login",
                    "category": "game_config",
                    "setting": "new_year_special",
                },
            ]
        }

    def previous_version(self) -> Optional[SoundVoltexBase]:
        return None

    def __game_to_db_clear_type(self, clear_type: int) -> int:
        return {
            self.GAME_CLEAR_TYPE_NO_PLAY: self.CLEAR_TYPE_NO_PLAY,
            self.GAME_CLEAR_TYPE_FAILED: self.CLEAR_TYPE_FAILED,
            self.GAME_CLEAR_TYPE_CLEAR: self.CLEAR_TYPE_CLEAR,
            self.GAME_CLEAR_TYPE_HARD_CLEAR: self.CLEAR_TYPE_HARD_CLEAR,
            self.GAME_CLEAR_TYPE_ULTIMATE_CHAIN: self.CLEAR_TYPE_ULTIMATE_CHAIN,
            self.GAME_CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: self.CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN,
        }[clear_type]

    def __db_to_game_clear_type(self, clear_type: int) -> int:
        return {
            self.CLEAR_TYPE_NO_PLAY: self.GAME_CLEAR_TYPE_NO_PLAY,
            self.CLEAR_TYPE_FAILED: self.GAME_CLEAR_TYPE_FAILED,
            self.CLEAR_TYPE_CLEAR: self.GAME_CLEAR_TYPE_CLEAR,
            self.CLEAR_TYPE_HARD_CLEAR: self.GAME_CLEAR_TYPE_HARD_CLEAR,
            self.CLEAR_TYPE_ULTIMATE_CHAIN: self.GAME_CLEAR_TYPE_ULTIMATE_CHAIN,
            self.CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: self.GAME_CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN,
        }[clear_type]

    def __game_to_db_grade(self, grade: int) -> int:
        return {
            self.GAME_GRADE_NO_PLAY: self.GRADE_NO_PLAY,
            self.GAME_GRADE_D: self.GRADE_D,
            self.GAME_GRADE_C: self.GRADE_C,
            self.GAME_GRADE_B: self.GRADE_B,
            self.GAME_GRADE_A: self.GRADE_A,
            self.GAME_GRADE_A_PLUS: self.GRADE_A_PLUS,
            self.GAME_GRADE_AA: self.GRADE_AA,
            self.GAME_GRADE_AA_PLUS: self.GRADE_AA_PLUS,
            self.GAME_GRADE_AAA: self.GRADE_AAA,
            self.GAME_GRADE_AAA_PLUS: self.GRADE_AAA_PLUS,
            self.GAME_GRADE_S: self.GRADE_S,
        }[grade]

    def __db_to_game_grade(self, grade: int) -> int:
        return {
            self.GRADE_NO_PLAY: self.GAME_GRADE_NO_PLAY,
            self.GRADE_D: self.GAME_GRADE_D,
            self.GRADE_C: self.GAME_GRADE_C,
            self.GRADE_B: self.GAME_GRADE_B,
            self.GRADE_A: self.GAME_GRADE_A,
            self.GRADE_A_PLUS: self.GAME_GRADE_A_PLUS,
            self.GRADE_AA: self.GAME_GRADE_AA,
            self.GRADE_AA_PLUS: self.GAME_GRADE_AA_PLUS,
            self.GRADE_AAA: self.GAME_GRADE_AAA,
            self.GRADE_AAA_PLUS: self.GAME_GRADE_AAA_PLUS,
            self.GRADE_S: self.GAME_GRADE_S,
        }[grade]

    def handle_game_sv6_exception_request(self, requset: Node) -> Node:
        return Node.void("game")

    def handle_game_sv6_lounge_request(self, requset: Node) -> Node:
        game = Node.void("game")
        # Refresh interval in seconds.
        game.add_child(Node.u32("interval", 10))
        return game

    def handle_game_sv6_entry_s_request(self, request: Node) -> Node:
        game = Node.void("game")
        # This should be created on the fly for a lobby that we're in.
        game.add_child(Node.u32("entry_id", 1))
        return game

    def handle_game_sv6_entry_e_request(self, request: Node) -> Node:
        # Lobby destroy method, eid node (u32) should be used
        # to destroy any open lobbies.
        game = Node.void("game")
        return game

    def __get_skill_analyzer_seasons(self) -> Dict[int, str]:
        return {
            1: "SKILL ANALYZER 第1回 Aコース",
            2: "SKILL ANALYZER 第1回 Bコース",
            3: "SKILL ANALYZER 第1回 Cコース",
            4: "BEMANI MASTER KOREA 2021",
            5: "SKILL ANALYZER 第2回",
            6: "10周年記念コース",
            7: "SKILL ANALYZER 第3回",
            8: "SKILL ANALYZER 第4回 Aコース",
            9: "SKILL ANALYZER 第4回 Bコース",
            10: "SKILL ANALYZER 第5回 Aコース",
            11: "SKILL ANALYZER 第5回 Bコース",
        }

    def __get_skill_analyzer_skill_levels(self) -> Dict[int, str]:
        return {
            1: "SKILL ANALYZER Level.01",
            2: "SKILL ANALYZER Level.02",
            3: "SKILL ANALYZER Level.03",
            4: "SKILL ANALYZER Level.04",
            5: "SKILL ANALYZER Level.05",
            6: "SKILL ANALYZER Level.06",
            7: "SKILL ANALYZER Level.07",
            8: "SKILL ANALYZER Level.08",
            9: "SKILL ANALYZER Level.09",
            10: "SKILL ANALYZER Level.10",
            11: "SKILL ANALYZER Level.11",
            12: "SKILL ANALYZER Level.∞",
        }

    def __get_skill_analyzer_skill_name_ids(self) -> Dict[int, int]:
        return {
            1: self.GAME_SKILL_NAME_ID_LV_01,
            2: self.GAME_SKILL_NAME_ID_LV_02,
            3: self.GAME_SKILL_NAME_ID_LV_03,
            4: self.GAME_SKILL_NAME_ID_LV_04,
            5: self.GAME_SKILL_NAME_ID_LV_05,
            6: self.GAME_SKILL_NAME_ID_LV_06,
            7: self.GAME_SKILL_NAME_ID_LV_07,
            8: self.GAME_SKILL_NAME_ID_LV_08,
            9: self.GAME_SKILL_NAME_ID_LV_09,
            10: self.GAME_SKILL_NAME_ID_LV_10,
            11: self.GAME_SKILL_NAME_ID_LV_11,
            12: self.GAME_SKILL_NAME_ID_LV_INF,
        }

    def __get_skill_analyzer_courses(self) -> List[Dict[str, Any]]:
        return [
            # Skill LV.01
            {
                "season_id": 1,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1383,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 334,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 774,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1066,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 1054,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1055,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1376,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 564,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 87,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1374,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 936,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 314,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1718,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 144,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 568,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 271,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 209,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1083,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1526,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 84,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 76,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 1441,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 274,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 569,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 1,
                "tracks": [
                    {
                        "id": 698,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 159,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 671,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            # Skill LV.02
            {
                "season_id": 1,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 74,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 771,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1125,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 768,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 948,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 755,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 34,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 932,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 945,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 1221,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 169,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 254,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 1659,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 739,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 561,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 1088,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 973,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 22,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 171,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 474,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 18,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 1057,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 865,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 721,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 2,
                "tracks": [
                    {
                        "id": 388,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1084,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 944,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            # Skill LV.03
            {
                "season_id": 1,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 784,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1126,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1075,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 401,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1320,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 485,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 1132,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1549,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 380,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 1429,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 462,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 237,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 1110,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1513,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 732,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 157,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1039,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 972,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 281,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1254,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 997,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 673,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 954,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1867,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 3,
                "tracks": [
                    {
                        "id": 854,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 321,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 512,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            # Skill LV.04
            {
                "season_id": 1,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 505,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1403,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 609,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 295,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 255,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1029,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 130,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1204,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1424,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 449,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 329,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1293,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 174,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1217,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 617,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 1395,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 238,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1342,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 417,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1572,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 539,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 461,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 538,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1510,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 4,
                "tracks": [
                    {
                        "id": 412,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 992,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1315,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            # Skill LV.05
            {
                "season_id": 1,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 630,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1598,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1475,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 1420,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1001,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1611,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 48,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 565,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1109,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 486,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 920,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1318,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 1564,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1679,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 285,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 283,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1551,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 573,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 1701,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 523,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 477,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 1300,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1697,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 476,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 5,
                "tracks": [
                    {
                        "id": 1085,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1229,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 212,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            # Skill LV.06
            {
                "season_id": 1,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1154,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1238,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 590,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1338,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 79,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1151,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1534,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1398,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1312,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1288,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 256,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1445,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 545,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1563,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 916,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1565,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1409,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 202,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1412,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1417,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1081,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1115,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1425,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 756,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 6,
                "tracks": [
                    {
                        "id": 1616,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1815,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 813,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            # Skill LV.07
            {
                "season_id": 1,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 1606,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 834,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 820,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 1047,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 982,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1042,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 962,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1560,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 357,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 1129,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1349,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1608,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 1719,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 344,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1322,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 866,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 330,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 669,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 1250,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 434,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 690,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 315,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 861,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1303,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 7,
                "tracks": [
                    {
                        "id": 411,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 990,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 514,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            # Skill LV.08
            {
                "season_id": 1,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 183,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1602,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 173,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 664,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1370,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 838,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 965,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 906,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 579,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 492,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 930,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 651,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 1410,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1761,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 63,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 399,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1166,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1305,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 460,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 772,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 891,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 484,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 905,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1539,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 8,
                "tracks": [
                    {
                        "id": 778,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1727,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1127,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            # Skill LV.09
            {
                "season_id": 1,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 1418,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 469,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1413,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 624,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1113,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1629,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 332,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 36,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1476,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 1607,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1240,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 510,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 882,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1759,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 993,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 234,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 886,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1716,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 1019,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 943,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1208,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 737,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1485,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1262,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 9,
                "tracks": [
                    {
                        "id": 96,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 976,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 801,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            # Skill LV.10
            {
                "season_id": 1,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1596,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1649,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 229,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1595,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1657,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 658,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 3,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1533,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1597,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1541,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1251,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1540,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1712,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1644,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1331,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1625,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1760,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 730,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1405,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 786,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 837,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1814,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 832,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1749,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 633,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 10,
                "tracks": [
                    {
                        "id": 1729,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 985,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 900,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                ],
            },
            # Skill LV.11
            {
                "season_id": 1,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1651,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1105,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1152,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1647,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1587,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 333,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1143,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1298,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1619,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1550,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1366,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1722,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1776,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1365,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 911,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 979,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1459,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1774,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 725,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 1201,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 654,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 11,
                "tracks": [
                    {
                        "id": 1517,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1335,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 367,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            # Skill LV.INF
            {
                "season_id": 1,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 1664,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1528,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1185,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 2,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 1363,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 692,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1270,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 5,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 1639,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1496,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1766,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 7,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 495,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1464,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1767,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 8,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 1364,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1661,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1099,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 9,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 914,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 376,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1362,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 10,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 704,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1176,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1889,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            {
                "season_id": 11,
                "skill_level": 12,
                "tracks": [
                    {
                        "id": 273,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 1581,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1888,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            # BEMANI MASTER KOREA 2021
            {
                "season_id": 4,
                "course_id": 1,
                "skill_level": 0,
                "course_name": "BEMANI MASTER KOREA 2021 ENJOY COURSE",
                "skill_name_id": self.GAME_SKILL_NAME_ID_BMK_2021,
                "tracks": [
                    {
                        "id": 1641,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1646,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 1642,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 4,
                "course_id": 2,
                "skill_level": 0,
                "course_name": "BEMANI MASTER KOREA 2021 ENTRY COURSE",
                "skill_name_id": self.GAME_SKILL_NAME_ID_BMK_2021,
                "tracks": [
                    {
                        "id": 1641,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1646,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                    {
                        "id": 1642,
                        "type": self.CHART_TYPE_MAXIMUM,
                    },
                ],
            },
            # 10TH YEAR
            {
                "season_id": 6,
                "course_id": 1,
                "skill_level": 0,
                "course_name": "10周年記念コース(梅)",
                "skill_name_id": self.GAME_SKILL_NAME_ID_10TH_YEAR,
                "tracks": [
                    {
                        "id": 247,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 611,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                    {
                        "id": 339,
                        "type": self.CHART_TYPE_NOVICE,
                    },
                ],
            },
            {
                "season_id": 6,
                "course_id": 2,
                "skill_level": 0,
                "course_name": "10周年記念コース(竹)",
                "skill_name_id": self.GAME_SKILL_NAME_ID_10TH_YEAR,
                "tracks": [
                    {
                        "id": 247,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 611,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                    {
                        "id": 339,
                        "type": self.CHART_TYPE_ADVANCED,
                    },
                ],
            },
            {
                "season_id": 6,
                "course_id": 3,
                "skill_level": 0,
                "course_name": "10周年記念コース(松)",
                "skill_name_id": self.GAME_SKILL_NAME_ID_10TH_YEAR,
                "tracks": [
                    {
                        "id": 247,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 611,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 339,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                ],
            },
            {
                "season_id": 6,
                "course_id": 4,
                "skill_level": 0,
                "course_name": "10周年記念コース(極)",
                "skill_name_id": self.GAME_SKILL_NAME_ID_10TH_YEAR,
                "tracks": [
                    {
                        "id": 793,
                        "type": self.CHART_TYPE_EXHAUST,
                    },
                    {
                        "id": 247,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                    {
                        "id": 339,
                        "type": self.CHART_TYPE_INFINITE,
                    },
                ],
            },
        ]

    def handle_game_sv6_common_request(self, request: Node) -> Node:
        game = Node.void("game")

        limited = Node.void("music_limited")
        game.add_child(limited)

        # Song unlock config
        game_config = self.get_game_config()
        if True:
            ids = set()
            songs = self.data.local.music.get_all_songs(self.game, self.version)
            for song in songs:
                if song.data.get_int("limited") in (
                        self.GAME_LIMITED_LOCKED,
                        self.GAME_LIMITED_UNLOCKABLE,
                ):
                    ids.add((song.id, song.chart))

            for (songid, chart) in ids:
                info = Node.void("info")
                limited.add_child(info)
                info.add_child(Node.s32("music_id", songid))
                info.add_child(Node.u8("music_type", chart))
                info.add_child(Node.u8("limited", self.GAME_LIMITED_UNLOCKED))

        # Event config
        event = Node.void("event")
        game.add_child(event)

        def enable_event(eid: str) -> None:
            evt = Node.void("info")
            event.add_child(evt)
            evt.add_child(Node.string("event_id", eid))

        if not game_config.get_bool("disable_matching"):
            enable_event("MATCHING_MODE")
            enable_event("MATCHING_MODE_FREE_IP")

        # enable_event("NEW_YEAR_2022\t3")
        # enable_event("ACHIEVEMENT_ENABLE")
        enable_event("VOLFORCE_ENABLE")
        enable_event("CONTINUATION")
        enable_event("TENKAICHI_MODE")
        enable_event("SERIALCODE_JAPAN")
        enable_event("DEMOGAME_PLAY")
        enable_event("KONAMI_50TH_LOGO")
        enable_event("LEVEL_LIMIT_EASING")
        enable_event("APICAGACHADRAW\t30")
        enable_event("AKANAME_ENABLE")
        enable_event("PAUSE_ONLINEUPDATE")
        # enable_event("QC_MODE")
        # enable_event("KAC_MODE")
        # enable_event("APPEAL_CARD_GEN_PRICE\t1000")
        # enable_event("APPEAL_CARD_GEN_NEW_PRICE\t2000")
        # enable_event(
        #     "APPEAL_CARD_UNLOCK\t0,20170914,0,20171014,0,20171116,0,20180201,0,20180607,0,20181206,0,20200326,0,20200611,4,10140732,6,10150431"
        # )
        enable_event("FAVORITE_APPEALCARD_MAX\t200")
        enable_event("FAVORITE_MUSIC_MAX\t200")
        enable_event("EVENTDATE_APRILFOOL")
        enable_event("OMEGA_ARS_ENABLE")
        enable_event("DISABLE_MONITOR_ID_CHECK")
        enable_event("SKILL_ANALYZER_ABLE")
        enable_event("BLASTER_ABLE")
        enable_event("STANDARD_UNLOCK_ENABLE")
        enable_event("PLAYERJUDGEADJ_ENABLE")
        # enable_event("MIXID_INPUT_ENABLE")
        enable_event("EVENTDATE_ONIGO")
        # enable_event("APRIL_GRACE")
        enable_event("EVENTDATE_GOTT")
        enable_event("GENERATOR_ABLE")
        enable_event("CREW_SELECT_ABLE")
        enable_event("PREMIUM_TIME_ENABLE")
        enable_event("OMEGA_ENABLE\t1,2,3,4,5,6,7,8,9")
        enable_event("HEXA_ENABLE\t1,2,3,4,5,6,7")
        enable_event("MEGAMIX_ENABLE")
        enable_event("VALGENE_ENABLE")
        enable_event("ARENA_ENABLE")
        # follwing is for test, if error, just delete.
        # enable_event("ARENA_ALTER_MODE_WINDOW_ENABLE")
        # enable_event("ARENA_PASS_MATCH_WINDOW_ENABLE")
        # enable_event("ARENA_VOTE_MODE_ENABLE")  # 选择是否投票
        # enable_event("ARENA_LOCAL_TO_ONLINE_ENABLE")
        # enable_event("ARENA_LOCAL_ULTIMATE_MATCH_ALWAYS")

        # Event parameters (we don't support story mode).
        extend = Node.void("extend")
        game.add_child(extend)

        # Use Information flag
        # Use Information flag
        if True:
            Title = "This is title"
            Contents = "This is contents"
            info = Node.void("info")
            extend.add_child(info)

            info.add_child(Node.u32("extend_id", 1))
            info.add_child(Node.u32("extend_type", 1))
            info.add_child(Node.s32("param_num_1", 1))
            info.add_child(Node.s32("param_num_2", Time.now()))
            info.add_child(Node.s32("param_num_3", 1))
            info.add_child(Node.s32("param_num_4", 1))
            info.add_child(Node.s32("param_num_5", 31))
            info.add_child(Node.string("param_str_1", Title))  # Title?
            info.add_child(Node.string("param_str_2", Contents))  # Content?
            info.add_child(Node.string("param_str_3", ""))
            info.add_child(Node.string("param_str_4", ""))
            info.add_child(Node.string("param_str_5", ""))

        # megamix?
        str1 = "6,75,86,87,94,115,116,117,118,120,121,122,123,124,125,126,128,134,251,253,258,259,271,272,304,344," \
               "357,358,359,360,361,362,363,364,365,366,367,368,369,370,372,373,374,375,376,377,381,437,479,495,538," \
               "542,543,546,553,581,607,625,626,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648," \
               "649,650,651,652,653,654,655,656,657,658,659,673,679,692,693,694,698,699,704,708,709,715,716,718,786," \
               "787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811," \
               "812,813,814,815,816,817,818,823,825,827,828,829,830,831,842,866,900,902,907,908,909,910,911,912,913," \
               "914,915,927,929,979,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037," \
               "1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1072,1099 "
        str2 = "1100,1101,1102,1103,1104,1105,1106,1107,1108,1117,1140,1141,1142,1143,1144,1145,1146,1147,1148,1176," \
               "1177,1178,1179,1180,1181,1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,1195,1196,1197," \
               "1198,1199,1200,1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217," \
               "1218,1220,1221,1260,1269,1270,1271,1272,1273,1274,1275,1276,1277,1278,1279,1280,1281,1282,1300,1301," \
               "1302,1329,1345,1346,1347,1348,1361,1362,1363,1364,1365,1366,1367,1368,1369,1370,1371,1372,1373,1374," \
               "1375,1376,1377,1378,1379,1380,1381,1382,1383,1384,1385,1386,1433,1434,1435,1436,1437,1459,1460,1461," \
               "1462,1463,1464,1465,1466,1467,1468,1490,1491,1495,1496,1497,1498,1499,1500,1501,1580,1581,1582,1583," \
               "1584,1585,1586,1587,1588,1589,1590,1591,1592,1593,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603," \
               "1604,1605,1606,1607,1608,1609,1610,1611,1660,1661,1662,1663,1664,1665,1666,1838,1839,1840,1841,1842," \
               "1843,1844,99001,99002,99003,99004 "

        info3 = Node.void("info")
        extend.add_child(info3)
        info3.add_child(Node.u32("extend_id", 91))
        info3.add_child(Node.u32("extend_type", 17))
        info3.add_child(Node.s32("param_num_1", 0))
        info3.add_child(Node.s32("param_num_2", 1))
        info3.add_child(Node.s32("param_num_3", 0))
        info3.add_child(Node.s32("param_num_4", 0))
        info3.add_child(Node.s32("param_num_5", 1))
        info3.add_child(Node.string("param_str_1", str1))
        info3.add_child(Node.string("param_str_2", str2))
        info3.add_child(Node.string("param_str_3", ""))
        info3.add_child(Node.string("param_str_4", ""))
        info3.add_child(Node.string("param_str_5", ""))

        # arena
        invest = Node.void("invest")
        game.add_child(invest)
        invest.add_child(Node.u64("limit_date", 1699872402000))

        arena = Node.void("arena")
        game.add_child(arena)
        arena.add_child(Node.s32("season", 1))
        arena.add_child(Node.s32("rule", 1))
        arena.add_child(Node.u64("time_start", 1668336402000))
        arena.add_child(Node.u64("time_end", 1704038400000))
        arena.add_child(Node.u64("shop_start", 1668336402000))
        arena.add_child(Node.u64("shop_end", 1704038400000))
        arena.add_child(Node.bool("is_open", True))
        arena.add_child(Node.bool("is_shop", True))

        # Available skill courses
        skill_course = Node.void("skill_course")
        game.add_child(skill_course)

        achievements = self.data.local.user.get_all_achievements(
            self.game, self.version, achievementtype="course"
        )
        courserates: Dict[Tuple[int, int], Dict[str, int]] = {}

        def getrates(season_id: int, course_id: int) -> Dict[str, int]:
            if (course_id, season_id) in courserates:
                return courserates[(course_id, season_id)]
            else:
                return {
                    "attempts": 0,
                    "clears": 0,
                    "total_score": 0,
                }

        for _, achievement in achievements:
            course_id = achievement.id % 100
            season_id = int(achievement.id / 100)
            rate = getrates(season_id, course_id)

            rate["attempts"] += 1
            if achievement.data.get_int("clear_type") >= 2:
                rate["clears"] += 1
            rate["total_score"] = achievement.data.get_int("score")
            courserates[(course_id, season_id)] = rate

        seasons = self.__get_skill_analyzer_seasons()
        skill_levels = self.__get_skill_analyzer_skill_levels()
        courses = self.__get_skill_analyzer_courses()
        skill_name_ids = self.__get_skill_analyzer_skill_name_ids()
        for course in courses:
            info = Node.void("info")
            skill_course.add_child(info)

            info.add_child(Node.s32("season_id", course["season_id"]))
            info.add_child(Node.string("season_name", seasons[course["season_id"]]))
            info.add_child(
                Node.bool("season_new_flg", course["season_id"] in {11})
            )
            info.add_child(
                Node.s16(
                    "course_id", course.get("course_id", course.get("skill_level", -1))
                )
            )
            info.add_child(
                Node.string(
                    "course_name",
                    course.get(
                        "course_name",
                        skill_levels.get(course.get("skill_level", -1), ""),
                    ),
                )
            )
            # Course type 0 is skill level courses. The course type is the same as the skill level (01-12).
            # If skill level is specified as '0', then the course type shows up as 'OTHER' instead of Skill Lv.01-12.
            info.add_child(Node.s16("course_type", course.get("course_type", 0)))
            info.add_child(Node.s16("skill_level", course.get("skill_level", 0)))
            info.add_child(
                Node.s16(
                    "skill_name_id",
                    course.get(
                        "skill_name_id",
                        skill_name_ids.get(course.get("skill_level", -1), 0),
                    ),
                )
            )
            info.add_child(
                Node.bool(
                    "matching_assist",
                    1 <= course.get("skill_level", -1) <= 7,
                )
            )

            # Calculate clear rate and average score
            rate = getrates(
                course["season_id"],
                course.get("course_id", course.get("skill_level", -1)),
            )
            if rate["attempts"] > 0:
                info.add_child(
                    Node.s32(
                        "clear_rate", int(100.0 * (rate["clears"] / rate["attempts"]))
                    )
                )
                info.add_child(
                    Node.u32("avg_score", rate["total_score"] // rate["attempts"])
                )
            else:
                info.add_child(Node.s32("clear_rate", 0))
                info.add_child(Node.u32("avg_score", 0))

            for trackno, trackdata in enumerate(course["tracks"]):
                track = Node.void("track")
                info.add_child(track)
                track.add_child(Node.s16("track_no", trackno))
                track.add_child(Node.s32("music_id", trackdata["id"]))
                track.add_child(Node.s8("music_type", trackdata["type"]))

        return game

    def handle_game_sv6_shop_request(self, request: Node) -> Node:
        self.update_machine_name(request.child_value("shopname"))

        # Respond with number of milliseconds until next request
        game = Node.void("game")
        game.add_child(Node.u32("nxt_time", 1000 * 5 * 60))
        return game

    def handle_game_sv6_hiscore_request(self, request: Node) -> Node:
        # Grab location for local scores
        locid = ID.parse_machine_id(request.child_value("locid"))

        game = Node.void("game")

        # Now, grab global and local scores as well as clear rates
        global_records = self.data.remote.music.get_all_records(self.game, self.version)
        users = {
            uid: prof
            for (uid, prof) in self.data.local.user.get_all_profiles(
                self.game, self.version
            )
        }
        area_users = [uid for uid in users if users[uid].get_int("loc", -1) == locid]
        area_records = self.data.local.music.get_all_records(
            self.game, self.version, userlist=area_users
        )
        clears = self.get_clear_rates()
        records: Dict[int, Dict[int, Dict[str, Tuple[UserID, Score]]]] = {}

        missing_users = [
                            userid for (userid, _) in global_records if userid not in users
                        ] + [userid for (userid, _) in area_records if userid not in users]
        for (userid, profile) in self.get_any_profiles(missing_users):
            users[userid] = profile

        for (userid, score) in global_records:
            if userid not in users:
                raise Exception("Logic error, missing profile for user!")
            if score.id not in records:
                records[score.id] = {}
            if score.chart not in records[score.id]:
                records[score.id][score.chart] = {}
            records[score.id][score.chart]["global"] = (userid, score)

        for (userid, score) in area_records:
            if userid not in users:
                raise Exception("Logic error, missing profile for user!")
            if score.id not in records:
                records[score.id] = {}
            if score.chart not in records[score.id]:
                records[score.id][score.chart] = {}
            records[score.id][score.chart]["area"] = (userid, score)

        # Output it to the game
        highscores = Node.void("sc")
        game.add_child(highscores)
        for musicid in records:
            for chart in records[musicid]:
                (globaluserid, globalscore) = records[musicid][chart]["global"]

                global_profile = users[globaluserid]
                if clears[musicid][chart]["total"] > 0:
                    clear_rate = float(clears[musicid][chart]["clears"]) / float(
                        clears[musicid][chart]["total"]
                    )
                else:
                    clear_rate = 0.0

                info = Node.void("d")
                highscores.add_child(info)
                info.add_child(Node.u32("id", musicid))
                info.add_child(Node.u32("ty", chart))
                info.add_child(
                    Node.string("a_sq", ID.format_extid(global_profile.extid))
                )
                info.add_child(Node.string("a_nm", global_profile.get_str("name")))
                info.add_child(Node.u32("a_sc", globalscore.points))
                info.add_child(Node.s32("cr", int(clear_rate * 10000)))
                info.add_child(Node.s32("avg_sc", clears[musicid][chart]["average"]))

                if "area" in records[musicid][chart]:
                    (localuserid, localscore) = records[musicid][chart]["area"]
                    local_profile = users[localuserid]
                    info.add_child(
                        Node.string("l_sq", ID.format_extid(local_profile.extid))
                    )
                    info.add_child(Node.string("l_nm", local_profile.get_str("name")))
                    info.add_child(Node.u32("l_sc", localscore.points))

        return game

    def handle_game_sv6_load_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        root = self.get_profile_by_refid(refid)
        if root is not None:
            return root

        # Figure out if this user has an older profile or not
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)

        if userid is not None:
            previous_game = self.previous_version()
        else:
            previous_game = None

        if previous_game is not None:
            profile = previous_game.get_profile(userid)
        else:
            profile = None

        if profile is not None:
            root = Node.void("game")
            root.add_child(Node.u8("result", 2))
            root.add_child(Node.string("name", profile.get_str("name")))
            return root
        else:
            root = Node.void("game")
            root.add_child(Node.u8("result", 1))
            return root

    def handle_game_sv6_frozen_request(self, request: Node) -> Node:
        game = Node.void("game")
        game.add_child(Node.u8("result", 0))
        return game

    def handle_game_sv6_new_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        name = request.child_value("name")
        loc = ID.parse_machine_id(request.child_value("locid"))
        self.new_profile_by_refid(refid, name, loc)

        root = Node.void("game")
        return root

    def handle_game_sv6_load_m_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            scores = self.data.remote.music.get_scores(self.game, self.version, userid)
        else:
            scores = []

        # Output to the game
        game = Node.void("game")
        music = Node.void("music")
        game.add_child(music)

        for score in scores:
            info = Node.void("info")
            music.add_child(info)

            stats = score.data.get_dict("stats")
            info.add_child(
                Node.u32_array(
                    "param",
                    [
                        score.id,
                        score.chart,
                        score.points,
                        stats.get_int("exscore", 0),
                        self.__db_to_game_clear_type(score.data.get_int("clear_type")),
                        self.__db_to_game_grade(score.data.get_int("grade")),
                        0,  # 6: Any value
                        0,  # 7: Any value
                        stats.get_int("btn_rate"),
                        stats.get_int("long_rate"),
                        stats.get_int("vol_rate"),
                        0,  # 11: Any value
                        0,  # 12: Another medal, perhaps old score medal?
                        0,  # 13: Another grade, perhaps old score grade?
                        0,  # 14: Any value
                        0,  # 15: Any value
                        0,  # 16: Any value
                        0,  # 17: Another medal, perhaps old score medal?
                        0,  # 18: Another grade, perhaps old score grade?
                        0,  # 19: Any value
                        0,  # 20. Any value
                    ],
                ),
            )

        return game

    def handle_game_sv6_load_r_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        game = Node.void("game")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            links = self.data.local.user.get_links(self.game, self.version, userid)
            index = 0
            for link in links:
                if link.type != "rival":
                    continue
                other_profile = self.get_profile(link.other_userid)
                if other_profile is None:
                    continue

                # Base information about rival
                rival = Node.void("rival")
                game.add_child(rival)
                rival.add_child(Node.s16("no", index))
                rival.add_child(
                    Node.string("seq", ID.format_extid(other_profile.extid))
                )
                rival.add_child(Node.string("name", other_profile.get_str("name")))

                # Keep track of index
                index = index + 1

                # Return scores for this user on random charts
                scores = self.data.remote.music.get_scores(
                    self.game, self.version, link.other_userid
                )
                for score in scores:
                    music = Node.void("music")
                    rival.add_child(music)
                    music.add_child(
                        Node.u32_array(
                            "param",
                            [
                                score.id,
                                score.chart,
                                score.points,
                                self.__db_to_game_clear_type(
                                    score.data.get_int("clear_type")
                                ),
                                self.__db_to_game_grade(score.data.get_int("grade")),
                            ],
                        )
                    )

        return game

    def handle_game_sv6_save_request(self, request: Node):
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            oldprofile = self.get_profile(userid)
            newprofile = self.unformat_profile(userid, request, oldprofile)
        else:
            newprofile = None

        if userid is not None and newprofile is not None:
            self.put_profile(userid, newprofile)

        return Node.void("game")

    def handle_game_sv6_save_m_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        # Broadcasting
        # card_data = {}
        # song = None

        # if userid is not None:
        #     profile = self.get_profile(userid)
        #     card_data[BroadcastConstants.PLAYER_NAME] = profile.get_str("name")

        # clear_map = {
        #     self.CLEAR_TYPE_NO_PLAY: "NO PLAY",
        #     self.CLEAR_TYPE_HARD_CLEAR: "HARD CLEAR",
        #     self.CLEAR_TYPE_CLEAR: "CLEAR",
        #     self.CLEAR_TYPE_FAILED: "FAILED",
        #     self.CLEAR_TYPE_ULTIMATE_CHAIN: "ULTIMATE CHAIN",
        #     self.CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: "⭐PUC⭐",
        # }
        # grade_map = {
        #     self.GAME_GRADE_NO_PLAY: "NO PLAY",
        #     self.GAME_GRADE_D: "D",
        #     self.GAME_GRADE_C: "C",
        #     self.GAME_GRADE_B: "B",
        #     self.GAME_GRADE_A: "A",
        #     self.GAME_GRADE_A_PLUS: "A+",
        #     self.GAME_GRADE_AA: "AA",
        #     self.GAME_GRADE_AA_PLUS: "AA+",
        #     self.GAME_GRADE_AAA: "AAA",
        #     self.GAME_GRADE_AAA_PLUS: "AAA+",
        #     self.GAME_GRADE_S: "S"
        # }

        track = None

        # This is new saving format for 20210831
        if request.child("track") is not None:
            track = request.child("track")
        else:
            track = request

        # Doesn't matter if userid is None here, that's an anonymous score
        musicid = track.child_value("music_id")
        chart = track.child_value("music_type")
        points = track.child_value("score")
        combo = track.child_value("max_chain")
        exscore = track.child_value("exscore")
        clear_type = self.__game_to_db_clear_type(track.child_value("clear_type"))
        grade = self.__game_to_db_grade(track.child_value("score_grade"))
        stats = {
            "exscore": track.child_value("exscore"),
            "btn_rate": track.child_value("btn_rate"),
            "long_rate": track.child_value("long_rate"),
            "vol_rate": track.child_value("vol_rate"),
            "critical": track.child_value("critical"),
            "near": track.child_value("near"),
            "error": track.child_value("error"),
        }

        # song = self.data.local.music.get_song(self.game, self.version, musicid, chart)
        # card_data[BroadcastConstants.SONG_NAME] = song.name
        # card_data[BroadcastConstants.ARTIST_NAME] = song.artist
        # card_data[BroadcastConstants.DIFFICULTY] = song.data.get("difficulty", 0)
        # card_data[BroadcastConstants.SCORE] = points
        # card_data[BroadcastConstants.EXSCORE] = track.child_value("exscore")
        # card_data[BroadcastConstants.GRADE] = grade_map.get(track.child_value("score_grade"), "NO PLAY")
        # card_data[BroadcastConstants.CLEAR_STATUS] = clear_map.get(track.child_value("clear_type"), "NO PLAY")
        # card_data[BroadcastConstants.PLAY_STATS_HEADER] = "⭐"
        # card_data[BroadcastConstants.CRITICAL] = stats.get("critical")
        # card_data[BroadcastConstants.NEAR] = stats.get("near")
        # card_data[BroadcastConstants.ERROR] = stats.get("error")
        # card_data[BroadcastConstants.MAX_CHAIN] = combo

        # Save the score
        self.update_score(
            userid,
            musicid,
            chart,
            points,
            clear_type,
            grade,
            combo,
            stats,
        )

        # self.data.triggers.broadcast_score(card_data, self.game, song)

        # Return a blank response
        return Node.void("game")

    def handle_game_sv6_play_e_request(self, request: Node) -> Node:
        return Node.void("game")

    def handle_game_sv6_save_e_request(self, request: Node) -> Node:
        # This has to do with Policy floor infection, but we don't
        # implement multi-game support so meh.
        game = Node.void("game")
        return game

    def handle_game_sv6_play_s_request(self, request: Node) -> Node:
        root = Node.void("game")
        root.add_child(Node.u32("play_id", 1))
        return root

    def handle_game_sv6_buy_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            profile = self.get_profile(userid)
        else:
            profile = None

        if userid is not None and profile is not None:
            # Look up packets and blocks
            packet = profile.get_int("packet")
            block = profile.get_int("block")

            # Add on any additional we earned this round
            packet = packet + (request.child_value("earned_gamecoin_packet") or 0)
            block = block + (request.child_value("earned_gamecoin_block") or 0)

            currency_type = request.child_value("currency_type")
            price = request.child_value("item/price")
            if isinstance(price, list):
                # Sometimes we end up buying more than one item at once
                price = sum(price)

            if currency_type == self.GAME_CURRENCY_PACKETS:
                # This is a valid purchase
                newpacket = packet - price
                if newpacket < 0:
                    result = 1
                else:
                    packet = newpacket
                    result = 0
            elif currency_type == self.GAME_CURRENCY_BLOCKS:
                # This is a valid purchase
                newblock = block - price
                if newblock < 0:
                    result = 1
                else:
                    block = newblock
                    result = 0
            else:
                # Bad currency type
                result = 1

            if result == 0:
                # Transaction is valid, update the profile with new packets and blocks
                profile.replace_int("packet", packet)
                profile.replace_int("block", block)
                self.put_profile(userid, profile)

                # If this was a song unlock, we should mark it as unlocked
                item_type = request.child_value("item/item_type")
                item_id = request.child_value("item/item_id")
                param = request.child_value("item/param")

                if not isinstance(item_type, list):
                    # Sometimes we buy multiple things at once. Make it easier by always assuming this.
                    item_type = [item_type]
                    item_id = [item_id]
                    param = [param]

                for i in range(len(item_type)):
                    self.data.local.user.put_achievement(
                        self.game,
                        self.version,
                        userid,
                        item_id[i],
                        f"item_{item_type[i]}",
                        {
                            "param": param[i],
                        },
                    )

        else:
            # Unclear what to do here, return a bad response
            packet = 0
            block = 0
            result = 1

        game = Node.void("game")
        game.add_child(Node.u32("gamecoin_packet", packet))
        game.add_child(Node.u32("gamecoin_block", block))
        game.add_child(Node.s8("result", result))
        return game

    def handle_game_sv6_save_c_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            season_id = request.child_value("ssnid")
            course_id = request.child_value("crsid")
            clear_type = request.child_value("ct")
            achievement_rate = request.child_value("ar")
            grade = request.child_value("gr")
            score = request.child_value("sc")
            exscore = request.child_value("ex")

            # Do not update the course achievement when old score is greater.
            old = self.data.local.user.get_achievement(
                self.game, self.version, userid, (season_id * 100) + course_id, "course"
            )
            if old is not None and old.get_int("score") > score:
                return Node.void("game")

            self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                (season_id * 100) + course_id,
                "course",
                {
                    "clear_type": clear_type,
                    "achievement_rate": achievement_rate,
                    "score": score,
                    "grade": grade,
                    "exscore": exscore,
                },
            )

        # Return a blank response
        return Node.void("game")

    def handle_game_sv6_save_mega_request(self, requset: Node) -> Node:
        return Node.void("game")

    def handle_game_sv6_print_request(self, request: Node) -> Node:
        game = Node.void("game")
        game.add_child(Node.s8("result", 0))
        genesis_cards = Node.void("genesis_cards")
        game.add_child(genesis_cards)
        after_power = Node.void("after_power")
        game.add_child(after_power)

        generator_list = []
        if request.child("genesis_card") is not None:
            for child in request.child("genesis_card").children:
                generator_id = child.child_value("generator_id")
                if generator_id not in generator_list:
                    generator_list.append(generator_id)

                info = Node.void("info")
                genesis_cards.add_child(info)
                info.add_child(Node.s32("index", child.child_value("index")))
                info.add_child(Node.s32("print_id", child.child_value("print_id")))

            for item in generator_list:
                info = Node.void("info")
                after_power.add_child(info)
                info.add_child(Node.s32("generator_id", item))
                info.add_child(Node.s32("param", 10))

        return game

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        game = Node.void("game")

        # Generic profile stuff
        game.add_child(Node.string("name", profile.get_str("name")))
        game.add_child(Node.string("code", ID.format_extid(profile.extid)))
        game.add_child(Node.string("sdvx_id", ID.format_extid(profile.extid)))
        game.add_child(Node.u16("appeal_id", profile.get_int("appealid")))
        game.add_child(Node.s16("skill_base_id", profile.get_int("skill_base_id")))
        game.add_child(Node.s16("skill_name_id", profile.get_int("skill_name_id")))
        game.add_child(Node.u32("gamecoin_packet", profile.get_int("packet")))
        game.add_child(Node.u32("gamecoin_block", profile.get_int("block")))
        game.add_child(Node.u32("blaster_energy", profile.get_int("blaster_energy")))
        game.add_child(Node.u32("blaster_count", profile.get_int("blaster_count")))
        game.add_child(Node.u16("extrack_energy", profile.get_int("extrack_energy")))

        # Play statistics
        statistics = self.get_play_statistics(userid)
        game.add_child(Node.u32("play_count", statistics.total_plays))
        game.add_child(Node.u32("today_count", statistics.today_plays))
        game.add_child(Node.u32("play_chain", statistics.consecutive_days))
        game.add_child(Node.u32("day_count", statistics.total_days))

        # Also exists but we don't support:
        # - max_play_chain: Max consecutive days in a row where the user had at last one play.
        # - week_count: Number of weeks here this user had at least one play.
        # - week_play_count: Number of plays in the last week (I think).
        # - week_chain: Number of weeks in a row where the user had at least one play in that week.
        # - max_week_chain: Maximum number of weeks in a row where the user had at least one play in that week.

        # Player options and last touched song.
        lastdict = profile.get_dict("last")
        game.add_child(Node.s32("last_music_id", lastdict.get_int("music_id", -1)))
        game.add_child(Node.u8("last_music_type", lastdict.get_int("music_type")))
        game.add_child(Node.u8("sort_type", lastdict.get_int("sort_type")))
        game.add_child(Node.u8("narrow_down", lastdict.get_int("narrow_down")))
        game.add_child(Node.u8("headphone", lastdict.get_int("headphone")))
        game.add_child(Node.u8("gauge_option", lastdict.get_int("gauge_option")))
        game.add_child(Node.u8("ars_option", lastdict.get_int("ars_option")))
        game.add_child(Node.u8("notes_option", lastdict.get_int("notes_option")))
        game.add_child(Node.u8("early_late_disp", lastdict.get_int("early_late_disp")))
        game.add_child(Node.u8("eff_c_left", lastdict.get_int("eff_c_left")))
        game.add_child(Node.u8("eff_c_right", lastdict.get_int("eff_c_right", 1)))
        game.add_child(Node.u32("lanespeed", lastdict.get_int("lanespeed")))
        game.add_child(Node.s32("hispeed", lastdict.get_int("hispeed")))
        game.add_child(Node.s32("draw_adjust", lastdict.get_int("draw_adjust")))

        # Item unlocks
        itemnode = Node.void("item")
        game.add_child(itemnode)

        game_config = self.get_game_config()
        achievements = self.data.local.user.get_achievements(
            self.game, self.version, userid
        )

        for item in achievements:
            if item.type[:5] != "item_":
                continue
            itemtype = int(item.type[5:])

            if (
                    game_config.get_bool("force_unlock_songs")
                    and itemtype == self.GAME_CATALOG_TYPE_SONG
            ):
                # Don't echo unlocked songs, we will add all of them later
                continue
            if (
                    game_config.get_bool("force_unlock_cards")
                    and itemtype == self.GAME_CATALOG_TYPE_APPEAL_CARD
            ):
                # Don't echo unlocked appeal cards, we will add all of them later
                continue
            if (
                    game_config.get_bool("force_unlock_crew")
                    and itemtype == self.GAME_CATALOG_TYPE_CREW
            ):
                # Don't echo unlocked crew, we will add all of them later
                continue

            info = Node.void("info")
            itemnode.add_child(info)
            info.add_child(Node.u8("type", itemtype))
            info.add_child(Node.u32("id", item.id))
            info.add_child(Node.u32("param", item.data.get_int("param")))

        if game_config.get_bool("force_unlock_songs"):
            ids: Dict[int, int] = {}
            songs = self.data.local.music.get_all_songs(self.game, self.version)
            for song in songs:
                if song.id not in ids:
                    ids[song.id] = 0

                if song.data.get_int("difficulty") > 0:
                    ids[song.id] = ids[song.id] | (1 << song.chart)

            for itemid in ids:
                if ids[itemid] == 0:
                    continue

                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", self.GAME_CATALOG_TYPE_SONG))
                info.add_child(Node.u32("id", itemid))
                info.add_child(Node.u32("param", ids[itemid]))

        # unlock appeal cards.
        if True:
            for appealcardid in range(1, 6000):
                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", 1))
                info.add_child(Node.u32("id", appealcardid))
                info.add_child(Node.u32("param", 1))

        # unlock crew:
        if True:
            for crewid in range(1, 999):
                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", 11))
                info.add_child(Node.u32("id", crewid))
                info.add_child(Node.u32("param", 15))

            info = Node.void("info")
            itemnode.add_child(info)
            info.add_child(Node.u8("type", 4))
            info.add_child(Node.u32("id", 599))
            info.add_child(Node.u32("param", 10))

        # Skill courses
        skill = Node.void("skill")
        game.add_child(skill)
        skill_level = 0

        for course in achievements:
            if course.type != "course":
                continue

            course_id = course.id % 100
            season_id = int(course.id / 100)

            if course.data.get_int("clear_type") >= 2:
                # The user cleared this, lets take the highest level clear for this
                courselist = [
                    c
                    for c in self.__get_skill_analyzer_courses()
                    if c.get("course_id", c.get("skill_level", -1)) == course_id
                       and c["season_id"] == season_id
                ]
                if len(courselist) > 0:
                    skill_level = max(skill_level, courselist[0]["skill_level"])

            course_node = Node.void("course")
            skill.add_child(course_node)
            course_node.add_child(Node.s16("ssnid", season_id))
            course_node.add_child(Node.s16("crsid", course_id))
            course_node.add_child(Node.s32("ex", course.data.get_int("exscore")))
            course_node.add_child(Node.s32("sc", course.data.get_int("score")))
            course_node.add_child(Node.s16("ct", course.data.get_int("clear_type")))
            course_node.add_child(Node.s16("gr", course.data.get_int("grade")))
            course_node.add_child(
                Node.s16("ar", course.data.get_int("achievement_rate"))
            )
            course_node.add_child(Node.s16("cnt", 1))

        # Calculated skill level
        game.add_child(Node.s16("skill_level", skill_level))

        # Game parameters
        paramnode = Node.void("param")
        game.add_child(paramnode)

        for param in achievements:
            if param.type[:6] != "param_":
                continue
            paramtype = int(param.type[6:])

            info = Node.void("info")
            paramnode.add_child(info)
            info.add_child(Node.s32("id", param.id))
            info.add_child(Node.s32("type", paramtype))
            info.add_child(
                Node.s32_array("param", param.data["param"])
            )  # This looks to be variable, so no validation on length

        # Blaster pass
        if game_config.get_bool("use_blasterpass"):
            eashop = Node.void("ea_shop")
            game.add_child(eashop)

            eashop.add_child(Node.bool("blaster_pass_enable", True))
            eashop.add_child(Node.u64("blaster_pass_limit_date", Time.now()))

        # Try to load arena status

        arena_node = Node.void("arena")
        game.add_child(arena_node)
        for arena in achievements:
            if arena.type != "arena":
                continue

            arena_node.add_child(Node.s32("last_play_season", 1))
            arena_node.add_child(Node.s32("rank_point", arena.data.get_int("rank_point")))
            arena_node.add_child(Node.s32("shop_point", arena.data.get_int("shop_point")))
            arena_node.add_child(Node.s32("ultimate_rate", 0))
            arena_node.add_child(Node.s32("ultimate_rank_num", 0))
            arena_node.add_child(Node.s32("rank_play_cnt", 0))
            arena_node.add_child(Node.s32("ultimate_play_cnt", 0))
        return game

    def unformat_profile(
            self, userid: UserID, request: Node, oldprofile: Profile
    ) -> Profile:
        newprofile = oldprofile.clone()

        # Update blaster energy and in-game currencies
        earned_gamecoin_packet = request.child_value("earned_gamecoin_packet")
        if earned_gamecoin_packet is not None:
            newprofile.replace_int(
                "packet", newprofile.get_int("packet") + earned_gamecoin_packet
            )
        earned_gamecoin_block = request.child_value("earned_gamecoin_block")
        if earned_gamecoin_block is not None:
            newprofile.replace_int(
                "block", newprofile.get_int("block") + earned_gamecoin_block
            )
        earned_blaster_energy = request.child_value("earned_blaster_energy")
        if earned_blaster_energy is not None:
            newprofile.replace_int(
                "blaster_energy",
                newprofile.get_int("blaster_energy") + earned_blaster_energy,
            )
        earned_extrack_energy = request.child_value("earned_extrack_energy")
        if earned_extrack_energy is not None:
            newprofile.replace_int(
                "extrack_energy",
                newprofile.get_int("extrack_energy") + earned_extrack_energy,
            )

        # Miscelaneous profile stuff
        newprofile.replace_int("blaster_count", request.child_value("blaster_count"))
        newprofile.replace_int("appealid", request.child_value("appeal_id"))
        newprofile.replace_int("skill_level", request.child_value("skill_level"))
        newprofile.replace_int("skill_base_id", request.child_value("skill_base_id"))
        newprofile.replace_int("skill_name_id", request.child_value("skill_name_id"))

        # Update user's unlock status if we aren't force unlocked
        game_config = self.get_game_config()

        if request.child("item") is not None:
            for child in request.child("item").children:
                if child.name != "info":
                    continue

                item_id = child.child_value("id")
                item_type = child.child_value("type")
                param = child.child_value("param")

                if (
                        game_config.get_bool("force_unlock_cards")
                        and item_type == self.GAME_CATALOG_TYPE_APPEAL_CARD
                ):
                    # Don't save back appeal cards because they were force unlocked
                    continue
                if (
                        item_type == self.GAME_CATALOG_TYPE_SONG
                ):
                    # Don't save back songs, because they were force unlocked
                    continue
                if (
                        game_config.get_bool("force_unlock_crew")
                        and item_type == self.GAME_CATALOG_TYPE_CREW
                ):
                    # Don't save back crew, because they were force unlocked
                    continue

                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    item_id,
                    f"item_{item_type}",
                    {
                        "param": param,
                    },
                )

        # Update params
        if request.child("param") is not None:
            for child in request.child("param").children:
                if child.name != "info":
                    continue

                param_id = child.child_value("id")
                param_type = child.child_value("type")
                param_param = child.child_value("param")
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    param_id,
                    f"param_{param_type}",
                    {
                        "param": param_param,
                    },
                )

        # New course saving items add in 2022021400
        if request.child("course") is not None:
            course = request.child("course")
            season_id = course.child_value("ssnid")
            course_id = course.child_value("crsid")
            clear_type = course.child_value("ct")
            achievement_rate = course.child_value("ar")
            grade = course.child_value("gr")
            score = course.child_value("sc")
            exscore = course.child_value("ex")

            # Do not update the course achievement when old score is greater.
            old = self.data.local.user.get_achievement(
                self.game, self.version, userid, (season_id * 100) + course_id, "course"
            )
            if old is not None and old.get_int("score") > score:
                pass
            if (old is not None and old.get_int("score") < score) or old is None:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    (season_id * 100) + course_id,
                    "course",
                    {
                        "clear_type": clear_type,
                        "achievement_rate": achievement_rate,
                        "score": score,
                        "grade": grade,
                        "exscore": exscore,
                    },
                )

        # Save arena result
        if request.child("arena") is not None:
            arena = request.child("arena")
            earned_rank_point = arena.child_value("earned_rank_point")
            earned_shop_point = arena.child_value("earned_shop_point")

            old = self.data.local.user.get_achievement(
                self.game, self.version, userid, 1, "arena"
            )

            if old is not None:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    1,
                    "arena",
                    {
                        "rank_point": old.get_int("rank_point") + earned_rank_point,
                        "shop_point": old.get_int("shop_point") + earned_shop_point,
                    },
                )
            else:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    1,
                    "arena",
                    {
                        "rank_point": earned_rank_point,
                        "shop_point": earned_shop_point,
                    },
                )

        # Grab last information and player options.
        lastdict = newprofile.get_dict("last")
        lastdict.replace_int("music_id", request.child_value("music_id"))
        lastdict.replace_int("music_type", request.child_value("music_type"))
        lastdict.replace_int("sort_type", request.child_value("sort_type"))
        lastdict.replace_int("narrow_down", request.child_value("narrow_down"))
        lastdict.replace_int("headphone", request.child_value("headphone"))
        lastdict.replace_int("gauge_option", request.child_value("gauge_option"))
        lastdict.replace_int("ars_option", request.child_value("ars_option"))
        lastdict.replace_int("notes_option", request.child_value("notes_option"))
        lastdict.replace_int("early_late_disp", request.child_value("early_late_disp"))
        lastdict.replace_int("eff_c_left", request.child_value("eff_c_left"))
        lastdict.replace_int("eff_c_right", request.child_value("eff_c_right"))
        lastdict.replace_int("lanespeed", request.child_value("lanespeed"))
        lastdict.replace_int("hispeed", request.child_value("hispeed"))
        lastdict.replace_int("draw_adjust", request.child_value("draw_adjust"))

        # Save back last information gleaned from results
        newprofile.replace_dict("last", lastdict)

        # Keep track of play statistics
        self.update_play_statistics(userid)

        return newprofile
