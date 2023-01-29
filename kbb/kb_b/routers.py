from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Request, HTTPException, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from kbb.kb_b.models import WorkoutModel, WorkoutActualModel
from kbb.app.user.models import User, get_user_db


def get_kbb_router(app):
    router = APIRouter()

    @router.post("/exercises/create", response_description="Add new exercise", response_model=WorkoutModel)
    async def create_exercises(request: Request, user: User = Depends(get_user_db),
                               exercises: WorkoutModel = Body()):
        exercises = jsonable_encoder(exercises)
        new_exercises = await app.db["exercises"].insert_one(exercises)
        inserted_id = new_exercises.inserted_id
        created_exercises = await app.db["exercises"].find_one({"_id": inserted_id})

        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_exercises)

    # @router.get("/exercises/get_current_workout/{workout_id}", response_description="List current workout",
    #             response_model=WorkoutModel)
    # async def list_exercises(workout_id: str, request: Request,
    #                          user: User = Depends(get_user_db())):
    #     if (workout := await app.db["exercises"].find_one({"_id": workout_id})) is not None:
    #         return workout
    #
    #     raise HTTPException(status_code=404, detail=f"Workout {workout_id} not found")
    #
    # @router.post("/exercises/track_workout/create", response_description="Track Current Workout",
    #              response_model=WorkoutActualModel)
    # async def track_workout(request: Request, user: User = Depends(get_user_db()),
    #                         workout: WorkoutActualModel = Body()):
    #     workout = jsonable_encoder(workout)
    #     new_workout = await app.db["workouts"].insert_one(workout)
    #     inserted_workout_id = new_workout.inserted_id
    #     created_workout = await app.db["workouts"].find_one({"_id": inserted_workout_id})
    #
    #     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_workout)
