document.addEventListener('DOMContentLoaded', function() {
    // Récupérer le contexte du canvas avec l'id 'myChart'
    var ctx = document.getElementById('myChart').getContext('2d');

    // Changer la taille du canvas
    document.getElementById('myChart').style.width = '600px'; // Largeur
    document.getElementById('myChart').style.height = '400px'; // Hauteur

    // Créer un nouveau graphique de type 'bar' avec le contexte récupéré
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            // Les étiquettes sur l'axe des x représentent les noms des villes
            labels: ['Bruxelles', 'Charleroi', 'Courtrai', 'Grobbendonk', 'Herzele', 'Jambes', 'Liege','Namur','Beveren' ],
            datasets: [{
                // Le label du dataset
                label: 'Nombre de Rues par Ville',
                // Les données représentent le nombre de rues par ville
                data: [4, 1, 2, 1, 3, 3, 2, 2, 1],
                // Les couleurs de fond des barres
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                // Les couleurs de bordure des barres
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                // L'épaisseur des bordures des barres
                borderWidth: 1
            }]
        },
        options: {
            // Les options du graphique
            scales: {
                y: {
                    beginAtZero: true // L'axe des y commence à 0
                }
            }
        }
    });
});
