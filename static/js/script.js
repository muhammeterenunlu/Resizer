document.addEventListener('DOMContentLoaded', function () {
  // Yüzde değerinin güncellenmesi
  document.getElementById('percentage').addEventListener('input', function () {
    document.getElementById('percentageValue').textContent = this.value + '%';
  });

  // "enhance" radyo butonlarına tıklandığında "color-choice" divini göster/gizle
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
});
