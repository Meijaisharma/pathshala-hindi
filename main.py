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

# --- HEALTH CHECK (UPTIME) ---
@routes.get('/health')
async def health_check(request):
    return web.Response(text="Alive", status=200)

# --- 1. HOME PAGE ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    
    # HTML Generator
    cards_html = ""
    if tab == 'lectures':
        for i in range(1, 158):
            cards_html += """
            <div class="bg-white rounded-2xl p-3 flex gap-3 card-shadow cursor-pointer transition hover:scale-[1.02] border border-transparent hover:border-indigo-100" 
                 onclick="window.location.href='/player?id={ID}'">
                <div class="relative w-28 h-20 flex-shrink-0 rounded-xl overflow-hidden bg-gradient-to-br from-indigo-600 to-purple-700 flex flex-col items-center justify-center shadow-lg">
                    <span class="text-white font-bold text-2xl drop-shadow-md">{ID}</span>
                </div>
                <div class="flex-1 flex flex-col justify-center">
                    <span class="text-[10px] font-bold text-pink-500 uppercase">हिन्दी साहित्य</span>
                    <h3 class="text-sm font-bold text-gray-800 leading-tight">Lecture #{ID}</h3>
                    <div class="flex items-center gap-2 mt-1">
                        <span class="text-[10px] text-indigo-500 font-medium">Watch Now &rarr;</span>
                    </div>
                </div>
            </div>""".replace("{ID}", str(i))
    
    elif tab == 'notes':
        for i in range(202, 288):
            cards_html += """
            <div class="bg-white rounded-xl p-4 flex items-center justify-between card-shadow border border-gray-100">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 bg-red-100 text-red-600 rounded-lg flex items-center justify-center">PDF</div>
                    <div>
                        <h3 class="text-sm font-bold text-gray-800">Note #{ID}</h3>
                    </div>
                </div>
                <a href="/download/{ID}" class="bg-gray-900 text-white px-3 py-1.5 rounded-lg text-xs font-bold">Download</a>
            </div>""".replace("{ID}", str(i))

    # Base HTML
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PathshalaX</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { font-family: sans-serif; background-color: #f8fafc; }
            .glass { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(0,0,0,0.05); }
            .active-tab { background: #111827; color: white; }
            .inactive-tab { background: #f3f4f6; color: #6b7280; }
        </style>
    </head>
    <body class="pb-20">
        <nav class="glass fixed top-0 w-full z-50 px-5 py-4 flex justify-between items-center">
            <div>
                <span class="text-xs font-bold text-indigo-600 uppercase">Daily Live Class</span>
                <h1 class="text-xl font-extrabold text-gray-900">Hindi Literature</h1>
            </div>
            <div class="bg-gradient-to-r from-pink-500 to-red-500 text-white text-[10px] font-bold px-2.5 py-1 rounded-full">PathshalaX</div>
        </nav>

        <div class="mt-20 px-4 flex gap-3">
            <a href="/?tab=lectures" class="flex-1 py-3 text-center rounded-xl font-bold text-sm transition-all TAB_LEC">📺 Video Classes</a>
            <a href="/?tab=notes" class="flex-1 py-3 text-center rounded-xl font-bold text-sm transition-all TAB_NOTE">📚 PDF Notes</a>
        </div>

        <div class="mt-6 px-4 space-y-4">CONTENT_HERE</div>

        <footer class="mt-12 text-center py-8 border-t border-gray-200">
            <p class="text-gray-900 font-bold text-sm">Made with ♥️ By Jai Sharma</p>
        </footer>
    </body>
    </html>
    """
    
    # Manually Replace Placeholders (No f-strings)
    html = html.replace("CONTENT_HERE", cards_html)
    if tab == 'lectures':
        html = html.replace("TAB_LEC", "active-tab shadow-lg").replace("TAB_NOTE", "inactive-tab")
    else:
        html = html.replace("TAB_LEC", "inactive-tab").replace("TAB_NOTE", "active-tab shadow-lg")

    return web.Response(text=html, content_type='text/html')

# --- 2. PLAYER PAGE ---
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
        <title>Class CID</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/theme.css" />
        <link rel="stylesheet" href="https://cdn.vidstack.io/player/video.css" />
        <script type="module" src="https://cdn.vidstack.io/player.js"></script>
    </head>
    <body class="bg-black text-white min-h-screen flex flex-col">
        <div class="w-full sticky top-0 z-50 bg-black shadow-2xl">
            <media-player title="Class CID" src="/stream/MID" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>
        <div class="bg-white text-gray-900 flex-1 rounded-t-3xl -mt-4 relative z-40 p-6">
            <div class="w-12 h-1.5 bg-gray-300 rounded-full mx-auto mb-6"></div>
            <div class="flex justify-between items-start">
                <div>
                    <span class="bg-pink-100 text-pink-600 px-2 py-0.5 rounded text-[10px] font-bold uppercase">Premium Lecture</span>
                    <h1 class="text-2xl font-extrabold mt-2">Class CID</h1>
                    <p class="text-sm text-gray-500 font-medium">By PathshalaX Faculty</p>
                </div>
                <a href="/download/MID" class="flex flex-col items-center gap-1 text-gray-500 hover:text-indigo-600">
                    <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">⬇️</div>
                    <span class="text-[10px] font-bold">Save</span>
                </a>
            </div>
            <div class="mt-8">
                <h3 class="font-bold text-gray-900 mb-3">Lecture Details</h3>
                <div class="bg-gray-50 p-4 rounded-xl border border-gray-100 text-sm text-gray-600 font-mono">DESC_TEXT</div>
            </div>
            <div class="mt-10 text-center border-t border-gray-100 pt-6">
                 <p class="text-gray-900 font-bold text-sm">Made with ♥️ By Jai Sharma</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Manual Replacement
    html = html.replace("CID", str(class_id)).replace("MID", str(msg_id)).replace("DESC_TEXT", desc)
    return web.Response(text=html, content_type='text/html')

# --- 3. STREAM & DOWNLOAD ---
@routes.get('/stream/{msg_id}')
@routes.get('/download/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        name = msg.file.name or "Pathshala_File"
        
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
            'Content-Type': msg.file.mime_type or 'application/octet-stream',
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
    print(f"🚀 SERVER LIVE ON PORT {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt: pass
