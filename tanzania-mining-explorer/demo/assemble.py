import json, subprocess, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()

data = json.load(open('frames.json'))
total = data['total']
frames = [f for f in data['frames']]

# Frame shown at scenario t=0: the last frame captured before 0 (page state at t0).
pre  = [f for f in frames if f['t'] <= 0]
post = [f for f in frames if 0 < f['t'] < total]
seq = ([{'t':0.0,'file':pre[-1]['file']}] if pre else []) + post

# concat manifest with per-frame durations
lines = ['ffconcat version 1.0']
for i, f in enumerate(seq):
    dur = (seq[i+1]['t'] - f['t']) if i+1 < len(seq) else (total - f['t'])
    dur = max(dur, 0.001)
    lines.append(f"file '{f['file']}'")
    lines.append(f"duration {dur:.4f}")
lines.append(f"file '{seq[-1]['file']}'")
open('list.ffconcat','w').write('\n'.join(lines)+'\n')
print(f"{len(seq)} frames over {total}s  (avg {len(seq)/total:.1f} fps)")

subprocess.run([FF,'-y','-hide_banner','-loglevel','error',
  '-f','concat','-safe','0','-i','list.ffconcat',
  '-i','audio.wav',
  '-vf','fps=25,format=yuv420p',
  '-c:v','libx264','-preset','medium','-crf','19',
  '-c:a','aac','-b:a','160k',
  '-t',str(total),'-movflags','+faststart',
  'ngao-console-demo.mp4'], check=True)
r=subprocess.run([FF,'-hide_banner','-i','ngao-console-demo.mp4'],capture_output=True,text=True)
print([l.strip() for l in r.stderr.splitlines() if 'Duration' in l or 'Stream' in l])
