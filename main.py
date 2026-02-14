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
NOTES_CACHE = {}

# --- SYSTEM SETUP (High Speed Connection) ---
client = TelegramClient(SESSION_NAME, API_ID, API_HASH, connection_retries=20, retry_delay=1)
routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

@routes.get('/health')
async def health_check(request):
    return web.Response(text="Alive", status=200)

# --- 1. HOME PAGE ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    
    content = ""
    if tab == 'lectures':
        for i in range(1, 158):
            content += """
            <div class="card" onclick="window.location.href='/player?id={ID}'">
                <div class="thumb">
                    <span class="thumb-id">{ID}</span>
                    <div class="play-btn"><svg viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M8 5v14l11-7z"/></svg></div>
                </div>
                <div class="info">
                    <div class="tag-row"><span class="tag">HINDI SAHITYA</span></div>
                    <h3 class="title">Lecture Class #{ID}</h3>
                    <p class="sub">PathshalaX • Full Coverage</p>
                </div>
            </div>""".replace("{ID}", str(i))
            
    elif tab == 'notes':
        ids = [i for i in range(202, 288) if i not in NOTES_CACHE]
        if ids:
            try:
                msgs = await client.get_messages(CHANNEL_USERNAME, ids=ids)
                for m in msgs:
                    if m and m.file: NOTES_CACHE[m.id] = m.file.name or f"Note_{m.id}"
            except: pass
            
        for i in range(202, 288):
            name = NOTES_CACHE.get(i, f"Class Note {i}")
            clean_name = name.replace('_', ' ').replace('.pdf', '')
            content += """
            <div class="note-card" onclick="window.location.href='/view/{ID}'">
                <div class="note-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="24" height="24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                </div>
                <div class="note-info"><h3>{NAME}</h3><p>PDF Document</p></div>
                <div class="arrow-btn">READ</div>
            </div>""".replace("{ID}", str(i)).replace("{NAME}", clean_name)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX</title>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #FFFFE3; --text: #4A4A4A; --slate: #6D8196; --yellow: #FFD600; --card-bg: #FFFFFF; }
            * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
            body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 100px; }
            .header { position: fixed; top: 0; width: 100%; z-index: 50; background: rgba(255, 255, 227, 0.95); backdrop-filter: blur(12px); padding: 15px 20px; border-bottom: 1px solid rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }
            .brand { font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }
            .profile-icon { width: 32px; height: 32px; background: var(--text); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; }
            .card-container { padding: 80px 20px 20px 20px; }
            .section-title { font-size: 18px; font-weight: 800; margin-bottom: 15px; color: var(--text); }
            .card { background: var(--card-bg); border-radius: 16px; padding: 12px; margin-bottom: 12px; display: flex; gap: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid transparent; transition: transform 0.1s; }
            .card:active { transform: scale(0.98); background: #fdfdfd; }
            .thumb { width: 100px; height: 75px; background: var(--text); border-radius: 12px; display: flex; align-items: center; justify-content: center; position: relative; color: var(--bg); }
            .thumb-id { font-size: 28px; font-weight: 800; opacity: 0.3; }
            .play-btn { position: absolute; width: 32px; height: 32px; background: var(--yellow); color: black; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
            .info { flex: 1; display: flex; flex-direction: column; justify-content: center; }
            .tag-row { margin-bottom: 6px; }
            .tag { font-size: 9px; font-weight: 800; background: #EDF2F7; color: var(--slate); padding: 3px 6px; border-radius: 4px; }
            .title { margin: 0; font-size: 15px; font-weight: 700; line-height: 1.3; color: var(--text); }
            .sub { margin: 4px 0 0 0; font-size: 11px; color: var(--slate); font-weight: 500; }
            .note-card { background: white; padding: 16px; border-radius: 16px; margin-bottom: 10px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.02); }
            .note-icon { width: 40px; height: 40px; background: #FFF4E5; color: #FF9800; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
            .note-info h3 { margin: 0; font-size: 14px; font-weight: 700; color: var(--text); }
            .note-info p { margin: 0; font-size: 11px; color: var(--slate); }
            .arrow-btn { margin-left: auto; font-size: 10px; font-weight: 800; background: var(--text); color: white; padding: 6px 12px; border-radius: 20px; }
            .nav-wrapper { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 100; }
            .pill-nav { background: white; height: 54px; border-radius: 100px; display: flex; align-items: center; padding: 4px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.05); gap: 8px; }
            .home-btn { width: 46px; height: 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #C4C4C4; text-decoration: none; transition: color 0.2s; }
            .home-btn.active { color: var(--text); background: #F5F5F5; }
            .check-btn { background: var(--yellow); height: 46px; border-radius: 100px; padding: 0 24px; display: flex; align-items: center; gap: 8px; text-decoration: none; color: black; font-weight: 800; font-size: 14px; letter-spacing: 0.5px; box-shadow: 0 4px 15px rgba(255, 214, 0, 0.25); }
            .footer { text-align: center; margin-top: 40px; font-size: 11px; font-weight: 700; color: var(--text); opacity: 0.4; }
        </style>
    </head>
    <body>
        <div class="header"><div class="brand">PathshalaX</div><div class="profile-icon">JS</div></div>
        <div class="card-container"><h2 class="section-title">{TITLE}</h2>{CONTENT}<div class="footer">Made with ♥️ By Jai Sharma</div></div>
        <div class="nav-wrapper">
            <div class="pill-nav">
                <a href="/?tab=lectures" class="home-btn {HOME_ACT}"><svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg></a>
                <a href="/?tab=notes" class="check-btn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>NOTES</a>
            </div>
        </div>
    </body>
    </html>
    """.replace("{CONTENT}", content)

    if tab == 'lectures': html = html.replace("{TITLE}", "Video Lectures").replace("{HOME_ACT}", "active")
    else: html = html.replace("{TITLE}", "Class Notes").replace("{HOME_ACT}", "")
    return web.Response(text=html, content_type='text/html')

# --- 2. PLAYER PAGE (WITH LOADING INDICATOR) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    desc = "Loading..."
    try:
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if msg and msg.message: desc = msg.message.replace('\n', '<br>')
    except: pass

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Playing Class</title>
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            :root { --bg: #FFFFE3; --text: #4A4A4A; --yellow: #FFD600; }
            body { margin: 0; background: var(--bg); font-family: 'Plus Jakarta Sans', sans-serif; }
            
            /* PLAYER CONTAINER */
            .player-container {
                position: sticky; top: 0; z-index: 100;
                width: 100%; aspect-ratio: 16/9; background: black;
                display: flex; align-items: center; justify-content: center;
            }
            media-player { width: 100%; height: 100%; }
            
            /* LOADING TEXT BEHIND PLAYER */
            .loading-text { position: absolute; color: white; font-size: 12px; font-weight: bold; opacity: 0.7; }

            /* HIDE DOWNLOAD */
            media-download-button { display: none !important; }

            .content { padding: 25px 20px; }
            .tag { background: var(--yellow); color: black; padding: 4px 8px; font-size: 10px; font-weight: 800; border-radius: 4px; }
            .title { font-size: 22px; font-weight: 800; color: var(--text); margin: 15px 0 5px 0; line-height: 1.2; }
            .sub { color: #6D8196; font-size: 14px; font-weight: 600; }
            .back-btn { display: block; margin: 20px 0; text-align: center; background: var(--text); color: white; padding: 12px; border-radius: 12px; font-weight: 700; text-decoration: none; }
            .desc-box { margin-top: 30px; background: white; padding: 20px; border-radius: 16px; font-size: 14px; color: var(--text); line-height: 1.6; border: 1px solid rgba(0,0,0,0.05); }
            .footer { text-align: center; margin-top: 30px; font-size: 12px; font-weight: 700; opacity: 0.5; }
        </style>
    </head>
    <body>
        <div class="player-container">
            <div class="loading-text">CONNECTING TO SERVER...</div>
            <media-player title="Class {CID}" src="/stream/{MID}" aspect-ratio="16/9" autoplay controlslist="nodownload">
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>

        <div class="content">
            <span class="tag">PREMIUM LECTURE</span>
            <h1 class="title">Hindi Sahitya Class #{CID}</h1>
            <p class="sub">PathshalaX • Full Chapter</p>
            <a href="/" class="back-btn">← Back to Classes</a>
            <div class="desc-box"><h3 style="margin-top:0; font-size:14px; font-weight:800; margin-bottom:10px;">LECTURE NOTES</h3>{DESC}</div>
            <div class="footer">Made with ♥️ By Jai Sharma</div>
        </div>
    </body>
    </html>
    """.replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    return web.Response(text=html, content_type='text/html')

@routes.get('/view/{id}')
async def view_pdf(request):
    msg_id = request.match_info['id']
    html = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{margin:0; height:100vh; display:flex; flex-direction:column; background:#222;}</style></head><body><div style="height:50px; background:#111; display:flex; align-items:center; justify-content:space-between; padding:0 20px; color:white; font-family:sans-serif;"><span style="font-weight:bold; font-size:14px;">Secure Viewer</span><a href="/?tab=notes" style="color:#FFD600; text-decoration:none; font-size:12px; font-weight:bold;">CLOSE</a></div><iframe src="/stream/{MID}#toolbar=0" style="flex:1; border:none;"></iframe></body></html>""".replace("{MID}", msg_id)
    return web.Response(text=html, content_type='text/html')

# --- 3. TURBO STREAMING ENGINE (64KB CHUNKS) ---
@routes.get('/stream/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        mime = "video/mp4" if 'video' in (msg.file.mime_type or "") else (msg.file.mime_type or "application/octet-stream")

        range_header = request.headers.get('Range')
        from_bytes, until_bytes = 0, file_size - 1
        if range_header:
            try:
                parts = range_header.replace('bytes=', '').split('-')
                from_bytes = int(parts[0])
                if len(parts) > 1 and parts[1]: until_bytes = int(parts[1])
            except: pass
        
        chunk_size = (until_bytes - from_bytes) + 1
        headers = {
            'Content-Type': mime,
            'Content-Range': f'bytes {from_bytes}-{until_bytes}/{file_size}',
            'Content-Length': str(chunk_size),
            'Content-Disposition': 'inline', 
            'Accept-Ranges': 'bytes',
        }
        resp = web.StreamResponse(status=206 if range_header else 200, headers=headers)
        await resp.prepare(request)

        # TURBO MODE: 64KB chunks for instant start on slow networks
        async for chunk in client.iter_download(msg.media, offset=from_bytes, request_size=64*1024):
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
    print(f"🚀 TURBO SERVER: {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
