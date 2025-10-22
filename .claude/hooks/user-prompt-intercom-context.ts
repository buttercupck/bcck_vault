#!/usr/bin/env bun
/**
 * user-prompt-intercom-context.ts
 *
 * Intelligently loads Intercom-related context when user mentions relevant keywords.
 * This hook runs on every user prompt submission and injects context into the session.
 *
 * Trigger Keywords:
 * - intercom, interpreter, interlingo
 * - Organization names: Kent, Yakima, Fife, Puyallup, Sumner, etc.
 * - Job-related: job, assignment, request, confirmation, reminder
 * - Email-related: REQ, CONF, REM, email template
 *
 * What it loads:
 * - Organization-specific instructions
 * - Current ROADMAP milestone
 * - Supabase schema
 * - Active SOPs
 * - Email templates
 */

import { readFileSync, existsSync, readdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

interface HookInput {
  session_id: string;
  prompt: string;
  transcript_path: string;
  hook_event_name: string;
}

/**
 * Read stdin with timeout
 */
async function readStdinWithTimeout(timeout: number = 5000): Promise<string> {
  return new Promise((resolve, reject) => {
    let data = '';
    const timer = setTimeout(() => {
      reject(new Error('Timeout reading from stdin'));
    }, timeout);

    process.stdin.on('data', (chunk) => {
      data += chunk.toString();
    });

    process.stdin.on('end', () => {
      clearTimeout(timer);
      resolve(data);
    });

    process.stdin.on('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
}

/**
 * Detect if prompt is about Intercom work
 */
function isIntercomRelated(prompt: string): boolean {
  const lowerPrompt = prompt.toLowerCase();

  // Primary keywords
  const primaryKeywords = [
    'intercom',
    'interpreter',
    'interlingo',
    'scheduling assistant'
  ];

  // Organization names
  const organizationKeywords = [
    'kent municipal',
    'yakima',
    'fife municipal',
    'puyallup municipal',
    'sumner municipal',
    'kirshenbaum',
    'stein lotzkar',
    'stewart macnichols'
  ];

  // Job-related terms
  const jobKeywords = [
    'job request',
    'assignment',
    'client request',
    'court request',
    'commitment block'
  ];

  // Email/communication terms
  const emailKeywords = [
    'req email',
    'conf email',
    'rem email',
    'email template',
    'email draft',
    'interpreter email'
  ];

  // Check all keyword categories
  const allKeywords = [
    ...primaryKeywords,
    ...organizationKeywords,
    ...jobKeywords,
    ...emailKeywords
  ];

  return allKeywords.some(keyword => lowerPrompt.includes(keyword));
}

/**
 * Load Intercom context based on prompt analysis
 */
function loadIntercomContext(prompt: string): string {
  const paiDir = process.env.PAI_DIR || join(homedir(), '.claude');
  const vaultDir = join(paiDir, '..');
  const intercomDir = join(vaultDir, 'INCOME/intercom');

  let context = '';

  // Always load core Intercom context
  context += '\n<intercom-context>\n';
  context += '# INTERCOM CONTEXT AUTO-LOADED\n\n';

  // Load Client README
  const clientReadmePath = join(intercomDir, 'Client/README.md');
  if (existsSync(clientReadmePath)) {
    context += '## Your Role\n';
    context += readFileSync(clientReadmePath, 'utf-8');
    context += '\n\n';
  }

  const lowerPrompt = prompt.toLowerCase();

  // Load ROADMAP if development-related
  if (lowerPrompt.includes('milestone') ||
      lowerPrompt.includes('feature') ||
      lowerPrompt.includes('build') ||
      lowerPrompt.includes('develop') ||
      lowerPrompt.includes('interlingo app')) {
    const roadmapPath = join(intercomDir, 'App - Interlingo/ROADMAP.md');
    if (existsSync(roadmapPath)) {
      context += '## Interlingo Development Roadmap\n';
      context += readFileSync(roadmapPath, 'utf-8');
      context += '\n\n';
    }
  }

  // Load Supabase Schema if database-related
  if (lowerPrompt.includes('database') ||
      lowerPrompt.includes('supabase') ||
      lowerPrompt.includes('schema') ||
      lowerPrompt.includes('query') ||
      lowerPrompt.includes('table')) {
    const schemaPath = join(intercomDir, 'App - Interlingo/Supabase-Schema.md');
    if (existsSync(schemaPath)) {
      context += '## Supabase Database Schema\n';
      context += readFileSync(schemaPath, 'utf-8');
      context += '\n\n';
    }
  }

  // Load SOPs if workflow-related
  if (lowerPrompt.includes('workflow') ||
      lowerPrompt.includes('procedure') ||
      lowerPrompt.includes('assignment') ||
      lowerPrompt.includes('sourcing') ||
      lowerPrompt.includes('sop')) {
    const sopPath = join(intercomDir, 'Z A R C H I V E/Interpreter Assignment SOP.md');
    if (existsSync(sopPath)) {
      context += '## Standard Operating Procedures\n';
      context += readFileSync(sopPath, 'utf-8');
      context += '\n\n';
    }
  }

  // Load email templates if email-related
  if (lowerPrompt.includes('email') ||
      lowerPrompt.includes('req') ||
      lowerPrompt.includes('conf') ||
      lowerPrompt.includes('rem') ||
      lowerPrompt.includes('template')) {
    const templatesDir = join(intercomDir, 'App - Interlingo/Templates');
    if (existsSync(templatesDir)) {
      context += '## Email Templates\n';
      const templateFiles = readdirSync(templatesDir).filter(f => f.endsWith('.md'));
      templateFiles.forEach(file => {
        const templatePath = join(templatesDir, file);
        context += `### ${file}\n`;
        context += readFileSync(templatePath, 'utf-8');
        context += '\n\n';
      });
    }
  }

  // Load organization-specific instructions if org mentioned
  const organizations = [
    { keywords: ['kent municipal'], file: 'Client Specifics - Kent Municipal Court.md' },
    { keywords: ['yakima district'], file: 'Client Specifics - Yakima District Court.md' },
    { keywords: ['yakima superior'], file: 'Client Specifics - Yakima Superior Court.md' },
    { keywords: ['fife municipal'], file: 'Org Specific - Fife Municipal Court.md' },
    { keywords: ['puyallup municipal'], file: 'Client Specifics - Puyallup Municipal Court.md' },
    { keywords: ['sumner municipal'], file: 'Client Specifics - Sumner Municipal Court.md' },
    { keywords: ['kirshenbaum'], file: 'Client Specifics - Kirshenbaum & Goss.md' },
    { keywords: ['stein lotzkar', 'stein, lotzkar'], file: 'Client Specifics - Stein, Lotzkar & Starr.md' },
    { keywords: ['stewart macnichols'], file: 'Client Specifics - Stewart MacNichols Harmell.md' }
  ];

  const orgInstructionsDir = join(intercomDir, 'App - Interlingo/Organization Specific Instructions');
  if (existsSync(orgInstructionsDir)) {
    organizations.forEach(org => {
      if (org.keywords.some(keyword => lowerPrompt.includes(keyword))) {
        const orgPath = join(orgInstructionsDir, org.file);
        if (existsSync(orgPath)) {
          context += `## Organization-Specific Instructions\n`;
          context += readFileSync(orgPath, 'utf-8');
          context += '\n\n';
        }
      }
    });
  }

  // Load system logic if interpreter matching mentioned
  if (lowerPrompt.includes('match') ||
      lowerPrompt.includes('suggest interpreter') ||
      lowerPrompt.includes('filter') ||
      lowerPrompt.includes('certification') ||
      lowerPrompt.includes('priorit')) {
    const logicDir = join(intercomDir, 'App - Interlingo/system_logic');
    if (existsSync(logicDir)) {
      context += '## Interpreter Matching Logic\n';
      const logicFiles = readdirSync(logicDir).filter(f => f.endsWith('.md'));
      logicFiles.forEach(file => {
        const logicPath = join(logicDir, file);
        context += `### ${file}\n`;
        context += readFileSync(logicPath, 'utf-8');
        context += '\n\n';
      });
    }
  }

  context += '</intercom-context>\n';

  return context;
}

async function main() {
  try {
    // Read hook input from stdin
    const input = await readStdinWithTimeout();
    const data: HookInput = JSON.parse(input);

    // Check if prompt is Intercom-related
    if (isIntercomRelated(data.prompt)) {
      // Load and output relevant context
      const context = loadIntercomContext(data.prompt);
      console.log(context);

      // Add metadata for debugging
      console.log('\n<!-- HOOK: Intercom context auto-loaded -->');
    }

    // Always exit cleanly
    process.exit(0);
  } catch (error) {
    // Silently fail to not interrupt Claude's flow
    console.error('Intercom context loader error:', error);
    process.exit(0);
  }
}

main();
