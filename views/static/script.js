const gridItems = document.querySelectorAll('box');

gridItems.forEach(gridItem => {
  gridItem.addEventListener('click', () => {
    gridItem.classList.toggle('green');
  });
});
