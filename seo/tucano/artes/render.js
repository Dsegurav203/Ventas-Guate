const {chromium}=require('playwright');const fs=require('fs');const S=process.argv[2];
(async()=>{const b=await chromium.launch();const jobs=JSON.parse(fs.readFileSync(S+'/html/jobs.json'));fs.mkdirSync(S+'/out',{recursive:true});
for(const [n,w,h] of jobs){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});await p.goto('file://'+S+'/html/'+n+'.html');await p.waitForTimeout(300);await p.screenshot({path:S+'/out/'+n+'.png'});await p.close();}
await b.close();console.log('ok')})();
