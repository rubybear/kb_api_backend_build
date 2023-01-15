from typing import List, Optional

import motor.motor_asyncio
from bson import ObjectId
from fastapi import FastAPI, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, BaseSettings, validator, root_validator
from starlette import status
from starlette.responses import JSONResponse


class Settings(BaseSettings):
    db_admin_username: str
    db_password: str
    db_uri: Optional[str] = None

    @validator('db_uri', always=True)
    def validate_uri(cls, v, values) -> str:
        admin = values['db_admin_username']
        password = values['db_password']
        return f"mongodb+srv://{admin}:{password}@cluster0.wr4ucuo.mongodb.net/?retryWrites=true&w=majority"


settings = Settings()
app = FastAPI()

conn_str = settings.db_uri
motor.motor_asyncio.AsyncIOMotorClient()
client = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
db = client.kettlebell_barbell


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
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


class WorkoutModel(BaseModel):
    workout_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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


class ExerciseActualModel(BaseModel):
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


class WorkoutActualModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
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


@app.post("/exercises/create", response_description="Add new exercise", response_model=WorkoutModel)
async def create_exercises(exercises: WorkoutModel = Body()):
    exercises = jsonable_encoder(exercises)
    new_exercises = await db["exercises"].insert_one(exercises)
    inserted_id = new_exercises.inserted_id
    created_exercises = await db["exercises"].find_one({"_id": inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_exercises)


@app.get("/exercises/get_current_workout/{workout_id}", response_description="List current workout",
         response_model=WorkoutModel)
async def list_exercises(workout_id: str):
    if (workout := await db["exercises"].find_one({"_id": workout_id})) is not None:
        return workout

    raise HTTPException(status_code=404, detail=f"Workout {workout_id} not found")


@app.post("/exercises/track_workout/create", response_description="Track Current Workout",
          response_model=WorkoutActualModel)
async def track_workout(workout: WorkoutActualModel = Body()):
    workout = jsonable_encoder(workout)
    new_workout = await db["workouts"].insert_one(workout)
    inserted_workout_id = new_workout.inserted_id
    created_workout = await db["workouts"].find_one({"_id": inserted_workout_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_workout)
