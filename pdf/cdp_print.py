#!/usr/bin/env python3
"""Print local HTML files to PDF via Chromium DevTools Protocol (pure stdlib)."""
import base64, hashlib, json, os, random, socket, ssl, struct, subprocess, sys, time, urllib.request

CHROME = "/opt/meta-chromium/chrome"
PORT = 19322

def ws_handshake(host, port, path):
    s = socket.create_connection((host, port), timeout=15)
    key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\n"
        f"Connection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
    )
    s.sendall(req.encode())
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = s.recv(4096)
        if not chunk:
            raise RuntimeError("handshake failed: no response")
        resp += chunk
    if b"101" not in resp.split(b"\r\n")[0]:
        raise RuntimeError("handshake failed: " + resp.split(b"\r\n")[0].decode())
    return s

def ws_send(s, text):
    data = text.encode()
    mask = os.urandom(4)
    hdr = bytes([0x81])
    n = len(data)
    if n < 126:
        hdr += bytes([0x80 | n])
    elif n < 65536:
        hdr += bytes([0x80 | 126]) + struct.pack(">H", n)
    else:
        hdr += bytes([0x80 | 127]) + struct.pack(">Q", n)
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    s.sendall(hdr + mask + masked)

def _recv_exact(s, n):
    buf = b""
    while len(buf) < n:
        chunk = s.recv(n - len(buf))
        if not chunk:
            raise RuntimeError("connection closed")
        buf += chunk
    return buf

def ws_recv(s):
    """Return one complete text message (reassembles fragments)."""
    parts = []
    while True:
        b1, b2 = _recv_exact(s, 2)
        fin = b1 & 0x80
        opcode = b1 & 0x0F
        masked = b2 & 0x80
        n = b2 & 0x7F
        if n == 126:
            n = struct.unpack(">H", _recv_exact(s, 2))[0]
        elif n == 127:
            n = struct.unpack(">Q", _recv_exact(s, 8))[0]
        if masked:
            mask = _recv_exact(s, 4)
        payload = _recv_exact(s, n)
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if opcode == 0x8:
            raise RuntimeError("server closed connection")
        if opcode == 0x9:  # ping -> pong
            s.sendall(bytes([0x8A, 0x80]) + os.urandom(4))
            continue
        parts.append(payload)
        if fin:
            break
    return b"".join(parts).decode()

def cdp_call(s, mid, method, params=None):
    msg = {"id": mid, "method": method}
    if params:
        msg["params"] = params
    ws_send(s, json.dumps(msg))
    while True:
        r = json.loads(ws_recv(s))
        if r.get("id") == mid:
            if "error" in r:
                raise RuntimeError(f"{method} error: {r['error']}")
            return r.get("result", {})

def html_to_pdf(html_path, pdf_path):
    url = "file://" + os.path.abspath(html_path)
    proc = subprocess.Popen(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         "--disable-dev-shm-usage", f"--remote-debugging-port={PORT}",
         "--remote-allow-origins=*", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        # wait for DevTools endpoint
        for _ in range(60):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=2) as r:
                    json.load(r)
                break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("DevTools endpoint never came up")
        # create target (blank), then navigate via CDP (more reliable than /json/new?url=)
        req = urllib.request.Request(
            f"http://127.0.0.1:{PORT}/json/new?{urllib.parse.urlencode({'url': 'about:blank'})}",
            method="PUT")
        with urllib.request.urlopen(req, timeout=15) as r:
            target = json.load(r)
        wsurl = target["webSocketDebuggerUrl"]
        from urllib.parse import urlparse
        p = urlparse(wsurl)
        s = ws_handshake(p.hostname, p.port or 80, p.path + ("?" + p.query if p.query else ""))
        mid = 1
        cdp_call(s, mid, "Page.enable"); mid += 1
        cdp_call(s, mid, "Page.navigate", {"url": url}); mid += 1
        # wait for load
        loaded = False
        s.settimeout(30)
        # poll for load event via evaluate readyState
        for _ in range(40):
            res = cdp_call(s, mid, "Runtime.evaluate",
                           {"expression": "document.readyState", "returnByValue": True})
            mid += 1
            if res.get("result", {}).get("value") == "complete":
                loaded = True
                break
            time.sleep(0.5)
        time.sleep(1.0)  # let fonts/layout settle
        res = cdp_call(s, mid, "Page.printToPDF",
                       {"printBackground": True, "displayHeaderFooter": False,
                        "preferCSSPageSize": True})
        mid += 1
        pdf_bytes = base64.b64decode(res["data"])
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        s.close()
        return os.path.getsize(pdf_path)
    finally:
        proc.terminate()

if __name__ == "__main__":
    import urllib.parse
    src, dst = sys.argv[1], sys.argv[2]
    size = html_to_pdf(src, dst)
    print(f"OK {dst} ({size} bytes)")
