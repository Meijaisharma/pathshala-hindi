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

# --- HOME PAGE LOGIC ---
@routes.get('/')
async def index_page(request):
    tab = request.query.get('tab', 'lectures')
    content_html = ""

    if tab == 'lectures':
        for i in range(1, 158):
            content_html += """
            <div class="ios-card animate-slide-up" onclick="window.location.href='/player?id={ID}'">
                <div class="thumb-container">
                    <div class="thumb-gradient"><span class="thumb-text">{ID}</span></div>
                </div>
                <div class="card-info">
                    <span class="tag-category">HINDI LITERATURE</span>
                    <h3 class="card-title">Lecture #{ID}</h3>
                    <div class="card-meta"><span class="text-blue-600 font-semibold text-[11px]">▶ Watch Now</span></div>
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
            content_html += """
            <div class="ios-list-item animate-slide-up" onclick="window.location.href='/view/{ID}'">
                <div class="icon-box bg-red-50 text-red-500">📄</div>
                <div class="list-info"><h3 class="list-title">{NAME}</h3><p class="list-sub">PDF Document</p></div>
                <div class="action-arrow">View</div>
            </div>""".replace("{ID}", str(i)).replace("{NAME}", clean_name)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>PathshalaX</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'SF Pro Display', sans-serif; background: #F2F2F7; padding-bottom: 90px; }
            .glass-header { position: fixed; top: 0; width: 100%; z-index: 50; background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.1); padding: 15px 20px; }
            .ios-card { background: white; border-radius: 18px; margin-bottom: 12px; padding: 12px; display: flex; gap: 14px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
            .thumb-container { width: 90px; height: 65px; border-radius: 12px; overflow: hidden; }
            .thumb-gradient { width: 100%; height: 100%; background: linear-gradient(135deg, #007AFF, #5856D6); display: flex; align-items: center; justify-content: center; }
            .thumb-text { color: white; font-weight: 800; font-size: 24px; }
            .card-title { font-size: 15px; font-weight: 600; color: #1C1C1E; margin-top: 2px; }
            .tag-category { font-size: 9px; font-weight: 700; color: #FF2D55; }
            .ios-list-item { background: white; border-radius: 14px; padding: 14px; margin-bottom: 10px; display: flex; align-items: center; gap: 14px; }
            .icon-box { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
            .list-title { font-size: 13px; font-weight: 600; color: #1C1C1E; }
            .list-sub { font-size: 11px; color: #8E8E93; }
            .action-arrow { font-size: 11px; font-weight: 600; color: #007AFF; margin-left: auto; background: #F2F2F7; padding: 4px 10px; border-radius: 20px; }
            .tab-bar { position: fixed; bottom: 0; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border-top: 1px solid rgba(0,0,0,0.1); display: flex; justify-content: space-around; padding: 10px 0; z-index: 100; }
            .tab-btn { display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #999; font-size: 10px; font-weight: 500; }
            .tab-btn.active { color: #007AFF; }
        </style>
    </head>
    <body>
        <div class="glass-header"><h1 class="text-xl font-bold tracking-tight">PathshalaX Premium</h1></div>
        <div class="h-20"></div>
        <div class="px-4">{CONTENT}</div>
        <div class="tab-bar">
            <a href="/?tab=lectures" class="tab-btn {ACT_LEC}"><span style="font-size:20px;">📺</span>Classes</a>
            <a href="/?tab=notes" class="tab-btn {ACT_NOTE}"><span style="font-size:20px;">📝</span>Notes</a>
        </div>
    </body>
    </html>
    """.replace("{CONTENT}", content_html)
    
    if tab == 'lectures': html = html.replace("{ACT_LEC}", "active").replace("{ACT_NOTE}", "")
    else: html = html.replace("{ACT_LEC}", "").replace("{ACT_NOTE}", "active")
    return web.Response(text=html, content_type='text/html')
# --- PLAYER & STREAMING LOGIC ---
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
        <style>
            body { background: white; font-family: -apple-system, sans-serif; }
            .sticky-player { position: sticky; top: 0; z-index: 100; background: black; width: 100%; }
        </style>
    </head>
    <body>
        <div class="sticky-player">
            <media-player title="Class {CID}" src="/stream/{MID}" aspect-ratio="16/9" autoplay>
                <media-provider></media-provider>
                <media-video-layout></media-video-layout>
            </media-player>
        </div>
        <div class="px-5 py-6">
            <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">PREMIUM</span>
            <h1 class="text-2xl font-bold text-gray-900 mt-2">Class #{CID}</h1>
            <div class="flex gap-3 mt-6 pb-6 border-b border-gray-100">
                <a href="/download/{MID}" class="flex-1 bg-gray-900 text-white text-center py-3 rounded-xl text-sm font-bold">Download Video</a>
                <a href="/" class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl text-sm font-bold">Back</a>
            </div>
            <div class="mt-6">
                <h3 class="font-bold text-gray-900 mb-2">Description</h3>
                <div class="bg-gray-50 p-4 rounded-xl text-sm text-gray-700 leading-relaxed font-mono">{DESC}</div>
            </div>
            <div class="mt-10 text-center text-xs text-gray-400 font-bold">Made with ♥️ By Jai Sharma</div>
        </div>
    </body>
    </html>
    """.replace("{CID}", str(class_id)).replace("{MID}", str(msg_id)).replace("{DESC}", desc)
    return web.Response(text=html, content_type='text/html')

@routes.get('/view/{id}')
async def view_pdf(request):
    msg_id = request.match_info['id']
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-900 h-screen flex flex-col">
        <div class="h-14 bg-gray-800 flex items-center justify-between px-4 border-b border-gray-700">
            <h1 class="text-white text-sm font-medium">PDF Preview</h1>
            <div class="flex gap-3"><a href="/download/{MID}" class="text-blue-400 text-xs font-bold">Save</a><a href="/?tab=notes" class="text-gray-400 text-xs">Close</a></div>
        </div>
        <iframe src="/stream/{MID}" class="flex-1 w-full border-none"></iframe>
    </body>
    </html>""".replace("{MID}", msg_id)
    return web.Response(text=html, content_type='text/html')

@routes.get('/stream/{msg_id}')
@routes.get('/download/{msg_id}')
async def media_handler(request):
    try:
        msg_id = int(request.match_info['msg_id'])
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        
        file_size = msg.file.size
        mime = msg.file.mime_type or "application/octet-stream"
        name = msg.file.name or f"File_{msg_id}"
        disposition = 'inline'
        if 'download' in request.path: disposition = f'attachment; filename="{name}"'
        elif 'pdf' in mime: disposition = 'inline'

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
    print(f"🚀 READY: {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
