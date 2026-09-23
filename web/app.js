(() => {
  const cards = [...document.querySelectorAll('.chapter')];
  if (!cards.length) return;
  const search = document.querySelector('#search'), group = document.querySelector('#group');
  let course = 'all';
  const fold = s => s.toLocaleLowerCase('tr').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/ı/g, 'i');
  const descriptions = {all:'Bütün bölümler kitap sırasıyla gösteriliyor. Ders seçerek temel, destek ve ileri okuma etiketlerini görebilirsiniz.',imo:'IMO301 · Örnekleme, standart hata ve çıkarım mantığına odaklanın. Destek ve ileri okumalar da görünür kalır.',pdr:'PDR209 · Etki büyüklüğü, ANOVA, varsayım kontrolü ve raporlamaya odaklanın. Destek okumaları da görünür kalır.'};
  function update() {
    let count = 0;
    cards.forEach(card => {
      card.hidden = !(fold(card.dataset.title).includes(fold(search.value.trim())) && (group.value === 'all' || card.dataset.group === group.value));
      if (!card.hidden) count++;
      const badge = card.querySelector('.level');
      if (!badge.dataset.original) badge.dataset.original = badge.textContent;
      badge.textContent = course === 'all' ? badge.dataset.original : card.dataset[course];
    });
    document.querySelector('#results').textContent = `${count} bölüm`;
    document.querySelector('#empty').hidden = count !== 0;
    document.querySelector('#route-note').textContent = descriptions[course];
  }
  document.querySelectorAll('[data-course]').forEach(button => button.addEventListener('click', () => {
    course = button.dataset.course;
    document.querySelectorAll('[data-course]').forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    update();
  }));
  search.addEventListener('input', update);
  group.addEventListener('change', update);
})();
