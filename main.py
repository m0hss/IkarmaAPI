from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from Routers import login, user, post



app = FastAPI(
    title= 'IkarmaAPI',
    description= 'Builded with FastAPI ❤️❤️',
    version ="1.0",
    contact= {"email":"contact@me.io"},
    docs_url ="/"
)


# app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(login.router)
app.include_router(user.router)
app.include_router(post.router)

# @app.get("/")
# async def main():
#     return RedirectResponse(url="/docs")

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)
