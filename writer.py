import aiofiles

from entity import Advertisement
from settings import DATETIME_FORMAT, NOW


class HtmlWriter:
    def __init__(self) -> None:
        self.file = None

    async def __aenter__(self):
        now_formatted = NOW.strftime(DATETIME_FORMAT)
        self.file = await aiofiles.open(f"inzeraty-{now_formatted}.html", "w+")
        await self.file.write(BEFORE.format(date=now_formatted))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.file is not None:
            await self.file.write(AFTER)
            await self.file.close()

    async def add_advertisement(self, ad: Advertisement):
        if self.file is None:
            raise RuntimeError("open writer before adding advertisements!")
        await self.file.write(self.render_advertisement(ad))

    @staticmethod
    def render_advertisement(ad: Advertisement) -> str:
        return AD_TEMPLATE.format(
            title=ad.title,
            url=ad.url,
            description=ad.description,
            name=ad.name,
            seen=ad.seen,
        )


AD_TEMPLATE = """
<div class="item">
    <h2>
        {title}
    </h2>
    <a href="{url}" target="_blank">click to open</a>
    <p class="description">
        {description}
    </p>
    <p class="detail">name: {name}</p>
    <p class="detail">seen: {seen}</p>
</div>
"""

BEFORE = """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
        <style>
            * {{
                box-sizing: border-box;
                font-family: "Trebuchet MS", Georgia, "Times New Roman", serif;
            }}
            html {{
                font-size: 16px;
            }}

            h1 {{
                font-size: 1.5em;
            }}

            div.main-container {{
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                max-width: 70%;
                margin: 0 auto;
                gap: 10px;
            }}

            div.item {{
                width: 100%;
                border-radius: 5px;
                border: 1px solid black;
                background-color: rgb(216, 250, 255);
                display: flex;
                flex-direction: column;
                justify-content: left;
                padding: 10px 10px;
                transition: 0.3s;
                box-shadow: 0 0 40px rgba(0, 0, 0, 0.2);
            }}

            div.item:hover {{
                background-color: rgb(179, 252, 150);
            }}

            div.item > h2 {{
                font-size: 1rem;
                margin: 0 0 0.5rem;
            }}

            div.item > a {{
                font-size: 1rem;
                margin: 0 0 0.7rem;
                transition: 0.3s;
            }}

            div.item > a:hover {{
                color: red;
            }}

            div.item p.description {{
                font-size: 0.9rem;
                margin: 0 0 0.7rem;
            }}

            p.detail {{
                font-size: 0.8rem;
                color: gray;
                margin: 0 0;
            }}

            p {{
                text-wrap: calc();
            }}
        </style>
    </head>
    <body>
        <div class="main-container">
            <h1>Inzeraty ziskany {date}</h1>
"""

AFTER = """
        </div>
    </body>
</html>
"""
