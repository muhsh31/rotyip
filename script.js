
// Get user IP first
fetch('https://api.ipify.org?format=json')
  .then(res => res.json())
  .then(ipData => {
    const userIP = ipData.ip;

    // Fetch from /api/check using the detected IP
    fetch('/api/check?ip=' + userIP)
      .then(response => response.json())
      .then(data => {
        let html = '';
        html += `<p class="result-item"><span>IP:</span> ${data.ip}</p>`;
        html += `<p class="result-item"><span>Country:</span> ${data.country}</p>`;
        html += `<p class="result-item"><span>City:</span> ${data.city}</p>`;

        if (data.zipcode && data.zipcode !== "-") {
          html += `<p class="result-item"><span>ZIP Code:</span> ${data.zipcode}</p>`;
        }
        if (data.fraud_score !== undefined) {
          html += `<p class="result-item"><span>Score:</span> ${data.fraud_score}</p>`;
        }

        html += `<p class="result-item"><span>Threat Level:</span> ${data.threat_level}</p>`;
        document.getElementById("result").innerHTML = html;
      });
  })
  .catch(error => {
    document.getElementById("result").innerHTML = "<p class='result-item'>Failed to fetch IP or data.</p>";
    console.error("Auto-check failed:", error);
  });
