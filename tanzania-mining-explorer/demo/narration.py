import json, subprocess, wave, pathlib

SEGS = [
 ("s1", "This is the Ngao Exploration Console — a mineral targeting workbench for Tanzania, developed under A.D. Ports Group's research and innovation programme."),
 ("s2", "Choose a commodity, and hyperspectral satellite imagery builds a heat map of concentration — reading minerals directly, and through their signature in vegetation."),
 ("s3", "Every ministry licence is overlaid on that surface — each with a passport: holder, declared minerals, and what has actually been excavated."),
 ("s4", "Roads, railways, ports and power complete the picture; a single AI score then ranks every block on the same basis."),
 ("s5", "The result is open ground, ranked: high anomaly, best access, not yet taken — with a peg application drafted in one click."),
 ("s6", "Our own licences track the field crews — drilling, gravity, geophysics — with every geological report one click away."),
 ("s7", "And the laboratory queue shows the backlog — thousands of samples past promise — so nothing stalls unseen."),
 ("s8", "Ngao. Find the licence before anyone else does."),
]

model = next(pathlib.Path('.').glob('en-us-ryan-high.onnx'))
durs = {}
for name, text in SEGS:
    subprocess.run(['python3','-m','piper','-m',str(model),'--length-scale','1.0',
                    '--sentence-silence','0.30','-f',f'{name}.wav'],
                   input=text.encode(), check=True, capture_output=True)
    with wave.open(f'{name}.wav') as w:
        durs[name] = w.getnframes()/w.getframerate()

# timeline: 1.2s lead-in, 0.7s gap between segments
t = 1.0
timeline = []
for name, text in SEGS:
    timeline.append({"name":name, "text":text, "start":round(t,2), "dur":round(durs[name],2)})
    t += durs[name] + 0.55
timeline_end = round(t + 1.6, 2)   # hold outro
json.dump({"segments":timeline, "total":timeline_end}, open('timeline.json','w'), indent=1)
for s in timeline: print(f"{s['name']}  start={s['start']:6.2f}  dur={s['dur']:5.2f}  | {s['text'][:56]}")
print("TOTAL", timeline_end)
