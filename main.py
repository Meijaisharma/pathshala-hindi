import os
import asyncio
from telethon import TelegramClient
from aiohttp import web
import aiohttp_cors

# --- CONFIGURATION ---
API_ID = 34092408
API_HASH = "13bdb62f6a9424169574109474cd6bde"
SESSION_NAME = "PathshalaSession"
CHANNEL_USERNAME = "pathshalax"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH, connection_retries=5, retry_delay=1)
routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

@routes.get('/health')
async def health_check(request):
    return web.Response(text="Alive", status=200)

# --- 1. HOME PAGE (INK WASH PALETTE) ---
@routes.get('/')
async def index_page(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #FFFFE3; /* Cream Background */
                --text: #4A4A4A; /* Dark Grey */
                --sub-text: #6D8196; /* Slate Blue */
                --card-bg: #FFFFFF;
                --accent: #FFD600; /* Yellow */
            }
            body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; }
            
            /* HEADER */
            .header {
                position: fixed; top: 0; width: 100%; z-index: 50;
                background: rgba(255, 255, 227, 0.95);
                backdrop-filter: blur(10px);
                padding: 15px 20px;
                border-bottom: 1px solid rgba(0,0,0,0.05);
                display: flex; justify-content: space-between; align-items: center;
            }
            .brand { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
            .badge { background: var(--accent); color: black; font-size: 10px; font-weight: 700; padding: 4px 8px; border-radius: 6px; }

            /* CARDS */
            .card-container { padding: 80px 20px 20px 20px; }
            .card {
                background: var(--card-bg); border-radius: 16px; padding: 12px; margin-bottom: 12px;
                display: flex; gap: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.02);
                transition: transform 0.2s; cursor: pointer;
            }
            .card:active { transform: scale(0.98); }
            
            .thumb {
                width: 90px; height: 70px; background: var(--text); border-radius: 12px;
                display: flex; align-items: center; justify-content: center; position: relative; color: var(--bg);
            }
            .thumb-id { font-size: 24px; font-weight: 800; opacity: 0.5; }
            .play-btn {
                position: absolute; width: 28px; height: 28px; background: var(--accent);
                color: black; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                font-size: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }

            .info { flex: 1; display: flex; flex-direction: column; justify-content: center; }
            .tag { font-size: 9px; font-weight: 700; color: var(--sub-text); background: #EDF2F7; padding: 2px 6px; border-radius: 4px; width: fit-content; margin-bottom: 4px; }
            .title { margin: 0; font-size: 15px; font-weight: 700; line-height: 1.3; }
            .sub { margin: 2px 0 0 0; font-size: 11px; color: var(--sub-text); }

            /* BOTTOM NAV */
            .nav-bar {
                position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
                background: var(--card-bg); padding: 6px; border-radius: 50px;
                display: flex; gap: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); z-index: 100;
            }
            .nav-item {
                padding: 10px 24px; border-radius: 40px; font-size: 14px; font-weight: 700;
                text-decoration: none; display: flex; align-items: center; gap: 6px; color: #9CA3AF;
            }
            .nav-item.active { background: var(--accent); color: black; box-shadow: 0 4px 15px rgba(255, 214, 0, 0.3); }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">PathshalaX</div>
            <div class="badge">PREMIUM</div>
        </div>

        <div class="card-container">
            <h2 style="font-size:18px; font-weight:800; margin-bottom:15px; color:var(--text);">Video Lectures</h2>
            <!-- CARDS INJECTED HERE -->
            {CARDS}
            <div style="text-align:center; margin-top:40px; font-size:12px; font-weight:700; opacity:0.5;">Made with ♥️ By Jai Sharma</div>
        </div>

        <div class="nav-bar">
            <a href="/" class="nav-item active">📺 Classes</a>
            <a href="#" class="nav-item">📝 Notes</a>
        </div>
    </body>
    </html>
    """
    
    cards = ""
    for i in range(1, 158):
        cards += """
        <div class="card" onclick="window.location.href='/player?id={ID}'">
            <div class="thumb">
                <span class="thumb-id">{ID}</span>
                <div class="play-btn">▶</div>
            </div>
            <div class="info">
                <span class="tag">HINDI SAHITYA</span>
                <h3 class="title">Lecture Class #{ID}</h3>
                <p class="sub">PathshalaX Faculty</p>
            </div>
        </div>""".replace("{ID}", str(i))

    return web.Response(text=html.replace("{CARDS}", cards), content_type='text/html')

# --- 2. PLAYER PAGE (VLC/PLAYIT STYLE TOOLS via VIDSTACK) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    
    desc = "Loading details..."
    try:
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if msg and msg.message: desc = msg.message.replace('\n', '<br>')
    except: pass

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Playing Class</title>
        <!-- VIDSTACK (THE BEST PLAYER ENGINE) -->
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #FFFFE3; --text: #4A4A4A; --sub: #6D8196; --accent: #FFD600; }
            body { margin: 0; background: var(--bg); font-family: 'Plus Jakarta Sans', sans-serif; }
            
            /* STICKY PLAYER */
            .player-wrapper {
                position: sticky; top: 0; z-index: 100; background: black; width: 100%; aspect-ratio: 16/9;
            }
            media-player { height: 100%; width: 100%; }

            .content { padding: 25px 20px; }
            .tag { background: var(--accent); color: black; padding: 4px 8px; font-size: 10px; font-weight: 800; border-radius: 4px; }
            .title { font-size: 22px; font-weight: 800; color: var(--text); margin: 15px 0 5px 0; line-height: 1.2; }
            .sub { color: var(--sub); font-size: 14px; font-weight: 600; }
            
            .desc-box { 
                margin-top: 30px; background: white; padding: 20px; 
                border-radius: 16px; font-size: 14px; color: var(--text); 
                line-height: 1.6; border: 1px solid rgba(0,0,0,0.05); 
            }
            .footer { text-align: center; margin-top: 40px; font-size: 12px; font-weight: 700; opacity: 0.5; }
        </style>
    </head>
    <body>
        <div class="player-wrapper">
            <media-player title="Class {CID}" src="/stream/{MID}" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <!-- LAYOUT: Enables Gestures, Speed, Quality, PIP (Like Playit/VLC) -->
                <media-video-layout></media-video-layout>
            </media-player>
        </div>

        <div class="content">
            <span class="tag">PREMIUM LECTURE</span>
            <h1 class="title">Hindi Sahitya Class #{CID}</h1>
            <p class="sub">PathshalaX • Full Chapter</p>
            
            <div class="desc-box">
                <h3 style="margin-top:0; font-size:14px; font-weight:800; margin-bottom:10px;">LECTURE NOTES</h3>
                {DESC}
            </div>

            <div class="footer">Made with ♥️ By Jai Sharma</div>
        </div>
    </body>
    </html>
    """.replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    return web.Response(text=html, content_type='text/html')

# --- 3. STREAMING ENGINE ---
@routes.get('/stream/{id}')
async def stream_video(request):
    try:
        msg_id = int(request.match_info['id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)

        file_size = msg.file.size
        range_header = request.headers.get('Range')
        from_bytes, until_bytes = 0, file_size - 1
        
        if range_header:
            try:
                bytes_range = range_header.replace('bytes=', '').split('-')
                from_bytes = int(bytes_range[0])
                if len(bytes_range) > 1 and bytes_range[1]: until_bytes = int(bytes_range[1])
            except: pass
        
        chunk_size = (until_bytes - from_bytes) + 1
        headers = {
            'Content-Type': 'video/mp4',
            'Content-Range': f'bytes {from_bytes}-{until_bytes}/{file_size}',
            'Accept-Ranges': 'bytes',
            'Content-Length': str(chunk_size),
        }
        resp = web.StreamResponse(status=206, headers=headers)
        await resp.prepare(request)

        async for chunk in client.iter_download(msg.media, offset=from_bytes, request_size=512*1024):
            try: await resp.write(chunk)
            except: break
            from_bytes += len(chunk)
            if from_bytes > until_bytes: break
        return resp
    except: return web.Response(status=500)

async def main():
    await client.start()
    app = web.Application()
    app.add_routes(routes)
    cors = aiohttp_cors.setup(app, defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")})
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🚀 INK WASH SERVER: {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
