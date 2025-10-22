---
description: End-of-day protocol with reflection, summary, and git sync
globs: ""
alwaysApply: false
---

# 🌅 END-OF-DAY PROTOCOL

**TRIGGER PHRASE:** "Initiate the End"

When the user invokes this command or says "Initiate the End", perform the complete end-of-day workflow below.

## 🎯 YOUR MISSION

Provide a comprehensive end-of-day review that:
1. **Celebrates wins** - Build excitement for tomorrow
2. **Captures knowledge** - Document what we learned
3.**Archives report** - Insert report into today's Daily Note
4. **Syncs work** - Safe git commit with user approval
5. **Sets next steps** - Clear direction for continuation

---

## 📋 STEP-BY-STEP WORKFLOW

### Step 1: Positive Reflection (Wins & Breakthroughs)

**Analyze the session and write an enthusiastic paragraph that:**
- Highlights specific wins and accomplishments
- Emphasizes breakthroughs and "aha!" moments
- Notes progress made on challenging problems
- Builds genuine excitement for tomorrow's work
- Uses positive, energizing language

**Example:**
> Today was incredibly productive! We successfully implemented the authentication system with JWT tokens, debugged that tricky race condition in the payment processor, and discovered a much cleaner approach to handling user permissions. The breakthrough with the caching layer was particularly exciting - reducing API calls by 80% will make a huge difference. You're building something really solid here, and tomorrow we can tackle the notification system with this strong foundation in place.

### Step 2: Session Summary

Provide a structured summary with these sections:

#### **📍 Where We Started**
- What was the initial task/question/problem?
- What was the state of the codebase/project at session start?

#### **🔍 Paths We Explored**
- What approaches did we investigate?
- What solutions did we try (successful and unsuccessful)?
- What research or documentation did we consult?

#### **💡 Knowledge Gained**
- Key technical insights or learnings
- "We discovered that..." or "We learned that..."
- Important gotchas or edge cases identified
- Best practices or patterns we adopted

#### **➡️ Next Steps - Chavvo's Perspective**
What I recommend doing next (as your AI assistant):
- Immediate next tasks (high priority)
- Follow-up items to consider
- Areas that might need attention
- Suggested improvements or optimizations

#### **✏️ Next Steps - Your Perspective**
[Leave blank space with prompt for user to fill in]

**User: What are your thoughts on next steps?**
### Step 3: Archive Report in Daily Note

**IMPORTANT: Insert the end-of-day report into today's Daily Note**

#### 3a. Determine Today's Date
Run `date +%Y-%m-%d` to get today's date in YYYY-MM-DD format

#### 3b. Locate or Create Daily Note
- Daily Note path: `/Users/itza/Documents/vault_self/bcck_vault/Daily Notes/YYYY-MM-DD.md`
- If the file doesn't exist, create it with frontmatter:
```yaml
---
date: YYYY-MM-DD
type: daily-log
aliases:
  - [MonthDay format like Oct21]
tags:
  - daily-log
---

## First thing:
---

```

#### 3c. Format the End-of-Day Report
Create a well-formatted report section with:
```markdown
---

## 🌅 End-of-Day Review - [Session Topic]

**Date:** [YYYY-MM-DD]
**Session:** [Brief description]

### 🎉 Today's Wins

[Positive reflection paragraph from Step 1]

### 📍 Where We Started

[Starting point from Step 2]

### 🔍 Paths We Explored

[Approaches investigated from Step 2]

### 💡 Knowledge Gained

[Key learnings from Step 2]

### ➡️ Next Steps

**Chavvo's Perspective:**
[Recommendations from Step 2]

**My Perspective:**
[User input or "To be determined"]

### 📊 Git Commit

- **Files Changed:** [X] files
- **Commit Message:** [First line of commit]
- **Committed At:** [timestamp]

---
```

#### 3d. Append to Daily Note
**CRITICAL RULES:**
1. ✅ **ALWAYS use Read tool FIRST** to read the existing Daily Note content
2. ✅ **APPEND to the end** - Never overwrite existing content
3. ✅ **Add separator** - Use `---` before the new section
4. ✅ **Use Edit tool to append** - Find the last line and add after it
5. ✅ **Verify insertion** - Read the file again to confirm

**Example Edit Pattern:**
```typescript
// Read existing content first
Read('/Users/itza/Documents/vault_self/bcck_vault/Daily Notes/2025-10-21.md')

// Append the report to the end
Edit({
  file_path: '/Users/itza/Documents/vault_self/bcck_vault/Daily Notes/2025-10-21.md',
  old_string: '[last few lines of existing content]',
  new_string: '[last few lines of existing content]\n\n---\n\n[End-of-day report]'
})
```

#### 3e. Confirm Insertion
After inserting, state:

✅ **End-of-day report archived in Daily Note:** `Daily Notes/YYYY-MM-DD.md`

### Step 4: Git Sync Workflow

**IMPORTANT: Follow this sequence exactly**

#### 4a. Check Git Status
Run the following git commands in parallel:
- `git status` - See all changes
- `git diff` - See unstaged changes
- `git diff --staged` - See staged changes
- `git log -3 --oneline` - See recent commit style

#### 4b. Analyze & Stage Changes
- Review all modified, new, and deleted files
- **DO NOT stage sensitive files** (.env, credentials, api_keys.md, etc.)
- **VERIFY repository** - Run `git remote -v` to confirm we're in the correct repo
- Stage appropriate files using `git add`

#### 4c. Generate Commit Message
Create a commit message that:
- Follows this repository's commit style (from git log)
- Accurately describes the changes (focus on "why" not just "what")
- Is concise (1-2 sentences)
- Ends with the standard attribution:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 4d. Present for Approval
**ASK THE USER:**
"I've prepared this commit message. Does this accurately capture the work? Please approve or suggest changes:

```
[proposed commit message]
```

Type 'yes' to proceed, or provide an alternative message."

#### 4e. Execute Commit
**ONLY after user approval:**
- Commit with the approved message using heredoc format
- Run `git status` to verify commit success

#### 4f. Completion Signal
**After successful commit, clearly state:**

✅ **Commit successful!**

🔄 **You can now proceed with remotelySync to sync your Obsidian vault.**


---

## 🎨 RESPONSE FORMAT

Use the mandatory PAI response format:

```
📅 [current date from date command]

📋 SUMMARY: End-of-day review for [session topic/focus]

🔍 ANALYSIS: [Session summary with all sections from Step 2]

⚡ ACTIONS:
- Reviewed session transcript
- Generated positive reflection
- Analyzed session progress
- Staged git changes: [list files]
- Created commit with user approval
- Inserted end-of-day report into Daily Note

✅ RESULTS:
[Positive reflection paragraph]

[Session summary sections]

Git Status:
- ✅ Committed: [X] files
- 📝 Commit: [first line of commit message]
- 🔄 Ready for remotelySync

📊 STATUS: End-of-day protocol completed, work safely committed, report archived in Daily Note

➡️ NEXT:
Chavvo's Perspective: [recommendations]
Your Perspective: [user input]

🎯 COMPLETED: Completed end-of-day review, git sync, and Daily Note archive

🗣️ CUSTOM COMPLETED: Day wrapped up successfully
```

---

## 🚨 CRITICAL SAFETY RULES

### Git Safety
1. ✅ **ALWAYS verify repository** with `git remote -v` before staging
2. ✅ **NEVER stage sensitive files** (.env, .claude/settings.json, api_keys.md, credentials)
3. ✅ **NEVER commit without user approval** - Always ask first
4. ✅ **Check for modified .gitignore** - Ensure sensitive patterns are excluded
5. ❌ **NEVER use --no-verify or skip hooks**
6. ❌ **NEVER force push or destructive operations**

### Response Requirements
1. ✅ **BE GENUINELY ENTHUSIASTIC** in positive reflection - not generic praise
2. ✅ **BE SPECIFIC** about wins - cite actual accomplishments
3. ✅ **BE HONEST** about knowledge gained - real insights, not platitudes
4. ✅ **USE THE MANDATORY FORMAT** - Triggers voice notifications
5. ✅ **WAIT FOR USER INPUT** on next steps and commit approval
6. ✅ **INSERT REPORT INTO DAILY NOTE** - Always append to today's Daily Note after commit

---

## 💡 EXAMPLE EXECUTION

**User:** "Initiate the End"

**Chavvo Response:**

📅 2025-10-21

📋 SUMMARY: End-of-day review for authentication system implementation

🔍 ANALYSIS:

**🎉 Today's Wins:**
Today was incredibly productive! We successfully implemented JWT-based authentication with refresh tokens, solved that persistent race condition in the session middleware, and discovered a much cleaner architecture using the middleware chain pattern. The breakthrough with the token validation caching was particularly exciting - we went from 100ms validation time to 5ms! You're building a robust, production-ready auth system, and tomorrow we can integrate it with the user dashboard with full confidence.

**📍 Where We Started:**
- Goal: Implement secure authentication for the web application
- State: Basic login form existed, no JWT implementation, session handling was incomplete

**🔍 Paths We Explored:**
- Researched JWT vs session-based authentication
- Tested multiple JWT libraries (jsonwebtoken vs jose)
- Investigated refresh token rotation strategies
- Experimented with different middleware patterns for token validation
- Consulted Express.js security best practices

**💡 Knowledge Gained:**
- We discovered that httpOnly cookies are essential for XSS protection
- We learned that refresh token rotation prevents token replay attacks
- JWT payload size matters - keep claims minimal for performance
- Middleware order is critical - validation must happen before route handlers
- Redis caching for token validation reduces database load significantly

**➡️ Next Steps - Chavvo's Perspective:**
1. Integrate authentication with the user dashboard routes
2. Add rate limiting to login endpoint (prevent brute force)
3. Implement password reset flow with email verification
4. Add comprehensive auth tests (unit + integration)
5. Document the auth flow for team members

**✏️ Next Steps - Your Perspective:**
What are your thoughts on next steps?

⚡ ACTIONS:
- Reviewed session transcript
- Generated positive reflection highlighting JWT implementation wins
- Analyzed complete session from initial auth research to final caching solution
- Verified repository: bcck_vault (correct repo)
- Staged git changes: src/auth/jwt.ts, src/middleware/auth.ts, src/routes/login.ts, package.json

✅ RESULTS:

I've prepared this commit message. Does this accurately capture the work? Please approve or suggest changes:

```
Implement JWT-based authentication with refresh token rotation

Added secure JWT authentication system with httpOnly cookies, refresh token rotation, and Redis caching for validation. Reduces validation time from 100ms to 5ms through intelligent caching layer.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Type 'yes' to proceed, or provide an alternative message.

[After user approval:]

✅ **Commit successful!**

[Now insert report into Daily Note...]

✅ **End-of-day report archived in Daily Note:** `Daily Notes/2025-10-21.md`

📊 STATUS: End-of-day protocol completed, work safely committed, report archived in Daily Note

Git Status:
- ✅ Committed: 4 files (src/auth/jwt.ts, src/middleware/auth.ts, src/routes/login.ts, package.json)
- 📝 Commit: "Implement JWT-based authentication with refresh token rotation"
- 🔄 Ready for remotelySync

Daily Note:
- ✅ Report inserted into: `Daily Notes/2025-10-21.md`
- 📝 Section: "End-of-Day Review - Authentication System Implementation"

➡️ NEXT:
Chavvo's Perspective: Integrate auth with dashboard, add rate limiting, implement password reset
Your Perspective: [awaiting user input]

🎯 COMPLETED: Completed end-of-day review, git sync, and Daily Note archive

🗣️ CUSTOM COMPLETED: Day wrapped up successfully

---

🔄 **You can now proceed with remotelySync to sync your Obsidian vault.**

---

## 🎤 VOICE NOTIFICATIONS

Voice notifications are AUTOMATIC when you use the mandatory response format. The stop-hook will:
- Extract your 🗣️ CUSTOM COMPLETED line
- Send "Day wrapped up successfully" to voice server with Jamie (Premium) voice
- Announce completion at 263 wpm

**YOU DO NOT NEED TO MANUALLY SEND VOICE NOTIFICATIONS** - just use the format.

---

## 🔄 POST-COMMIT ACTIONS

After successful commit:
1. ✅ Insert end-of-day report into today's Daily Note
2. ✅ Clearly state "You can now proceed with remotelySync"
3. ✅ DO NOT automatically push to remote (user handles this)
4. ✅ DO NOT run remotelySync automatically (user-controlled Obsidian sync)
5. ✅ Session can continue if user has more work, or end naturally

---

**This is the complete end-of-day protocol. Execute it thoroughly and enthusiastically.**
