# CSS Loading Debug Guide

## What I've Added

1. **Debug comments in HTML** - Shows CSS path, baseurl, and URL in HTML source
2. **JavaScript console logging** - Checks if CSS file loads and logs the path
3. **Visual debug indicator** - Red box appears if CSS doesn't load
4. **Inline fallback styles** - Ensures background color shows even if CSS fails

## How to Debug

### Step 1: Check HTML Source
1. Visit your deployed site
2. Right-click → "View Page Source" (or Ctrl+U / Cmd+U)
3. Look for these debug comments in the `<head>`:
   ```
   <!-- Debug: CSS Path = /assets/css/main.css -->
   <!-- Debug: Baseurl =  -->
   <!-- Debug: URL =  -->
   ```

### Step 2: Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for:
   - `CSS Debug Info:` - Shows the CSS path being used
   - `CSS file exists: true/false` - Shows if file was found
   - `CSS file error:` - Shows any loading errors

### Step 3: Check Network Tab
1. Open DevTools → Network tab
2. Refresh the page
3. Look for `main.css` file:
   - **Status 200** = File found and loaded ✅
   - **Status 404** = File not found ❌
   - **Status (other)** = Error loading file ❌
4. Click on `main.css` to see:
   - Request URL (actual path being requested)
   - Response (should show CSS content, not HTML error page)

### Step 4: Check GitHub Actions (if using GitHub Actions)
1. Go to your repository → Actions tab
2. Click on the latest workflow run
3. Check the "Build with Jekyll" step:
   - Look for errors about SCSS compilation
   - Check if `_site/assets/css/main.css` is created
   - Look for any warnings about missing files

## Common Issues

### Issue 1: CSS Path is Wrong
**Symptom**: Network tab shows 404 for main.css
**Check**: The debug comment shows wrong path
**Fix**: Update `_config.yml` baseurl if repository isn't `username.github.io`

### Issue 2: SCSS Not Compiling
**Symptom**: main.css doesn't exist in `_site/assets/css/` after build
**Check**: GitHub Actions logs show SCSS compilation errors
**Fix**: Check SCSS syntax, ensure front matter is correct

### Issue 3: Workflow Interference
**Symptom**: Using GitHub Actions but build fails
**Check**: Actions tab shows build errors
**Fix**: Either fix workflow or switch to automatic build

### Issue 4: Baseurl Mismatch
**Symptom**: CSS path includes wrong baseurl
**Check**: Debug comment shows baseurl that doesn't match repository name
**Fix**: Set correct baseurl in `_config.yml`

## Next Steps After Debugging

Once you have the debug information:
1. Note what the CSS path is (from debug comment)
2. Note if CSS file exists (from Network tab)
3. Note any errors (from Console or Actions)
4. Share this information for further troubleshooting
