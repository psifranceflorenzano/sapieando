# CSS Loading Fix - Based on GitHub Community Discussion

## Reference
Based on: https://github.com/orgs/community/discussions/22495

## Changes Applied

### 1. Switched to Root `css/` Folder
- **Changed**: CSS file location from `assets/css/main.css` to `css/main.css`
- **Reason**: Root folder files bypass Jekyll processing, which can interfere with CSS file serving
- **File**: `css/main.css` (already created with corrected font paths)

### 2. Updated HTML Link
- **Changed**: Updated `_layouts/default.html` to use root `css/main.css`
- **Added**: `type="text/css"` attribute (mentioned as helpful in discussion)
- **Path**: Using `{{ '/css/main.css' | relative_url }}` for proper Jekyll path resolution

### 3. Updated `_config.yml`
- **Added**: `css` folder to `include:` list to ensure it's processed
- **Verified**: `css` folder is NOT in `exclude:` list

## Common Issues from Discussion (All Addressed)

✅ **Leading slash issue**: Using `relative_url` filter handles this correctly
✅ **Jekyll processing**: Root `css/` folder bypasses Jekyll processing
✅ **Case sensitivity**: All paths use lowercase
✅ **Missing type attribute**: Added `type="text/css"`
✅ **File location**: Using root folder instead of `assets/` subfolder

## Testing Checklist

After deploying:
1. Check browser Network tab - `css/main.css` should return 200 (not 404)
2. Verify styles are applied to the page
3. Check console for debug messages
4. Verify colors: #873D35 (text), #E3CAB1 (background)

## If Still Not Working

Try these alternatives in order:

1. **Remove relative_url filter** (uncomment alternative link in default.html):
   ```html
   <link rel="stylesheet" type="text/css" href="css/main.css">
   ```

2. **Check file is committed**: Ensure `css/main.css` exists in repository

3. **Clear browser cache**: Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

4. **Verify capitalization**: Ensure folder is `css/` not `CSS/` or `Css/`

5. **Check GitHub Pages build**: Settings → Pages → Check build logs for errors

## Files Modified

- `_layouts/default.html` - Updated CSS link to use root `css/main.css`
- `_config.yml` - Added `css` to include list
- `css/main.css` - Already exists with correct font paths
