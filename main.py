import os
import asyncio
from telethon import TelegramClient
from aiohttp import web
import aiohttp_cors

# --- CONFIGURATION ---
API_ID = 34092408
API_HASH = "13bdb62f6a9424169574109474cd6bde"
SESSION_NAME = "PathshalaSession"  # Ye file GitHub pe honi chahiye
CHANNEL_USERNAME = "pathshalax"

# --- SYSTEM SETUP ---
# Connection Retries badha diye taaki Timeout na ho
client = TelegramClient(SESSION_NAME, API_ID, API_HASH, connection_retries=5, retry_delay=1)
routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

# --- 1. HOME PAGE ---
@routes.get('/')
async def index_page(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PathshalaX - Hindi Sahitya</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
            .glass-header { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid #e5e7eb; }
            .thumbnail-gradient { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); }
        </style>
    </head>
    <body class="pb-10">
        <nav class="glass-header fixed top-0 w-full z-50 px-4 py-3 flex justify-between items-center">
            <h1 class="text-lg font-bold text-gray-800">Hindi Literature</h1>
            <span class="bg-indigo-100 text-indigo-700 text-xs font-bold px-2 py-1 rounded">PathshalaX</span>
        </nav>
        <div class="mt-16 px-4 space-y-4" id="cardContainer"></div>
        <script>
            const container = document.getElementById('cardContainer');
            for (let i = 1; i <= 157; i++) {
                container.innerHTML += `
                <div class="bg-white rounded-2xl p-3 flex gap-3 shadow-sm cursor-pointer" onclick="window.location.href='/player?id=${i}'">
                    <div class="relative w-28 h-36 flex-shrink-0 rounded-xl overflow-hidden thumbnail-gradient flex flex-col items-center justify-center">
                        <span class="text-white font-bold text-3xl opacity-90">${i}</span>
                        <span class="text-white/80 text-[10px] uppercase mt-1">Class</span>
                    </div>
                    <div class="flex-1 flex flex-col justify-between py-1">
                        <div>
                            <span class="text-[10px] font-bold text-pink-500 uppercase">हिंदी साहित्य</span>
                            <h3 class="text-sm font-bold text-gray-900 leading-tight mt-1">Lecture #${i} (Full Coverage)</h3>
                        </div>
                        <button class="text-blue-600 text-xs font-bold bg-blue-50 px-2 py-1 rounded-lg w-max">View Class</button>
                    </div>
                </div>`;
            }
        </script>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

# --- 2. PLAYER PAGE ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    caption_text = "Loading details..."
    try:
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if msg and msg.message: caption_text = msg.message.replace('\\n', '<br>')
    except: caption_text = "Details unavailable."

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Class {class_id}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    </head>
    <body class="bg-white">
        <div class="sticky top-0 z-50 bg-black w-full shadow-lg">
            <video id="player" playsinline controls>
                <source src="/stream/{class_id}" type="video/mp4" />
            </video>
        </div>
        <div class="max-w-4xl mx-auto px-4 py-6">
            <h1 class="text-2xl font-bold text-gray-900">Class {class_id}</h1>
            <div class="mt-4 bg-gray-50 rounded-xl p-5 border border-gray-100 text-sm text-gray-600 font-mono">
                {caption_text}
            </div>
        </div>
        <script src="https://cdn.plyr.io/3.7.8/plyr.js"></script>
        <script>
            const player = new Plyr('#player', {{ speed: {{ selected: 1, options: [0.5, 1, 1.25, 1.5, 2] }} }});
        </script>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

# --- 3. STREAMING ENGINE ---
@routes.get('/stream/{id}')
async def stream_video(request):
    try:
        class_id = request.match_info['id']
        msg_id = get_real_id(class_id)
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

        # 512KB chunks are best for streaming
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
    # RENDER PORT HANDLING
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🚀 SERVER LIVE ON PORT {port}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
