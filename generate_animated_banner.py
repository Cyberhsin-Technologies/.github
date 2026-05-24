import os
import random
from PIL import Image, ImageDraw, ImageFont

def create_cyberpunk_game_banner_gif():
    # 1. Load the new highly diversified neon high-tech low-life base image
    base_image_path = "/Users/Hsin-Li/.gemini/antigravity/brain/9c3668cd-d0a9-4767-881c-41badba547e2/cyberpunk_diverse_neon_1779618222618.png"
    if not os.path.exists(base_image_path):
        print(f"Error: Base city image not found at {base_image_path}")
        return
        
    base_img = Image.open(base_image_path).convert("RGBA")
    
    # 2. Crop to cinematic wide 1024x410 dimension
    # Crop from y=200 to y=610 to simultaneously showcase massive high-tech skyscrapers,
    # the incredible variety of glowing neon signs (brain, cyborg, dragon, multilinguistic panels),
    # and the congested low-life street alleys below!
    crop_box = (0, 200, 1024, 610)
    cropped_base = base_img.crop(crop_box)
    width, height = cropped_base.size # 1024x410
    
    # 3. Setup rain and HUD elements
    num_frames = 24  # Loop size
    frames = []
    
    # Set up perfectly vertical glowing rain drops
    drops = []
    for _ in range(320):
        drops.append({
            'x': random.randint(0, width),
            'y': random.randint(-150, height),
            'length': random.randint(15, 32),
            'speed': random.randint(15, 26),
            'thickness': random.choice([1, 2]),
            'color': random.choice([
                (0, 255, 200, random.randint(90, 160)),   # Glowing cyber cyan
                (255, 0, 180, random.randint(85, 150)),   # Glowing neon magenta
                (255, 230, 0, random.randint(50, 110))    # Glowing Cyberpunk 2077 neon yellow
            ])
        })
        
    # Font for HUD overlay
    font_path = "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"
    try:
        hud_font = ImageFont.truetype(font_path, 10)
        warning_font = ImageFont.truetype(font_path, 12)
    except IOError:
        hud_font = ImageFont.load_default()
        warning_font = ImageFont.load_default()

    def draw_hud_overlay(draw, frame_idx):
        margin = 15
        blen = 20 # Bracket arm length
        h_color = (255, 180, 0, 180) # Cyberpunk yellow-orange
        c_color = (0, 240, 255, 180) # Cyber cyan
        
        # Top-Left Bracket
        draw.line([(margin, margin), (margin + blen, margin)], fill=h_color, width=2)
        draw.line([(margin, margin), (margin, margin + blen)], fill=h_color, width=2)
        
        # Top-Right Bracket
        draw.line([(width - margin, margin), (width - margin - blen, margin)], fill=h_color, width=2)
        draw.line([(width - margin, margin), (width - margin, margin + blen)], fill=h_color, width=2)
        
        # Bottom-Left Bracket
        draw.line([(margin, height - margin), (margin + blen, height - margin)], fill=h_color, width=2)
        draw.line([(margin, height - margin), (margin, height - margin - blen)], fill=h_color, width=2)
        
        # Bottom-Right Bracket
        draw.line([(width - margin, height - margin), (width - margin - blen, height - margin)], fill=h_color, width=2)
        draw.line([(width - margin, height - margin), (width - margin, height - margin - blen)], fill=h_color, width=2)
        
        # Center Targeting HUD
        cx, cy = width // 2, height // 2
        draw.rectangle([(cx - 25, cy - 25), (cx + 25, cy + 25)], outline=(0, 240, 255, 60), width=1)
        draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(0, 240, 255, 120), width=1)
        draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(0, 240, 255, 120), width=1)
        
        # Cybernetic diagnostic overlay text
        draw.text((margin + 10, margin + 25), "KIROSHI OPTICS v3.54", font=hud_font, fill=h_color)
        draw.text((margin + 10, margin + 40), "NEURAL_LINK_STABLE", font=hud_font, fill=c_color)
        
        # Scanning radar line sweeping down in loop
        scan_y = (frame_idx * height) // num_frames
        draw.line([(0, scan_y), (width, scan_y)], fill=(0, 240, 255, 45), width=2)
        # Scanline trace glow
        draw.rectangle([(0, max(0, scan_y - 8)), (width, scan_y)], fill=(0, 240, 255, 12))
        
        # Flashing Warning / Target indicator (every 6 frames)
        if (frame_idx // 3) % 2 == 0:
            draw.rectangle([(width - margin - 150, margin + 22), (width - margin - 10, margin + 38)], outline=(255, 60, 60, 200), fill=(100, 0, 0, 100), width=1)
            draw.text((width - margin - 138, margin + 24), "SYSTEM HAZARD", font=warning_font, fill=(255, 90, 90, 230))

    def apply_slice_glitch(img, shift_amount=15, num_slices=4):
        glitched = img.copy()
        for _ in range(num_slices):
            slice_y = random.randint(10, height - 15)
            slice_h = random.randint(8, 20)
            dx = random.choice([-1, 1]) * random.randint(8, shift_amount)
            
            box = (0, slice_y, width, slice_y + slice_h)
            slice_region = img.crop(box)
            glitched.paste(slice_region, (dx, slice_y))
        return glitched

    for frame_idx in range(num_frames):
        # Copy base city image
        frame_canvas = cropped_base.copy()
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw_obj = ImageDraw.Draw(overlay)
        
        # Draw vertical rain (dx = 0)
        for drop in drops:
            dx = 0
            dy = drop['speed']
            
            x1 = drop['x']
            y1 = drop['y']
            x2 = x1
            y2 = y1 + drop['length']
            
            if 0 <= y1 <= height or 0 <= y2 <= height:
                draw_obj.line([(x1, y1), (x2, y2)], fill=drop['color'], width=drop['thickness'])
            
            # Update drop coordinates
            drop['y'] += dy
            if drop['y'] > height:
                drop['x'] = random.randint(0, width)
                drop['y'] = random.randint(-50, 0)
                
        # Draw HUD overlays on top of the rain
        draw_hud_overlay(draw_obj, frame_idx)
        
        # Merge layers
        frame_final = Image.alpha_composite(frame_canvas, overlay).convert("RGB")
        
        # Signal interference glitch
        if frame_idx in [7, 8, 19, 20]:
            frame_final = apply_slice_glitch(frame_final, shift_amount=20, num_slices=6)
            
        frames.append(frame_final)
        
    # Save the loop as an animated GIF (cache busting v5!)
    output_dir = "profile/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "cyberpunk_banner_v5.gif")
    
    # 55ms per frame loop
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=55,
        loop=0
    )
    print(f"Animated Masterpiece Highly Diversified Neon HUD rain banner successfully saved to {output_path}")

if __name__ == "__main__":
    create_cyberpunk_game_banner_gif()
