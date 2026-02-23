# Windows Encoding Fix

## Problem
When running the blog manager on Windows after developing on macOS, the application crashed with a `UnicodeDecodeError` when trying to read post files containing special characters (like Portuguese accented characters).

## Root Cause
- macOS and Windows use different default file encodings
- Post files created on macOS may contain UTF-8 encoded characters
- Windows Python defaults to cp1252 encoding when opening files
- The original code specified `encoding='utf-8'`, but some files may have been saved with different encodings

## Solution
Implemented encoding fallback mechanism in two methods:

1. `PostManager.parse_post_file()` - Tries multiple encodings in order:
   - utf-8 (standard)
   - utf-8-sig (UTF-8 with BOM)
   - latin-1 (common in Western Europe)
   - cp1252 (Windows default)

2. `CommentManager.get_post_title()` - Same fallback mechanism

## Jekyll Detection Fix

### Problem
The blog manager showed "Jekyll não encontrado" warning even when Jekyll was installed, because:
1. The code used Unix `which` command instead of Windows `where` command
2. Windows batch files (.bat) require `shell=True` in subprocess calls

### Solution
Updated Jekyll detection to be cross-platform:
- Uses `where` on Windows, `which` on Unix/Linux/macOS
- Adds `shell=True` for Windows subprocess calls
- Verifies Ruby is available on Windows (required for bundle)
- Tests actual bundle execution to confirm it works

## Files Modified
- `blog_manager.py` - Added encoding fallback logic and cross-platform Jekyll detection

## Testing
- Encoding fix: Successfully parses posts with Portuguese characters (e.g., "Bem-vindo", "Psicanálise")
- Jekyll detection: Properly detects Jekyll when Ruby and bundle are installed on Windows

## Usage
Simply run the blog manager as usual:
```bash
start-blog-manager.bat
```

The application will now:
- Automatically handle files with different encodings
- Correctly detect Jekyll installation on Windows
- Show "✓ Jekyll detectado" when Jekyll is properly configured

