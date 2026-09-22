#!/usr/bin/env node
/** Copy a stable application input set for an independent build and film run.
 * No existing source or snapshot is overwritten. Installed dependencies are
 * shared read-only by convention; this is a source snapshot, not a hermetic VM.
 */
import { createHash, randomUUID } from 'node:crypto';
import { mkdir, readdir, readFile, writeFile, symlink, lstat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
if (process.argv.includes('--help')) {
  console.log('node pipeline/snapshot-app.mjs\nCreates artifacts/pipeline/source-snapshots/<unique>/app, checks copied input hashes, and prints its path as JSON. Build and serve the returned app separately. No network calls.');
  process.exit(0);
}
if (process.argv.length > 2) throw new Error('No options supported. Use --help.');
const source = path.join(root, 'app');
const digest = (data) => createHash('sha256').update(data).digest('hex');
async function inventory() {
  const entries = [];
  const walk = async (rel) => {
    for (const entry of (await readdir(path.join(source, rel), { withFileTypes: true })).sort((a,b)=>a.name.localeCompare(b.name))) {
      if (entry.name.startsWith('._') || entry.name === '.DS_Store') continue;
      const name = path.join(rel, entry.name);
      if (entry.isSymbolicLink()) throw new Error(`Source symlink is not supported: ${name}`);
      if (entry.isDirectory()) await walk(name);
      else if (entry.isFile()) entries.push({path:name,sha256:digest(await readFile(path.join(source,name)))});
    }
  };
  for (const rel of ['src','scripts','public']) {
    try { await lstat(path.join(source,rel)); } catch (e) { if(e.code==='ENOENT' && rel!=='src') continue; throw e; }
    await walk(rel);
  }
  for (const rel of ['index.html','package.json','package-lock.json','tsconfig.json','vite.config.ts','LICENSE'])
    entries.push({path:rel,sha256:digest(await readFile(path.join(source,rel)))});
  return entries.sort((a,b)=>a.path.localeCompare(b.path));
}
const before = await inventory();
const run = `${new Date().toISOString().replaceAll(':','-').replaceAll('.','-')}-${randomUUID().slice(0,8)}`;
const folder = path.join(root,'artifacts/pipeline/source-snapshots',run);
const app = path.join(folder,'app');
await mkdir(app,{recursive:true});
const record = {schema_version:'architecture-source-snapshot.v1',status:'COPYING',created_at:new Date().toISOString(),source_root:source,snapshot_app:app,files:before,dependency_mode:'SHARED_LOCAL_NODE_MODULES',node:process.version};
try {
  for (const entry of before) {
    const bytes=await readFile(path.join(source,entry.path));
    if(digest(bytes)!==entry.sha256) throw new Error(`SOURCE_HASH_CHANGED while copying ${entry.path}`);
    const output=path.join(app,entry.path);
    await mkdir(path.dirname(output),{recursive:true});
    await writeFile(output,bytes,{flag:'wx'});
  }
  if(JSON.stringify(before)!==JSON.stringify(await inventory())) throw new Error('SOURCE_HASH_CHANGED during snapshot');
  for(const entry of before) if(digest(await readFile(path.join(app,entry.path)))!==entry.sha256) throw new Error(`COPY_HASH_MISMATCH ${entry.path}`);
  await symlink(path.join(source,'node_modules'),path.join(app,'node_modules'),'dir');
  record.status='SOURCE_COPY_VERIFIED';
  record.source_sha256=digest(JSON.stringify(before));
} catch(e) {record.status='FAILED';record.reason=e.message;process.exitCode=1;}
await writeFile(path.join(folder,'source-manifest.json'),JSON.stringify(record,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({status:record.status,app_root:app,manifest:path.join(folder,'source-manifest.json'),source_sha256:record.source_sha256,reason:record.reason},null,2));
