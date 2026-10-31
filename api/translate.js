const htmlDecode=s=>s.replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&quot;/g,'"').replace(/&#39;/g,"'");
module.exports=async function(req,res){
 res.setHeader('Cache-Control','no-store'); res.setHeader('Content-Type','application/json; charset=utf-8');
 if(req.method!=='POST')return res.status(405).json({error:'POST required'});
 if(!process.env.GOOGLE_TRANSLATE_KEY)return res.status(503).json({error:'Google Cloud Translate not configured; configure GOOGLE_TRANSLATE_KEY in Vercel environment variables.'});
 const {text,source,target}=req.body||{};
 if(typeof text!=='string'||text.length<1||text.length>2000||!['bua','mn'].includes(source)||!['bua','mn'].includes(target)||source===target)return res.status(400).json({error:'Input must contain 1–2,000 characters and different valid languages.'});
 if(Number(req.headers['content-length']||0)>8000)return res.status(413).json({error:'Request too large'});
 try{
  const ctrl=new AbortController();const timeout=setTimeout(()=>ctrl.abort(),12000);
  let upstream;
  try{upstream=await fetch('https://translation.googleapis.com/language/translate/v2?key='+encodeURIComponent(process.env.GOOGLE_TRANSLATE_KEY),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q:text,source,target,format:'text'}),signal:ctrl.signal})}finally{clearTimeout(timeout)}
  if(!upstream.ok)return res.status(502).json({error:'Translation provider failed; check Google Cloud billing, API restrictions, language support and quotas.'});
  const data=await upstream.json();const translation=data?.data?.translations?.[0]?.translatedText;
  if(typeof translation!=='string')return res.status(502).json({error:'Unexpected translation provider response'});
  return res.status(200).json({translation:htmlDecode(translation),provider:'Google Cloud Translation',reviewed:false});
 }catch{return res.status(502).json({error:'Translation service temporarily unavailable'})}
};
