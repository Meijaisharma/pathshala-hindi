import os
import asyncio
import mimetypes
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

# --- ID MAPPINGS ---
def get_video_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

# --- UPTIME ROBOT ENDPOINT (Zinda Rakhne Ke Liye) ---
@routes.get('/health')
async def health_check(request):
    return web.Response(text="I am Alive!", status=200)

# --- 1. MASTER INTERFACE (Tab System for Videos & Notes) ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')  # lectures or notes
    
    # --- UI COMPONENTS ---
    video_list = ""
    if tab == 'lectures':
        for i in range(1, 158):
            video_list += f"""
            <div class="bg-white rounded-2xl p-3 flex gap-3 card-shadow cursor-pointer transition hover:scale-[1.02] border border-transparent hover:border-indigo-100" 
                 onclick="window.location.href='/player?id={i}'">
                <div class="relative w-32 h-20 flex-shrink-0 rounded-xl overflow-hidden bg-gradient-to-br from-indigo-600 to-purple-700 flex flex-col items-center justify-center shadow-lg">
                    <span class="text-white font-bold text-2xl drop-shadow-md">{i}</span>
                    <div class="absolute bottom-1 right-1 bg-black/50 px-1 rounded text-[8px] text-white">HD</div>
                </div>
                <div class="flex-1 flex flex-col justify-center">
                    <span class="text-[10px] font-bold text-pink-500 uppercase tracking-wider">हिन्दी साहित्य</span>
                    <h3 class="text-sm font-bold text-gray-800 leading-tight">Class Lecture #{i}</h3>
                    <div class="flex items-center gap-2 mt-1">
                        <span class="text-[10px] bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded">Video</span>
                        <span class="text-[10px] text-indigo-500 font-medium">Watch Now &rarr;</span>
                    </div>
                </div>
            </div>"""
    
    notes_list = ""
    if tab == 'notes':
        # Notes from ID 202 to 287
        for i in range(202, 288):
            notes_list += f"""
            <div class="bg-white rounded-xl p-4 flex items-center justify-between card-shadow border border-gray-100">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    </div>
                    <div>
                        <h3 class="text-sm font-bold text-gray-800">Class Note #{i}</h3>
                        <p class="text-xs text-gray-500">PDF Document</p>
                    </div>
                </div>
                <a href="/download/{i}" class="bg-gray-900 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-gray-800 flex items-center gap-1">
                    Download <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                </a>
            </div>"""

    # --- FULL HTML ---
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX - Learning App</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Outfit', sans-serif; background-color: #f8fafc; }}
            .glass {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(0,0,0,0.05); }}
            .card-shadow {{ box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05); }}
            .active-tab {{ background: #111827; color: white; }}
            .inactive-tab {{ background: #f3f4f6; color: #6b7280; }}
        </style>
    </head>
    <body class="pb-20">
        <!-- HEADER -->
        <nav class="glass fixed top-0 w-full z-50 px-5 py-4 flex justify-between items-center transition-all">
            <div>
                <span class="text-xs font-bold text-indigo-600 uppercase tracking-widest">Daily Live Class</span>
                <h1 class="text-xl font-extrabold text-gray-900">Hindi Literature</h1>
            </div>
            <div class="bg-gradient-to-r from-pink-500 to-red-500 text-white text-[10px] font-bold px-2.5 py-1 rounded-full shadow-md flex items-center gap-1">
                <div class="w-1.5 h-1.5 bg-white rounded-full animate-pulse"></div> PathshalaX
            </div>
        </nav>

        <!-- TABS -->
        <div class="mt-20 px-4 flex gap-3">
            <a href="/?tab=lectures" class="flex-1 py-3 text-center rounded-xl font-bold text-sm transition-all { 'active-tab shadow-lg' if tab == 'lectures' else 'inactive-tab' }">
                📺 Video Classes
            </a>
            <a href="/?tab=notes" class="flex-1 py-3 text-center rounded-xl font-bold text-sm transition-all { 'active-tab shadow-lg' if tab == 'notes' else 'inactive-tab' }">
                📚 PDF Notes
            </a>
        </div>

        <!-- CONTENT AREA -->
        <div class="mt-6 px-4 space-y-4">
            {video_list if tab == 'lectures' else notes_list}
        </div>

        <!-- FOOTER -->
        <footer class="mt-12 text-center py-8 border-t border-gray-200">
            <p class="text-gray-900 font-bold text-sm">Made with ♥️ By Jai Sharma</p>
            <p class="text-gray-400 text-xs mt-1">© 2024 PathshalaX. All Rights Reserved.</p>
        </footer>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

# --- 2. PREMIUM VIDEO PLAYER (High Tech) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_video_id(class_id)
    
    # Fetch Metadata
    try:
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        desc = msg.message.replace('\\n', '<br>') if msg and msg.message else "No description available."
    except: desc = "Loading info..."

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Watching Class {class_id}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
        <!-- VIDSTACK PLAYER (Netflix Like) -->
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
        <style>
            body {{ font-family: 'Outfit', sans-serif; background-color: #000; color: white; }}
            .glass-panel {{ background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
            /* Custom Player Colors */
            media-player {{ 
                --media-brand: #6366f1; 
                --media-focus-ring: #6366f1;
            }}
        </style>
    </head>
    <body class="min-h-screen flex flex-col">
        
        <!-- PLAYER AREA -->
        <div class="w-full sticky top-0 z-50 bg-black shadow-2xl">
            <media-player title="Class {class_id} - Hindi Sahitya" src="/stream/{msg_id}" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>

        <!-- INFO AREA -->
        <div class="bg-white text-gray-900 flex-1 rounded-t-3xl -mt-4 relative z-40 p-6 shadow-[0_-10px_40px_rgba(0,0,0,0.2)]">
            <div class="w-12 h-1.5 bg-gray-300 rounded-full mx-auto mb-6"></div>
            
            <div class="flex justify-between items-start">
                <div>
                    <span class="bg-pink-100 text-pink-600 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Premium Lecture</span>
                    <h1 class="text-2xl font-extrabold mt-2">Hindi Sahitya - Class {class_id}</h1>
                    <p class="text-sm text-gray-500 font-medium">By PathshalaX Faculty</p>
                </div>
                <!-- DOWNLOAD BUTTON -->
                <a href="/download/{msg_id}" class="flex flex-col items-center gap-1 text-gray-500 hover:text-indigo-600 transition">
                    <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    </div>
                    <span class="text-[10px] font-bold">Save</span>
                </a>
            </div>

            <!-- DESCRIPTION -->
            <div class="mt-8">
                <h3 class="font-bold text-gray-900 mb-3 flex items-center gap-2">
                    <span class="w-1 h-5 bg-indigo-600 rounded-full"></span> Lecture Details
                </h3>
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 text-sm text-gray-600 leading-relaxed font-mono whitespace-pre-wrap">
                    {desc}
                </div>
            </div>

            <div class="mt-10 text-center border-t border-gray-100 pt-6">
                 <p class="text-gray-900 font-bold text-sm">Made with ♥️ By Jai Sharma</p>
                 <p class="text-gray-400 text-xs">© 2024 PathshalaX</p>
            </div>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

# --- 3. UNIVERSAL DOWNLOAD/STREAM ENGINE ---
@routes.get('/stream/{msg_id}')
@routes.get('/download/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        
        if not msg or not msg.media: return web.Response(status=404, text="File Not Found")
        
        file_size = msg.file.size
        name = "PathshalaX_File"
        mime = "application/octet-stream"
        
        # Detect Name & Mime
        if msg.file.name: name = msg.file.name
        elif msg.media.document: 
            for attr in msg.media.document.attributes:
                if hasattr(attr, 'file_name'): name = attr.file_name
        
        # Force Download for /download route
        disposition = 'inline'
        if 'download' in request.path: disposition = f'attachment; filename="{name}"'

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
            'Content-Type': msg.file.mime_type or mime,
            'Content-Range': f'bytes {from_bytes}-{until_bytes}/{file_size}',
            'Content-Length': str(chunk_size),
            'Content-Disposition': disposition,
            'Accept-Ranges': 'bytes',
        }
        
        resp = web.StreamResponse(status=206 if range_header else 200, headers=headers)
        await resp.prepare(request)

        async for chunk in client.iter_download(msg.media, offset=from_bytes, request_size=1024*1024):
            try: await resp.write(chunk)
            except: break
            from_bytes += len(chunk)
            if from_bytes > until_bytes: break
        return resp
    except Exception as e:
        print(e)
        return web.Response(status=500)

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
    print(f"🚀 PATHSHALAX PRO LIVE ON PORT {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # RENDER UPTIME FIX (Event Loop)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt: pass
