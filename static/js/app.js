const $ = id => document.getElementById(id);
const form = $('farmForm');
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = $('submitBtn');
  $('errorMsg').textContent = '';
  button.disabled = true; button.innerHTML = 'Reading your field… <span>✳</span>';
  const payload = {
    city: $('city').value.trim(), N: $('n').value, P: $('p').value, K: $('k').value,
    ph: $('ph').value, temperature: $('temperature').value, humidity: $('humidity').value,
    rainfall: $('rainfall').value, soil_moisture: $('soil_moisture').value,
    soil_type: $('soil_type').value, growth_stage: $('growth_stage').value
  };
  try {
    const response = await fetch('/api/recommend', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    const data = await response.json();
    if (!response.ok || !data.success) throw new Error(data.error || 'Could not generate recommendations.');
    $('emptyState').hidden = true; $('results').hidden = false;
    $('cropName').textContent = data.crop;
    $('confidence').textContent = `${data.confidence}%`;
    $('modelNote').textContent = data.model_note;
    $('fertilizerText').textContent = data.fertilizer;
    $('irrigationStatus').textContent = data.irrigation.status;
    $('irrigationText').textContent = data.irrigation.advice;
    $('nextCheck').textContent = `Suggested next check: ${data.irrigation.next_check}.`;
    $('rankings').innerHTML = data.ranking.map((item, index) => `<div class="rank-row"><span class="rank-no">0${index+1}</span><span class="rank-name">${escapeHtml(item.crop)}</span><div class="rank-track"><i style="width:${Math.max(0,Math.min(100,item.score))}%"></i></div><strong>${item.score}%</strong></div>`).join('');
  } catch (err) { $('errorMsg').textContent = err.message; }
  finally { button.disabled = false; button.innerHTML = 'Generate farm insights <span>↗</span>'; }
});
function escapeHtml(value) { return String(value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch])); }
$('weatherBtn').addEventListener('click', async () => {
  const msg = $('weatherMsg'); msg.textContent = 'Fetching current conditions…';
  try {
    const response = await fetch('/api/weather', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({city:$('city').value,api_key:$('weatherKey').value})});
    const data = await response.json();
    if (!data.ok) throw new Error(data.error || 'Weather lookup failed.');
    $('temperature').value = data.temperature; $('humidity').value = data.humidity; $('rainfall').value = data.rainfall;
    msg.textContent = `${data.description} · ${data.temperature}°C · humidity ${data.humidity}% · rainfall ${data.rainfall} mm (last hour)`;
  } catch (err) { msg.textContent = err.message; }
});
$('historyBtn').addEventListener('click', async () => {
  const list = $('historyList'); list.innerHTML = '<span class="muted">Loading…</span>';
  try {
    const response = await fetch('/api/history'); const data = await response.json();
    list.innerHTML = data.items.length ? data.items.map(item => `<div class="history-row"><div><b>${escapeHtml(item.recommended_crop || 'Recommendation')}</b><small>${escapeHtml(item.soil_type || 'Soil not specified')} · ${escapeHtml(item.growth_stage || '')}</small></div><time>${escapeHtml((item.created_at || '').replace('T',' '))}</time></div>`).join('') : '<span class="muted">No recommendations saved yet.</span>';
  } catch { list.innerHTML = '<span class="muted">Could not load history.</span>'; }
});
