document.addEventListener("DOMContentLoaded", function(event) {
  var savedTheme = localStorage.getItem("theme");
  var currentTheme = savedTheme || "light";
  document.documentElement.setAttribute("data-theme", currentTheme);

  var themeSwitcher = document.getElementById("theme-switcher");
  var themeImage = document.getElementById("theme-image");

  themeImage.src = currentTheme === "dark" ? "/static/img/off.png" : "/static/img/on.png";

  var changeCount = 0; 
  var resetTimeout;

  themeSwitcher.onclick = function() {
    var switchToTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", switchToTheme);
    localStorage.setItem("theme", switchToTheme);

    themeImage.src = switchToTheme === "dark" ? "/static/img/off.png" : "/static/img/on.png";
    currentTheme = switchToTheme; 

    changeCount++;

    if (changeCount >= 5) {
      alert("Досить гратися світлом, а то прийде до тебе вночі ДТЕК і все відключить");
      clearTimeout(resetTimeout); 
      changeCount = 0; 
    } else {
      resetTimeout = setTimeout(function() {
        changeCount = 0; 
      }, 5000);
    }
  }
});