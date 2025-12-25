import os
import random
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("EARMEOU_SECRET", "dev-secret-change-me")

THEME = {
    "bg": "#79b49a",
    "surface": "#76a890",
    "elevated": "#d4e8dd",
    "text": "#1a2e26",
    "muted": "#6b8e7a",
    "accent": "#5a9d7a",
    "accent_contrast": "#ffffff",
}

def get_messages():
    if "messages" not in session:
        session["messages"] = []
    return session["messages"]

def add_msg(role, content):
    msgs = get_messages()
    msgs.append({"role": role, "content": content})
    session["messages"] = msgs

def get_response(text):
    responses = [
        "I'm listening. Could you tell me a bit more about that?",
        "That sounds really tough. How long have you been feeling this way?",
        "Thank you for sharing. What do you feel you need right now?",
        "If it helps, we can take it one step at a time.",
        "It's okay to feel exactly how you feel. What's the part that feels heaviest?",
    ]
    return random.choice(responses)

SHELL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ page_title or 'EarMeOut' }}</title>
  <meta name="description" content="EarMeOut: a safe, judgment-free space to vent and feel heard.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/ogl@1.0.3/dist/ogl.umd.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <style>
    .darkveil-canvas { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; border-radius: 28px; }

    /* PillNav Styles */
    .pill-nav-container { position: sticky; top: 0; z-index: 100; display: flex; justify-content: center; padding: 16px; }
    .pill-nav { display: flex; align-items: center; gap: 8px; background: rgba(90,157,122,0.95); backdrop-filter: blur(12px); padding: 8px 16px; border-radius: 999px; box-shadow: 0 4px 24px rgba(0,0,0,0.15); }
    .pill-logo { display: flex; align-items: center; text-decoration: none; font-weight: 800; font-size: 1.4rem; color: #ffffff !important; padding: 4px 12px; }
    .pill-logo img { height: 32px; width: auto; }
    .pill-nav-items { display: flex; align-items: center; overflow: visible; }
    .pill-list { display: flex; list-style: none; margin: 0; padding: 0; gap: 4px; }
    .pill { position: relative; display: flex; align-items: center; justify-content: center; padding: 8px 16px; text-decoration: none; color: #ffffff !important; font-weight: 500; border-radius: 999px; overflow: hidden; cursor: pointer; }
    .pill .hover-circle { position: absolute; left: 50%; background: #fff; border-radius: 50%; pointer-events: none; transform: scale(0); }
    .pill .label-stack { position: relative; display: flex; flex-direction: column; align-items: center; overflow: hidden; height: 1.4em; }
    .pill .pill-label { color: #ffffff !important; transition: color 0.2s; display: block; }
    .pill .pill-label-hover { position: absolute; top: 0; color: #1a2e26 !important; opacity: 0; }
    .pill.is-active { background: rgba(255,255,255,0.2); }
    .mobile-menu-button { display: none; background: transparent; border: none; cursor: pointer; padding: 8px; }
    .hamburger-line { display: block; width: 24px; height: 2px; background: #fff; margin: 4px 0; border-radius: 2px; }
    .mobile-menu-popover { position: fixed; top: 80px; left: 50%; transform: translateX(-50%); background: rgba(90,157,122,0.98); backdrop-filter: blur(12px); border-radius: 16px; padding: 16px 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.2); z-index: 99; }
    .mobile-menu-list { list-style: none; margin: 0; padding: 0; }
    .mobile-menu-link { display: block; padding: 12px 0; color: #fff; text-decoration: none; font-weight: 500; text-align: center; }
    .mobile-menu-link.is-active { opacity: 0.7; }
    .desktop-only { display: flex; }
    .mobile-only { display: none; }
    @media (max-width: 768px) {
      .desktop-only { display: none; }
      .mobile-only { display: block; }
      .pill-nav { padding: 8px 12px; }
    }
    :root {
      --color-bg: {{ theme.bg }};
      --color-surface: {{ theme.surface }};
      --color-elevated: {{ theme.elevated }};
      --color-text: {{ theme.text }};
      --color-muted: {{ theme.muted }};
      --color-accent: {{ theme.accent }};
      --color-accent-contrast: {{ theme.accent_contrast }};
      --radius: 14px;
      --shadow-lg: 0 20px 25px -5px rgba(0,0,0,0.25), 0 8px 10px -6px rgba(0,0,0,0.2);
      --shadow-sm: 0 1px 2px rgba(0,0,0,0.25);
    }
    * { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin: 0;
      font-family: 'Oswald', sans-serif;
      color: var(--color-text);
      background: radial-gradient(1200px 800px at 10% 10%, #d4e8dd 0%, #e8f5ef 35%, #f0f7f4 100%), var(--color-bg);
      line-height: 1.5;
      text-align: center;
    }
    .visually-hidden { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,1px,1px); white-space: nowrap; border: 0; }
    .container { width: min(1100px, 92%); margin: 0 auto; }
    .section { padding: 64px 0; }
    .section.alt { background: rgba(212,232,221,0.3); }

    .site-header { position: sticky; top: 0; z-index: 20; background: rgba(232,245,239,0.8); backdrop-filter: saturate(140%) blur(12px); border-bottom: 1px solid rgba(107,142,122,0.2); }
    .nav { display: flex; flex-direction: row; align-items: center; justify-content: space-between; gap: 12px; padding: 14px min(4vw, 22px); }
    .brand { color: var(--color-text); font-weight: 800; text-decoration: none; letter-spacing: 0.2px; font-size: 1.9rem; }
    .nav-links { display: flex; list-style: none; gap: 18px; margin: 0; padding: 0; }
    .nav a { color: var(--color-muted); text-decoration: none; }
    .nav a:hover { color: var(--color-text); }

    .button { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 16px; border-radius: 999px; border: 1px solid transparent; cursor: pointer; transition: transform 0.05s ease, filter 0.15s ease, background 0.2s ease; text-decoration: none; font-weight: 600; }
    .button:active { transform: translateY(1px); }
    .button.primary { background: var(--color-accent); color: var(--color-accent-contrast); box-shadow: 0 8px 24px rgba(90,157,122,0.3); border-color: transparent; }
    .button.secondary { background: transparent; color: var(--color-text); border-color: rgba(107,142,122,0.3); border: 1px solid rgba(107,142,122,0.3); }

    .site-footer { padding: 28px 0 40px; background: rgba(232,245,239,0.6); border-top: 1px solid rgba(107,142,122,0.2); }
    .footer-content { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; padding-bottom: 10px; text-align: left; }
    .footer-links { display: flex; gap: 12px; }
    .footer-bottom { color: var(--color-muted); text-align: left; }

    .hero { display: grid; grid-template-columns: 1fr 1fr; align-items: center; gap: clamp(16px, 4vw, 36px); padding: clamp(36px, 7vw, 84px) 0; position: relative; overflow: hidden; border-radius: 28px; background: var(--color-elevated); }
    .hero-content { max-width: 640px; padding-inline: 16px; }
    .hero-content h1 { font-size: clamp(36px, 6.5vw, 64px); line-height: 1.05; margin: 0 0 12px; letter-spacing: -0.02em; text-align: center; }
    .hero-content p { color: var(--color-muted); margin: 0 0 24px; font-size: 1.2rem; }
    .hero-cta { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
    .hero-visual { display: grid; place-items: center; margin-top: -455px; }
    .hero-visual .bot { width: min(420px, 42vw); max-width: 100%; height: auto; filter: drop-shadow(0 10px 30px rgba(90,157,122,0.25)); }
    .hero-veil { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
    .hero > * { position: relative; z-index: 1; }
    .cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
    .card { background: var(--color-elevated); border: 1px solid rgba(107,142,122,0.2); border-radius: 16px; padding: 16px; box-shadow: var(--shadow-sm); text-align: center; }
    .card .photo { width: 100%; aspect-ratio: 1 / 1; border-radius: 12px; background: rgba(232,245,239,0.5); border: 1px solid rgba(107,142,122,0.3); display: grid; place-items: center; color: var(--color-muted); font-size: 0.9rem; overflow: hidden; }
    .card .photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .card .text { margin-top: 10px; color: var(--color-muted); font-size: 0.95rem; }
    .chat { background: var(--color-surface); border: 1px solid rgba(107,142,122,0.3); border-radius: var(--radius); box-shadow: var(--shadow-lg); overflow: hidden; }
    .chat-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: linear-gradient(180deg, rgba(212,232,221,0.3), transparent); border-bottom: 1px solid rgba(107,142,122,0.2); }
    .chat-title { font-weight: 600; }
    .chat-messages { padding: 12px; display: flex; flex-direction: column; gap: 8px; max-height: 40vh; overflow: auto; }
    .bubble { padding: 10px 12px; border-radius: 12px; border: 1px solid rgba(107,142,122,0.3); max-width: 80%; }
    .bubble.assistant { background: rgba(212,232,221,0.4); width: fit-content; }
    .bubble.user { background: rgba(90,157,122,0.2); border-color: rgba(90,157,122,0.4); margin-left: auto; }
    .chat-input { display: grid; grid-template-columns: 1fr auto; gap: 8px; padding: 10px; border-top: 1px solid rgba(107,142,122,0.2); }
    .chat-input input { width: 100%; background: rgba(240,247,244,0.8); color: var(--color-text); border: 1px solid rgba(107,142,122,0.3); border-radius: 999px; padding: 10px 12px; }
    @media (max-width: 960px) { .cards { grid-template-columns: 1fr; } .hero { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="pill-nav-container">
    <nav class="pill-nav" aria-label="Primary">
      <a class="pill-logo" href="{{ url_for('home') }}" aria-label="Home">EarMeOut</a>
      <div class="pill-nav-items desktop-only" id="pill-nav-items">
        <ul class="pill-list" role="menubar">
          <li role="none">
            <a role="menuitem" href="{{ url_for('home') }}" class="pill" data-index="0">
              <span class="hover-circle" aria-hidden="true"></span>
              <span class="label-stack">
                <span class="pill-label">Home</span>
                <span class="pill-label-hover" aria-hidden="true">Home</span>
              </span>
            </a>
          </li>
          <li role="none">
            <a role="menuitem" href="{{ url_for('chat_page') }}" class="pill" data-index="1">
              <span class="hover-circle" aria-hidden="true"></span>
              <span class="label-stack">
                <span class="pill-label">Chat</span>
                <span class="pill-label-hover" aria-hidden="true">Chat</span>
              </span>
            </a>
          </li>
          <li role="none">
            <a role="menuitem" href="{{ url_for('contact') }}" class="pill" data-index="2">
              <span class="hover-circle" aria-hidden="true"></span>
              <span class="label-stack">
                <span class="pill-label">Contact</span>
                <span class="pill-label-hover" aria-hidden="true">Contact</span>
              </span>
            </a>
          </li>
        </ul>
      </div>
      <button class="mobile-menu-button mobile-only" id="mobile-menu-btn" aria-label="Toggle menu">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </button>
    </nav>
    <div class="mobile-menu-popover mobile-only" id="mobile-menu" style="visibility: hidden; opacity: 0;">
      <ul class="mobile-menu-list">
        <li><a href="{{ url_for('home') }}" class="mobile-menu-link">Home</a></li>
        <li><a href="{{ url_for('chat_page') }}" class="mobile-menu-link">Chat</a></li>
        <li><a href="{{ url_for('contact') }}" class="mobile-menu-link">Contact</a></li>
      </ul>
    </div>
  </div>

  {{ content|safe }}

  <footer id="contact" class="site-footer">
    <div class="container footer-content">
      <div>
        <strong>EarMeOut</strong>
        <p>Because being heard matters to us and we want to help.</p>
      </div>
      <div class="footer-links">
        <a href="{{ url_for('chat_page') }}">Chat</a>
        <a href="{{ url_for('home') }}">Top</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <small>
        This site is not a substitute for professional help. If you're in crisis, please contact your local emergency number or a crisis hotline in your region.
      </small>
    </div>
  </footer>
<script>
// Dark Veil Background
document.addEventListener('DOMContentLoaded', function() {
  const canvas = document.getElementById('darkveil-canvas');
  if (!canvas) {
    console.log('No darkveil canvas found');
    return;
  }
  if (typeof OGL === 'undefined') {
    console.error('OGL not loaded');
    return;
  }
  const parent = canvas.parentElement;
  const { Renderer, Program, Mesh, Triangle, Vec2 } = OGL;

  const vertex = `attribute vec2 position;void main(){gl_Position=vec4(position,0.0,1.0);}`;

  const fragment = `
#ifdef GL_ES
precision lowp float;
#endif
uniform vec2 uResolution;
uniform float uTime;
uniform float uHueShift;
uniform float uNoise;
uniform float uScan;
uniform float uScanFreq;
uniform float uWarp;
#define iTime uTime
#define iResolution uResolution

vec4 buf[8];
float rand(vec2 c){return fract(sin(dot(c,vec2(12.9898,78.233)))*43758.5453);}

mat3 rgb2yiq=mat3(0.299,0.587,0.114,0.596,-0.274,-0.322,0.211,-0.523,0.312);
mat3 yiq2rgb=mat3(1.0,0.956,0.621,1.0,-0.272,-0.647,1.0,-1.106,1.703);

vec3 hueShiftRGB(vec3 col,float deg){
    vec3 yiq=rgb2yiq*col;
    float rad=radians(deg);
    float cosh=cos(rad),sinh=sin(rad);
    vec3 yiqShift=vec3(yiq.x,yiq.y*cosh-yiq.z*sinh,yiq.y*sinh+yiq.z*cosh);
    return clamp(yiq2rgb*yiqShift,0.0,1.0);
}

vec4 sigmoid(vec4 x){return 1./(1.+exp(-x));}

vec4 cppn_fn(vec2 coordinate,float in0,float in1,float in2){
    buf[6]=vec4(coordinate.x,coordinate.y,0.3948333106474662+in0,0.36+in1);
    buf[7]=vec4(0.14+in2,sqrt(coordinate.x*coordinate.x+coordinate.y*coordinate.y),0.,0.);
    buf[0]=mat4(vec4(6.5404263,-3.6126034,0.7590882,-1.13613),vec4(2.4582713,3.1660357,1.2219609,0.06276096),vec4(-5.478085,-6.159632,1.8701609,-4.7742867),vec4(6.039214,-5.542865,-0.90925294,3.251348))*buf[6]+mat4(vec4(0.8473259,-5.722911,3.975766,1.6522468),vec4(-0.24321538,0.5839259,-1.7661959,-5.350116),vec4(0.,0.,0.,0.),vec4(0.,0.,0.,0.))*buf[7]+vec4(0.21808943,1.1243913,-1.7969975,5.0294676);
    buf[1]=mat4(vec4(-3.3522482,-6.0612736,0.55641043,-4.4719114),vec4(0.8631464,1.7432913,5.643898,1.6106541),vec4(2.4941394,-3.5012043,1.7184316,6.357333),vec4(3.310376,8.209261,1.1355612,-1.165539))*buf[6]+mat4(vec4(5.24046,-13.034365,0.009859298,15.870829),vec4(2.987511,3.129433,-0.89023495,-1.6822904),vec4(0.,0.,0.,0.),vec4(0.,0.,0.,0.))*buf[7]+vec4(-5.9457836,-6.573602,-0.8812491,1.5436668);
    buf[0]=sigmoid(buf[0]);buf[1]=sigmoid(buf[1]);
    buf[2]=mat4(vec4(-15.219568,8.095543,-2.429353,-1.9381982),vec4(-5.951362,4.3115187,2.6393783,1.274315),vec4(-7.3145227,6.7297835,5.2473326,5.9411426),vec4(5.0796127,8.979051,-1.7278991,-1.158976))*buf[6]+mat4(vec4(-11.967154,-11.608155,6.1486754,11.237008),vec4(2.124141,-6.263192,-1.7050359,-0.7021966),vec4(0.,0.,0.,0.),vec4(0.,0.,0.,0.))*buf[7]+vec4(-4.17164,-3.2281182,-4.576417,-3.6401186);
    buf[3]=mat4(vec4(3.1832156,-13.738922,1.879223,3.233465),vec4(0.64300746,12.768129,1.9141049,0.50990224),vec4(-0.049295485,4.4807224,1.4733979,1.801449),vec4(5.0039253,13.000481,3.3991797,-4.5561905))*buf[6]+mat4(vec4(-0.1285731,7.720628,-3.1425676,4.742367),vec4(0.6393625,3.714393,-0.8108378,-0.39174938),vec4(0.,0.,0.,0.),vec4(0.,0.,0.,0.))*buf[7]+vec4(-1.1811101,-21.621881,0.7851888,1.2329718);
    buf[2]=sigmoid(buf[2]);buf[3]=sigmoid(buf[3]);
    buf[4]=mat4(vec4(5.214916,-7.183024,2.7228765,2.6592617),vec4(-5.601878,-25.3591,4.067988,0.4602802),vec4(-10.57759,24.286327,21.102104,37.546658),vec4(4.3024497,-1.9625226,2.3458803,-1.372816))*buf[0]+mat4(vec4(-17.6526,-10.507558,2.2587414,12.462782),vec4(6.265566,-502.75443,-12.642513,0.9112289),vec4(-10.983244,20.741234,-9.701768,-0.7635988),vec4(5.383626,1.4819539,-4.1911616,-4.8444734))*buf[1]+mat4(vec4(12.785233,-16.345072,-0.39901125,1.7955981),vec4(-30.48365,-1.8345358,1.4542528,-1.1118771),vec4(19.872723,-7.337935,-42.941723,-98.52709),vec4(8.337645,-2.7312303,-2.2927687,-36.142323))*buf[2]+mat4(vec4(-16.298317,3.5471997,-0.44300047,-9.444417),vec4(57.5077,-35.609753,16.163465,-4.1534753),vec4(-0.07470326,-3.8656476,-7.0901804,3.1523974),vec4(-12.559385,-7.077619,1.490437,-0.8211543))*buf[3]+vec4(-7.67914,15.927437,1.3207729,-1.6686112);
    buf[5]=mat4(vec4(-1.4109162,-0.372762,-3.770383,-21.367174),vec4(-6.2103205,-9.35908,0.92529047,8.82561),vec4(11.460242,-22.348068,13.625772,-18.693201),vec4(-0.3429052,-3.9905605,-2.4626114,-0.45033523))*buf[0]+mat4(vec4(7.3481627,-4.3661838,-6.3037653,-3.868115),vec4(1.5462853,6.5488915,1.9701879,-0.58291394),vec4(6.5858274,-2.2180402,3.7127688,-1.3730392),vec4(-5.7973905,10.134961,-2.3395722,-5.965605))*buf[1]+mat4(vec4(-2.5132585,-6.6685553,-1.4029363,-0.16285264),vec4(-0.37908727,0.53738135,4.389061,-1.3024765),vec4(-0.70647055,2.0111287,-5.1659346,-3.728635),vec4(-13.562562,10.487719,-0.9173751,-2.6487076))*buf[2]+mat4(vec4(-8.645013,6.5546675,-6.3944063,-5.5933375),vec4(-0.57783127,-1.077275,36.91025,5.736769),vec4(14.283112,3.7146652,7.1452246,-4.5958776),vec4(2.7192075,3.6021907,-4.366337,-2.3653464))*buf[3]+vec4(-5.9000807,-4.329569,1.2427121,8.59503);
    buf[4]=sigmoid(buf[4]);buf[5]=sigmoid(buf[5]);
    buf[6]=mat4(vec4(-1.61102,0.7970257,1.4675229,0.20917463),vec4(-28.793737,-7.1390953,1.5025433,4.656581),vec4(-10.94861,39.66238,0.74318546,-10.095605),vec4(-0.7229728,-1.5483948,0.7301322,2.1687684))*buf[0]+mat4(vec4(3.2547753,21.489103,-1.0194173,-3.3100595),vec4(-3.7316632,-3.3792162,-7.223193,-0.23685838),vec4(13.1804495,0.7916005,5.338587,5.687114),vec4(-4.167605,-17.798311,-6.815736,-1.6451967))*buf[1]+mat4(vec4(0.604885,-7.800309,-7.213122,-2.741014),vec4(-3.522382,-0.12359311,-0.5258442,0.43852118),vec4(9.6752825,-22.853785,2.062431,0.099892326),vec4(-4.3196306,-17.730087,2.5184598,5.30267))*buf[2]+mat4(vec4(-6.545563,-15.790176,-6.0438633,-5.415399),vec4(-43.591583,28.551912,-16.00161,18.84728),vec4(4.212382,8.394307,3.0958717,8.657522),vec4(-5.0237565,-4.450633,-4.4768,-5.5010443))*buf[3]+mat4(vec4(1.6985557,-67.05806,6.897715,1.9004834),vec4(1.8680354,2.3915145,2.5231109,4.081538),vec4(11.158006,1.7294737,2.0738268,7.386411),vec4(-4.256034,-306.24686,8.258898,-17.132736))*buf[4]+mat4(vec4(1.6889864,-4.5852966,3.8534803,-6.3482175),vec4(1.3543309,-1.2640043,9.932754,2.9079645),vec4(-5.2770967,0.07150358,-0.13962056,3.3269649),vec4(28.34703,-4.918278,6.1044083,4.085355))*buf[5]+vec4(6.6818056,12.522166,-3.7075126,-4.104386);
    buf[7]=mat4(vec4(-8.265602,-4.7027016,5.098234,0.7509808),vec4(8.6507845,-17.15949,16.51939,-8.884479),vec4(-4.036479,-2.3946867,-2.6055532,-1.9866527),vec4(-2.2167742,-1.8135649,-5.9759874,4.8846445))*buf[0]+mat4(vec4(6.7790847,3.5076547,-2.8191125,-2.7028968),vec4(-5.743024,-0.27844876,1.4958696,-5.0517144),vec4(13.122226,15.735168,-2.9397483,-4.101023),vec4(-14.375265,-5.030483,-6.2599335,2.9848232))*buf[1]+mat4(vec4(4.0950394,-0.94011575,-5.674733,4.755022),vec4(4.3809423,4.8310084,1.7425908,-3.437416),vec4(2.117492,0.16342592,-104.56341,16.949184),vec4(-5.22543,-2.994248,3.8350096,-1.9364246))*buf[2]+mat4(vec4(-5.900337,1.7946124,-13.604192,-3.8060522),vec4(6.6583457,31.911177,25.164474,91.81147),vec4(11.840538,4.1503043,-0.7314397,6.768467),vec4(-6.3967767,4.034772,6.1714606,-0.32874924))*buf[3]+mat4(vec4(3.4992442,-196.91893,-8.923708,2.8142626),vec4(3.4806502,-3.1846354,5.1725626,5.1804223),vec4(-2.4009497,15.585794,1.2863957,2.0252278),vec4(-71.25271,-62.441242,-8.138444,0.50670296))*buf[4]+mat4(vec4(-12.291733,-11.176166,-7.3474145,4.390294),vec4(10.805477,5.6337385,-0.9385842,-4.7348723),vec4(-12.869276,-7.039391,5.3029537,7.5436664),vec4(1.4593618,8.91898,3.5101583,5.840625))*buf[5]+vec4(2.2415268,-6.705987,-0.98861027,-2.117676);
    buf[6]=sigmoid(buf[6]);buf[7]=sigmoid(buf[7]);
    buf[0]=mat4(vec4(1.6794263,1.3817469,2.9625452,0.),vec4(-1.8834411,-1.4806935,-3.5924516,0.),vec4(-1.3279216,-1.0918057,-2.3124623,0.),vec4(0.2662234,0.23235129,0.44178495,0.))*buf[0]+mat4(vec4(-0.6299101,-0.5945583,-0.9125601,0.),vec4(0.17828953,0.18300213,0.18182953,0.),vec4(-2.96544,-2.5819945,-4.9001055,0.),vec4(1.4195864,1.1868085,2.5176322,0.))*buf[1]+mat4(vec4(-1.2584374,-1.0552157,-2.1688404,0.),vec4(-0.7200217,-0.52666044,-1.438251,0.),vec4(0.15345335,0.15196142,0.272854,0.),vec4(0.945728,0.8861938,1.2766753,0.))*buf[2]+mat4(vec4(-2.4218085,-1.968602,-4.35166,0.),vec4(-22.683098,-18.0544,-41.954372,0.),vec4(0.63792,0.5470648,1.1078634,0.),vec4(-1.5489894,-1.3075932,-2.6444845,0.))*buf[3]+mat4(vec4(-0.49252132,-0.39877754,-0.91366625,0.),vec4(0.95609266,0.7923952,1.640221,0.),vec4(0.30616966,0.15693925,0.8639857,0.),vec4(1.1825981,0.94504964,2.176963,0.))*buf[4]+mat4(vec4(0.35446745,0.3293795,0.59547555,0.),vec4(-0.58784515,-0.48177817,-1.0614829,0.),vec4(2.5271258,1.9991658,4.6846647,0.),vec4(0.13042648,0.08864098,0.30187556,0.))*buf[5]+mat4(vec4(-1.7718065,-1.4033192,-3.3355875,0.),vec4(3.1664357,2.638297,5.378702,0.),vec4(-3.1724713,-2.6107926,-5.549295,0.),vec4(-2.851368,-2.249092,-5.3013067,0.))*buf[6]+mat4(vec4(1.5203838,1.2212278,2.8404984,0.),vec4(1.5210563,1.2651345,2.683903,0.),vec4(2.9789467,2.4364579,5.2347264,0.),vec4(2.2270417,1.8825914,3.8028636,0.))*buf[7]+vec4(-1.5468478,-3.6171484,0.24762098,0.);
    buf[0]=sigmoid(buf[0]);
    return vec4(buf[0].x,buf[0].y,buf[0].z,1.);
}

void mainImage(out vec4 fragColor,in vec2 fragCoord){
    vec2 uv=fragCoord/uResolution.xy*2.-1.;
    uv.y*=-1.;
    uv+=uWarp*vec2(sin(uv.y*6.283+uTime*0.5),cos(uv.x*6.283+uTime*0.5))*0.05;
    fragColor=cppn_fn(uv,0.1*sin(0.3*uTime),0.1*sin(0.69*uTime),0.1*sin(0.44*uTime));
}

void main(){
    vec4 col;mainImage(col,gl_FragCoord.xy);
    col.rgb=hueShiftRGB(col.rgb,uHueShift);
    float scanline_val=sin(gl_FragCoord.y*uScanFreq)*0.5+0.5;
    col.rgb*=1.-(scanline_val*scanline_val)*uScan;
    col.rgb+=(rand(gl_FragCoord.xy+uTime)-0.5)*uNoise;
    gl_FragColor=vec4(clamp(col.rgb,0.0,1.0),1.0);
}
`;

  const hueShift = 100;
  const noiseIntensity = 0;
  const scanlineIntensity = 0;
  const speed = 0.5;
  const scanlineFrequency = 0;
  const warpAmount = 0;
  const resolutionScale = 1;

  const renderer = new Renderer({ dpr: Math.min(window.devicePixelRatio, 2), canvas });
  const gl = renderer.gl;
  const geometry = new Triangle(gl);

  const program = new Program(gl, {
    vertex,
    fragment,
    uniforms: {
      uTime: { value: 0 },
      uResolution: { value: new Vec2() },
      uHueShift: { value: hueShift },
      uNoise: { value: noiseIntensity },
      uScan: { value: scanlineIntensity },
      uScanFreq: { value: scanlineFrequency },
      uWarp: { value: warpAmount }
    }
  });

  const mesh = new Mesh(gl, { geometry, program });

  const resize = () => {
    const w = parent.clientWidth, h = parent.clientHeight;
    renderer.setSize(w * resolutionScale, h * resolutionScale);
    program.uniforms.uResolution.value.set(w, h);
  };

  window.addEventListener('resize', resize);
  resize();

  const start = performance.now();
  let frame = 0;

  const loop = () => {
    program.uniforms.uTime.value = ((performance.now() - start) / 1000) * speed;
    renderer.render({ scene: mesh });
    frame = requestAnimationFrame(loop);
  };

  loop();
});

// PillNav Animation
document.addEventListener('DOMContentLoaded', function() {
  if (typeof gsap === 'undefined') {
    console.error('GSAP not loaded');
    return;
  }

  const pills = document.querySelectorAll('.pill');
  const ease = 'power3.out';

  pills.forEach((pill) => {
    const circle = pill.querySelector('.hover-circle');
    const label = pill.querySelector('.pill-label');
    const hoverLabel = pill.querySelector('.pill-label-hover');

    if (circle) {
      const rect = pill.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height) * 2;
      circle.style.width = size + 'px';
      circle.style.height = size + 'px';
      circle.style.bottom = '-' + (size / 2) + 'px';
      gsap.set(circle, { xPercent: -50, scale: 0 });
    }

    if (hoverLabel) {
      gsap.set(hoverLabel, { y: 20, opacity: 0 });
    }

    pill.addEventListener('mouseenter', () => {
      if (circle) gsap.to(circle, { scale: 1, duration: 0.4, ease });
      if (label) gsap.to(label, { y: -20, opacity: 0, duration: 0.3, ease });
      if (hoverLabel) gsap.to(hoverLabel, { y: 0, opacity: 1, duration: 0.3, ease });
    });

    pill.addEventListener('mouseleave', () => {
      if (circle) gsap.to(circle, { scale: 0, duration: 0.3, ease });
      if (label) gsap.to(label, { y: 0, opacity: 1, duration: 0.3, ease });
      if (hoverLabel) gsap.to(hoverLabel, { y: 20, opacity: 0, duration: 0.3, ease });
    });
  });

  // Mobile menu
  const menuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  let menuOpen = false;

  if (menuBtn && mobileMenu) {
    menuBtn.addEventListener('click', () => {
      menuOpen = !menuOpen;
      const lines = menuBtn.querySelectorAll('.hamburger-line');
      if (menuOpen) {
        gsap.to(lines[0], { rotation: 45, y: 3, duration: 0.3, ease });
        gsap.to(lines[1], { rotation: -45, y: -3, duration: 0.3, ease });
        gsap.set(mobileMenu, { visibility: 'visible' });
        gsap.to(mobileMenu, { opacity: 1, y: 0, duration: 0.3, ease });
      } else {
        gsap.to(lines[0], { rotation: 0, y: 0, duration: 0.3, ease });
        gsap.to(lines[1], { rotation: 0, y: 0, duration: 0.3, ease });
        gsap.to(mobileMenu, { opacity: 0, y: 10, duration: 0.2, ease, onComplete: () => gsap.set(mobileMenu, { visibility: 'hidden' }) });
      }
    });
  }

  // Initial load animation
  const logo = document.querySelector('.pill-logo');
  const navItems = document.getElementById('pill-nav-items');
  if (logo) {
    gsap.from(logo, { scale: 0, duration: 0.6, ease, delay: 0.1 });
  }
  if (navItems) {
    gsap.from(navItems, { width: 0, opacity: 0, duration: 0.6, ease, delay: 0.2 });
  }
});
</script>
</body>
</html>
"""


def render_page(content, title):
    return render_template_string(SHELL_TEMPLATE, theme=THEME, content=content, page_title=title)


@app.get("/")
def home():
    content = """
        <main id="home" class="site-main">
          <section class="hero container">
            <canvas id="darkveil-canvas" class="darkveil-canvas"></canvas>
            <div class="hero-content">
              <h1>Vent without judgement.</h1>
              <p>Your mental health matters. Talk to someone who cares, 24/7.</p>
              <div class="hero-cta">
                <a class="button primary" href="{{ url_for('chat_page') }}">Start Talking</a>
                <a class="button secondary" href="{{ url_for('contact') }}">Learn More</a>
              </div>
            </div>
            <div class="hero-visual">
              <img class="bot" alt="EarMeOut bot" src="{{ url_for('static', filename='bot.png') }}" onerror="this.style.display='none'">
            </div>
          </section>
        </main>
        """
    return render_page(render_template_string(content), "EarMeOut — Home")


@app.get("/chat")
def chat_page():
    messages = get_messages()
    content = render_template_string(
        """
        <main class="site-main">
          <section class="section">
            <div class="container" style="max-width: 720px;">
              <div class="chat" style="min-height: 60vh; display: flex; flex-direction: column;">
                <div class="chat-header">
                  <div class="chat-title">🎧 EarMeOut</div>
                  <form method="post" action="{{ url_for('reset_chat') }}">
                    <button class="button secondary" type="submit">Reset</button>
                  </form>
                </div>
                <div class="chat-messages" style="flex: 1; min-height: 300px;">
                  {% if not messages %}
                    <div class="bubble assistant">Hi, I'm here to listen. What's on your mind today?</div>
                  {% else %}
                    {% for m in messages %}
                      <div class="bubble {{ m.role }}">{{ m.content }}</div>
                    {% endfor %}
                  {% endif %}
                </div>
                <form class="chat-input" method="post" action="{{ url_for('send_message') }}" autocomplete="off">
                  <label for="message" class="visually-hidden">Message</label>
                  <input id="message" name="message" type="text" placeholder="Type your message..." required>
                  <button class="button primary" type="submit">Send</button>
                </form>
              </div>
            </div>
          </section>
        </main>
        """,
        messages=messages,
    )
    return render_page(content, "EarMeOut — Chat")


@app.post("/chat")
def send_message():
    text = request.form.get("message", "").strip()
    if text:
        add_msg("user", text)
        reply = get_response(text)
        add_msg("assistant", reply)
    return redirect(url_for("chat_page"))


@app.post("/reset")
def reset_chat():
    session.pop("messages", None)
    return redirect(url_for("chat_page"))


@app.get("/about")
def about():
    content = """
    <main class="site-main">
      <section class="section">
        <div class="container">
          <h1>About EarMeOut</h1>
          <p style="color:var(--color-muted)">We're a team committed to creating a supportive, judgment-free space.</p>
          <div class="cards" style="margin-top:18px;">
            <div class="card">
              <div class="photo">Member 1 Photo</div>
              <div class="text">Member 1 bio/role text goes here.</div>
            </div>
            <div class="card">
              <div class="photo">Member 2 Photo</div>
              <div class="text">Member 2 bio/role text goes here.</div>
            </div>
            <div class="card">
              <div class="photo">Member 3 Photo</div>
              <div class="text">Member 3 bio/role text goes here.</div>
            </div>
          </div>
        </div>
      </section>
    </main>
    """
    return render_page(content, "EarMeOut — About")

@app.get("/contact")
def contact():
    content = """
    <main class="site-main">
      <section class="section">
        <div class="container">
          <h1>Contact</h1>
          <p style="color:var(--color-muted)">We'd love to hear from you. Reach us at <a href="mailto:earmeoutnonprofit@gmail.com">earmeoutnonprofit@gmail.com</a>.</p>
        </div>
      </section>
    </main>
    """
    return render_page(content, "EarMeOut — Contact")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
