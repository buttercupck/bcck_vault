# Vault Repository Clone Instructions

## Overview
This guide walks you through replacing your old vault folder on your work computer with a fresh clone of the updated repository.

## Prerequisites
- Git installed on your work computer
- Access credentials for the vault repository
- Backup of any uncommitted work in the old vault folder

---

## Step 1: Backup Current Vault (Safety First)

Before making any changes, create a backup of your existing vault folder:

```bash
# Navigate to the parent directory of your vault
cd ~/Documents/vault_self  # Adjust path as needed

# Create a backup with timestamp
cp -r bcck_vault bcck_vault_backup_$(date +%Y%m%d_%H%M%S)
```

**Important:** Check if you have any uncommitted changes or local-only files:

```bash
cd bcck_vault
git status
git log --branches --not --remotes  # Check for unpushed commits
```

If you have uncommitted changes, either commit and push them, or save them separately.

---

## Step 2: Remove Old Vault Folder

Once you've confirmed your backup is safe:

```bash
# Navigate to parent directory
cd ~/Documents/vault_self

# Remove the old vault folder
rm -rf bcck_vault
```

**Alternative (Safer):** Just rename it instead of deleting:

```bash
mv bcck_vault bcck_vault_old
```

---

## Step 3: Clone Fresh Repository

Clone the updated repository:

```bash
# Still in ~/Documents/vault_self
git clone <YOUR_REPO_URL> bcck_vault

# Example:
# git clone git@github.com:username/bcck_vault.git bcck_vault
# or
# git clone https://github.com/username/bcck_vault.git bcck_vault
```

---

## Step 4: Navigate and Verify

```bash
cd bcck_vault

# Verify the clone was successful
git status
git log -5  # Check recent commits

# Verify branch
git branch -a
```

---

## Step 5: Set Up PAI Configuration

The PAI system requires environment variables to be set. Check if your `.zshrc` or `.bashrc` has the PAI_DIR variable:

```bash
# Check current shell config
cat ~/.zshrc | grep PAI_DIR
# or
cat ~/.bashrc | grep PAI_DIR
```

If not present, add it:

```bash
echo 'export PAI_DIR="$HOME/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY"' >> ~/.zshrc
# or for bash:
# echo 'export PAI_DIR="$HOME/Documents/vault_self/bcck_vault/PAI/PAI_DIRECTORY"' >> ~/.bashrc
```

Then reload your shell:

```bash
source ~/.zshrc
# or
# source ~/.bashrc
```

---

## Step 6: Verify PAI Directory Structure

Ensure the PAI directory structure is correct:

```bash
ls -la $PAI_DIR
```

You should see:
- `hooks/` - Hook scripts
- `commands/` - Command files
- `settings.json` - Configuration
- `statusline-command.sh` - Status line script
- Other PAI system files

---

## Step 7: Update Claude Code Settings (If Needed)

If you're using Claude Code, ensure it points to the correct PAI directory:

1. Open Claude Code settings (usually in `~/.claude/settings.json`)
2. Verify the hook paths reference `${PAI_DIR}`
3. The settings should auto-resolve the environment variable

Alternatively, if your `settings.json` is in the vault:

```bash
# Check if settings.json exists in the vault
ls -la PAI/PAI_DIRECTORY/settings.json

# If it exists and you want to use it, symlink or copy it:
cp PAI/PAI_DIRECTORY/settings.json ~/.claude/settings.json
```

---

## Step 8: Test the Setup

Test that everything works:

```bash
# Test PAI_DIR variable
echo $PAI_DIR

# Test that hooks are accessible
ls -la $PAI_DIR/hooks/

# Test status line command
bash $PAI_DIR/statusline-command.sh
```

---

## Step 9: Configure Git (If Needed)

Set up your git identity for this repository:

```bash
cd ~/Documents/vault_self/bcck_vault

# Configure user (if not already set globally)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Verify configuration
git config --list --local
```

---

## Step 10: Pull Latest Changes

Ensure you have the absolute latest:

```bash
git pull origin main
# or whatever your main branch is named (master, main, etc.)
```

---

## Troubleshooting

### Issue: PAI_DIR not found
**Solution:** Make sure you've set the environment variable and restarted your terminal or ran `source ~/.zshrc`

### Issue: Hooks not executing
**Solution:** Check hook file permissions:
```bash
chmod +x $PAI_DIR/hooks/*.ts
chmod +x $PAI_DIR/statusline-command.sh
```

### Issue: Settings not loading
**Solution:** Verify `settings.json` exists and is properly formatted:
```bash
cat $PAI_DIR/settings.json | jq .
```

### Issue: Git authentication fails
**Solution:** Set up SSH keys or use HTTPS with credentials:
- For SSH: Generate and add SSH key to GitHub
- For HTTPS: Use personal access token

---

## Post-Setup Checklist

- [ ] Old vault backed up
- [ ] New vault cloned successfully
- [ ] PAI_DIR environment variable set
- [ ] Hooks directory accessible
- [ ] Status line command works
- [ ] Git configured with correct user info
- [ ] Latest changes pulled from remote
- [ ] Claude Code (if used) configured correctly

---

## Important Notes

1. **Never commit sensitive data** - Use `.gitignore` for secrets
2. **Regular backups** - Keep backups of important vault data
3. **API Keys** - Ensure all API keys in `settings.json` are updated with your keys
4. **Bash version** - Ensure bash 4.0+ is installed (required for statusline-command.sh)
   ```bash
   bash --version
   # If < 4.0, install via: brew install bash
   ```

---

## Additional Setup (If Using Obsidian)

If this vault is used with Obsidian:

1. Open Obsidian
2. Click "Open another vault"
3. Select "Open folder as vault"
4. Navigate to `~/Documents/vault_self/bcck_vault`
5. Open the vault

---

## Questions or Issues?

If you encounter problems:
1. Check git status: `git status`
2. Check git logs: `git log --oneline -10`
3. Verify PAI_DIR: `echo $PAI_DIR`
4. Check permissions: `ls -la $PAI_DIR`

---

**Last Updated:** 2025-10-09
