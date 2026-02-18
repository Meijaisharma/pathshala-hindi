import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from aiohttp import web
import aiohttp_cors

# --- CONFIGURATION ---
API_ID = 34092408
API_HASH = "13bdb62f6a9424169574109474cd6bde"
SESSION_NAME = "PathshalaSession"
CHANNEL_USERNAME = "pathshalax"

# 👇 YAHAN APNA STRING SESSION PASTE KAREIN 👇
STRING_SESSION = "1BVtsOI4Bu4XSxk3bkZmIEajcTQSb2_BNvySfxpAa5adWDRfI9yNYzaV-6P8kVf40qj1jw8Yy2ErXs-QtzP-N_jQgzm4w0tlPaHpFJO2Ub3Tn4PYJMc_FITYErApi_wmldzdOndC2dT4cFPix7gh2U-LHz-1Pp5N_HnNRQorM9_5CCC-cnebzq5X6P8FCUnvBGkqRILXuQ3bHKOU9vFa1ZBegl7jzUd2MIWTmKC7ItmXl_ghEqVvHnpxmflCaKAHNGNkasb1hwncpsF0jagWgPNWwYyx_MuoASdWyYYeyS6IIXgCJEhMWLKdQ8IQAkzMG5MAtDE2K2beg19UEH0WtSWW-kLY9WyA="

# --- SYSTEM SETUP ---
if STRING_SESSION == "PASTE_YOUR_STRING_HERE":
    print("❌ ERROR: String Session missing!")
    exit()
else:
    client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, connection_retries=5, retry_delay=1)

routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

# --- 1. HOME PAGE (INK WASH THEME) ---
@routes.get('/')
async def index_page(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PathshalaX</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            :root { --ink-dark: #4A4A4A; --ink-light: #CBCBCB; --ink-cream: #FFFFE3; --ink-blue: #6D8196; }
            body { font-family: 'DM Sans', sans-serif; background-color: var(--ink-cream); color: var(--ink-dark); }
            .nav-glass { background: rgba(255, 255, 227, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--ink-light); }
            .card { background: white; border: 1px solid var(--ink-light); border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(74, 74, 74, 0.05); transition: transform 0.2s; }
            .card:active { transform: scale(0.98); }
            .thumb-box { background-color: var(--ink-blue); color: white; border-radius: 12px; }
            .btn-view { background-color: var(--ink-blue); color: white; padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: bold; }
        </style>
    </head>
    <body class="pb-10">
        <nav class="nav-glass fixed top-0 w-full z-50 px-5 py-4 flex justify-between items-center">
            <h1 class="text-xl font-bold text-[#4A4A4A]">Hindi Sahitya</h1>
            <span class="bg-[#6D8196] text-white text-xs font-bold px-2 py-1 rounded">PREMIUM</span>
        </nav>
        <div class="mt-20 px-4 space-y-4" id="cardContainer"></div>
        <script>
            const c = document.getElementById('cardContainer');
            function getMockDuration(i) {
                const h = 2; const m = (10 + (i * 3)) % 60;
                return `${h}h ${m < 10 ? '0'+m : m}m`;
            }
            for (let i = 1; i <= 157; i++) {
                c.innerHTML += 
                `<div class="card p-3 flex gap-4 cursor-pointer" onclick="window.location.href='/player?id=${i}'">
                    <div class="thumb-box w-24 h-32 flex-shrink-0 flex flex-col items-center justify-center">
                        <span class="text-3xl font-bold opacity-90">${i}</span>
                        <span class="text-[10px] uppercase tracking-wider opacity-80">Class</span>
                    </div>
                    <div class="flex-1 flex flex-col justify-between py-1">
                        <div>
                            <span class="text-[10px] font-bold text-[#6D8196] uppercase tracking-wide">PathshalaX Stream</span>
                            <h3 class="text-base font-bold text-[#4A4A4A] leading-tight mt-1">Lecture #${i} Full Coverage</h3>
                            <div class="flex items-center gap-2 mt-2">
                                <svg class="w-3 h-3 text-[#6D8196]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                <span class="text-xs text-gray-500 font-medium">${getMockDuration(i)}</span>
                            </div>
                        </div>
                        <div class="flex justify-end"><button class="btn-view">Play Class</button></div>
                    </div>
                </div>`;
            }
        </script>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')
# --- 2. PLAYER PAGE (FIXED BUTTON PLACEMENT) ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    caption = "Loading..."
    try:
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if msg and msg.message: caption = msg.message.replace('\n', '<br>')
    except: pass

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Class {class_id}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {{ --ink-dark: #4A4A4A; --ink-light: #CBCBCB; --ink-cream: #FFFFE3; --ink-blue: #6D8196; }}
            body {{ background-color: white; margin: 0; font-family: sans-serif; overflow-x: hidden; }}
            
            /* --- DEFAULT PLAYER --- */
            .default-container {{ position: sticky; top: 0; width: 100%; background: black; z-index: 50; overflow: hidden; }}
            video {{ width: 100%; display: block; }}
            
            /* Hide Native Fullscreen Button to avoid double buttons */
            video::-webkit-media-controls-fullscreen-button {{ display: none !important; }}
            video::-webkit-media-controls-enclosure {{ overflow: hidden; }}
            
            /* THE CUSTOM CINEMA BUTTON (SHI JAGAH) */
            .cinema-trigger {{
                position: absolute; bottom: 10px; right: 15px; z-index: 60;
                color: white; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
                padding: 6px 10px; border-radius: 6px; font-size: 14px;
                border: 1px solid rgba(255,255,255,0.2); cursor: pointer;
                display: flex; align-items: center; gap: 5px; pointer-events: auto;
            }}
            
            .details-box {{ padding: 20px; background: white; }}
            
            /* --- CINEMA MODE (LANDSCAPE) --- */
            #fs-layer {{ display: none; position: fixed; inset: 0; background: black; z-index: 9999; width: 100vw; height: 100vh; }}
            .overlay {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: space-between; z-index: 20; transition: opacity 0.3s; pointer-events: none; }}
            .overlay.active {{ pointer-events: auto; opacity: 1; }}
            .overlay.fade {{ opacity: 0; pointer-events: none; }}
            .shade {{ background: rgba(0,0,0,0.6); backdrop-filter: blur(2px); pointer-events: auto; }}
            
            /* Cinema Controls */
            input[type=range] {{ -webkit-appearance: none; width: 100%; background: transparent; cursor: pointer; }}
            input[type=range]::-webkit-slider-thumb {{ -webkit-appearance: none; height: 16px; width: 16px; background: var(--ink-blue); border-radius: 50%; margin-top: -6px; border: 2px solid white; }}
            input[type=range]::-webkit-slider-runnable-track {{ width: 100%; height: 4px; background: rgba(255,255,255,0.3); border-radius: 2px; }}
            
            .gesture-area {{ position: absolute; top: 20%; bottom: 20%; z-index: 10; pointer-events: auto; }}
            .toast {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); background: rgba(0,0,0,0.7); padding: 15px 25px; border-radius: 12px; color: white; display: flex; flex-direction: column; align-items: center; opacity: 0; transition: 0.2s; pointer-events: none; }}
            .toast-bar {{ width: 100px; height: 4px; background: #555; margin-top: 8px; border-radius: 2px; overflow: hidden; }}
            .toast-fill {{ height: 100%; background: var(--ink-blue); width: 0%; }}
            #bright-mask {{ position: absolute; inset: 0; background: black; opacity: 0; pointer-events: none; z-index: 5; }}
            
            .c-btn {{ color: white; font-size: 2.5rem; opacity: 0.9; cursor: pointer; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5)); }}
            .c-btn-main {{ font-size: 4rem; margin: 0 40px; }}
            .top-row {{ display: flex; justify-content: space-between; padding: 20px 30px; color: white; align-items: center; }}
            .bot-row {{ padding: 20px 30px; color: white; display: flex; flex-direction: column; gap: 10px; }}
        </style>
    </head>
    <body>

        <!-- DEFAULT PLAYER -->
        <div id="defaultMode">
            <div class="default-container relative">
                <video id="vid" playsinline controls controlsList="nodownload">
                    <source src="/stream/{class_id}" type="video/mp4" />
                </video>
                <!-- SINGLE CINEMA BUTTON (OVER VIDEO) -->
                <div class="cinema-trigger" onclick="enterCinemaMode()">
                    <i class="fas fa-expand"></i> Cinema
                </div>
            </div>
            
            <div class="details-box">
                <div class="flex justify-between items-center mb-4">
                    <h1 class="text-2xl font-bold text-[#4A4A4A]">Class {class_id}</h1>
                    <button onclick="window.history.back()" class="bg-[#CBCBCB] px-4 py-1 rounded text-sm font-bold">Back</button>
                </div>
                <div class="bg-[#FFFFE3] border border-[#CBCBCB] rounded-lg p-4 text-sm text-[#4A4A4A] font-mono whitespace-pre-wrap">
                    {caption}
                </div>
            </div>
        </div>

        <!-- CINEMA MODE LAYER -->
        <div id="fs-layer">
            <div id="fs-video-box" class="relative w-full h-full bg-black flex items-center justify-center">
                <div id="bright-mask"></div>
                <div class="gesture-area" style="left:0; width:45%;" id="touchL"></div>
                <div class="gesture-area" style="right:0; width:45%;" id="touchR"></div>
                <div class="gesture-area" style="left:45%; width:10%;" id="touchC"></div>
                
                <div id="toast" class="toast">
                    <i id="t-icon" class="fas fa-volume-up text-2xl mb-1"></i>
                    <div id="t-val" class="font-bold text-lg">100%</div>
                    <div class="toast-bar"><div id="t-fill" class="toast-fill"></div></div>
                </div>

                <div id="overlay" class="overlay active">
                    <div class="shade top-row">
                        <div class="flex items-center gap-4">
                            <i class="fas fa-arrow-left text-xl cursor-pointer" onclick="exitCinemaMode()"></i>
                            <div><h2 class="font-bold text-lg">Class {class_id}</h2><p class="text-xs opacity-70">Hindi Sahitya</p></div>
                        </div>
                        <div class="flex gap-6 text-xl"><i class="fas fa-closed-captioning opacity-70"></i><i class="fas fa-cog cursor-pointer" onclick="cycleSpeed()"></i></div>
                    </div>
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex items-center pointer-events-auto">
                        <i class="fas fa-undo-alt c-btn" onclick="seek(-10)"></i>
                        <i class="fas fa-pause c-btn c-btn-main" id="cPlay" onclick="togglePlay()"></i>
                        <i class="fas fa-redo-alt c-btn" onclick="seek(10)"></i>
                    </div>
                    <div class="shade bot-row">
                        <div class="flex justify-between text-xs font-mono opacity-90"><span id="curT">00:00</span><span id="durT">00:00</span></div>
                        <input type="range" id="skBar" value="0" max="100">
                        <div class="flex justify-between items-center mt-1">
                            <div class="flex gap-6 text-sm font-bold">
                                <span onclick="cycleFit()" id="fitTxt" class="cursor-pointer">FIT</span>
                                <span onclick="alert('Locked')" class="cursor-pointer"><i class="fas fa-unlock"></i> LOCK</span>
                            </div>
                            <div class="flex gap-4 items-center">
                                <span id="spdDisplay" class="text-xs font-bold bg-[#6D8196] px-2 py-1 rounded">1.0x</span>
                                <i class="fas fa-compress text-xl cursor-pointer" onclick="exitCinemaMode()"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const vid = document.getElementById('vid');
            const defMode = document.getElementById('defaultMode');
            const fsLayer = document.getElementById('fs-layer');
            const fsBox = document.getElementById('fs-video-box');
            const defContainer = document.querySelector('.default-container');
            const overlay = document.getElementById('overlay');
            let isCinema = false, uiTimer;

            function enterCinemaMode() {{
                isCinema = true;
                fsBox.insertBefore(vid, fsBox.firstChild);
                vid.controls = false; vid.style.width = '100%'; vid.style.height = '100%';
                defMode.style.display = 'none'; fsLayer.style.display = 'block';
                if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
                if (screen.orientation && screen.orientation.lock) screen.orientation.lock('landscape').catch(e=>{{}});
                resetUI();
            }}

            function exitCinemaMode() {{
                isCinema = false;
                defContainer.insertBefore(vid, defContainer.querySelector('.cinema-trigger'));
                vid.controls = true; vid.style.height = 'auto';
                fsLayer.style.display = 'none'; defMode.style.display = 'block';
                if (document.exitFullscreen) document.exitFullscreen();
                if (screen.orientation && screen.orientation.unlock) screen.orientation.unlock();
            }}

            function togglePlay() {{ if(vid.paused) {{ vid.play(); setPlayIcon(true); }} else {{ vid.pause(); setPlayIcon(false); }} resetUI(); }}
            function setPlayIcon(playing) {{ document.getElementById('cPlay').className = `fas ${{playing ? 'fa-pause' : 'fa-play'}} c-btn c-btn-main`; }}
            vid.addEventListener('play', () => {{ setPlayIcon(true); resetUI(); }});
            vid.addEventListener('pause', () => {{ setPlayIcon(false); overlay.classList.remove('fade'); }});
            function seek(sec) {{ vid.currentTime += sec; resetUI(); }}
            
            vid.ontimeupdate = () => {{
                if(!isCinema) return;
                const pct = (vid.currentTime / vid.duration) * 100;
                document.getElementById('skBar').value = pct || 0;
                document.getElementById('curT').innerText = fmt(vid.currentTime);
                document.getElementById('durT').innerText = fmt(vid.duration);
            }};
            document.getElementById('skBar').addEventListener('input', (e) => vid.currentTime = (e.target.value / 100) * vid.duration);
            function fmt(s) {{ return new Date(s*1000).toISOString().substr(14,5); }}

            let startY = 0, startVal = 0, activeG = null;
            const handleStart = (e, type) => {{ startY = e.touches[0].clientY; activeG = type; startVal = type === 'vol' ? vid.volume : parseFloat(document.getElementById('bright-mask').style.opacity) || 0; }};
            const handleMove = (e) => {{
                if(!activeG) return; e.preventDefault();
                const delta = startY - e.touches[0].clientY; const sensitivity = 200;
                if(activeG === 'vol') {{
                    let v = startVal + (delta / sensitivity); if(v > 1) v = 1; if(v < 0) v = 0; vid.volume = v; showToast('fa-volume-up', Math.round(v*100));
                }} else {{
                    let b = startVal - (delta / sensitivity); if(b < 0) b = 0; if(b > 0.8) b = 0.8; document.getElementById('bright-mask').style.opacity = b; showToast('fa-sun', Math.round((1-(b/0.8))*100));
                }}
            }};
            document.getElementById('touchR').addEventListener('touchstart', e => handleStart(e, 'vol'));
            document.getElementById('touchL').addEventListener('touchstart', e => handleStart(e, 'bright'));
            fsBox.addEventListener('touchmove', handleMove, {{ passive: false }});
            fsBox.addEventListener('touchend', () => {{ activeG = null; setTimeout(()=> document.getElementById('toast').style.opacity=0, 500); }});

            function showToast(icon, val) {{
                const t = document.getElementById('toast'); document.getElementById('t-icon').className = `fas ${{icon}} text-2xl mb-1`; document.getElementById('t-val').innerText = val + '%'; document.getElementById('t-fill').style.width = val + '%'; t.style.opacity = 1;
            }}
            document.getElementById('touchR').addEventListener('dblclick', () => seek(10));
            document.getElementById('touchL').addEventListener('dblclick', () => seek(-10));

            function resetUI() {{ clearTimeout(uiTimer); overlay.classList.remove('fade'); if(!vid.paused) uiTimer = setTimeout(() => overlay.classList.add('fade'), 3500); }}
            document.getElementById('touchC').addEventListener('click', () => {{ if(overlay.classList.contains('fade')) resetUI(); else overlay.classList.add('fade'); }});

            let speeds = [1, 1.25, 1.5, 2]; let sI = 0;
            function cycleSpeed() {{ sI = (sI+1)%speeds.length; vid.playbackRate = speeds[sI]; document.getElementById('spdDisplay').innerText = speeds[sI] + 'x'; }}
            let fit = false;
            function cycleFit() {{ fit = !fit; vid.style.objectFit = fit ? 'cover' : 'contain'; document.getElementById('fitTxt').innerText = fit ? 'FILL' : 'FIT'; }}
        </script>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

@routes.get('/stream/{id}')
async def stream_video(request):
    try:
        class_id = request.match_info['id']
        msg_id = get_real_id(class_id)
        msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
        if not msg or not msg.media: return web.Response(status=404)
        size = msg.file.size
        range_h = request.headers.get('Range')
        start, end = 0, size - 1
        if range_h:
            parts = range_h.replace('bytes=', '').split('-')
            start = int(parts[0])
            if len(parts)>1 and parts[1]: end = int(parts[1])
        headers = {'Content-Type': 'video/mp4', 'Content-Range': f'bytes {start}-{end}/{size}', 'Content-Length': str((end-start)+1), 'Accept-Ranges': 'bytes'}
        resp = web.StreamResponse(status=206, headers=headers)
        await resp.prepare(request)
        async for chunk in client.iter_download(msg.media, offset=start, request_size=1024*1024):
            try: await resp.write(chunk)
            except: break
            start += len(chunk)
            if start > end: break
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
    await web.TCPSite(runner, '0.0.0.0', port).start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except: pass
