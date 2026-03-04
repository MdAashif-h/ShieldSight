// Load stats
chrome.runtime.sendMessage({ action: 'getStats' }, (stats) => {
  document.getElementById('totalScans').textContent = stats.totalScans;
  document.getElementById('threatsBlocked').textContent = stats.threatsBlocked;
  document.getElementById('safeLinks').textContent = stats.safeLinks;
});

// Open dashboard button
document.getElementById('openDashboard').addEventListener('click', () => {
  chrome.tabs.create({ url: 'https://your-frontend.vercel.app' });
});