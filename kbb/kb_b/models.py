from typing import List

from beanie import PydanticObjectId, Document
from bson import ObjectId
from pydantic import BaseModel, Field

class ExerciseModel(Document):
    exercise_id: PydanticObjectId
    type: str = Field()
    name: str = Field()
    sets: int = Field()
    reps: int = Field()
    weight: float = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "type": "barbell",
                "name": "benchpress",
                "sets": 3,
                "reps": 10,
                "weight": 225.0
            }
        }


class WorkoutModel(Document):
    workout_id: PydanticObjectId
    exercises: List[ExerciseModel]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"exercises": [
                {
                    "name": "benchpress",
                    "type": "barbell",
                    "sets": 3,
                    "reps": 10,
                    "weight": 225

                },
                {
                    "name": "squat",
                    "type": "barbell",
                    "sets": 3,
                    "reps": 5,
                    "weight": 500

                }
            ]
            }
        }


class ExerciseActualModel(Document):
    exercise_id: str
    actual_reps: List[int]
    actual_sets: int
    weight: List[int]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"exercise_id": "63b767985156fb9741e62abd",
                        "actual_reps": [10, 10, 9],
                        "actual_sets": 3,
                        "weight": [200, 195, 195]
                        }


class WorkoutActualModel(Document):
    id: PydanticObjectId
    workout_id: str
    exercise_data: List[ExerciseActualModel]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"workout_id": "63b767985156fb9741e62abc",
                        "exercise_date": [
                            {"exercise_id": "63b767985156fb9741e62abd",
                             "actual_reps": [10, 10, 9],
                             "actual_sets": 3,
                             "weight": [200, 195, 195]
                             }
                        ]}
