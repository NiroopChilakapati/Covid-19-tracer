// Prevent right-click menu
document.addEventListener('contextmenu', function (e) {
    e.preventDefault();

});

// Prevent F12 key
document.addEventListener('keydown', function (e) {
    if (e.key === "F12" || e.keyCode === 123 || (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "J"))) {
        e.preventDefault();
    }
});

// Redirect the website to the "sorry" page if the inspect option is opened

