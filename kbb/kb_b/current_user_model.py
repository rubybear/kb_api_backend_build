from beanie import PydanticObjectId
from pydantic import BaseModel

from kbb.kb_b.documents import ExercisesMeta, ExerciseTracker


class CurrentUser(BaseModel):
    user: str
    current_workout: PydanticObjectId
    current_exercise: ExercisesMeta
    tracker: ExerciseTracker
