// ========== فحص IP تلقائي ==========
fetch('https://api.ipify.org?format=json')
  .then(res => res.json())
  .then(ipData => {
    const userIP = ipData.ip;

    fetch('https://rotyip.onrender.com/api/check?ip=' + userIP)
      .then(response => response.json())
      .then(data => {
        let html = '';
        html += `<p><strong>IP:</strong> ${data.ip}</p>`;
        html += `<p><strong>Country:</strong> ${data.country}</p>`;
        html += `<p><strong>City:</strong> ${data.city}</p>`;

        if (data.zipcode && data.zipcode !== "-") {
          html += `<p><strong>ZIP Code:</strong> ${data.zipcode}</p>`;
        } else {
          html += `<p><strong>ZIP Code:</strong> Not Available</p>`;
        }

        if (data.street_address && data.street_address !== "Not Available") {
          html += `<p><strong>Address:</strong> ${data.street_address}</p>`;
        } else {
          html += `<p><strong>Address:</strong> Not Available</p>`;
        }

        if (data.fraud_score !== undefined) {
          html += `<p><strong>Score:</strong> ${data.fraud_score}</p>`;
        }

        html += `<p><strong>Threat Level:</strong> ${data.threat_level}</p>`;

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


// ========== توليد وفحص الإيميل ==========
function generateAndCheckEmail() {
  const first = document.getElementById("firstName").value.trim().toLowerCase();
  const last = document.getElementById("lastName").value.trim().toLowerCase();
  const resultBox = document.getElementById("emailResult");

  if (!first) {
    resultBox.innerHTML = "❌ أدخل الاسم الأول على الأقل.";
    return;
  }

  const domains = ["gmail.com", "yahoo.com", "outlook.com"];
  const base = last ? `${first}${last}` : `${first}`;
  const number = Math.floor(Math.random() * 90) + 10;
  const email = `${base}${number}@${domains[Math.floor(Math.random() * domains.length)]}`;

  resultBox.innerHTML = `⏳ يتم فحص <b>${email}</b> ...`;
  checkEmail(email, resultBox);
}

function manualEmailCheck() {
  const email = document.getElementById("manualEmail").value.trim();
  const resultBox = document.getElementById("emailResult");

  if (!email) {
    resultBox.innerHTML = "❌ يرجى إدخال إيميل.";
    return;
  }

  resultBox.innerHTML = `⏳ يتم فحص <b>${email}</b> ...`;
  checkEmail(email, resultBox);
}

function checkEmail(email, resultBox) {
  fetch(`https://rotyip.onrender.com/api/email-check?email=${encodeURIComponent(email)}`)
    .then(res => res.json())
    .then(data => {
      let status = data.status || "unknown";
      let message = "";

      if (status === "deliverable") {
        message = `✅ الإيميل صالح: <b>${email}</b>`;
      } else if (status === "risky") {
        message = `⚠️ الإيميل قابل للتوصيل ولكن غير مضمون: <b>${email}</b>`;
      } else if (status === "undeliverable") {
        message = `❌ الإيميل غير صالح: <b>${email}</b>`;
      } else {
        message = `❓ حالة غير معروفة: ${status} - <b>${email}</b>`;
      }

      resultBox.innerHTML = message;
    })
    .catch(err => {
      resultBox.innerHTML = `⚠️ حدث خطأ أثناء الفحص.`;
    });
}


// ========== فحص ZIP ==========
function lookupZipStreets() {
  const zip = document.getElementById("zipInput").value.trim();
  const zipCityState = document.getElementById("zipCityState");
  const resultBox = document.getElementById("zipStreetsResult");

  if (!zip) {
    resultBox.innerHTML = "❌ أدخل ZIP أولاً.";
    return;
  }

  resultBox.innerHTML = "⏳ جاري جلب البيانات ...";

  fetch(`https://api.zippopotam.us/us/${zip}`)
    .then(res => {
      if (!res.ok) throw new Error("ZIP غير صحيح");
      return res.json();
    })
    .then(data => {
      const place = data.places?.[0];
      if (!place) {
        resultBox.innerHTML = "❌ لم يتم العثور على بيانات.";
        return;
      }

      const city = place["place name"];
      const state = place["state abbreviation"];
      zipCityState.innerText = `📍 ${city}, ${state}`;
      resultBox.innerHTML = `✅ الرمز يعود إلى: <b>${city}, ${state}</b>`;
    })
    .catch(err => {
      resultBox.innerHTML = "⚠️ لم يتم العثور على نتائج للرمز.";
    });
}
