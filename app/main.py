from fastapi import FastAPI
from routers import task, user

app = FastAPI()

@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)


# # Настройка Jinja2Templates
# templates = Jinja2Templates(directory="templates")
#
# # Модель пользователя
# class User(BaseModel):
#     id: int
#     username: str = Field(..., min_length=5, max_length=20, description="Enter username", example="UrbanUser")
#     age: int = Field(..., ge=18, le=120, description="Enter age", example=24)
#
# # Список пользователей
# users: List[User] = []
#
# # Главная страница: отображение списка пользователей
# @app.get("/", response_class=HTMLResponse)
# async def get_users_page(request: Request):
#     """
#     Отображает список пользователей через шаблон.
#     """
#     return templates.TemplateResponse("users.html", {"request": request, "users": users})
#
# # Получение информации о конкретном пользователе
# @app.get("/user/{user_id}", response_class=HTMLResponse)
# async def get_user_page(
#     request: Request,
#     user_id: Annotated[int, Path(ge=1, description="Enter User ID", example=1)]
# ):
#     """
#     Отображает информацию о конкретном пользователе через шаблон.
#     """
#     for user in users:
#         if user.id == user_id:
#             return templates.TemplateResponse("users.html", {"request": request, "user": user})
#     raise HTTPException(status_code=404, detail="User was not found")
#
# # Создание пользователя
# @app.post("/user/{username}/{age}", response_model=User)
# async def create_user(
#     username: Annotated[
#         str,
#         Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")
#     ],
#     age: Annotated[
#         int,
#         Path(ge=18, le=120, description="Enter age", example=24)
#     ]
# ) -> User:
#     """
#     Создает нового пользователя и добавляет его в список.
#     """
#     new_id = users[-1].id + 1 if users else 1
#     new_user = User(id=new_id, username=username, age=age)
#     users.append(new_user)
#     return new_user
