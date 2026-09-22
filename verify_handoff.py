from pathlib import Path
import json,hashlib,sys
r=Path(__file__).resolve().parent
m=json.loads((r/'manifest.json').read_text())
bad=[]
for item in m['files']:
 p=r/item['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:bad.append(item['path'])
print(json.dumps({'checked':len(m['files']),'failed':bad},ensure_ascii=False,indent=2))
sys.exit(bool(bad))
