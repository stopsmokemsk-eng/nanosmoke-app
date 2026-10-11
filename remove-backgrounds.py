from pathlib import Path
from PIL import Image,ImageOps
from rembg import remove,new_session
import hashlib,json,shutil
root=Path('_site');data=json.loads((root/'catalog.json').read_text());destdir=root/'cutouts';destdir.mkdir(exist_ok=True);session=None;report={'processed':[],'failed':[],'visualReviewRequired':True};memo={}
for product in data['products']:
    rel=product.get('image')
    if not rel:continue
    if rel in memo:
        product['sourceImage']=rel;product['image']=memo[rel];continue
    source=root/rel
    try:
        if not source.is_file() or source.suffix.lower()=='.svg':raise ValueError('missing or unsupported source')
        key='isnet-v1-'+hashlib.sha256(source.read_bytes()).hexdigest()[:24]+'.png';dest=destdir/key;cached=Path('cutouts')/key
        if cached.is_file():shutil.copy2(cached,dest)
        else:
            image=ImageOps.exif_transpose(Image.open(source)).convert('RGBA');image.thumbnail((1600,1600),Image.Resampling.LANCZOS)
            if image.getchannel('A').getextrema()[0]<255:cutout=image
            else:
                if session is None:session=new_session('isnet-general-use',providers=['CPUExecutionProvider'])
                cutout=remove(image,session=session).convert('RGBA')
            alpha=cutout.getchannel('A');bbox=alpha.point(lambda p:255 if p>12 else 0).getbbox()
            if bbox is None:raise ValueError('empty foreground')
            hist=alpha.histogram();coverage=sum(hist[13:])/(cutout.width*cutout.height)
            if coverage<0.005 or alpha.getextrema()[0]==255:raise ValueError('invalid or opaque mask')
            cutout=cutout.crop(bbox);canvas=Image.new('RGBA',(cutout.width+32,cutout.height+32),(0,0,0,0));canvas.alpha_composite(cutout,(16,16));canvas.save(dest,optimize=True)
        product['sourceImage']=rel;product['image']='cutouts/'+key;memo[rel]=product['image'];report['processed'].append({'name':product['name'],'source':rel,'cutout':product['image']})
    except Exception as e:report['failed'].append({'name':product['name'],'source':rel,'error':str(e)})
    if 'VOLT' in product['name'].upper() and product['category']=='accessories':product['category']='models'
report['allPhotosConverted']=not report['failed'];report['uniqueCutouts']=len(memo)
(root/'catalog.json').write_text(json.dumps(data,ensure_ascii=False));(root/'cutout-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
