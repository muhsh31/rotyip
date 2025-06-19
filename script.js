window.onload = async function () {
  try {
    const ipData = await fetch("https://api64.ipify.org?format=json").then(r => r.json());
    const ip = ipData.ip;
    document.getElementById("ip").textContent = ip;

    const response = await fetch("https://rotyip.onrender.com/api/check?ip=" + ip);
    const data = await response.json();

    document.getElementById("country").textContent = data.country || "-";
    document.getElementById("city").textContent = data.city || "-";
    document.getElementById("timezone").textContent = data.timezone || "-";
    document.getElementById("threat").textContent = data.threat_level || "-";

    if (typeof applyThreatColor === "function") {
      applyThreatColor(data.threat_level);
    }
  } catch (e) {
    console.error("Auto-check failed:", e);
  }
};