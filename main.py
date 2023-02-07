from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules import check_video_url
from pytube import YouTube


import os
app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get("/tryagain")
async def download(request: Request):
    return templates.TemplateResponse("trya.html", context={"request": request})


@app.get("/getall", response_class=HTMLResponse)
async def getall(request: Request, uri: str):

    verify = check_video_url(uri)
    if verify == True:
        yt = YouTube(uri)
        main = yt.streams
        title = yt.title

        # videos
        video_resolution = [int(i.split("p")[0]) for i in (
            list(dict.fromkeys([i.resolution for i in yt.streams.filter(progressive=True).all() if i.resolution])))]
        # audio
        audio = yt.streams.filter(only_audio=True)
        uri = uri.replace("/", "|")
        return templates.TemplateResponse("info.html", context={"request": request, "resolutions": video_resolution, "title": title, "audio": audio, "uri": uri})
    else:
        return RedirectResponse("/tryagain")


# @app.get("/daudio/{abr}/{uri}")
# async def download(request: Request, abr: str, uri: str):
#     uri = uri.replace("|", "/")

#     file_path = f"audio/"

#     verify = check_video_url(uri)
#     if verify == True:
#         yt = YouTube(uri)
#         aud = yt.streams.filter(
#             only_audio=True, abr=abr).first().download(f"{file_path}/")

#         # print(aud)
#         return FileResponse(aud)
#     else:
#         return HTMLResponse("Internal Server error")


@app.get("/daudio")
async def download(request: Request, abr:str , uri:str):
    uri = request.query_params.get("uri")
    abr = request.query_params.get("abr")
    uri = uri.replace("|", "/")
    verify = check_video_url(uri)
    if verify == True:
        yt = YouTube(uri)
        audio_url = yt.streams.filter(only_audio=True, abr=abr).first().url
        title = yt.title
        return templates.TemplateResponse("embed.html", context={"request": request,"audio_url": audio_url, "title": title})
    else:
        return RedirectResponse("/tryagain")

@app.get("/dvideo")
async def download(request: Request, res: str, uri: str):
    uri = request.query_params.get("uri")
    uri = uri.replace("|", "/")

    print(uri)
    verify = check_video_url(uri)

    if verify == True:
        yt = YouTube(uri)
        video_url = yt.streams.filter(res=f'{res}p').first().url
        title = yt.title
        return templates.TemplateResponse("embed.html", context={"request": request,"video_url":video_url,"title":title})
    else:
        return RedirectResponse("/tryagain")


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return RedirectResponse("/tryagain")