# Fix Caido TLS Handshake Error

**Error**: `Failed to perform TLS handshake - SSL alert number 40`
**Cause**: Browser doesn't trust Caido's CA certificate
**Solution**: Install Caido's CA certificate in macOS Keychain

---

## Step-by-Step Fix

### Step 1: Download Caido's CA Certificate

1. **Open your browser** (Chrome, Firefox, Safari)
2. **Navigate to**: http://caido.local (or http://127.0.0.1:8888)
3. **Look for "Certificate" or "CA" option** in Caido's interface
   - Usually in Settings → Certificate
   - Or a "Download CA Certificate" button
4. **Download the certificate** (caido-ca.pem or similar)

**Alternative - Direct Download**:
If Caido provides it at a specific URL:
```bash
curl http://127.0.0.1:8888/ca-cert -o ~/Downloads/caido-ca.crt
```

---

### Step 2: Install Certificate in macOS Keychain

**Method 1: Double-Click (Easiest)**
1. **Locate** the downloaded `caido-ca.crt` or `.pem` file
2. **Double-click** it
3. **Keychain Access** will open
4. **Select**: "System" keychain (NOT login)
5. **Click**: "Add"
6. **Enter** your Mac password

**Method 2: Command Line**
```bash
# Add to system keychain
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain \
  ~/Downloads/caido-ca.crt
```

---

### Step 3: Trust the Certificate

1. **Open**: Keychain Access app (Cmd+Space → "Keychain Access")
2. **Select**: "System" keychain (left sidebar)
3. **Search** for: "Caido" or "caido"
4. **Double-click** the Caido certificate
5. **Expand**: "Trust" section
6. **Set "When using this certificate"** to: **Always Trust**
7. **Close** the window (enter password when prompted)

---

### Step 4: Restart Browser

1. **Completely quit** your browser (Cmd+Q)
2. **Reopen** browser
3. **Configure proxy** settings:
   - HTTP Proxy: 127.0.0.1:8080
   - HTTPS Proxy: 127.0.0.1:8080
   - (Check Caido for the exact proxy port)

---

## Verification

Test the fix:
1. **Visit** https://www.google.com
2. **Should work** without certificate errors
3. **Check Caido** - you should see the HTTPS request captured

---

## If Certificate Not in Caido Interface

Some versions of Caido generate the certificate differently. Try:

1. **Check Caido Settings** → Look for:
   - "Certificate Authority"
   - "CA Certificate"
   - "Export Certificate"

2. **Check Caido documentation**:
   - Visit: https://docs.caido.io
   - Search for "certificate installation"

3. **Ask Caido to generate it**:
   - In Caido, look for "Regenerate CA Certificate"
   - Then download from the interface

---

## Troubleshooting

### Still getting TLS errors?

1. **Check proxy settings** in browser:
   - Make sure port matches Caido's proxy port
   - Usually 8080, NOT 8888 (8888 is the web UI)

2. **Check Caido is intercepting**:
   - Open Caido web interface (http://127.0.0.1:8888)
   - Look for "Proxy" or "Intercept" tab
   - Make sure intercept is ON

3. **Certificate not showing in Keychain?**
   - Try installing to "login" keychain instead of "system"
   - Then move it to system later

4. **Browser-specific issues**:
   - **Firefox**: Uses its own certificate store
     - Go to: Settings → Privacy & Security → Certificates → View Certificates
     - Import Caido's CA certificate there
   - **Chrome/Safari**: Use macOS keychain (steps above)

---

## Quick Reference Commands

```bash
# Download CA cert (if Caido serves it)
curl http://127.0.0.1:8888/ca-cert -o ~/Downloads/caido-ca.crt

# Install to system keychain
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain \
  ~/Downloads/caido-ca.crt

# Verify installation
security find-certificate -a -c "Caido" /Library/Keychains/System.keychain
```

---

**Next Step**: Once certificate is installed and trusted, try accessing https://qa.growthgrader.hubspot.com:8443 through Caido
