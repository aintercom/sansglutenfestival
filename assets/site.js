// Inscriptions par ville : Web3Forms envoie chaque inscription à contact@ (clé publique, faite pour être dans le code).
var W3F_KEY = "a4f6ae0e-dc1d-4ea9-b04a-1de9e9daf871";
document.querySelectorAll(".notify").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var city = form.dataset.city;
    var btn = form.querySelector("button");
    if (form.botcheck && form.botcheck.checked) return;
    btn.disabled = true;
    btn.textContent = "…";
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        access_key: W3F_KEY,
        subject: "Prévenez-moi — " + city,
        from_name: "Site Sans Gluten Festival",
        ville: city,
        page: location.pathname,
        email: form.email.value.trim()
      })
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (!res.success) throw new Error(res.message);
      var done = document.createElement("p");
      done.className = "notify-done";
      done.setAttribute("role", "status");
      done.textContent = "Merci ! On vous prévient dès que la date de " + city + " est annoncée.";
      form.replaceWith(done);
    }).catch(function () {
      btn.disabled = false;
      btn.textContent = "OK";
      var err = form.querySelector(".notify-err") || document.createElement("span");
      err.className = "notify-err";
      err.setAttribute("role", "alert");
      err.textContent = "L’envoi n’a pas marché. Réessayez, ou écrivez à contact@sansglutenfestival.fr";
      form.appendChild(err);
    });
  });
});
