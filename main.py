from fastapi import FastAPI, Depends, Request, Path, HTTPException, status, Response
from starlette.responses import RedirectResponse
from Routers import Login, User, Post



app = FastAPI(
    title= 'IkarmaAPI',
    description= 'Builded with FastAPI ❤️❤️',
    version ="1.0",
    contact= {"email":"contact@me.io"},
    docs_url ="/"
)

app.include_router(Login.router)
app.include_router(User.router)

if __name__ == "__main__":
    app.run(port=7000)

# @app.get("/")
# async def main():
#     return RedirectResponse(url="/docs")