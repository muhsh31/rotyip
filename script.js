
// Example fetch call with injection of ZIP Code and Score display logic
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
