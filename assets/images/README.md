# Images Directory

Place your site images here, including:

## Logo/Icon

- **Location**: `assets/images/logo.png` (or `.jpg`, `.svg`, `.webp`)
- **Recommended size**: 147x147 pixels or larger (square images work best)
- **Format**: PNG with transparency, SVG, or JPG
- **Styling**: Images will automatically be displayed in a circular canvas (147px diameter)

### How to Set Up Your Logo

1. **Add your image file** to this directory:
   ```
   assets/images/logo.png
   ```

2. **Update `_config.yml`** to reference your logo:
   ```yaml
   logo: /assets/images/logo.png
   ```

3. **That's it!** The logo will automatically appear in the circular canvas in your site header.

## Other Images

You can also store other images here for use in posts or pages:

- Post images: `assets/images/posts/`
- General images: `assets/images/`

### Using Images in Posts

Reference images in your Markdown posts like this:

```markdown
![Alt text](/assets/images/your-image.jpg)
```

Or using Jekyll's relative_url filter in HTML:

```html
<img src="{{ '/assets/images/your-image.jpg' | relative_url }}" alt="Description">
```

## Image Optimization Tips

- **Format**: Use PNG for logos/icons, JPG for photos, SVG for scalable graphics
- **Size**: Optimize images before uploading (use tools like TinyPNG or ImageOptim)
- **Dimensions**: Logo should be at least 147x147px (will be cropped to circle)
- **File size**: Keep images under 500KB when possible for faster loading
