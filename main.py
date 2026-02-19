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

# 👇 AAPKA SESSION STRING 👇
STRING_SESSION = "1BVtsOI4BuzUbE4ea7cRuLrIRgjBghi3F7y_VB2aGFaMznEzEJ-juauZCHQMatA0LNBJ3Jwsv3oCQSdUMvNr136tCZimRQ7YzqotkgEESUQha0GPT_sKJ7zJRR1Fdu5AsRloPGL0JRcNBaXGJ5GDdMoFRPKqIUrEkhFfqQXhDIRTu6lDhzKtrD17w4k-pGNrebks_7oy61n_jkfja8TaN6g2zs9EdSJHWFyHwkd2ZDi66DY6pYF8lZLUb6IKyxKpxwe1zDFL3CG8WlJgRZFOaY2fh4El9thO_aX2M6teB4fMsn4fozjh2e_J09oGisF0hTcb-cx60jN_w81rnqBj2WscRbhrTNMc="

# --- CLIENT SETUP ---
client = None
async def start_telegram():
    global client
    if not STRING_SESSION:
        print("❌ CRITICAL: String Session Missing!")
        return
    try:
        client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
        await client.start()
        print("✅ Telegram Connected Successfully!")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

routes = web.RouteTableDef()

def get_real_id(class_id):
    cid = int(class_id)
    if 1 <= cid <= 115: return cid + 1
    elif cid >= 116: return cid + 43
    return cid

def extract_smart_title(text):
    if not text: return "Hindi Sahitya Class"
    lines = text.split('\n')
    for i, line in enumerate(lines):
        if "अवधि" in line or "Duration" in line or "Time" in line:
            if i > 0:
                clean_title = lines[i-1].strip()
                if not clean_title and i > 1: return lines[i-2].strip()
                return clean_title
    return lines[0][:50]

# --- 1. HOME PAGE ---
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
            .nav-glass { background: rgba(255, 255, 227, 0.95); backdrop-filter: blur(12px); border-bottom: 1px solid var(--ink-light); }
            .card { background: white; border: 1px solid var(--ink-light); border-radius: 16px; box-shadow: 0 4px 10px -2px rgba(74, 74, 74, 0.08); transition: transform 0.2s; }
            .card:active { transform: scale(0.97); }
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
# --- 2. HIGH-TECH PLAYER PAGE ---
@routes.get('/player')
async def player_page(request):
    class_id = request.query.get('id', '1')
    msg_id = get_real_id(class_id)
    caption = "Loading..."
    real_title = f"Lecture {class_id}"
    
    if client:
        try:
            msg = await client.get_messages(CHANNEL_USERNAME, ids=msg_id)
            if msg and msg.message: 
                caption = msg.message.replace('\n', '<br>')
                real_title = extract_smart_title(msg.message)
        except: pass

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>{real_title}</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            :root {{ --ink-dark: #4A4A4A; --ink-light: #CBCBCB; --ink-cream: #FFFFE3; --ink-blue: #6D8196; }}
            body {{ background-color: white; margin: 0; font-family: sans-serif; overflow-x: hidden; }}
            
            .default-container {{ position: sticky; top: 0; width: 100%; background: black; z-index: 50; overflow: hidden; }}
            video {{ width: 100%; display: block; }}
            video::-webkit-media-controls-fullscreen-button {{ display: none !important; }}
            
            .cinema-trigger {{
                position: absolute; bottom: 10px; right: 15px; z-index: 60;
                color: white; background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
                padding: 6px 12px; border-radius: 8px; font-size: 13px; font-weight: bold;
                border: 1px solid rgba(255,255,255,0.2); cursor: pointer; display: flex; align-items: center; gap: 6px;
            }}
            .details-box {{ padding: 20px; background: white; min-height: 60vh; }}
            
            #fs-layer {{ display: none; position: fixed; inset: 0; background: black; z-index: 9999; width: 100vw; height: 100vh; }}
            .overlay {{ position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: space-between; z-index: 20; transition: opacity 0.2s ease-out; pointer-events: none; }}
            .overlay.active {{ pointer-events: auto; opacity: 1; }}
            .overlay.fade {{ opacity: 0; pointer-events: none; }}
            
            .shade {{ background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent); pointer-events: auto; }}
            .shade-bot {{ background: linear-gradient(to top, rgba(0,0,0,0.95), transparent); pointer-events: auto; }}
            
            input[type=range].seek-slider {{ -webkit-appearance: none; width: 100%; background: transparent; cursor: pointer; height: 20px; }}
            input[type=range].seek-slider::-webkit-slider-thumb {{ -webkit-appearance: none; height: 14px; width: 14px; background: var(--ink-blue); border-radius: 50%; margin-top: -5px; border: 2px solid white; box-shadow: 0 0 10px rgba(255,255,255,0.5); transform: scale(1); transition: transform 0.1s; }}
            input[type=range].seek-slider::-webkit-slider-runnable-track {{ width: 100%; height: 4px; background: rgba(255,255,255,0.3); border-radius: 2px; }}
            
            .speed-container {{
                position: absolute; right: 40px; top: 50%; transform: translateY(-50%);
                height: 180px; width: 50px; background: rgba(20,20,20,0.85); backdrop-filter: blur(8px);
                border-radius: 25px; border: 1px solid rgba(255,255,255,0.1);
                display: none; flex-direction: column; align-items: center; justify-content: space-between;
                padding: 15px 0; transition: all 0.2s; pointer-events: auto;
            }}
            .speed-val {{ color: white; font-weight: bold; font-size: 14px; margin-bottom: 5px; }}
            .v-slider-wrapper {{ height: 120px; display: flex; align-items: center; }}
            input[type=range].v-slider {{
                -webkit-appearance: none; width: 120px; height: 4px; background: rgba(255,255,255,0.2);
                border-radius: 2px; transform: rotate(-90deg); cursor: pointer;
            }}
            input[type=range].v-slider::-webkit-slider-thumb {{
                -webkit-appearance: none; height: 16px; width: 16px; background: #4ade80; border-radius: 50%;
                box-shadow: 0 0 8px rgba(74, 222, 128, 0.6); border: 2px solid white;
            }}

            .hud {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.6); backdrop-filter: blur(10px); padding: 20px; border-radius: 16px; display: flex; flex-direction: column; align-items: center; min-width: 120px; border: 1px solid rgba(255,255,255,0.1); opacity: 0; transition: opacity 0.2s; pointer-events: none; }}
            .hud-bar {{ width: 100%; height: 4px; background: rgba(255,255,255,0.2); border-radius: 2px; margin-top: 8px; overflow: hidden; }}
            .hud-fill {{ height: 100%; background: var(--ink-blue); width: 0%; transition: width 0.05s linear; }}
            .ai-badge {{ position: absolute; top: 20px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.7); color: #4ade80; padding: 5px 12px; border-radius: 20px; font-size: 12px; display: none; align-items: center; gap: 6px; border: 1px solid rgba(74, 222, 128, 0.3); }}
            .pulse {{ width: 8px; height: 8px; background: #4ade80; border-radius: 50%; animation: pulse 1.5s infinite; }}
            @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
            #bright-mask {{ position: absolute; inset: 0; background: black; opacity: 0; pointer-events: none; z-index: 5; }}
            .c-btn {{ color: white; font-size: 2.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5)); cursor: pointer; transition: transform 0.1s; pointer-events: auto; }}
            .c-btn:active {{ transform: scale(0.9); }}
        </style>
    </head>
    <body>
        <div id="defaultMode">
            <div class="default-container relative">
                <video id="vid" playsinline controls controlsList="nodownload"><source src="/stream/{class_id}" type="video/mp4" /></video>
                <div class="cinema-trigger" onclick="enterCinema()"><i class="fas fa-expand"></i> Cinema</div>
            </div>
            <div class="details-box">
                <div class="flex justify-between items-start mb-6 gap-4">
                    <h1 class="text-xl font-bold text-[#4A4A4A] leading-snug">{real_title}</h1>
                    <button onclick="window.history.back()" class="bg-[#CBCBCB] px-4 py-2 rounded-lg text-sm font-bold shadow-sm shrink-0">Back</button>
                </div>
                <div class="bg-[#FFFFE3] border border-[#CBCBCB] rounded-xl p-5 text-sm text-[#4A4A4A] font-mono leading-relaxed shadow-inner">{caption}</div>
            </div>
        </div>

        <div id="fs-layer">
            <div id="fs-box" class="relative w-full h-full bg-black flex items-center justify-center">
                <div id="bright-mask"></div>
                <div id="hud" class="hud"><i id="h-icon" class="fas fa-volume-up text-2xl text-white mb-2"></i><div id="h-val" class="text-white font-bold text-lg">50%</div><div class="hud-bar"><div id="h-fill" class="hud-fill"></div></div></div>
                <div id="ai-status" class="ai-badge"><div class="pulse"></div> AI Captions: Hindi (Generated)</div>

                <div id="speedCtrl" class="speed-container">
                    <div id="spVal" class="speed-val">1.0x</div>
                    <div class="v-slider-wrapper">
                        <input type="range" class="v-slider" min="0.5" max="3.0" step="0.25" value="1.0" oninput="setSpeed(this.value)">
                    </div>
                    <i class="fas fa-tachometer-alt text-gray-400 text-sm"></i>
                </div>

                <div id="overlay" class="overlay active">
                    <div class="shade p-5 flex justify-between items-center text-white">
                        <div class="flex items-center gap-4"><i class="fas fa-arrow-left text-xl cursor-pointer pointer-events-auto" onclick="exitCinema()"></i><div><h2 class="font-bold text-lg line-clamp-1">{real_title}</h2><p class="text-xs opacity-70">High-Tech Player</p></div></div>
                        <div class="flex gap-6 text-xl">
                            <i class="fas fa-clone cursor-pointer pointer-events-auto" onclick="togglePiP()" title="PiP Mode"></i>
                            <i class="fas fa-closed-captioning cursor-pointer pointer-events-auto opacity-70" onclick="toggleAI()"></i>
                            <i class="fas fa-tachometer-alt cursor-pointer pointer-events-auto" onclick="toggleSpeedMenu()"></i>
                        </div>
                    </div>
                    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex items-center gap-12 pointer-events-auto">
                        <i class="fas fa-undo-alt c-btn opacity-80 hover:opacity-100" onclick="seek(-10)"></i>
                        <i class="fas fa-play c-btn text-6xl" id="cPlay" onclick="togglePlay()"></i>
                        <i class="fas fa-redo-alt c-btn opacity-80 hover:opacity-100" onclick="seek(10)"></i>
                    </div>
                    
                    <div class="shade-bot p-5 text-white">
                        <div class="flex justify-between text-sm font-mono font-bold opacity-90 mb-2">
                            <span id="cur">0:00:00</span>
                            <span id="dur">0:00:00</span>
                        </div>
                        <input type="range" id="bar" value="0" max="100" class="seek-slider pointer-events-auto">
                        <div class="flex justify-between items-center mt-3">
                            <div class="flex gap-6 text-sm font-bold"><span onclick="cycleFit()" id="fitTxt" class="cursor-pointer pointer-events-auto">FIT</span><span class="cursor-pointer pointer-events-auto text-gray-400"><i class="fas fa-unlock"></i></span></div>
                            <div class="flex gap-4 items-center"><i class="fas fa-compress text-xl cursor-pointer pointer-events-auto" onclick="exitCinema()"></i></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            const v = document.getElementById('vid');
            const fsBox = document.getElementById('fs-box');
            const overlay = document.getElementById('overlay');
            const hud = document.getElementById('hud');
            const classKey = 'resume_pos_{class_id}';
            let isFull = false, uiTimer;

            v.addEventListener('loadedmetadata', () => {{
                const savedTime = localStorage.getItem(classKey);
                if (savedTime) v.currentTime = parseFloat(savedTime);
            }});

            v.addEventListener('timeupdate', () => {{
                localStorage.setItem(classKey, v.currentTime);
                if(isFull && v.duration) {{
                    document.getElementById('bar').value = (v.currentTime/v.duration)*100; 
                    document.getElementById('cur').innerText = formatTime(v.currentTime);
                    document.getElementById('dur').innerText = formatTime(v.duration);
                }}
            }});

            function formatTime(s) {{
                if(isNaN(s)) return "0:00:00";
                let h = Math.floor(s / 3600);
                let m = Math.floor((s % 3600) / 60);
                let sc = Math.floor(s % 60);
                if(h > 0) return `${{h}}:${{m<10?'0'+m:m}}:${{sc<10?'0'+sc:sc}}`;
                return `${{m}}:${{sc<10?'0'+sc:sc}}`;
            }}

            function enterCinema() {{
                isFull = true; fsBox.insertBefore(v, fsBox.firstChild);
                v.controls = false; v.style.width='100%'; v.style.height='100%';
                document.getElementById('defaultMode').style.display='none';
                document.getElementById('fs-layer').style.display='block';
                if(document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
                if(screen.orientation && screen.orientation.lock) screen.orientation.lock('landscape').catch(()=>{{}});
                resetUI();
            }}
            function exitCinema() {{
                isFull = false;
                document.querySelector('.default-container').insertBefore(v, document.querySelector('.cinema-btn'));
                v.controls = true; v.style.height='auto';
                document.getElementById('fs-layer').style.display='none';
                document.getElementById('defaultMode').style.display='block';
                if(document.exitFullscreen) document.exitFullscreen();
                if(screen.orientation) screen.orientation.unlock();
            }}

            let startX=0, startY=0, startVol=1, startBright=0, startSeek=0;
            let activeGesture = null; 

            fsBox.addEventListener('touchstart', e => {{
                if(e.target.closest('.pointer-events-auto')) return;
                startX = e.touches[0].clientX; startY = e.touches[0].clientY;
                startVol = v.volume; startBright = parseFloat(document.getElementById('bright-mask').style.opacity) || 0;
                startSeek = v.currentTime; activeGesture = null;
            }});

            fsBox.addEventListener('touchmove', e => {{
                if(e.target.closest('.pointer-events-auto')) return;
                e.preventDefault(); 
                const x = e.touches[0].clientX; const y = e.touches[0].clientY;
                const diffX = x - startX; const diffY = startY - y; 

                if (!activeGesture) {{
                    if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 10) activeGesture = 'seek';
                    else if (Math.abs(diffY) > 10) activeGesture = (startX > window.innerWidth / 2) ? 'vol' : 'bright';
                }}

                if (activeGesture === 'vol') {{
                    let val = startVol + (diffY / 200); if(val > 1) val = 1; if(val < 0) val = 0; v.volume = val;
                    showHUD('fa-volume-up', Math.round(val*100)+'%', val*100);
                }} 
                else if (activeGesture === 'bright') {{
                    let val = startBright + (diffY / 300); if(val < 0) val = 0; if(val > 0.8) val = 0.8;
                    document.getElementById('bright-mask').style.opacity = (0.8 - val);
                    let pct = Math.round((val / 0.8) * 100); showHUD('fa-sun', pct+'%', pct);
                }}
                else if (activeGesture === 'seek') {{
                    let time = startSeek + (diffX / 5); if(time < 0) time = 0; if(time > v.duration) time = v.duration; v.currentTime = time;
                    const sign = diffX > 0 ? '+' : '-'; const sec = Math.abs(Math.round(diffX/5));
                    showHUD(diffX > 0 ? 'fa-forward' : 'fa-backward', `${{sign}}${{sec}}s`, 50);
                }}
            }}, {{ passive: false }});

            fsBox.addEventListener('touchend', () => {{ activeGesture = null; setTimeout(() => hud.style.opacity = 0, 300); }});

            function showHUD(icon, text, fill) {{
                document.getElementById('h-icon').className = `fas ${{icon}} hud-icon`;
                document.getElementById('h-val').innerText = text;
                document.getElementById('h-fill').style.width = fill + '%';
                hud.style.opacity = 1;
            }}

            function toggleSpeedMenu() {{ const m = document.getElementById('speedCtrl'); m.style.display = (m.style.display === 'flex') ? 'none' : 'flex'; resetUI(); }}
            function setSpeed(val) {{ v.playbackRate = val; document.getElementById('spVal').innerText = val + 'x'; }}

            function togglePlay() {{ if(v.paused){{v.play(); upd(true);}} else{{v.pause(); upd(false);}} resetUI(); }}
            function upd(p) {{ document.getElementById('cPlay').className = `fas ${{p?'fa-pause':'fa-play'}} c-btn text-6xl`; }}
            v.addEventListener('play', ()=>upd(true)); v.addEventListener('pause', ()=>{{upd(false); overlay.classList.remove('fade');}});
            
            function resetUI() {{ clearTimeout(uiTimer); overlay.classList.remove('fade'); if(!v.paused) uiTimer = setTimeout(()=>overlay.classList.add('fade'), 3000); }}
            fsBox.addEventListener('click', (e) => {{ if(!e.target.closest('.pointer-events-auto')) {{ if(overlay.classList.contains('fade')) resetUI(); else overlay.classList.add('fade'); }} }});
            
            document.getElementById('bar').addEventListener('input', e => v.currentTime = (e.target.value/100)*v.duration);
            function seek(s) {{ v.currentTime += s; resetUI(); showHUD(s>0?'fa-redo':'fa-undo', s>0?'+10s':'-10s', 50); }}
            
            let fit=false; function cycleFit() {{ fit=!fit; v.style.objectFit=fit?'cover':'contain'; document.getElementById('fitTxt').innerText=fit?'FILL':'FIT'; showHUD('fa-expand', fit?'FILL':'FIT', 100); }}
            function togglePiP() {{ if(document.pictureInPictureElement) document.exitPictureInPicture(); else if(document.pictureInPictureEnabled) v.requestPictureInPicture(); }}
            function toggleAI() {{ const b = document.getElementById('ai-status'); b.style.display = (b.style.display === 'flex') ? 'none' : 'flex'; if(b.style.display==='flex') alert('AI Captions: Listening...'); }}
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
        if not client: return web.Response(status=500, text="Server initializing...")
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
    app = web.Application()
    app.add_routes(routes)
    cors = aiohttp_cors.setup(app, defaults={"*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")})
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    await web.TCPSite(runner, '0.0.0.0', port).start()
    print(f"🚀 Server running on port {port}")
    await start_telegram()
    while True: await asyncio.sleep(3600)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(main())
    except KeyboardInterrupt: pass
