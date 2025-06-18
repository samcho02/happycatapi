from app.schemas.gifs import GIFcollection, GIFmodel
from pydantic import HttpUrl

gifs_dict = {
    "happycat": {
        "id": "0",
        "tag": ["happycat"],
        "url": "https://tenor.com/bXAn9.gif"
    },
    "carla": {
        "id": "1",
        "tag": ["carla"],
        "url": "https://tenor.com/rJ4PNMf6dC5.gif"
    },
    "ripcarla": {
        "id": "2",
        "tag": ["ripcarla"],
        "url": "https://tenor.com/b78eKUM95k3.gif"
    },
    "huhcat": {
        "id": "3",
        "tag": ["huhcat"],
        "url": "https://tenor.com/sqMU1WMDcgD.gif"
    },
    "chipichipi": {
        "id": "4",
        "tag": ["chipichipi"],
        "url": "https://tenor.com/dpqqxee0PFw.gif"
    },
    "hdldance": {
        "id": "5",
        "tag": ["hdldance"],
        "url": "https://tenor.com/sKMxKWD1BOs.gif"
    },
    "heyyoucat": {
        "id": "6",
        "tag": ["heyyoucat"],
        "url": "https://tenor.com/mpDJICZ3lTJ.gif"
    },
    "oiia": {
        "id": "7",
        "tag": ["oiia"],
        "url": "https://tenor.com/fFr2do9u7Kw.gif"
    },
    "crunchycat": {
        "id": "8",
        "tag": ["crunchyc"],
        "url": "https://tenor.com/qPlYb0nisbU.gif"
    },
    "maxwell": {
        "id": "9",
        "tag": ["maxwell"],
        "url": "https://tenor.com/cNWODIeA4CV.gif"
    },
    "applecat": {
        "id": "10",
        "tag": ["applecat"],
        "url": "https://tenor.com/bpwiu.gif"
    },
    "bananacatcry": {
        "id": "11",
        "tag": ["bananacatcry"],
        "url": "https://tenor.com/bpwiu.gif"
    },
    "bananacatwalk": {
        "id": "12",
        "tag": ["bananacatwalk"],
        "url": "https://tenor.com/G15XUSxrbT.gif"
    },
    "orangelolcat": {
        "id": "13",
        "tag": ["applecat"],
        "url": "https://tenor.com/ft2fuNAbJ2T.gif"
    },
    "sickcat": {
        "id": "14",
        "tag": ["sickcat"],
        "url": "https://tenor.com/safyMl4za99.gif"
    },
    "blinkcat": {
        "id": "15",
        "tag": ["blinkcat"],
        "url": "https://tenor.com/fLz7Y2ikd98.gif"
    },
}

gifs_test_db = GIFcollection(gifs=[
    GIFmodel(
        name=key,
        id=value["id"],
        url=value["url"],
        tag=value["tag"]
    ) for key, value in gifs_dict.items()
])