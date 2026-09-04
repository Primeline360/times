"""Render Pink Threads narration using a licensed open-weight neural female voice.
The production branch does not modify the live website or attendance system.
"""
import json, os, re
from pathlib import Path
import numpy as np
import soundfile as sf
import torch
from kokoro import KPipeline

torch.set_num_threads(2)
scenes = [
('opening', 'Pink Threads of Remembrance.', 'Pink Threads of Remembrance. Fashion that heals. Fabric that remembers. A Namibian fashion story shaped by remembrance, strength, and hope.'),
('story1', 'Every stitch is a story.', 'Every stitch is a story. Every pink piece holds a life, a fight, a name we refuse to forget.'),
('story2', 'We remember. We celebrate. We protect.', 'For the ones we lost, we honor you. For the ones still fighting, we celebrate you. For the ones who come next, we protect you.'),
('story3', 'Pain into purpose.', 'We turned grief into garments. Silence into statements. Pain into purpose. Sustainable fashion, with soul. A runway that raises awareness. A collection that raises funds. A movement that raises hope.'),
('story4', 'Pink threads, holding us together.', "Because healing doesn't always look like medicine. Sometimes it looks like a dress you wear with pride. Sometimes it looks like a shirt that starts a conversation. Sometimes it looks like pink threads, holding us all together."),
('story5', 'This is remembrance you can wear.', 'This is not just fashion. This is remembrance you can wear.'),
('collection', 'The collection', 'Our first collection brings six pink pieces together, with prices from fifty-five to one hundred Namibian dollars. Each carries the same invitation: wear something meaningful, and start a conversation.'),
('ribbon', 'Pink Ribbon Bracelet', 'The Pink Ribbon Bracelet, at sixty-five Namibian dollars, combines metal links with soft pink ribbon. Its delicate bow makes remembrance something you can carry into everyday life.'),
('button', 'Button Bracelet', 'The Button Bracelet, at seventy-five Namibian dollars, brings together textured pink cord, button details and metallic accents. Small materials become a distinctive piece with character and meaning.'),
('shirt', 'Pink Statement Shirt', 'The Pink Statement Shirt, at one hundred Namibian dollars, gives the collection its signature garment. Pink and white panels, a bow and button details turn familiar clothing into a conversation starter.'),
('headband', 'Headband', 'At fifty-five Namibian dollars, the Headband brings bright colour and playful texture to everyday styling. It is an accessible way to wear the collection and share its message.'),
('necklace', 'Statement Necklace', 'The Statement Necklace, at ninety-five Namibian dollars, brings pink thread, buttons and spool-like details into one bold centrepiece. It puts the language of making at the heart of the design.'),
('earrings', 'Earrings', 'The Earrings, at sixty Namibian dollars, complete the collection with coordinated pink details. Together, these six pieces connect personal style with a shared story of remembrance and hope.'),
('value', 'Wear the memory. Fund the future.', 'Our vision connects three forms of value: fashion with meaning, creative reuse of materials, and community support. We want people to choose the products for their design, and stay connected because of the purpose behind them.'),
('process', 'Source. Create. Show. Grow.', 'The model starts with usable offcuts, surplus textiles and other materials suitable for reuse. We create small collections, test quality, and show them through events, pop-ups and the digital catalogue. Income can support further production, while agreed fundraising proceeds support selected initiatives.'),
('market', 'Three audiences. One shared cause.', 'Our intended customers include students, young professionals and supporters of local design. Potential sponsors and retail partners can help us reach them. The people we aim to support include cancer survivors, affected families and selected communities. These relationships will be built through formal agreements.'),
('business', 'Beyond one fashion show.', 'Product sales sit at the centre of the business. Future events, sponsorships and collaborations can create additional income. Donations are a separate fundraising stream, not a substitute for a viable product. Clear records will distinguish operating income, costs and funds committed to community support.'),
('impact', 'The impact we plan to create', 'By the end of twenty twenty-seven, our target is to divert ten thousand kilograms of usable material through reuse and upcycling, supported by sourcing partnerships. As we grow, we aim to create fair-work opportunities for a small number of people affected by cancer, and help fund two community projects. These are goals, not achievements we claim today.'),
('proof', 'Purpose, backed by evidence.', 'Progress will be measured through material weights, funds raised, paid work created and support delivered. We will use consent when sharing personal stories, verify partner contributions, and report results honestly. Trust has to grow alongside the collection.'),
('roadmap', 'Start small. Grow with purpose.', 'First, complete and photograph the collection. Next, test demand and improve the products. Then build partnerships and launch selected events. Expansion should follow evidence of demand, reliable production and the resources needed to deliver our impact goals.'),
('partner', 'Help us build what comes next.', 'We are seeking material suppliers, makers, event partners, retailers, mentors and future investors. Support can help turn the first collection into a growing Namibian brand. Sponsor recognition and commercial opportunities will be agreed openly, with no promise of guaranteed returns.'),
('closing', 'This is remembrance you can wear.', 'For those we remember. For those still fighting. For the future we want to create. Pink Threads of Remembrance. Fashion that heals. Fabric that remembers. This is remembrance you can wear.')
]
output = Path('narration-output')
output.mkdir(exist_ok=True)
pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M', device='cpu')
manifest=[]
for number, (key, title, text) in enumerate(scenes):
    pieces=[]
    for result in pipeline(text, voice='af_heart', speed=0.90):
        if result.audio is not None:
            pieces.append(result.audio.detach().cpu().numpy())
    if not pieces:
        raise RuntimeError(f'No audio generated for {key}')
    audio=np.concatenate(pieces)
    if not np.all(np.isfinite(audio)) or np.max(np.abs(audio)) < 0.02:
        raise RuntimeError(f'Invalid or silent narration: {key}')
    filename=f'{number:02d}_{key}.wav'
    sf.write(output/filename, audio, 24000, subtype='PCM_16')
    manifest.append(dict(id=key,title=title,text=text,file=filename,seconds=len(audio)/24000,voice='af_heart',voice_type='neural female English'))
    print(json.dumps(manifest[-1]), flush=True)
(output/'scenes.json').write_text(json.dumps(manifest,indent=2))
(output/'VOICE_README.txt').write_text('Neural female English voice: Kokoro af_heart. Model: hexgrad/Kokoro-82M, Apache-2.0. Generated with kokoro 0.9.4. Each WAV is 24 kHz PCM. No basic system speech synthesizer is used.\n')
print('DONE',sum(x['seconds'] for x in manifest),flush=True)
