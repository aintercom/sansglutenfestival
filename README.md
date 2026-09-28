# SANS GLUTEN FESTIVAL

Le rendez-vous sans gluten de votre ville : des petits événements à taille humaine, avec food trucks et bar, dans les grandes villes de France.

🌐 [sansglutenfestival.fr](https://sansglutenfestival.fr) · 📸 [@sansglutenfestival](https://www.instagram.com/sansglutenfestival/)

## Modifier le site

Les pages (accueil, une page par ville, 404, sitemap) sont générées par un script :

```
python3 tools/build_pages.py
```

Villes, textes et titres se modifient dans `tools/build_pages.py`. Le style est dans `assets/site.css`, les formulaires d'inscription (Web3Forms) dans `assets/site.js`.
