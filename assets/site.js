// Inscriptions par ville : Web3Forms envoie chaque inscription à contact@ (clé publique, faite pour être dans le code).
var W3F_KEY = "a4f6ae0e-dc1d-4ea9-b04a-1de9e9daf871";
document.querySelectorAll(".notify").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var propose = form.classList.contains("propose");
    var city = form.dataset.city || (form.ville && form.ville.value.trim());
    var btn = form.querySelector("button");
    if (form.botcheck && form.botcheck.checked) return;
    btn.disabled = true;
    btn.textContent = "…";
    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify({
        access_key: W3F_KEY,
        subject: (propose ? "Ville proposée — " : "Prévenez-moi — ") + city,
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
      done.textContent = propose
        ? "Merci ! On note " + city + ", et on vous écrit si on y va."
        : "Merci ! On vous prévient dès que la date de " + city + " est annoncée.";
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

// « Prévenir un ami » : feuille de partage du téléphone si elle existe, sinon WhatsApp
document.querySelectorAll(".share").forEach(function (a) {
  a.addEventListener("click", function (e) {
    if (!navigator.share) return;
    e.preventDefault();
    navigator.share({ title: "Sans Gluten Festival", text: a.dataset.text.replace(a.dataset.url, "").trim(), url: a.dataset.url }).catch(function () {});
  });
});
