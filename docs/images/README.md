# Dashboard Screenshots

This directory contains screenshot images for the README preview section.

## Adding Screenshots

To add screenshots to the README:

1. **Take screenshots** of your running dashboard:
   - Factory Overview (full dashboard view)
   - Worker Analytics (metrics cards)
   - Event Stream (live event feed)
   - Workstation Grid (utilization heatmap)

2. **Recommended naming:**
   - `dashboard-preview.png` - Main dashboard overview
   - `worker-analytics.png` - Worker metrics section
   - `event-stream.png` - Real-time event feed
   - `workstation-grid.png` - Workstation utilization
   - `api-docs.png` - FastAPI Swagger documentation

3. **Image specifications:**
   - Format: PNG or JPG
   - Resolution: 1920x1080 or higher
   - File size: < 500KB (optimize with tools like TinyPNG)
   - Use dark mode for consistency

4. **Add to this folder:**
   ```bash
   docs/images/dashboard-preview.png
   docs/images/worker-analytics.png
   docs/images/event-stream.png
   ```

5. **Reference in README:**
   The README.md already includes placeholders for these images. Once you add the files, they'll automatically display on GitHub.

## Example Commands

### Take screenshots (Windows)
- Press `Win + Shift + S` to capture region
- Save as PNG in this folder

### Optimize images
```bash
# Using ImageMagick (optional)
magick convert dashboard-preview.png -resize 1920x1080 -quality 85 dashboard-preview.png
```

### Verify images
Images should appear in GitHub README once pushed:
```bash
git add docs/images/
git commit -m "docs: Add dashboard screenshots"
git push origin main
```

## Tips for Great Screenshots

✅ **DO:**
- Use the production build for cleaner UI (`npm run build`)
- Include realistic data (seed the database first)
- Capture full screens showing multiple features
- Use dark mode consistently
- Highlight key metrics and features

❌ **DON'T:**
- Include personal/sensitive information
- Use development error messages
- Show incomplete/buggy UI states
- Mix light and dark mode screenshots
- Include browser dev tools unless demonstrating something specific

---

**Need help?** See [CONTRIBUTING.md](../../CONTRIBUTING.md) for more details.
