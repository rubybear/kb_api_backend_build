from typing import List

import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, Body
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()

conn_str = "mongodb+srv://admin:Bushdid911@cluster0.wr4ucuo.mongodb.net/?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.kettlebell_barbell


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ExerciseModel(BaseModel):
    exercise_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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


class ExercisesModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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


@app.post("/mongotest", response_description="add new exercise", response_model=ExercisesModel)
async def create_exercises(exercises: ExercisesModel = Body()):
    exercises = jsonable_encoder(exercises)
    new_exercises = await db["exercises"].insert_one(exercises)
    created_exercises = await db["exercises"].find_one({"_id": new_exercises.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_exercises)


class ExerciseSet(BaseModel):
    set_number: int
    reps: int
    weight: float


class Exercise(BaseModel):
    name: str
    exercise_set: list[ExerciseSet]


class ExercisesStored(BaseModel):
    exercise_id: str
    exercise: Exercise


sampleExercise = Exercise(
    name="test",
    exercise_set=[
        ExerciseSet(set_number=1, reps=10, weight=100.5),
        ExerciseSet(set_number=2, reps=10, weight=100.5)]
)

sampleData = dict(ExercisesStored(exercise_id="sample_1", exercise=sampleExercise))
templates = Jinja2Templates(directory='templates')


@app.get("/exercises/")
async def get_exercises(q: str | None = None):
    return sampleExercise


@app.put('/exercises/{exercise_id}')
async def update_exercise(exercise_id: str, exercise: Exercise):
    return templates.TemplateResponse("form.html", {"exercise_id": exercise_id, "exercise": exercise})