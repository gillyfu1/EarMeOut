# EarMeOut

A static website for a mental health support chatbot. Open directly in your browser - no server needed.

## File Structure

### `index.html`
**Main home page** - The landing page with hero section, bot image, chatbot widget, and site navigation. All CSS and JavaScript is embedded inline.

### `about.html`
**About page** - Team member sections (3 placeholders for photos and bios). Currently has placeholder text waiting for content.

### `resources.html`
**Resources page** - Lists mental health resources (grounding techniques, journaling prompts, crisis support links).

### `contact.html`
**Contact page** - Contact information page.

### `static/bot.png.png`
**Bot character image** - The chatbot character image displayed on the home page. Note: filename has double `.png` extension.

## How to Use

1. **Open the website**: Double-click `index.html` to open in your browser
2. **Navigate**: Use the top navigation bar to switch between pages
3. **Chat**: Click the heart button (💟) in the bottom-right corner to open the chatbot

## Customization

- **Colors**: Edit CSS variables in the `<style>` section of each HTML file
- **Content**: Edit the HTML directly - all content is in plain HTML
- **Bot Image**: Replace `static/bot.png.png` with your own image (keep the same filename)

## Notes

- All pages are self-contained (CSS/JS inline) - no external dependencies
- No Python, no server, no build step - just pure HTML/CSS/JS
- The chatbot currently uses stubbed responses - integrate a real API when ready
