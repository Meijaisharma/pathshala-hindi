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

# --- HOME PAGE WITH INK WASH THEME ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    
    content = ""
    if tab == 'lectures':
        for i in range(1, 158):
            content += """
            <div class="class-card" onclick="window.location.href='/player?id={ID}'">
                <div class="thumb-section">
                    <span class="thumb-number">{ID}</span>
                    <div class="play-icon">▶</div>
                </div>
                <div class="info-section">
                    <div class="tags">
                        <span class="tag subject">HINDI SAHITYA</span>
                        <span class="tag live">RECORDED</span>
                    </div>
                    <h3 class="class-title">Lecture Class #{ID}</h3>
                    <p class="class-subtitle">Full Coverage • PathshalaX Faculty</p>
                    <div class="status-bar">
                        <div class="progress-line"></div>
                        <span class="status-text">Start Watching</span>
                    </div>
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
                <div class="note-icon">📄</div>
                <div class="note-info">
                    <h3>{NAME}</h3>
                    <p>PDF Document</p>
                </div>
                <div class="arrow-btn">View</div>
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
            :root {
                --bg: #FFFFE3; /* Cream from Ink Wash */
                --text-dark: #4A4A4A; /* Dark Grey */
                --text-light: #6D8196; /* Slate Blue */
                --card-bg: #FFFFFF;
                --accent-yellow: #FFD600; /* Yellow Button */
                --border: #E5E5E5;
            }
            * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
            body { 
                font-family: 'Plus Jakarta Sans', sans-serif; 
                background-color: var(--bg); 
                color: var(--text-dark);
                margin: 0; padding-bottom: 100px;
            }

            /* Header */
            .header {
                position: fixed; top: 0; width: 100%; z-index: 50;
                background: rgba(255, 255, 227, 0.95);
                backdrop-filter: blur(10px);
                padding: 15px 20px;
                border-bottom: 1px solid rgba(0,0,0,0.05);
                display: flex; justify-content: space-between; align-items: center;
            }
            .brand { font-size: 20px; font-weight: 800; color: var(--text-dark); letter-spacing: -0.5px; }
            .profile { w-8 h-8 rounded-full bg-gray-200; }

            /* Cards (Unacademy Style) */
            .class-card {
                background: var(--card-bg);
                border-radius: 16px;
                padding: 12px;
                margin-bottom: 12px;
                display: flex; gap: 15px;
                border: 1px solid transparent;
                box-shadow: 0 2px 10px rgba(0,0,0,0.03);
                transition: all 0.2s;
            }
            .class-card:active { transform: scale(0.98); background: #fafafa; }
            
            .thumb-section {
                width: 100px; height: 75px;
                background: #4A4A4A;
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                position: relative;
                color: #FFFFE3;
            }
            .thumb-number { font-size: 24px; font-weight: 800; opacity: 0.5; }
            .play-icon { 
                position: absolute; width: 30px; height: 30px; 
                background: var(--accent-yellow); color: black;
                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                font-size: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }

            .info-section { flex: 1; display: flex; flex-direction: column; justify-content: center; }
            .tags { display: flex; gap: 6px; margin-bottom: 4px; }
            .tag { font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 4px; }
            .tag.subject { background: #EDF2F7; color: var(--text-light); }
            .tag.live { background: #FFE4E6; color: #E11D48; }
            
            .class-title { margin: 0; font-size: 15px; font-weight: 700; color: var(--text-dark); line-height: 1.3; }
            .class-subtitle { margin: 2px 0 8px 0; font-size: 11px; color: var(--text-light); font-weight: 500; }
            
            .status-bar { display: flex; align-items: center; gap: 6px; }
            .progress-line { height: 3px; background: #E2E8F0; flex: 1; border-radius: 2px; }
            .status-text { font-size: 10px; font-weight: 600; color: var(--accent-yellow); text-shadow: 0 0 1px black;}

            /* Notes */
            .note-card {
                background: white; padding: 16px; border-radius: 16px;
                margin-bottom: 10px; display: flex; align-items: center; gap: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            }
            .note-icon { font-size: 24px; }
            .note-info h3 { margin: 0; font-size: 14px; font-weight: 600; color: var(--text-dark); }
            .note-info p { margin: 0; font-size: 11px; color: var(--text-light); }
            .arrow-btn { margin-left: auto; font-size: 11px; font-weight: 700; color: #6D8196; }

            /* Bottom Nav (Pill Style) */
            .floating-nav {
                position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%);
                background: white;
                padding: 6px;
                border-radius: 50px;
                display: flex; gap: 8px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.1);
                border: 1px solid rgba(0,0,0,0.05);
                z-index: 100;
            }
            .nav-item {
                padding: 10px 24px;
                border-radius: 40px;
                font-size: 14px; font-weight: 700;
                text-decoration: none;
                transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
                display: flex; align-items: center; gap: 6px;
            }
            /* Inactive State */
            .nav-item.inactive { color: #9CA3AF; background: transparent; }
            
            /* Active State (Yellow Pill) */
            .nav-item.active {
                background: var(--accent-yellow);
                color: black;
                box-shadow: 0 4px 15px rgba(255, 214, 0, 0.3);
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="brand">PathshalaX</div>
            <div style="width:32px; height:32px; background:#4A4A4A; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-size:12px;">JS</div>
        </div>

        <div style="padding: 80px 20px 20px 20px;">
            <h2 style="font-size:18px; font-weight:800; margin-bottom:15px; color:#4A4A4A;">{TITLE}</h2>
            {CONTENT}
        </div>

        <!-- FLOATING PILL NAV -->
        <div class="floating-nav">
            <a href="/?tab=lectures" class="nav-item {ACT_LEC}">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            </a>
            <a href="/?tab=notes" class="nav-item {ACT_NOTE}">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                CHECK
            </a>
        </div>
    </body>
    </html>
    """.replace("{CONTENT}", content)

    if tab == 'lectures': html = html.replace("{TITLE}", "Recommended Classes").replace("{ACT_LEC}", "active").replace("{ACT_NOTE}", "inactive")
    else: html = html.replace("{TITLE}", "Class Materials").replace("{ACT_LEC}", "inactive").replace("{ACT_NOTE}", "active")
    
    return web.Response(text=html, content_type='text/html')
# --- PLAYER PAGE (NO DOWNLOAD) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    
    desc = "Loading description..."
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
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            body { margin:0; background: #FFFFE3; font-family: 'Plus Jakarta Sans', sans-serif; }
            .video-container { position: sticky; top: 0; background: black; z-index: 100; width: 100%; }
            .content { padding: 20px; }
            .badge { background: #FFD600; color: black; padding: 4px 8px; font-size: 10px; font-weight: 800; border-radius: 4px; text-transform: uppercase; }
            .title { font-size: 22px; font-weight: 800; color: #4A4A4A; margin: 10px 0 5px 0; line-height: 1.2; }
            .sub { color: #6D8196; font-size: 13px; font-weight: 600; }
            .desc-box { margin-top: 25px; background: white; padding: 20px; border-radius: 16px; font-size: 14px; color: #4A4A4A; line-height: 1.6; border: 1px solid rgba(0,0,0,0.05); }
            /* Hiding Download Button in Native Controls if any */
            video::-internal-media-controls-download-button { display:none; }
            video::-webkit-media-controls-enclosure { overflow:hidden; }
            video::-webkit-media-controls-panel { width: calc(100% + 30px); }
        </style>
    </head>
    <body>
        <div class="video-container">
            <!-- No Download Attributes added -->
            <media-player src="/stream/{MID}" aspect-ratio="16/9" autoplay controlslist="nodownload">
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>
        <div class="content">
            <span class="badge">Premium Class</span>
            <h1 class="title">Hindi Sahitya Class #{CID}</h1>
            <p class="sub">PathshalaX • Full Chapter</p>
            
            <div class="desc-box">
                <h3 style="margin-top:0; font-size:14px; font-weight:800; color:#4A4A4A;">LECTURE NOTES</h3>
                {DESC}
            </div>
            
            <div style="text-align:center; margin-top:30px; font-size:11px; font-weight:700; color:#CBCBCB;">
                PROTECTED CONTENT • NO DOWNLOAD
            </div>
        </div>
    </body>
    </html>
    """.replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    return web.Response(text=html, content_type='text/html')

# --- PDF VIEWER ---
@routes.get('/view/{id}')
async def view_pdf(request):
    msg_id = request.match_info['id']
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>body{margin:0; height:100vh; display:flex; flex-direction:column; background:#4A4A4A;}</style>
    </head>
    <body>
        <div style="height:50px; background:#333; display:flex; align-items:center; px:20px; color:white; justify-content:space-between; padding:0 20px;">
            <span style="font-family:sans-serif; font-weight:bold; font-size:14px;">Secure View</span>
            <a href="/?tab=notes" style="color:#CBCBCB; text-decoration:none; font-size:12px;">CLOSE</a>
        </div>
        <iframe src="/stream/{MID}#toolbar=0" style="flex:1; border:none;"></iframe>
    </body>
    </html>""".replace("{MID}", msg_id)
    return web.Response(text=html, content_type='text/html')

# --- SECURE STREAMER (FORCE NO DOWNLOAD) ---
@routes.get('/stream/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        # Force Inline (Browser will try to play/view, not save)
        mime = msg.file.mime_type or "application/octet-stream"
        
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
            'Content-Disposition': 'inline', # <--- THIS STOPS AUTO DOWNLOAD
            'Accept-Ranges': 'bytes',
        }
        
        resp = web.StreamResponse(status=206 if range_header else 200, headers=headers)
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
    print(f"🚀 SECURE SERVER: {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
