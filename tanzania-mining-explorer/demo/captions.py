import json, re

tl = json.load(open('timeline.json'))

def chunks(text):
    """Split narration into caption-sized pieces at punctuation."""
    parts = re.split(r'(?<=[.;:]) +|(?= — )', text)
    out=[]
    for p in parts:
        p=p.strip()
        if not p: continue
        if out and len((out[-1]+' '+p).split())<=10: out[-1]=out[-1]+' '+p
        else: out.append(p)
    return out

def fmt(t):
    ms=int(round(t*1000)); h=ms//3600000; m=ms%3600000//60000; s=ms%60000//1000; r=ms%1000
    return f"{h:02d}:{m:02d}:{s:02d},{r:03d}"

cues=[]; sched=[]
for seg in tl['segments']:
    cs=chunks(seg["text"].replace("A.D. ","AD "))
    words=sum(len(c.split()) for c in cs)
    t=seg['start']
    for i,c in enumerate(cs):
        d=seg['dur']*len(c.split())/words
        end=t+d+(0.35 if i==len(cs)-1 else 0.0)
        cues.append((t,end,c.strip(' —')))
        sched.append({"t":round(t,2),"end":round(end,2),"text":c.strip(' —')})
        t+=d

with open('subtitles.srt','w') as f:
    for i,(a,b,c) in enumerate(cues,1):
        f.write(f"{i}\n{fmt(a)} --> {fmt(b)}\n{c}\n\n")
json.dump(sched, open('captions.json','w'))
print(f"{len(cues)} cues, last ends {cues[-1][1]:.1f}s")
