import aiofiles

from entity import Advertisement
from settings import DATETIME_FORMAT, NOW


class HtmlWriter:
    def __init__(self) -> None:
        self.file = None

    async def __aenter__(self):
        now_formatted = NOW.strftime(DATETIME_FORMAT)
        self.file = await aiofiles.open(f"inzeraty-{now_formatted}.html", "w+")
        await self.file.write(BEFORE.format(date=now_formatted, title=now_formatted))
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
            location=ad.location,
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
    <p class="detail">location: {location}</p>
    <p class="detail">seen: {seen}</p>
</div>
"""

BEFORE = """
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <style>
  * {{
    box-sizing: border-box;
    font-family: "Trebuchet MS", Georgia, "Times New Roman", serif;
  }}
  html {{ font-size: 16px; }}
  body {{
    background: #f0f4ff;
    margin: 0;
    padding: 2rem 1rem;
  }}
  h1 {{
    font-size: 1.4rem;
    font-weight: 600;
    color: #1a1f36;
    letter-spacing: 0.04em;
    margin: 0 0 1.25rem;
  }}
  div.main-container {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    gap: 12px;
    padding: 0 1rem;
  }}
  div.item {{
    width: 100%;
    border-radius: 16px;
    border: 1px solid rgba(99, 130, 255, 0.15);
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    display: flex;
    flex-direction: column;
    padding: 18px 20px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    box-shadow: 0 2px 16px rgba(80, 100, 200, 0.07);
  }}
  div.item:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(80, 100, 200, 0.14);
    border-color: rgba(99, 130, 255, 0.35);
  }}
  div.item > h2 {{
    font-size: 0.975rem;
    font-weight: 600;
    margin: 0 0 0.5rem;
    color: #1a1f36;
    line-height: 1.5;
    text-wrap: balance;
  }}
  div.item > a {{
    font-size: 0.85rem;
    margin: 0 0 0.75rem;
    transition: color 0.2s ease;
    color: #5b6ef5;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    width: fit-content;
  }}
  div.item > a::after {{
    content: "↗";
    font-size: 0.75rem;
    transition: transform 0.2s ease;
  }}
  div.item > a:hover {{ color: #3a4fd4; }}
  div.item > a:hover::after {{ transform: translate(2px, -2px); }}
  div.item p.description {{
    font-size: 0.875rem;
    margin: 0 0 0.85rem;
    color: #4a5270;
    line-height: 1.7;
    text-wrap: pretty;
  }}
  .details {{
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
    padding-top: 10px;
    border-top: 1px solid rgba(99, 130, 255, 0.1);
  }}
  p.detail {{
    font-size: 0.75rem;
    color: #8a93b8;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 5px;
  }}
  p.detail::before {{
    content: '';
    display: inline-block;
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #c5cbf0;
    flex-shrink: 0;
  }}
  p {{ text-wrap: pretty; }}

  @media (max-width: 600px) {{
    body {{ padding: 1.25rem 0; }}
    div.main-container {{
      padding: 0 0.75rem;
      gap: 10px;
    }}
    h1 {{ font-size: 1.15rem; margin-bottom: 1rem; }}
    div.item {{
      border-radius: 12px;
      padding: 14px 16px;
    }}
    div.item > h2 {{ font-size: 0.9rem; }}
    div.item p.description {{ font-size: 0.825rem; }}
    div.item:hover {{ transform: none; }}
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
