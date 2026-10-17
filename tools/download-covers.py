#!/usr/bin/env python3
"""Rebuild the manually reviewed local anime images.

Install Pillow: python3 -m pip install -r tools/requirements-assets.txt
Run: npm run assets (add -- --force to replace existing files).
The fixed selection prevents later API randomness from introducing watermarks
or unsuitable crops. Article covers are 1920x1080; the Furina hero is 3840x2160.
Downloads, backups and source reports stay in the system temporary directory.
API availability does not grant copyright; artwork belongs to its creators.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'source' / 'img'
CACHE = Path(tempfile.gettempdir()) / 'shumunet-blog-assets'
COVERS = [{'id': 4010501,
  'url': 'https://safebooru.org/images/3839/1be7912c13ab285f43f1754be82c8f08f525cc5b.jpg',
  'source': 'https://twitter.com/roshidere/status/1518188713158885376'},
 {'id': 4010473,
  'url': 'https://safebooru.org/images/3839/6a1f186c338af005625e7656a650b994b73a6a80.jpg',
  'source': 'https://twitter.com/roshidere/status/1521429367649292290'},
 {'id': 3539352,
  'url': 'https://safebooru.org/images/3402/a4f14af96e6015ec8b0bd51fe3618c5258a15bc0.jpg',
  'source': 'https://twitter.com/roshidere/status/1411980600647438337'},
 {'id': 3539355,
  'url': 'https://safebooru.org/images/3402/d78780f83d0e63d4b2b87ebb4cdff0920d511f20.jpg',
  'source': 'https://twitter.com/roshidere/status/1409076478403244035'},
 {'id': 3991499,
  'url': 'https://safebooru.org/images/3820/4ce49edc68ba616446e371d2b748167d2b6d5a93.jpg',
  'source': 'https://twitter.com/roshidere/status/1521791751131787264'},
 {'id': 3159894,
  'url': 'https://safebooru.org/images/3035/d8c664fe12575b9db4bc61f3a1b40a492c736772.jpg',
  'source': 'https://i.pximg.net/img-original/img/2020/05/04/18/02/28/81288742_p0.jpg'},
 {'id': 3255239,
  'url': 'https://safebooru.org/images/3128/6677dcf67a496b3b3ed5ecd93565b24e6879923b.png',
  'source': 'https://i.pximg.net/img-original/img/2020/08/20/22/17/08/83818462_p0.png'},
 {'url': 'https://uapis.cn/assets/acg/pc/0072Vf1pgy1foxk3wgs1qj31kw0w01jo.jpg',
  'source': 'https://uapis.cn/api/v1/random/image?category=acg&type=pc'},
 {'url': 'https://uapis.cn/assets/acg/pc/110382939_p0.jpg',
  'source': 'https://uapis.cn/api/v1/random/image?category=acg&type=pc'},
 {'url': 'https://uapis.cn/assets/acg/pc/a15b4afegy1fmvjg5oaksj21hc0u07pp.jpg',
  'source': 'https://uapis.cn/api/v1/random/image?category=acg&type=pc'},
 {'url': 'https://uapis.cn/assets/acg/pc/110394662_p5.jpg',
  'source': 'https://uapis.cn/api/v1/random/image?category=acg&type=pc'},
 {'id': 6021995,
  'url': 'https://safebooru.org/images/4376/99955b551b1534bed2e0ac81f056d3ae.jpeg',
  'source': ''},
 {'id': 5842762,
  'url': 'https://safebooru.org/images/4368/32bf1d5a8b405589f36b6c1215fcace1.jpeg',
  'source': ''},
 {'id': 4193750,
  'url': 'https://safebooru.org/images/4013/8f3387f16644d94afc83fe4ca3fcab033292040d.jpg',
  'source': 'https://twitter.com/green322green/status/1587202758301519876'}]
HERO = {'id': 4669706, 'url': 'https://safebooru.org/images/4478/c8a11eb01b884ed671cf429878bda54e79e03d8f.png', 'source': 'https://i.pximg.net/img-original/img/2023/11/19/19/18/38/113538220_p0.png'}


def fetch(url):
    target = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if not target.exists():
        partial = target.with_suffix('.part')
        try:
            subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                            '--connect-timeout', '10', '--max-time', '60', '--retry', '2',
                            '--output', str(partial), url], check=True)
            # Verify before caching an API error page or incomplete download.
            with Image.open(partial) as image:
                image.verify()
            partial.replace(target)
        finally:
            partial.unlink(missing_ok=True)
    return target


def render_cover(source, target):
    with Image.open(source) as image:
        artwork = ImageOps.exif_transpose(image).convert('RGB')
    # Selected horizontal artwork fills the card, matching the reference style.
    save(ImageOps.fit(artwork, (1920, 1080), method=Image.Resampling.LANCZOS, centering=(0.5, 0.3)), target, 90)


def render_hero(source, target):
    with Image.open(source) as image:
        artwork = ImageOps.exif_transpose(image).convert('RGB')
    # Remove uniform black letterboxing, then fill the complete 4K canvas.
    bounds = artwork.convert('L').point(lambda x: 0 if x < 12 else 255).getbbox()
    if bounds:
        artwork = artwork.crop(bounds)
    save(ImageOps.fit(artwork, (3840, 2160), method=Image.Resampling.LANCZOS), target, 92)


def save(image,target,quality):
    target.parent.mkdir(parents=True,exist_ok=True)
    partial=target.with_suffix('.tmp.webp')
    image.save(partial,'WEBP',quality=quality,method=6)
    partial.replace(target)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force',action='store_true')
    args=parser.parse_args()
    CACHE.mkdir(parents=True,exist_ok=True)
    records=[]
    def cover(item):
        i,entry=item
        target=OUT/'covers'/f'anime-{i+1:02}.webp'
        if args.force or not target.exists():render_cover(fetch(entry['url']),target)
        print(f'Cover ready: {target.name}',flush=True)
        return {'file':str(target.relative_to(ROOT)),**entry}
    with ThreadPoolExecutor(max_workers=3) as pool:
        records.extend(pool.map(cover,enumerate(COVERS)))
    hero=OUT/'furina-hero.webp'
    if args.force or not hero.exists():render_hero(fetch(HERO['url']),hero)
    records.append({'file':str(hero.relative_to(ROOT)),**HERO})
    avatar=OUT/'avatar.webp'
    avatar_url='https://q1.qlogo.cn/g?b=qq&nk=705778569&s=640'
    if not avatar.exists():
        with Image.open(fetch(avatar_url)) as image:
            save(ImageOps.fit(image.convert('RGB'),(256,256),method=Image.Resampling.LANCZOS),avatar,92)
    records.append({'file':str(avatar.relative_to(ROOT)),'url':avatar_url})
    (CACHE/'sources.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    print(f'Images ready; source report outside project: {CACHE / "sources.json"}')

if __name__=='__main__':
    main()
