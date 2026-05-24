import os
import random
from PIL import Image, ImageDraw, ImageFont

def create_borderless_crt_gif():
    # Configuration - pure borderless CRT screen panel matching the 1024px width of the banner
    width = 1024
    height = 70
    
    # Colors
    screen_bg = (3, 12, 3)            # #030c03 (Extremely dark phosphor green screen)
    text_color = (51, 255, 51)        # #33ff33 (Glowing green phosphor text)
    glow_color = (0, 102, 17)         # #006611 (Phosphor text glow)
    
    # Glitch colors (Satoshi Kon/Ghost in the Shell Chromatic Aberration)
    magenta_glitch = (255, 0, 128)    # Chromatic aberration offset
    cyan_glitch = (0, 240, 255)       # Chromatic aberration offset
    
    # Fonts
    font_path = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
    font_size = 20
    hud_font_size = 9
    
    try:
        font = ImageFont.truetype(font_path, font_size)
        hud_font = ImageFont.truetype(font_path, hud_font_size)
    except IOError:
        font = ImageFont.load_default()
        hud_font = ImageFont.load_default()
        
    full_text = "[>_] GHOST IN THE MACHINE"
    
    # Calculate the exact stable starting x-position to perfectly center the text at completion
    temp_img = Image.new("RGB", (10, 10))
    temp_draw = ImageDraw.Draw(temp_img)
    fl, ft, fr, fb = temp_draw.textbbox((0, 0), full_text + "█", font=font)
    full_text_width = fr - fl
    start_x = (width - full_text_width) // 2
    
    # Calculate the exact starting x-position to center the HUD text
    hud_text = "SYS_SYNC: 98.74%  //  GHOST: ACTIVE  //  NEURAL_LINK_#8207"
    hl, ht, hr, hb = temp_draw.textbbox((0, 0), hud_text, font=hud_font)
    hud_width = hr - hl
    hud_start_x = (width - hud_width) // 2
    
    # Pre-generate Matrix Code Rain columns to animate their falling
    # Scale columns to cover the full 1024px width
    cols = []
    x_positions = list(range(15, width - 15, 30))
    for x in x_positions:
        cols.append({
            'x': x,
            'y': random.randint(-20, height + 10),
            'speed': random.randint(3, 5),
            'chars': [random.choice(['0', '1', 'X', 'Y', 'Z', '7', '4']) for _ in range(5)]
        })
        
    def update_matrix_rain():
        for col in cols:
            col['y'] += col['speed']
            if col['y'] > height + 20:
                col['y'] = -20
                col['speed'] = random.randint(3, 5)
                
    def draw_matrix_rain(draw):
        for col in cols:
            cx = col['x']
            cy = col['y']
            for idx, char in enumerate(col['chars']):
                char_y = cy - (idx * 11)
                if 0 < char_y < height - 5:
                    brightness = int(45 / (idx + 1))
                    char_color = (0, brightness, 0)
                    draw.text((cx, char_y), char, font=hud_font, fill=char_color)

    def draw_borderless_crt_screen(img, glitch_screen=False):
        draw = ImageDraw.Draw(img)
        
        # 1. Fill screen background
        draw.rectangle([(0, 0), (width - 1, height - 1)], fill=screen_bg)
        
        # 2. Draw matrix code rain
        draw_matrix_rain(draw)
        
        # 3. Draw HUD stats centered at the top
        hx_offset = random.randint(-4, 4) if glitch_screen else 0
        draw.text((hud_start_x + hx_offset, 4), hud_text, font=hud_font, fill=(0, 110, 15))
        
        # 4. Draw horizontal scanlines across the entire image height
        for y_coord in range(1, height, 2):
            draw.line([(0, y_coord), (width - 1, y_coord)], fill=(0, 8, 0), width=1)
            
        # 5. Draw a very subtle green outer screen frame highlight (no bulky bezel)
        draw.rectangle([(0, 0), (width - 1, height - 1)], outline=(0, 45, 10), width=1)

    def apply_slice_glitch(img, shift_amount=12, num_slices=4):
        glitched = img.copy()
        for _ in range(num_slices):
            slice_y = random.randint(10, height - 15)
            slice_h = random.randint(6, 12)
            dx = random.choice([-1, 1]) * random.randint(6, shift_amount)
            
            box = (0, slice_y, width, slice_y + slice_h)
            slice_region = img.crop(box)
            glitched.paste(slice_region, (dx, slice_y))
        return glitched

    # Generate typing sequence
    frames = []
    
    # Typing phase
    for i in range(len(full_text) + 1):
        update_matrix_rain()
        current_text = full_text[:i]
        if i < len(full_text):
            current_text += "█"
        else:
            current_text += " "
            
        # Create base frame
        img = Image.new("RGB", (width, height), screen_bg)
        draw_borderless_crt_screen(img)
        
        # Draw glowing phosphor text
        draw = ImageDraw.Draw(img)
        left, top, right, bottom = draw.textbbox((0, 0), current_text, font=font)
        text_height = bottom - top
        # Center vertically inside the 15-70 body area
        y = 15 + (55 - text_height) // 2 - 2
        
        # Text glow + sharp text layer centered horizontally at start_x
        draw.text((start_x + 1, y + 1), current_text, font=font, fill=glow_color)
        draw.text((start_x - 1, y), current_text, font=font, fill=glow_color)
        draw.text((start_x, y), current_text, font=font, fill=text_color)
        
        # Tiny slice glitch during typing
        if random.random() < 0.1 and i > 5:
            img = apply_slice_glitch(img, shift_amount=6, num_slices=2)
            
        frames.append(img)
        
    # Blinking cursor phase
    last_frame_no_cursor = frames[-1]
    
    # Generate static blinking frames with glitches
    for frame_idx in range(80):
        update_matrix_rain()
        cursor_on = (frame_idx // 8) % 2 == 0
        
        is_glitched = False
        glitch_type = None
        
        if 20 <= frame_idx <= 24:
            is_glitched = True
            glitch_type = "aberration"
        elif 48 <= frame_idx <= 54:
            is_glitched = True
            glitch_type = "slice"
            
        img = Image.new("RGB", (width, height), screen_bg)
        draw_borderless_crt_screen(img, glitch_screen=is_glitched)
        draw_f = ImageDraw.Draw(img)
        
        current_text = (full_text + "█") if cursor_on else (full_text + " ")
        
        left, top, right, bottom = draw_f.textbbox((0, 0), current_text, font=font)
        text_height = bottom - top
        y = 15 + (55 - text_height) // 2 - 2
        
        if is_glitched and glitch_type == "aberration":
            shift_x = random.randint(3, 5)
            draw_f.text((start_x - shift_x, y), current_text, font=font, fill=magenta_glitch)
            draw_f.text((start_x + shift_x, y), current_text, font=font, fill=cyan_glitch)
            draw_f.text((start_x, y), current_text, font=font, fill=(200, 255, 200))
        else:
            draw_f.text((start_x + 1, y + 1), current_text, font=font, fill=glow_color)
            draw_f.text((start_x - 1, y), current_text, font=font, fill=glow_color)
            draw_f.text((start_x, y), current_text, font=font, fill=text_color)
            
        if is_glitched and glitch_type == "slice":
            img = apply_slice_glitch(img, shift_amount=12, num_slices=5)
            
        frames.append(img)
        
    # Save as terminal_status_v7.gif (Cache busting!)
    output_dir = "profile/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "terminal_status_v7.gif")
    
    durations = [100] * (len(full_text) + 1) + [50] * 80
    
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=False,
        duration=durations,
        loop=0
    )
    print(f"Animated widescreen borderless CRT GIF successfully saved to {output_path}")

if __name__ == "__main__":
    create_borderless_crt_gif()
