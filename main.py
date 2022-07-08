import uvicorn
from fastapi import FastAPI
from routers import authentication, user, groups

app = FastAPI()


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(groups.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9010, reload=True)
