from pathlib import Path
from PIL import Image,ImageOps,ImageChops
from rembg import remove,new_session
import hashlib,json,shutil
root=Path('_site');data=json.loads((root/'catalog.json').read_text());folder=root/'cutouts';folder.mkdir(exist_ok=True);memo={};session=None;report={'processed':[],'failed':[],'visualReviewRequired':True,'algorithm':'always-segment-v2'}
for p in data['products']:
    rel=p.get('image')
    if not rel:
        report['failed'].append({'name':p['name'],'error':'missing image'});continue
    try:
        if rel in memo:p['sourceImage']=rel;p['image']=memo[rel];continue
        src=root/rel
        if not src.is_file() or src.suffix.lower()=='.svg':raise ValueError('missing or unsupported source')
        name='isnet-v2-'+hashlib.sha256(src.read_bytes()).hexdigest()[:24]+'.png';out=folder/name;cached=Path('cutouts')/name
        if cached.is_file():shutil.copy2(cached,out)
        else:
            image=ImageOps.exif_transpose(Image.open(src)).convert('RGBA');image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
            if session is None:session=new_session('isnet-general-use',providers=['CPUExecutionProvider'])
            result=remove(image,session=session).convert('RGBA');result.putalpha(ImageChops.multiply(result.getchannel('A'),image.getchannel('A')))
            alpha=result.getchannel('A');box=alpha.point(lambda x:255 if x>12 else 0).getbbox()
            if box is None or alpha.getextrema()[0]==255:raise ValueError('empty or opaque mask')
            result=result.crop(box);canvas=Image.new('RGBA',(result.width+32,result.height+32),(0,0,0,0));canvas.alpha_composite(result,(16,16));canvas.save(out,optimize=True)
        p['sourceImage']=rel;p['image']='cutouts/'+name;memo[rel]=p['image'];report['processed'].append({'name':p['name'],'source':rel,'cutout':p['image']})
    except Exception as e:report['failed'].append({'name':p['name'],'source':rel,'error':str(e)})
report['allPhotosConverted']=not report['failed'];report['uniqueCutouts']=len(memo);(root/'catalog.json').write_text(json.dumps(data,ensure_ascii=False));(root/'cutout-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
