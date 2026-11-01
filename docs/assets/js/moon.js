(function () {
  'use strict';

  var LUNAR_CYCLE = 29.53059;
  var PHASE_STEP = LUNAR_CYCLE / 8;
  var REFERENCE_DATE = new Date(2000, 0, 5);

  var PHASES = [
    {
      key: 'NEW_MOON',
      label: 'Nouvelle lune',
      image: 'NEW_MOON.png'
    },
    {
      key: 'WAXING_CRESCENT',
      label: 'Premier croissant',
      image: 'WAXING_CRESCE.png'
    },
    {
      key: 'FIRST_QUARTER',
      label: 'Premier quartier',
      image: 'FIRST_QUARTER.png'
    },
    {
      key: 'WAXING_GIBBOUS',
      label: 'Gibbeuse croissante',
      image: 'WAXING_GIBBOU.png'
    },
    {
      key: 'FULL_MOON',
      label: 'Pleine lune',
      image: 'FULL_MOON.png'
    },
    {
      key: 'WANING_GIBBOUS',
      label: 'Gibbeuse décroissante',
      image: 'WANING_GIBBOU.png'
    },
    {
      key: 'LAST_QUARTER',
      label: 'Dernier quartier',
      image: 'LAST_QUARTER.png'
    },
    {
      key: 'WANING_CRESCENT',
      label: 'Dernier croissant',
      image: 'WANING_CRESCE.png'
    }
  ];

  /** Moyennes mock (vélos/jour) — pleine lune vs autres jours, comme l'app Flask. */
  var MOCK_BIKE_AVERAGES = {
    fullMoon: 47,
    otherDays: 52
  };

  function parseInputDate(value) {
    if (!value) {
      return null;
    }

    var parts = value.split('-').map(Number);
    if (parts.length !== 3 || parts.some(function (part) { return Number.isNaN(part); })) {
      return null;
    }

    return new Date(parts[0], parts[1] - 1, parts[2]);
  }

  function moonAge(dateVoulu, dateReference) {
    var msPerDay = 86400000;
    var target = new Date(dateVoulu.getFullYear(), dateVoulu.getMonth(), dateVoulu.getDate());
    var reference = new Date(dateReference.getFullYear(), dateReference.getMonth(), dateReference.getDate());
    var diffDays = Math.floor((target - reference) / msPerDay);
    var age = diffDays % LUNAR_CYCLE;

    if (age < 0) {
      age += LUNAR_CYCLE;
    }

    return age;
  }

  function moonPhase(ageLune) {
    var normalized = ((ageLune % LUNAR_CYCLE) + LUNAR_CYCLE) % LUNAR_CYCLE;
    var index = Math.min(Math.floor(normalized / PHASE_STEP), PHASES.length - 1);
    return PHASES[index];
  }

  function formatAge(age) {
    return (Math.round(age * 100) / 100).toFixed(2);
  }

  function updateMoonDisplay(dateValue) {
    var ageEl = document.getElementById('moon-age');
    var phaseEl = document.getElementById('moon-phase-label');
    var imageEl = document.getElementById('moon-phase-image');
    var dateEl = document.getElementById('moon-selected-date');

    if (!ageEl || !phaseEl || !imageEl) {
      return;
    }

    var selectedDate = parseInputDate(dateValue);
    if (!selectedDate) {
      ageEl.textContent = '—';
      phaseEl.textContent = '—';
      imageEl.removeAttribute('src');
      imageEl.alt = 'Phase de la Lune';
      if (dateEl) {
        dateEl.textContent = '';
      }
      return;
    }

    var age = moonAge(selectedDate, REFERENCE_DATE);
    var phase = moonPhase(age);

    ageEl.textContent = formatAge(age);
    phaseEl.textContent = phase.label;
    imageEl.src = 'assets/img/images/' + phase.image;
    imageEl.alt = phase.label;

    if (dateEl) {
      dateEl.textContent = selectedDate.toLocaleDateString('fr-BE', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }

  function initMoonChart() {
    var canvas = document.getElementById('moonChart');
    if (!canvas || typeof Chart === 'undefined') {
      return;
    }

    new Chart(canvas.getContext('2d'), {
      type: 'pie',
      data: {
        labels: ['Jours de pleine lune', 'Jours normaux'],
        datasets: [{
          label: 'Moyenne de vélos',
          data: [MOCK_BIKE_AVERAGES.fullMoon, MOCK_BIKE_AVERAGES.otherDays],
          backgroundColor: [
            'rgba(255, 99, 132, 0.7)',
            'rgba(54, 162, 235, 0.7)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        plugins: {
          legend: {
            labels: {
              color: '#fff'
            }
          }
        }
      }
    });
  }

  function initMoonPage() {
    var form = document.getElementById('moon-form');
    var dateInput = document.getElementById('moon-date');

    if (!form || !dateInput) {
      return;
    }

    var today = new Date();
    var isoToday = [
      today.getFullYear(),
      String(today.getMonth() + 1).padStart(2, '0'),
      String(today.getDate()).padStart(2, '0')
    ].join('-');

    dateInput.value = isoToday;
    updateMoonDisplay(isoToday);

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      updateMoonDisplay(dateInput.value);
    });

    dateInput.addEventListener('change', function () {
      updateMoonDisplay(dateInput.value);
    });

    initMoonChart();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMoonPage);
  } else {
    initMoonPage();
  }

  window.WaybeMoon = {
    moonAge: moonAge,
    moonPhase: moonPhase,
    REFERENCE_DATE: REFERENCE_DATE,
    LUNAR_CYCLE: LUNAR_CYCLE
  };
})();
