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

# --- CACHE FOR NOTES NAMES (Taaki baar baar load na ho) ---
NOTES_CACHE = {}

# --- SYSTEM SETUP ---
client = TelegramClient(SESSION_NAME, API_ID, API_HASH, connection_retries=5, retry_delay=1)
routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

# --- HEALTH CHECK ---
@routes.get('/health')
async def health_check(request):
    return web.Response(text="Alive", status=200)

# --- 1. HOME PAGE (iOS MASTERPIECE) ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    
    # --- LECTURES LOGIC ---
    content_html = ""
    if tab == 'lectures':
        for i in range(1, 158):
            content_html += """
            <div class="ios-card animate-slide-up" onclick="window.location.href='/player?id={ID}'">
                <div class="thumb-container">
                    <div class="thumb-gradient">
                        <span class="thumb-text">{ID}</span>
                        <div class="hd-badge">HD</div>
                    </div>
                    <div class="play-overlay">
                        <svg class="w-8 h-8 text-white fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                    </div>
                </div>
                <div class="card-info">
                    <span class="tag-category">HINDI LITERATURE</span>
                    <h3 class="card-title">Class Lecture #{ID}</h3>
                    <div class="card-meta">
                        <span class="text-blue-600 font-semibold flex items-center gap-1">
                            Play Now <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </span>
                    </div>
                </div>
            </div>""".replace("{ID}", str(i))

    # --- NOTES LOGIC (REAL NAME FETCHING) ---
    elif tab == 'notes':
        # Batch fetch IDs 202 to 287
        ids_to_fetch = []
        start_id = 202
        end_id = 287
        
        # Check cache first
        for i in range(start_id, end_id + 1):
            if i not in NOTES_CACHE:
                ids_to_fetch.append(i)
        
        # Fetch missing names from Telegram
        if ids_to_fetch:
            try:
                msgs = await client.get_messages(CHANNEL_USERNAME, ids=ids_to_fetch)
                for m in msgs:
                    if m and m.file:
                        NOTES_CACHE[m.id] = m.file.name or f"Class_Note_{m.id}.pdf"
                    else:
                        NOTES_CACHE[m.id] = f"Note_{m.id}_Unavailable"
            except: pass

        # Generate HTML
        for i in range(start_id, end_id + 1):
            name = NOTES_CACHE.get(i, f"Loading Note {i}...")
            # Clean name
            clean_name = name.replace('_', ' ').replace('.pdf', '')
            
            content_html += """
            <div class="ios-list-item animate-slide-up" onclick="window.location.href='/view/{ID}'">
                <div class="icon-box bg-red-50 text-red-500">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
                </div>
                <div class="list-info">
                    <h3 class="list-title">{NAME}</h3>
                    <p class="list-sub">PDF Document • Read Now</p>
                </div>
                <div class="action-arrow">
                    <svg class="w-5 h-5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
                </div>
            </div>""".replace("{ID}", str(i)).replace("{NAME}", clean_name)

    # --- MAIN HTML STRUCTURE ---
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX Premium</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-color: #F2F2F7;
                --card-bg: #FFFFFF;
                --primary: #007AFF;
                --text-main: #1C1C1E;
                --text-sub: #8E8E93;
            }
            body { 
                font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif; 
                background-color: var(--bg-color); 
                color: var(--text-main);
                padding-bottom: 90px;
                -webkit-tap-highlight-color: transparent;
            }

            /* Glassmorphism Header */
            .glass-header {
                position: fixed; top: 0; width: 100%; z-index: 50;
                background: rgba(255, 255, 255, 0.85);
                backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
                border-bottom: 0.5px solid rgba(0,0,0,0.1);
                padding: 10px 20px;
                padding-top: max(10px, env(safe-area-inset-top));
            }

            /* Cards (Video) */
            .ios-card {
                background: var(--card-bg);
                border-radius: 20px;
                margin-bottom: 16px;
                padding: 12px;
                display: flex;
                gap: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.03);
                transition: transform 0.2s ease;
            }
            .ios-card:active { transform: scale(0.97); }

            .thumb-container {
                position: relative; width: 110px; height: 80px; border-radius: 14px; overflow: hidden;
            }
            .thumb-gradient {
                width: 100%; height: 100%;
                background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
                display: flex; align-items: center; justify-content: center;
            }
            .thumb-text { color: white; font-weight: 800; font-size: 28px; opacity: 0.9; }
            .hd-badge {
                position: absolute; bottom: 4px; right: 4px;
                background: rgba(0,0,0,0.6); color: white;
                font-size: 8px; font-weight: 700; padding: 2px 4px; border-radius: 4px;
            }
            .play-overlay {
                position: absolute; inset: 0; background: rgba(0,0,0,0.2);
                display: flex; align-items: center; justify-content: center; opacity: 0;
            }

            .card-info { flex: 1; display: flex; flex-col; justify-content: center; }
            .tag-category { font-size: 9px; font-weight: 700; color: #FF2D55; uppercase; letter-spacing: 0.5px; }
            .card-title { font-size: 16px; font-weight: 600; margin-top: 2px; line-height: 1.3; }
            .card-meta { margin-top: auto; padding-top: 6px; }

            /* List Items (Notes) */
            .ios-list-item {
                background: var(--card-bg);
                border-radius: 16px;
                padding: 16px;
                margin-bottom: 12px;
                display: flex; align-items: center; gap: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            }
            .icon-box { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
            .list-info { flex: 1; }
            .list-title { font-size: 14px; font-weight: 600; color: #000; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical; overflow: hidden; }
            .list-sub { font-size: 12px; color: #8E8E93; margin-top: 2px; }

            /* Animations */
            @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
            .animate-slide-up { animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

            /* Bottom Tab Bar (The Magic) */
            .tab-bar {
                position: fixed; bottom: 0; width: 100%;
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
                border-top: 0.5px solid rgba(0,0,0,0.1);
                display: flex; justify-content: space-around;
                padding: 8px 0;
                padding-bottom: max(8px, env(safe-area-inset-bottom));
                z-index: 100;
            }
            .tab-btn {
                display: flex; flex-direction: column; align-items: center;
                text-decoration: none; color: #999999;
                font-size: 10px; font-weight: 500;
                transition: color 0.2s;
            }
            .tab-btn svg { width: 26px; height: 26px; margin-bottom: 4px; transition: transform 0.2s; }
            .tab-btn.active { color: #007AFF; }
            .tab-btn.active svg { transform: translateY(-2px); }

        </style>
    </head>
    <body>

        <!-- HEADER -->
        <div class="glass-header flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-bold tracking-tight">PathshalaX</h1>
                <p class="text-xs text-gray-500 font-medium">Hindi Sahitya Premium</p>
            </div>
            <div class="w-8 h-8 rounded-full bg-gray-200 overflow-hidden border border-gray-300">
                <img src="https://ui-avatars.com/api/?name=Jai+Sharma&background=0D8ABC&color=fff" />
            </div>
        </div>

        <!-- SPACER FOR HEADER -->
        <div class="h-24"></div>

        <!-- CONTENT -->
        <div class="px-5 pb-5">
            <h2 class="text-lg font-bold text-gray-900 mb-4">{TITLE}</h2>
            {CONTENT}
        </div>

        <!-- TAB BAR -->
        <div class="tab-bar">
            <a href="/?tab=lectures" class="tab-btn {ACT_LEC}">
                <svg viewBox="0 0 24 24" fill="{FILL_LEC}" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Classes
            </a>
            <a href="/?tab=notes" class="tab-btn {ACT_NOTE}">
                <svg viewBox="0 0 24 24" fill="{FILL_NOTE}" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                Notes
            </a>
        </div>

    </body>
    </html>
    """.replace("{CONTENT}", content_html)

    # Dynamic Replacements
    if tab == 'lectures':
        html = html.replace("{TITLE}", "Recent Live Classes").replace("{ACT_LEC}", "active").replace("{ACT_NOTE}", "").replace("{FILL_LEC}", "currentColor").replace("{FILL_NOTE}", "none")
    else:
        html = html.replace("{TITLE}", "Study Material").replace("{ACT_LEC}", "").replace("{ACT_NOTE}", "active").replace("{FILL_LEC}", "none").replace("{FILL_NOTE}", "currentColor")

    return web.Response(text=html, content_type='text/html')

# --- 2. PLAYER PAGE (VIDEO FIRST) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    
    # Metadata Fetch
    desc = "Loading description..."
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
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
        <style>
            body { background: white; font-family: -apple-system, sans-serif; padding-bottom: 50px; }
            .sticky-player { position: sticky; top: 0; z-index: 100; background: black; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
            .action-btn { display: flex; flex-direction: column; align-items: center; gap: 4px; font-size: 11px; color: #555; font-weight: 500; }
            .action-icon { width: 40px; height: 40px; border-radius: 50%; background: #F2F2F7; display: flex; align-items: center; justify-content: center; }
        </style>
    </head>
    <body>
        
        <!-- VIDEO PLAYER (STICKY) -->
        <div class="sticky-player">
            <media-player title="Hindi Sahitya Class {CID}" src="/stream/{MID}" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>

        <!-- CONTENT -->
        <div class="px-5 py-6">
            
            <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">PREMIUM LECTURE</span>
            <h1 class="text-2xl font-bold text-gray-900 mt-3 leading-tight">Hindi Sahitya Optional - Class #{CID}</h1>
            <p class="text-sm text-gray-500 mt-1">PathshalaX • Full Coverage</p>

            <!-- ACTION BAR (YouTube Style) -->
            <div class="flex justify-around mt-6 border-b border-gray-100 pb-6">
                <a href="/download/{MID}" class="action-btn">
                    <div class="action-icon">
                        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    </div>
                    Download
                </a>
                <div class="action-btn">
                    <div class="action-icon">
                        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"/></svg>
                    </div>
                    Share
                </div>
                <a href="/" class="action-btn">
                    <div class="action-icon">
                        <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
                    </div>
                    Back
                </a>
            </div>

            <!-- DESCRIPTION -->
            <div class="mt-6">
                <h3 class="font-bold text-gray-900 mb-2">Lecture Notes & Description</h3>
                <div class="bg-gray-50 p-4 rounded-xl text-sm text-gray-700 leading-relaxed font-mono whitespace-pre-wrap border border-gray-100">
                    {DESC}
                </div>
            </div>

            <div class="mt-12 text-center">
                 <p class="text-[10px] font-bold text-gray-300 uppercase">Made with ♥️ By Jai Sharma</p>
            </div>
        </div>
    </body>
    </html>
    """.replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    
    return web.Response(text=html, content_type='text/html')

# --- 3. GOOGLE DRIVE STYLE PDF VIEWER ---
@routes.get('/view/{id}')
async def view_pdf(request):
    msg_id = request.match_info['id']
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reading Note</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body, html { height: 100%; margin: 0; overflow: hidden; background: #202124; }</style>
    </head>
    <body>
        <div class="h-[56px] bg-[#202124] flex items-center justify-between px-4 border-b border-gray-700">
            <h1 class="text-white font-medium text-sm truncate">Document Preview</h1>
            <div class="flex gap-3">
                <a href="/download/{MID}" class="text-blue-400 text-sm font-bold">Save</a>
                <a href="/?tab=notes" class="text-gray-400 text-sm">Close</a>
            </div>
        </div>
        <iframe src="/stream/{MID}" width="100%" height="100%" style="border:none;"></iframe>
    </body>
    </html>
    """.replace("{MID}", msg_id)
    return web.Response(text=html, content_type='text/html')

# --- 4. STREAMING ENGINE ---
@routes.get('/stream/{msg_id}')
@routes.get('/download/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        mime_type = msg.file.mime_type or "application/octet-stream"
        name = msg.file.name or f"File_{msg_id}"
        
        disposition = 'inline'
        if 'download' in request.path: disposition = f'attachment; filename="{name}"'
        elif 'pdf' in mime_type: disposition = 'inline'

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
            'Content-Type': mime_type,
            'Content-Range': f'bytes {from_bytes}-{until_bytes}/{file_size}',
            'Content-Length': str(chunk_size),
            'Content-Disposition': disposition,
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
    site = web.TCPS
