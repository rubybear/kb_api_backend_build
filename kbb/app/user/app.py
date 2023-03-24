from beanie import init_beanie
from fastapi import FastAPI, Depends

import kbb
from kbb.app.user.db import user_db
from kbb.kb_b.documents import ExerciseTracker, ExercisesMeta, Workouts
from kbb.kb_b.routers import workout_router
from kbb.app.user.auth import current_active_user, auth_backend
from kbb.app.user.models import User, UserCreate, UserUpdate, UserRead
from kbb.app.user.routers import fastapi_users

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    workout_router,
    prefix="/workout",
    tags=["workouts"]
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=user_db,
        document_models=[
            User,
            ExerciseTracker,
            ExercisesMeta,
            Workouts
        ],
    )

    # app.include_router(get_kbb_router(app))
