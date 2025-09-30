const navSlide = () => {
  const expand = document.querySelector('.expand');
  const nav = document.querySelector('.nav-links');
  const navLinks = document.querySelectorAll('.nav-links li');

  expand.addEventListener('click', () => {
    // toggles the navigation
    nav.classList.toggle('nav-active');

    // animates links in navigation
    navLinks.forEach((link, index) => {
      if(link.style.animation){
        link.style.animation = '';
      }
      else{
        link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.375}s`;
      }
    });
    expand.classList.toggle('toggle');
  });
}

navSlide();