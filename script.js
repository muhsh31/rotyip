// Get user IP first
fetch('https://api.ipify.org?format=json')
  .then(res => res.json())
  .then(ipData => {
    const userIP = ipData.ip;

    // Fetch from Render backend API
    fetch('https://rotyip.onrender.com/api/check?ip=' + userIP)
      .then(response => response.json())
      .then(data => {
        let html = '';
        html += <p><strong>IP:</strong> ${data.ip}</p>;
        html += <p><strong>Country:</strong> ${data.country}</p>;
        html += <p><strong>City:</strong> ${data.city}</p>;

        if (data.zipcode && data.zipcode !== "-") {
          html += <p><strong>ZIP Code:</strong> ${data.zipcode}</p>;
        } else {
          html += <p><strong>ZIP Code:</strong> Not Available</p>;
        }

        if (data.street_address && data.street_address !== "Not Available") {
          html += <p><strong>Address:</strong> ${data.street_address}</p>;
        } else {
          html += <p><strong>Address:</strong> Not Available</p>;
        }

        if (data.fraud_score !== undefined) {
          html += <p><strong>Score:</strong> ${data.fraud_score}</p>;
        }

        html += <p><strong>Threat Level:</strong> ${data.threat_level}</p>;
        
        const box = document.querySelector(".result-box");
        if (box) {
          box.innerHTML = html;
        }
      });
  })
  .catch(error => {
    const box = document.querySelector(".result-box");
    if (box) {
      box.innerHTML = "<p>⚠️ Failed to fetch IP or scan data.</p>";
    }
    console.error("Auto-check failed:", error);
  });