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

# --- CSS & TEMPLATES (iOS STYLE) ---
IOS_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {
        --ios-bg: #F2F2F7;
        --ios-card: #FFFFFF;
        --ios-blue: #007AFF;
        --ios-text: #000000;
        --ios-gray: #8E8E93;
        --glass: rgba(255, 255, 255, 0.85);
    }
    body { font-family: 'Inter', -apple-system, sans-serif; background-color: var(--ios-bg); color: var(--ios-text); margin: 0; padding-bottom: 80px; -webkit-font-smoothing: antialiased; }
    
    /* Animations */
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    .animate-enter { animation: slideUp 0.4s cubic-bezier(0.2, 0.8, 0.2, 1); }
    
    /* Glassmorphism Headers */
    .glass-nav {
        background: var(--glass); backdrop-filter: saturate(180%) blur(20px); -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-bottom: 1px solid rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 100;
    }
    
    /* iOS Cards */
    .ios-card {
        background: var(--ios-card); border-radius: 18px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.04); transition: transform 0.2s;
        border: 1px solid rgba(0,0,0,0.02);
    }
    .ios-card:active { transform: scale(0.98); }

    /* Thumbnails */
    .thumb-gradient { background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%); }
    
    /* Bottom Tab Bar */
    .tab-bar {
        position: fixed; bottom: 0; width: 100%; background: var(--glass);
        backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid rgba(0,0,0,0.1); display: flex; justify-content: space-around;
        padding: 10px 0; padding-bottom: max(10px, env(safe-area-inset-bottom)); z-index: 99;
    }
    .tab-item { text-align: center; color: var(--ios-gray); font-size: 10px; font-weight: 500; text-decoration: none; }
    .tab-item.active { color: var(--ios-blue); }
    .tab-icon { font-size: 24px; display: block; margin-bottom: 2px; }
</style>
"""

# --- 1. HOME PAGE ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    
    content = ""
    if tab == 'lectures':
        for i in range(1, 158):
            content += """
            <div class="ios-card p-3 flex gap-4 mb-4 animate-enter" onclick="window.location.href='/player?id={ID}'">
                <div class="w-24 h-24 thumb-gradient rounded-2xl flex flex-col items-center justify-center text-white shadow-sm flex-shrink-0">
                    <span class="text-3xl font-bold">{ID}</span>
                    <span class="text-[9px] font-medium opacity-80 uppercase">Class</span>
                </div>
                <div class="flex-1 py-1 flex flex-col justify-center">
                    <span class="text-[10px] font-bold text-indigo-500 uppercase tracking-wide">Hindi Literature</span>
                    <h3 class="text-[16px] font-semibold leading-tight text-gray-900 mt-1">Lecture Class #{ID}</h3>
                    <div class="mt-auto flex items-center gap-2">
                        <span class="bg-gray-100 text-gray-600 text-[10px] font-bold px-2 py-1 rounded-full">Full HD</span>
                        <span class="text-blue-600 text-[11px] font-medium flex items-center">Play Now <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg></span>
                    </div>
                </div>
            </div>""".replace("{ID}", str(i))
            
    elif tab == 'notes':
        for i in range(202, 288):
            content += """
            <div class="ios-card p-4 flex items-center justify-between mb-3 animate-enter">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    </div>
                    <div>
                        <h3 class="text-sm font-bold text-gray-900">Class Note #{ID}</h3>
                        <p class="text-xs text-gray-500">PDF • 2.4 MB</p>
                    </div>
                </div>
                <a href="/view/{ID}" class="bg-gray-100 text-blue-600 px-4 py-2 rounded-xl text-xs font-bold hover:bg-gray-200">View</a>
            </div>""".replace("{ID}", str(i))

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX</title>
        <script src="https://cdn.tailwindcss.com"></script>
        {CSS}
    </head>
    <body>
        <div class="glass-nav px-5 py-4 flex justify-between items-center">
            <div>
                <p class="text-xs font-semibold text-gray-500 uppercase">Welcome back</p>
                <h1 class="text-2xl font-extrabold text-black tracking-tight">PathshalaX</h1>
            </div>
            <div class="w-8 h-8 rounded-full bg-gradient-to-r from-pink-500 to-orange-500 p-[2px]">
                <div class="w-full h-full bg-white rounded-full overflow-hidden">
                   <img src="https://ui-avatars.com/api/?name=J+S&background=random" class="w-full h-full"/>
                </div>
            </div>
        </div>

        <div class="px-4 mt-6">
            <h2 class="text-lg font-bold text-gray-900 mb-4">{TITLE}</h2>
            {CONTENT}
        </div>

        <div class="tab-bar">
            <a href="/?tab=lectures" class="tab-item {ACT_LEC}">
                <span class="tab-icon">📺</span> Classes
            </a>
            <a href="/?tab=notes" class="tab-item {ACT_NOTE}">
                <span class="tab-icon">📝</span> Notes
            </a>
        </div>
        
        <div class="text-center mt-10 mb-20">
            <p class="text-[10px] font-bold text-gray-400">Made with ♥️ By Jai Sharma</p>
        </div>
    </body>
    </html>
    """.replace("{CSS}", IOS_CSS).replace("{CONTENT}", content)
    
    if tab == 'lectures':
        html = html.replace("{TITLE}", "Recent Live Classes").replace("{ACT_LEC}", "active").replace("{ACT_NOTE}", "")
    else:
        html = html.replace("{TITLE}", "Study Material").replace("{ACT_LEC}", "").replace("{ACT_NOTE}", "active")
        
    return web.Response(text=html, content_type='text/html')

# --- 2. PREMIUM VIDEO PLAYER (IOS STYLE) ---
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
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Playing Class</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
        {CSS}
        <style>
            .video-sticky { position: sticky; top: 0; z-index: 50; width: 100%; background: black; }
        </style>
    </head>
    <body style="background: white;">
        
        <!-- VIDEO AREA (STICKY TOP) -->
        <div class="video-sticky">
             <media-player title="Class {CID}" src="/stream/{MID}" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>

        <!-- DETAILS SCROLL AREA -->
        <div class="p-5">
            <div class="flex justify-between items-start">
                <div>
                    <span class="text-[10px] font-bold bg-blue-100 text-blue-600 px-2 py-1 rounded">HINDI SAHITYA</span>
                    <h1 class="text-2xl font-bold text-gray-900 mt-2">Lecture Class {CID}</h1>
                    <p class="text-sm text-gray-500">By PathshalaX Faculty</p>
                </div>
                <a href="/" class="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-gray-600 font-bold">✕</a>
            </div>

            <!-- ACTION BUTTONS -->
            <div class="flex gap-3 mt-6">
                <a href="/download/{MID}" class="flex-1 bg-gray-900 text-white text-center py-3 rounded-xl text-sm font-bold flex items-center justify-center gap-2 shadow-lg">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                    Download Video
                </a>
            </div>

            <!-- DESCRIPTION -->
            <div class="mt-8">
                <h3 class="font-bold text-gray-900 text-lg mb-3">About this Class</h3>
                <div class="bg-gray-50 p-5 rounded-2xl text-sm text-gray-700 leading-relaxed font-mono">
                    {DESC}
                </div>
            </div>

            <div class="mt-10 text-center pb-10">
                <p class="text-xs text-gray-400 font-medium">Made with ♥️ By Jai Sharma</p>
            </div>
        </div>
    </body>
    </html>
    """.replace("{CSS}", IOS_CSS).replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    
    return web.Response(text=html, content_type='text/html')

# --- 3. PDF VIEWER (GOOGLE DRIVE STYLE) ---
@routes.get('/view/{id}')
async def view_pdf(request):
    msg_id = request.match_info['id']
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Viewing Note</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body, html { height: 100%; margin: 0; overflow: hidden; background: #f3f4f6; }</style>
    </head>
    <body>
        <div class="h-[60px] bg-white border-b flex items-center justify-between px-4">
            <h1 class="font-bold text-gray-800">Note Preview</h1>
            <div class="flex gap-2">
                <a href="/download/{MID}" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-xs font-bold">Download</a>
                <a href="/?tab=notes" class="bg-gray-200 text-gray-700 px-3 py-2 rounded-lg text-xs font-bold">Close</a>
            </div>
        </div>
        <iframe src="/stream/{MID}" width="100%" height="100%" style="border:none;"></iframe>
    </body>
    </html>
    """.replace("{MID}", msg_id)
    return web.Response(text=html, content_type='text/html')

# --- 4. UNIVERSAL STREAMER (Video & PDF) ---
@routes.get('/stream/{msg_id}')
@routes.get('/download/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        # Auto detect mime type (PDF or MP4)
        mime_type = msg.file.mime_type or "application/octet-stream"
        name = msg.file.name or f"Pathshala_File_{msg_id}"
        
        disposition = 'inline'
        # Force download only on /download route, otherwise show/play
        if 'download' in request.path: 
            disposition = f'attachment; filename="{name}"'
        elif 'pdf' in mime_type:
             disposition = 'inline' # Opens in browser PDF viewer

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
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🚀 IOS ENGINE LIVE: {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
