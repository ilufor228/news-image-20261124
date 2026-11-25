import os
from PIL import Image, ImageDraw, ImageFont

def create_newspaper():
    # 1024x1024 canvas
    width, height = 1024, 1024
    image = Image.new("RGB", (width, height), color="#F7F5F0")
    draw = ImageDraw.Draw(image)

    # Load fonts (fallback to default if system fonts aren't available)
    def get_font(size, bold=False):
        try:
            if bold:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
            else:
                return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except IOError:
            return ImageFont.load_default()

    font_title = get_font(36, bold=True)
    font_sub = get_font(13, bold=False)
    font_panel_title = get_font(14, bold=True)
    font_panel_body = get_font(11, bold=False)
    font_tag = get_font(10, bold=True)

    # Margins and border
    margin = 24
    draw.rectangle([margin, margin, width - margin, height - margin], outline="#222222", width=3)
    draw.rectangle([margin + 4, margin + 4, width - margin - 4, height - margin - 4], outline="#222222", width=1)

    # Masthead Section
    top_y = margin + 12
    draw.text((width // 2, top_y), "THE GLOBAL CHRONICLE", fill="#111111", font=font_title, anchor="mt")
    
    sub_text = "TUESDAY, 24 NOVEMBER 2026  |  WORLD DAILY EDITION  |  PRICE: $2.50"
    draw.text((width // 2, top_y + 46), sub_text, fill="#444444", font=font_sub, anchor="mt")

    # Divider line under masthead
    div_y = top_y + 70
    draw.line([margin + 16, div_y, width - margin - 16, div_y], fill="#222222", width=2)
    draw.line([margin + 16, div_y + 3, width - margin - 16, div_y + 3], fill="#222222", width=1)

    # 6 Panels layout: 3 columns, 2 rows
    cols = 3
    rows = 2
    grid_left = margin + 16
    grid_top = div_y + 16
    grid_right = width - margin - 16
    grid_bottom = height - margin - 16

    total_w = grid_right - grid_left
    total_h = grid_bottom - grid_top

    col_w = total_w / cols
    row_h = total_h / rows

    stories = [
        {
            "tag": "MIDDLE EAST",
            "title": "1. IRAN BLOCKADE SHOWDOWN",
            "caption": "US naval blockade of Iran tightens. VP JD Vance & SecState Marco Rubio meet Qatari PM at White House. Iran vows to use all tools."
        },
        {
            "tag": "UKRAINE",
            "title": "2. ZAPORIZHZHIA HIT",
            "caption": "Overnight Russian strike on apartment building in Zaporizhzhia kills 2 and wounds ~40, including 4 children."
        },
        {
            "tag": "CONFLICT",
            "title": "3. GAZA STRIKE",
            "caption": "Israeli airstrikes kill Hamas internal security chief Naeem Abu Nahel and six others, including two police officers."
        },
        {
            "tag": "MARKETS",
            "title": "4. NVIDIA COMEBACK",
            "caption": "Jensen Huang reinstated as Nvidia CEO 11 days after resigning. Shares jump ~30% as Wall Street rebounds strongly."
        },
        {
            "tag": "LATIN AMERICA",
            "title": "5. COLOMBIA CAR BOMB",
            "caption": "Car bomb outside Meta governor office in Villavicencio injures 23. President blames FARC dissidents before peace anniversary."
        },
        {
            "tag": "DEFENSE",
            "title": "6. NATO SPACE WARNING",
            "caption": "NATO chief Mark Rutte vows alliance will defend space assets after reports of Russian nuclear-armed satellite preparations."
        }
    ]

    for idx, story in enumerate(stories):
        c = idx % cols
        r = idx // cols

        px = grid_left + c * col_w + 8
        py = grid_top + r * row_h + 8
        pw = col_w - 16
        ph = row_h - 16

        # Panel border & background
        draw.rectangle([px, py, px + pw, py + ph], fill="#FFFFFF", outline="#333333", width=1)
        
        # Panel header banner background
        draw.rectangle([px, py, px + pw, py + 24], fill="#222222")
        draw.text((px + 8, py + 6), story["tag"], fill="#FFFFFF", font=font_tag)

        # Panel Title
        text_y = py + 32
        draw.text((px + 8, text_y), story["title"], fill="#111111", font=font_panel_title)

        # Decorative separator rule inside panel
        draw.line([px + 8, text_y + 20, px + pw - 8, text_y + 20], fill="#CCCCCC", width=1)

        # Panel Caption / Body text with manual wrapping
        words = story["caption"].split(" ")
        lines = []
        current_line = ""
        max_line_width = pw - 16
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font_panel_body)
            if bbox[2] <= max_line_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        body_y = text_y + 28
        for line in lines:
            draw.text((px + 8, body_y), line, fill="#333333", font=font_panel_body)
            body_y += 16

    # Save output
    os.makedirs(os.path.dirname(os.path.abspath("entry.png")), exist_ok=True)
    image.save("entry.png", "PNG")
    print("Successfully generated entry.png")

if __name__ == "__main__":
    create_newspaper()
