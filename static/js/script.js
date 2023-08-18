document.getElementById('percentage').addEventListener('input', function () {
  document.getElementById('percentageValue').textContent = this.value + '%';
});

document.querySelectorAll('[name="enhance"]').forEach(function (el) {
  el.addEventListener('change', function () {
    if (this.value == 'yes') {
      document.querySelector('.color-choice').style.display = 'flex';
    } else {
      document.getElementById('colorGroup').style.display = 'none';
    }
  });
});

document.addEventListener('DOMContentLoaded', function () {
  let enhanceChoices = document.querySelectorAll("input[name='enhance']");
  let colorChoiceDiv = document.querySelector('.color-choice');

  enhanceChoices.forEach(choice => {
    choice.addEventListener('change', function () {
      if (this.value === 'yes') {
        colorChoiceDiv.style.display = 'flex';
      } else {
        colorChoiceDiv.style.display = 'none';
      }
    });
  });

  document.getElementById('percentage').addEventListener('input', function () {
    document.getElementById('percentageValue').textContent = this.value + '%';
  });
});
