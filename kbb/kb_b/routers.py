from typing import List, Callable, Tuple, Any, Dict, Coroutine

from beanie import WriteRules
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Body, Request, HTTPException, Depends
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from kbb.app.user.auth import fastapi_users
from kbb.kb_b.current_user_model import CurrentUser
from kbb.kb_b.documents import ExerciseTracker, ExercisesMeta, Workouts

workout_router = APIRouter()

current_active_user = fastapi_users.current_user(active=True, verified=True)


@workout_router.post("/create_workout", response_description="Create the exercises that make up a workout",
                     response_model=Workouts)
async def create_new_workout(workout: Workouts, user=Depends(current_active_user)):
    workout.user = user.email
    await workout.save(link_rule=WriteRules.WRITE)
    new_workout = await workout.get(workout.id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_workout.json())

@workout_router.post("/track", response_description="TEST", response_model=ExerciseTracker)
async def create_exercise2(exercise: ExerciseTracker):
    await exercise.create()
    new_exercise = await exercise.get(exercise.id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_exercise.json())

# @workout_router.get("/exercises/get_current_workout/{workout_id}", response_description="List current workout",
#                     response_model=WorkoutModel)
# async def list_exercises(workout_id: str, request: Request,
#                          user: User = Depends(get_user_db())):
#     if (workout := await user_db.db["exercises"].find_one({"_id": workout_id})) is not None:
#         return workout
#
#     raise HTTPException(status_code=404, detail=f"Workout {workout_id} not found")
#
#
# @workout_router.post("/exercises/track_workout/create", response_description="Track Current Workout",
#                      response_model=WorkoutActualModel)
# async def track_workout(request: Request, user: User = Depends(get_user_db()),
#                         workout: WorkoutActualModel = Body()):
#     workout = jsonable_encoder(workout)
#     new_workout = await user_db.db["workouts"].insert_one(workout)
#     inserted_workout_id = new_workout.inserted_id
#     created_workout = await user_db.db["workouts"].find_one({"_id": inserted_workout_id})
#
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_workout)
