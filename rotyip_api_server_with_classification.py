<nav>
  <a href="#about">About</a>
  <a href="#pricing">Pricing</a>
  <a href="#documentation">Documentation</a>
  <a href="#ziplookup">ZIP Lookup</a>
  <a href="#emailCheck">Email Check</a>
</nav>
</header>
<section class="hero">
  <div class="hero-text">
    <h1>IP Geolocation and Threat Intelligence API</h1>
    <p>Lookup the location and threat profile of any IP Address to localize your website content, analyze logs, enrich forms, enforce GDPR compliance, block threats and more.</p>
    <div class="buttons">
      <a class="btn-primary" href="#pricing">Get Started</a>
      <a class="btn-secondary" href="#documentation">Documentation</a>
    </div>
  </div>
  <div class="result-box">
    <div class="result-item">IP: <span id="ip">-</span></div>
    <div class="result-item">Country: <span id="country">-</span></div>
    <div class="result-item">City: <span id="city">-</span></div>
    <div class="result-item">Time Zone: <span id="timezone">-</span></div>
    <div class="result-item">Threat Level: <span id="threat">-</span></div>
  </div>

  <div class="email-check-inline" id="emailCheck">
    <h2>📧 توليد وفحص الإيميل</h2>
    <input id="firstName" type="text" placeholder="First Name (مثال: John)">
    <input id="lastName" type="text" placeholder="Last Name (اختياري)">
    <button onclick="generateAndCheckEmail()">🎲 إنشاء وفحص</button>
    <input id="manualEmail" type="email" placeholder="أو أدخل إيميل يدويًا هنا">
    <button onclick="manualEmailCheck()">🔍 فحص يدوي</button>
    <div id="emailResult"></div>
  </div>

  <div class="zip-lookup-inline" id="ziplookup">
    <h2>🏠 البحث عن الشوارع حسب ZIP</h2>
    <input id="zipInput" type="text" placeholder="أدخل ZIP Code مثل 30301" />
    <button onclick="lookupZipStreets()">بحث</button>
    <div id="zipCityState"></div>
    <div class="zip-result-box" id="zipStreetsResult">📬 أدخل الرمز البريدي لعرض الشوارع...</div>
  </div>
</section>

<script>
// استرجاع بيانات IP تلقائياً
fetch('https://api.ipify.org?format=json')
  .then(res => res.json())
  .then(ipData => {
    const userIP = ipData.ip;
    fetch('https://rotyip.onrender.com/api/check?ip=' + userIP)
      .then(response => response.json())
      .then(data => {
        document.getElementById("ip").textContent = data.ip || "-";
        document.getElementById("country").textContent = data.country || "-";
        document.getElementById("city").textContent = data.city || "-";
        document.getElementById("timezone").textContent = data.timezone || "-";
        document.getElementById("threat").textContent = data.threat_level || "-";
      });
  })
  .catch(error => {
    console.error("Auto IP lookup failed:", error);
  });

function lookupZipStreets() {
  const zip = document.getElementById("zipInput").value.trim();
  if (!zip) return;

  document.getElementById("zipStreetsResult").innerHTML = "⏳ يتم البحث ...";

  fetch(`https://rotyip.onrender.com/api/check?ip=8.8.8.8&zip=${zip}`)
    .then(res => res.json())
    .then(data => {
      let result = "";
      if (data.street_address && data.street_address !== "Not Available") {
        result = `<p><strong>عنوان تقريبي:</strong> ${data.street_address}</p><button onclick="copyToClipboard(\"${data.street_address}\")">📂 نسخ</button>`;
      } else {
        result = "⚠️ لا يوجد عنوان متاح";
      }
      document.getElementById("zipStreetsResult").innerHTML = result;
    })
    .catch(() => {
      document.getElementById("zipStreetsResult").innerHTML = "❌ حدث خطأ";
    });
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    const toast = document.getElementById("copyToast");
    toast.style.visibility = "visible";
    setTimeout(() => {
      toast.style.visibility = "hidden";
    }, 2000);
  });
}
</script>

<section class="doc-section" id="documentation">
  <h2>Documentation</h2>
  <p>To get started, make a GET request to the following endpoint:</p>
  <p><code>https://api.rotyip.com/v1/ip/{ip-address}</code></p>
  <p>Replace <code>{ip-address}</code> with a valid IPv4 or IPv6 address.</p>
  <p><strong>Response Example:</strong></p>
  <pre><code>{
  "ip": "8.8.8.8",
  "country": "United States",
  "city": "New York",
  "timezone": "America/New_York",
  "threat_level": "low"
}</code></pre>
  <p>You can also use the API without authentication for basic usage. For extended usage, consider our paid plans (see <a href="#pricing">Pricing</a>).</p>
</section>
<section class="pricing-section" id="pricing">
  <h2>Pricing</h2>
  <p>Choose the plan that fits your needs. No hidden fees.</p>
  <div class="pricing-cards">
    <div class="card">
      <h3>Free</h3>
      <p class="price">$0/mo</p>
      <p>Up to 200 requests/day<br/>Basic geolocation<br/>No API key required</p>
    </div>
    <div class="card">
      <h3>Pro</h3>
      <p class="price">$19/mo</p>
      <p>Up to 10,000 requests/day<br/>Full threat analysis<br/>Email support</p>
    </div>
    <div class="card">
      <h3>Enterprise</h3>
      <p class="price">Contact Us</p>
      <p>Unlimited usage<br/>Custom SLAs<br/>Priority support<br/>Dedicated IPs</p>
    </div>
  </div>
</section>
<section class="about-section" id="about">
  <h2>About Rotyip</h2>
  <p>Rotyip is a lightweight IP intelligence platform designed to provide accurate geolocation and threat detection in real-time.</p>
  <p>Our mission is to help developers, analysts, and security teams make informed decisions by giving them fast and reliable access to IP data.</p>
  <p>Whether you're protecting your application, customizing content, or analyzing traffic, Rotyip delivers the data you need with minimal setup.</p>
  <p>We value simplicity, speed, and privacy – and we are committed to continuous improvement.</p>
</section>
<div id="copyToast" style="visibility: hidden;min-width: 220px;background-color: #333;color: #fff;text-align: center;border-radius: 8px;padding: 10px;position: fixed;z-index: 9999;left: 50%;bottom: 30px;transform: translateX(-50%);font-size: 14px;box-shadow: 0 0 8px rgba(0,0,0,0.3);">
  ✅ تم نسخ العنوان إلى الحافظة
</div>
<footer>
  © 2025 rotyip.com — All rights reserved.
</footer>
