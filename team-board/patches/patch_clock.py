p='team.html'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]); s=s.replace(a,b)

LIGHT='--paper:#F4F4F2;--surface:#FFFFFF;--ink:#141417;--muted:#5E5E66;--line:#E2E2DF;--accent:#EB1843;--accent-ink:#FFFFFF;--strike:#B0102C;--soft:#ECECE9;--p0:#EB1843;--p1:#141417;--p2:#6B4FC8;--p3:#1F6FB5;--p4:#2E7D46;--p5:#C2410C;--p6:#8A6A12;color-scheme:light'
DARK='--paper:#0E0E11;--surface:#18181C;--ink:#EDEDF0;--muted:#9A9AA3;--line:#2C2C33;--accent:#FF4D6D;--accent-ink:#17080B;--strike:#FF8A9C;--soft:#232329;--p0:#FF4D6D;--p1:#E6E6EA;--p2:#A48CF0;--p3:#6FB0EE;--p4:#66C987;--p5:#F59E5B;--p6:#D9B44A;color-scheme:dark'
rep('.col.is-me{box-shadow:0 0 0 2px var(--c)}',
'''.col.is-me{box-shadow:0 0 0 2px var(--c)}
.col.day{'''+LIGHT+''';background:var(--surface);color:var(--ink)}
.col.night{'''+DARK+''';background:var(--surface);color:var(--ink)}
.col{transition:background-color .6s,color .6s}
.clock{display:inline-flex;align-items:center;gap:5px;margin-left:8px;padding:1px 8px 1px 6px;border-radius:999px;background:var(--soft);color:var(--ink);font-size:13px;font-weight:600;font-variant-numeric:tabular-nums;white-space:nowrap}
.clock svg{flex:none}
.clock .sun{color:#E8A317}.clock .moon{color:#B9B4F5}
.where-edit{flex-wrap:wrap}
.where-edit select{font:inherit;font-size:14px;color:var(--ink);border:1px solid var(--line);background:var(--surface);border-radius:8px;padding:5px 7px;max-width:240px}
.where-edit .tzq{flex-basis:100%;margin:0;font-size:13px;color:var(--muted)}''')

JS = r'''
  // ---------- local time & day/night per location ----------
  var CITIES = {
    'dubai':[25.20,55.27,'Asia/Dubai'],'abu dhabi':[24.45,54.38,'Asia/Dubai'],'sharjah':[25.35,55.42,'Asia/Dubai'],'ras al khaimah':[25.79,55.94,'Asia/Dubai'],'uae':[25.20,55.27,'Asia/Dubai'],
    'riyadh':[24.71,46.68,'Asia/Riyadh'],'jeddah':[21.49,39.19,'Asia/Riyadh'],'alula':[26.61,37.92,'Asia/Riyadh'],'neom':[28.00,35.20,'Asia/Riyadh'],'dammam':[26.42,50.09,'Asia/Riyadh'],
    'doha':[25.29,51.53,'Asia/Qatar'],'kuwait':[29.38,47.99,'Asia/Kuwait'],'kuwait city':[29.38,47.99,'Asia/Kuwait'],'muscat':[23.59,58.41,'Asia/Muscat'],'manama':[26.23,50.59,'Asia/Bahrain'],'bahrain':[26.23,50.59,'Asia/Bahrain'],
    'beirut':[33.89,35.50,'Asia/Beirut'],'amman':[31.95,35.93,'Asia/Amman'],'cairo':[30.04,31.24,'Africa/Cairo'],'istanbul':[41.01,28.98,'Europe/Istanbul'],'baghdad':[33.31,44.36,'Asia/Baghdad'],'tehran':[35.69,51.39,'Asia/Tehran'],
    'cape town':[-33.92,18.42,'Africa/Johannesburg'],'johannesburg':[-26.20,28.05,'Africa/Johannesburg'],'durban':[-29.86,31.03,'Africa/Johannesburg'],'nairobi':[-1.29,36.82,'Africa/Nairobi'],'lagos':[6.52,3.38,'Africa/Lagos'],'addis ababa':[9.03,38.74,'Africa/Addis_Ababa'],'casablanca':[33.57,-7.59,'Africa/Casablanca'],'marrakech':[31.63,-8.01,'Africa/Casablanca'],
    'london':[51.51,-0.13,'Europe/London'],'manchester':[53.48,-2.24,'Europe/London'],'liverpool':[53.41,-2.98,'Europe/London'],'dublin':[53.35,-6.26,'Europe/Dublin'],'edinburgh':[55.95,-3.19,'Europe/London'],
    'paris':[48.86,2.35,'Europe/Paris'],'cannes':[43.55,7.01,'Europe/Paris'],'berlin':[52.52,13.40,'Europe/Berlin'],'munich':[48.14,11.58,'Europe/Berlin'],'amsterdam':[52.37,4.90,'Europe/Amsterdam'],'brussels':[50.85,4.35,'Europe/Brussels'],
    'madrid':[40.42,-3.70,'Europe/Madrid'],'barcelona':[41.39,2.17,'Europe/Madrid'],'cordoba':[37.88,-4.78,'Europe/Madrid'],'seville':[37.39,-5.98,'Europe/Madrid'],'lisbon':[38.72,-9.14,'Europe/Lisbon'],
    'rome':[41.90,12.50,'Europe/Rome'],'milan':[45.46,9.19,'Europe/Rome'],'florence':[43.77,11.26,'Europe/Rome'],'tuscany':[43.77,11.26,'Europe/Rome'],'athens':[37.98,23.73,'Europe/Athens'],'nicosia':[35.17,33.36,'Asia/Nicosia'],'limassol':[34.68,33.04,'Asia/Nicosia'],
    'bratislava':[48.15,17.11,'Europe/Bratislava'],'vienna':[48.21,16.37,'Europe/Vienna'],'prague':[50.08,14.44,'Europe/Prague'],'budapest':[47.50,19.04,'Europe/Budapest'],'warsaw':[52.23,21.01,'Europe/Warsaw'],'bucharest':[44.43,26.10,'Europe/Bucharest'],'belgrade':[44.79,20.45,'Europe/Belgrade'],'zurich':[47.38,8.54,'Europe/Zurich'],'geneva':[46.20,6.14,'Europe/Zurich'],
    'stockholm':[59.33,18.07,'Europe/Stockholm'],'oslo':[59.91,10.75,'Europe/Oslo'],'copenhagen':[55.68,12.57,'Europe/Copenhagen'],'helsinki':[60.17,24.94,'Europe/Helsinki'],'reykjavik':[64.15,-21.94,'Atlantic/Reykjavik'],'iceland':[64.15,-21.94,'Atlantic/Reykjavik'],
    'moscow':[55.76,37.62,'Europe/Moscow'],'kyiv':[50.45,30.52,'Europe/Kyiv'],'tbilisi':[41.72,44.79,'Asia/Tbilisi'],'baku':[40.41,49.87,'Asia/Baku'],'tashkent':[41.30,69.24,'Asia/Tashkent'],'almaty':[43.24,76.89,'Asia/Almaty'],
    'mumbai':[19.08,72.88,'Asia/Kolkata'],'delhi':[28.61,77.21,'Asia/Kolkata'],'new delhi':[28.61,77.21,'Asia/Kolkata'],'bangalore':[12.97,77.59,'Asia/Kolkata'],'bengaluru':[12.97,77.59,'Asia/Kolkata'],'chennai':[13.08,80.27,'Asia/Kolkata'],'kochi':[9.93,76.27,'Asia/Kolkata'],'kerala':[9.93,76.27,'Asia/Kolkata'],'hyderabad':[17.39,78.49,'Asia/Kolkata'],
    'karachi':[24.86,67.01,'Asia/Karachi'],'lahore':[31.55,74.34,'Asia/Karachi'],'colombo':[6.93,79.86,'Asia/Colombo'],'kathmandu':[27.72,85.32,'Asia/Kathmandu'],'dhaka':[23.81,90.41,'Asia/Dhaka'],
    'singapore':[1.35,103.82,'Asia/Singapore'],'bangkok':[13.76,100.50,'Asia/Bangkok'],'manila':[14.60,120.98,'Asia/Manila'],'jakarta':[-6.21,106.85,'Asia/Jakarta'],'bali':[-8.65,115.22,'Asia/Makassar'],'kuala lumpur':[3.14,101.69,'Asia/Kuala_Lumpur'],
    'hong kong':[22.32,114.17,'Asia/Hong_Kong'],'shanghai':[31.23,121.47,'Asia/Shanghai'],'beijing':[39.90,116.41,'Asia/Shanghai'],'seoul':[37.57,126.98,'Asia/Seoul'],'tokyo':[35.68,139.69,'Asia/Tokyo'],
    'sydney':[-33.87,151.21,'Australia/Sydney'],'melbourne':[-37.81,144.96,'Australia/Melbourne'],'auckland':[-36.85,174.76,'Pacific/Auckland'],
    'new york':[40.71,-74.01,'America/New_York'],'nyc':[40.71,-74.01,'America/New_York'],'miami':[25.76,-80.19,'America/New_York'],'toronto':[43.65,-79.38,'America/Toronto'],'montreal':[45.50,-73.57,'America/Toronto'],'vancouver':[49.28,-123.12,'America/Vancouver'],
    'los angeles':[34.05,-118.24,'America/Los_Angeles'],'la':[34.05,-118.24,'America/Los_Angeles'],'san francisco':[37.77,-122.42,'America/Los_Angeles'],'chicago':[41.88,-87.63,'America/Chicago'],'mexico city':[19.43,-99.13,'America/Mexico_City'],'sao paulo':[-23.55,-46.63,'America/Sao_Paulo'],'buenos aires':[-34.60,-58.38,'America/Argentina/Buenos_Aires']
  };
  var CITY_NAMES = ['Dubai','Abu Dhabi','Riyadh','Cape Town','Jeddah','Doha','London','Bratislava','Paris','Cairo','Beirut','Istanbul','Mumbai','Kochi','Johannesburg','New York','Los Angeles','Singapore','Reykjavik'];
  function cityKey(v){ return String(v || '').trim().toLowerCase().replace(/[^a-z ]/g, '').replace(/\s+/g, ' ').replace(/^(the )/, ''); }
  function cityInfo(v){
    var k = cityKey(v); if(!k) return null;
    if(CITIES[k]) return CITIES[k];
    var first = k.split(/,| - /)[0].trim(); if(CITIES[first]) return CITIES[first];
    return null;
  }
  function validTz(tz){ try { new Intl.DateTimeFormat('en-GB', { timeZone: tz }); return true; } catch(e){ return false; } }
  function tzOf(p){ var c = cityInfo(p.location); if(c) return c[2]; if(p.tz && validTz(p.tz)) return p.tz; return null; }
  function localParts(tz, d){
    var parts = {}; new Intl.DateTimeFormat('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit', weekday: 'short', hourCycle: 'h23' }).formatToParts(d).forEach(function(x){ parts[x.type] = x.value; });
    return parts;
  }
  function sunAltitude(lat, lon, d){
    var rad = Math.PI / 180, n = d.getTime() / 86400000 + 2440587.5 - 2451545.0;
    var L = (280.460 + 0.9856474 * n) % 360, g = ((357.528 + 0.9856003 * n) % 360) * rad;
    var lam = (L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * rad, eps = (23.439 - 0.0000004 * n) * rad;
    var ra = Math.atan2(Math.cos(eps) * Math.sin(lam), Math.cos(lam)), dec = Math.asin(Math.sin(eps) * Math.sin(lam));
    var gmst = (18.697374558 + 24.06570982441908 * n) % 24;
    var ha = ((gmst * 15 + lon) * rad) - ra;
    return Math.asin(Math.sin(lat * rad) * Math.sin(dec) + Math.cos(lat * rad) * Math.cos(dec) * Math.cos(ha)) / rad;
  }
  function isNight(p, d){
    var c = cityInfo(p.location);
    if(c) return sunAltitude(c[0], c[1], d) < -0.833;
    var tz = tzOf(p); if(!tz) return null;
    var h = +localParts(tz, d).hour; return h < 6 || h >= 19;
  }
  var SUN = '<svg class="sun" width="13" height="13" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3.2" fill="currentColor"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3 3l1.4 1.4M11.6 11.6L13 13M3 13l1.4-1.4M11.6 4.4L13 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
  var MOON = '<svg class="moon" width="13" height="13" viewBox="0 0 16 16" aria-hidden="true"><path d="M13.5 10.3A6 6 0 015.7 2.5a6 6 0 107.8 7.8z" fill="currentColor"/></svg>';
  function applyClock(pid){
    var p = person(pid), u = ui[pid]; if(!p || !u || !u.col) return;
    var d = new Date(), tz = tzOf(p), night = isNight(p, d);
    u.col.classList.toggle('night', night === true);
    u.col.classList.toggle('day', night === false);
    var el = u.col.querySelector('.clock'); if(!el) return;
    if(!tz){ el.hidden = true; return; }
    var parts = localParts(tz, d), mine = localParts(Intl.DateTimeFormat().resolvedOptions().timeZone, d);
    el.hidden = false;
    el.innerHTML = (night ? MOON : SUN) + '<span></span>';
    el.querySelector('span').textContent = parts.hour + ':' + parts.minute + (parts.weekday !== mine.weekday ? ' ' + parts.weekday : '');
    el.title = 'Local time in ' + p.location + (night ? ' (night)' : ' (day)');
  }
  function applyClocks(){ state.people.forEach(function(p){ applyClock(p.id); }); }
  setInterval(applyClocks, 30000);
  document.addEventListener('visibilitychange', function(){ if(!document.hidden) applyClocks(); });
  function tzOptions(sel, current){
    var list = []; try { list = Intl.supportedValuesOf('timeZone'); } catch(e){ list = ['Asia/Dubai','Asia/Riyadh','Africa/Johannesburg','Europe/London','Europe/Bratislava','America/New_York']; }
    sel.innerHTML = '';
    list.forEach(function(z){ var o = document.createElement('option'); o.value = z; o.textContent = z.replace(/_/g, ' '); sel.appendChild(o); });
    sel.value = current && list.indexOf(current) >= 0 ? current : Intl.DateTimeFormat().resolvedOptions().timeZone;
  }
  function locFields(p, v, tz){
    var f = { location: v }, c = cityInfo(v);
    f.tz = c ? c[2] : (tz || p.tz || null);
    return f;
  }

  function renderWhere(pid){'''
rep('\n  function renderWhere(pid){', JS)

# edit mode: datalist + tz select for unknown places
rep("""      var inp = document.createElement('input'); inp.type = 'text'; inp.value = place; inp.setAttribute('aria-label', 'Where is ' + p.name + ' now');""",
"""      var inp = document.createElement('input'); inp.type = 'text'; inp.value = place; inp.setAttribute('aria-label', 'Where is ' + p.name + ' now');
      var dl = document.getElementById('cityList');
      if(!dl){ dl = document.createElement('datalist'); dl.id = 'cityList'; CITY_NAMES.forEach(function(n){ var o = document.createElement('option'); o.value = n; dl.appendChild(o); }); document.body.appendChild(dl); }
      inp.setAttribute('list', 'cityList');
      var tzq = document.createElement('p'); tzq.className = 'tzq'; tzq.textContent = 'Which time zone is that in?';
      var tzs = document.createElement('select'); tzs.setAttribute('aria-label', 'Time zone'); tzOptions(tzs, p.tz);
      function syncTz(){ var unknown = !!inp.value.trim() && !cityInfo(inp.value); tzq.hidden = tzs.hidden = !unknown; }
      inp.addEventListener('input', syncTz);""")
rep("""        if(save && v && v !== place){ change({ type: 'pset', pid: pid, fields: { location: v } }); }
        renderWhere(pid);""",
"""        if(save && v){
          var nf = locFields(p, v, tzs.hidden ? null : tzs.value);
          if(v !== place || nf.tz !== p.tz) change({ type: 'pset', pid: pid, fields: nf });
        }
        renderWhere(pid); applyClock(pid);""")
rep("""      w.append(inp, ok); box.appendChild(w);""", """      w.append(inp, ok, tzq, tzs); box.appendChild(w); syncTz();""")
rep("""    btn.append('Currently in ', b);""", """    btn.append('Currently in ', b);
    var clk = document.createElement('span'); clk.className = 'clock'; clk.hidden = true; btn.appendChild(clk);""")
rep("""    box.appendChild(btn);
  }""", """    box.appendChild(btn);
    applyClock(pid);
  }""")
# team panel office field
rep("""if(v && v !== p.location) change({ type: 'pset', pid: p.id, fields: { location: v } }); else loc.value = p.location; });""",
    """if(v && v !== p.location) change({ type: 'pset', pid: p.id, fields: locFields(p, v, null) }); else loc.value = p.location; });""")
open(p,'w').write(s); print('ok')
