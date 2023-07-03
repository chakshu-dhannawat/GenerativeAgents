from PIL import Image

def extract_frames(gif_path, num_frames):
    gif = Image.open(gif_path)
    frames = []
    
    try:
        while len(frames) < num_frames:
            gif.seek(len(frames))
            frame = gif.copy().convert('RGBA')
            frames.append(frame)
    except EOFError:
        pass
    
    return frames

# Example usage
gif_path = 'Assets\\killing.gif'
num_frames = 100

frames = extract_frames(gif_path, num_frames)
for i, frame in enumerate(frames):
    frame.save(f'Assets\\killing\\{i}.png')
