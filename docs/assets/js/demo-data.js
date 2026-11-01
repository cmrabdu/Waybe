var WAYBE_DEMO = {
  cities: [
    {
      name: "Charleroi",
      traffic: { lourd: 4820, pieton: 620, voiture: 18450, velo: 280 },
      streets: [
        "Boulevard Tirou",
        "Rue de la Montagne",
        "Avenue Général Michel",
        "Rue de Dampremy",
        "Boulevard Joseph II",
        "Rue de la Paix",
        "Chaussée de Marcinelle"
      ],
      streetsCount: 7
    },
    {
      name: "Namur",
      traffic: { lourd: 1240, pieton: 2180, voiture: 5620, velo: 1890 },
      streets: [
        "Rue de Fer",
        "Avenue de la Gare",
        "Boulevard Adolphe Sax",
        "Rue de l'Ange",
        "Rue de Bruxelles",
        "Quai de Meuse"
      ],
      streetsCount: 6
    },
    {
      name: "Bruxelles",
      traffic: { lourd: 2890, pieton: 8420, voiture: 9680, velo: 5240 },
      streets: [
        "Avenue Louise",
        "Boulevard Anspach",
        "Rue Antoine Dansaert",
        "Chaussée de Wavre",
        "Avenue de Tervueren",
        "Rue du Bailli",
        "Boulevard Léopold II",
        "Rue de la Loi",
        "Avenue des Arts",
        "Rue Neuve"
      ],
      streetsCount: 10
    },
    {
      name: "Liege",
      traffic: { lourd: 3560, pieton: 2940, voiture: 7820, velo: 3120 },
      streets: [
        "Avenue Rogier",
        "Boulevard de la Sauvenière",
        "Rue de la Casquette",
        "Quai de Rome",
        "Rue Pont d'Avroy",
        "Boulevard de la Constitution",
        "Rue de la Régence"
      ],
      streetsCount: 7
    },
    {
      name: "Courtrai",
      traffic: { lourd: 680, pieton: 1540, voiture: 3280, velo: 4680 },
      streets: [
        "Grote Markt",
        "Budastraat",
        "Doorniksesteenweg",
        "Ringlaan",
        "Brugsesteenweg"
      ],
      streetsCount: 5
    },
    {
      name: "Jambes",
      traffic: { lourd: 420, pieton: 980, voiture: 6120, velo: 740 },
      streets: [
        "Avenue Albert Ier",
        "Chaussée de Liège",
        "Rue de la Station",
        "Rue des Deportés"
      ],
      streetsCount: 4
    },
    {
      name: "Beveren",
      traffic: { lourd: 6240, pieton: 480, voiture: 8920, velo: 520 },
      streets: [
        "Havenstraat",
        "Grote Markt",
        "Kruisweg",
        "Vijfstraten",
        "Leopoldlaan"
      ],
      streetsCount: 5
    },
    {
      name: "Grobbendonk",
      traffic: { lourd: 180, pieton: 620, voiture: 1420, velo: 5840 },
      streets: [
        "Grote Steenweg",
        "Heideveld",
        "Bosstraat",
        "Kerkstraat"
      ],
      streetsCount: 4
    },
    {
      name: "Herzele",
      traffic: { lourd: 260, pieton: 540, voiture: 2180, velo: 4920 },
      streets: [
        "Geraardsbergsesteenweg",
        "Kerkplein",
        "Steenhuize",
        "Brielken"
      ],
      streetsCount: 4
    }
  ],

  tableStats: {
    ville: 9,
    vitesse: 1842,
    v85: 1842,
    traffic: 45280,
    rue: 52
  },

  bikeRanking: [
    ["Grobbendonk", 4.82],
    ["Herzele", 4.51],
    ["Courtrai", 3.94],
    ["Bruxelles", 2.87],
    ["Namur", 2.41],
    ["Liege", 2.18],
    ["Jambes", 1.02],
    ["Beveren", 0.48],
    ["Charleroi", 0.31]
  ],

  periods: [
    { id: "week", label: "7 derniers jours" },
    { id: "month", label: "30 derniers jours" },
    { id: "quarter", label: "Trimestre en cours" }
  ]
};
