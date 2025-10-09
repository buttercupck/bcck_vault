#!/usr/bin/env bun
/**
 * PAIVoice - Personal AI Voice notification server using macOS native voices
 * Zero-cost, offline, premium quality text-to-speech
 */

import { serve } from "bun";
import { spawn } from "child_process";
import { homedir } from "os";
import { join } from "path";
import { existsSync } from "fs";

// Load .env from PAI_DIR if available
const paiDir = process.env.PAI_DIR || join(homedir(), '.claude');
const envPath = join(paiDir, '.env');
if (existsSync(envPath)) {
  const envContent = await Bun.file(envPath).text();
  envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value && !key.startsWith('#')) {
      process.env[key.trim()] = value.trim().replace(/^["']|["']$/g, '');
    }
  });
}

// Load voice configuration
const voicesConfigPath = join(paiDir, 'voice-server', 'voices.json');
let voicesConfig: any = {
  default_rate: 175,
  voices: {
    chavvo: {
      voice_name: "Jamie",
      rate_multiplier: 1.3,
      rate_wpm: 228,
      description: "UK Male - Professional, conversational",
      type: "Premium"
    }
  }
};

if (existsSync(voicesConfigPath)) {
  try {
    voicesConfig = await Bun.file(voicesConfigPath).json();
  } catch (error) {
    console.warn('⚠️  Could not load voices.json, using defaults');
  }
}

const PORT = parseInt(process.env.PORT || "8888");
const DEFAULT_VOICE = voicesConfig.voices.chavvo?.voice_name || "Jamie";
const DEFAULT_RATE = voicesConfig.voices.chavvo?.rate_wpm || 228;

// Sanitize input for shell commands
function sanitizeForShell(input: string): string {
  return input.replace(/[^a-zA-Z0-9\s.,!?\-']/g, '').trim().substring(0, 500);
}

// Validate and sanitize user input
function validateInput(input: any): { valid: boolean; error?: string } {
  if (!input || typeof input !== 'string') {
    return { valid: false, error: 'Invalid input type' };
  }

  if (input.length > 500) {
    return { valid: false, error: 'Message too long (max 500 characters)' };
  }

  const dangerousPatterns = [
    /[;&|><`\$\(\)\{\}\[\]\\]/,
    /\.\.\//,
    /<script/i,
  ];

  for (const pattern of dangerousPatterns) {
    if (pattern.test(input)) {
      return { valid: false, error: 'Invalid characters in input' };
    }
  }

  return { valid: true };
}

// Generate speech using macOS native say command
function speakText(text: string, voiceName: string = DEFAULT_VOICE, rate: number = DEFAULT_RATE): Promise<void> {
  return new Promise((resolve, reject) => {
    // Clean the voice name (remove Premium/Enhanced suffix if present)
    const cleanVoiceName = voiceName.replace(/\s*\((Premium|Enhanced)\)/i, '').trim();

    const args = ['-v', cleanVoiceName, '-r', rate.toString(), text];
    const proc = spawn('/usr/bin/say', args);

    proc.on('error', (error) => {
      console.error('Error with text-to-speech:', error);
      reject(error);
    });

    proc.on('exit', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`say command exited with code ${code}`));
      }
    });
  });
}

// Spawn a process safely
function spawnSafe(command: string, args: string[]): Promise<void> {
  return new Promise((resolve, reject) => {
    const proc = spawn(command, args);

    proc.on('error', (error) => {
      console.error(`Error spawning ${command}:`, error);
      reject(error);
    });

    proc.on('exit', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`${command} exited with code ${code}`));
      }
    });
  });
}

// Send macOS notification with voice
async function sendNotification(
  title: string,
  message: string,
  voiceEnabled = true,
  voiceName: string | null = null,
  rate: number | null = null
) {
  // Validate inputs
  const titleValidation = validateInput(title);
  const messageValidation = validateInput(message);

  if (!titleValidation.valid) {
    throw new Error(`Invalid title: ${titleValidation.error}`);
  }

  if (!messageValidation.valid) {
    throw new Error(`Invalid message: ${messageValidation.error}`);
  }

  // Sanitize inputs
  const safeTitle = sanitizeForShell(title);
  const safeMessage = sanitizeForShell(message);

  // Speak the message using macOS native voice
  if (voiceEnabled) {
    try {
      const voice = voiceName || DEFAULT_VOICE;
      const speechRate = rate || DEFAULT_RATE;
      console.log(`🎙️  Speaking with macOS voice: ${voice} at ${speechRate} wpm`);
      await speakText(safeMessage, voice, speechRate);
    } catch (error) {
      console.error("Failed to speak text:", error);
    }
  }

  // Display macOS notification
  try {
    const script = `display notification "${safeMessage}" with title "${safeTitle}" sound name ""`;
    await spawnSafe('/usr/bin/osascript', ['-e', script]);
  } catch (error) {
    console.error("Notification display error:", error);
  }
}

// Rate limiting
const requestCounts = new Map<string, { count: number; resetTime: number }>();
const RATE_LIMIT = 10;
const RATE_WINDOW = 60000;

function checkRateLimit(ip: string): boolean {
  const now = Date.now();
  const record = requestCounts.get(ip);

  if (!record || now > record.resetTime) {
    requestCounts.set(ip, { count: 1, resetTime: now + RATE_WINDOW });
    return true;
  }

  if (record.count >= RATE_LIMIT) {
    return false;
  }

  record.count++;
  return true;
}

// Start HTTP server
const server = serve({
  port: PORT,
  async fetch(req) {
    const url = new URL(req.url);

    const clientIp = req.headers.get('x-forwarded-for') || 'localhost';

    const corsHeaders = {
      "Access-Control-Allow-Origin": "http://localhost",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type"
    };

    if (req.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders, status: 204 });
    }

    if (!checkRateLimit(clientIp)) {
      return new Response(
        JSON.stringify({ status: "error", message: "Rate limit exceeded" }),
        {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
          status: 429
        }
      );
    }

    if (url.pathname === "/notify" && req.method === "POST") {
      try {
        const data = await req.json();
        const title = data.title || "PAI Notification";
        const message = data.message || "Task completed";
        const voiceEnabled = data.voice_enabled !== false;
        const voiceName = data.voice_name || null;
        const rate = data.rate || null;

        if (voiceName && typeof voiceName !== 'string') {
          throw new Error('Invalid voice_name');
        }

        console.log(`📨 Notification: "${title}" - "${message}" (voice: ${voiceEnabled}, voice: ${voiceName || DEFAULT_VOICE})`);

        await sendNotification(title, message, voiceEnabled, voiceName, rate);

        return new Response(
          JSON.stringify({ status: "success", message: "Notification sent" }),
          {
            headers: { ...corsHeaders, "Content-Type": "application/json" },
            status: 200
          }
        );
      } catch (error: any) {
        console.error("Notification error:", error);
        return new Response(
          JSON.stringify({ status: "error", message: error.message || "Internal server error" }),
          {
            headers: { ...corsHeaders, "Content-Type": "application/json" },
            status: error.message?.includes('Invalid') ? 400 : 500
          }
        );
      }
    }

    if (url.pathname === "/pai" && req.method === "POST") {
      try {
        const data = await req.json();
        const title = data.title || "PAI Assistant";
        const message = data.message || "Task completed";

        console.log(`🤖 PAI notification: "${title}" - "${message}"`);

        await sendNotification(title, message, true, null, null);

        return new Response(
          JSON.stringify({ status: "success", message: "PAI notification sent" }),
          {
            headers: { ...corsHeaders, "Content-Type": "application/json" },
            status: 200
          }
        );
      } catch (error: any) {
        console.error("PAI notification error:", error);
        return new Response(
          JSON.stringify({ status: "error", message: error.message || "Internal server error" }),
          {
            headers: { ...corsHeaders, "Content-Type": "application/json" },
            status: error.message?.includes('Invalid') ? 400 : 500
          }
        );
      }
    }

    if (url.pathname === "/health") {
      return new Response(
        JSON.stringify({
          status: "healthy",
          port: PORT,
          voice_system: "macOS Native",
          default_voice: DEFAULT_VOICE,
          default_rate: DEFAULT_RATE
        }),
        {
          headers: { ...corsHeaders, "Content-Type": "application/json" },
          status: 200
        }
      );
    }

    return new Response("PAIVoice Server - POST to /notify or /pai", {
      headers: corsHeaders,
      status: 200
    });
  },
});

console.log(`🚀 PAIVoice Server running on port ${PORT}`);
console.log(`🎙️  Using macOS native voices (default: ${DEFAULT_VOICE})`);
console.log(`📡 POST to http://localhost:${PORT}/notify`);
console.log(`🔒 Security: CORS restricted to localhost, rate limiting enabled`);
console.log(`💰 Zero cost - 100% offline - Complete privacy`);
