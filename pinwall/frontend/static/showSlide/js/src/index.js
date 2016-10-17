$(document).ready(function(){
    var url = location.href;
    var pos=url.indexOf("?");
    var targetUrl=url.substring(pos+1);
    var presentation = Crocodoc.createViewer('.presentation', {
        url: targetUrl,
        layout: Crocodoc.LAYOUT_PRESENTATION
    });
    presentation.load();

//console.log(presentation);

// Bind 'ready' and 'pagefocus' event handlers to update the page controls
    presentation.on('ready', function (event) {
        updatePageControls(event.data.page, event.data.numPages);
    });
    presentation.on('pagefocus', function (event) {
        updatePageControls(event.data.page, event.data.numPages);
    });

// Bind 'zoom' event to update the zoom controls
    presentation.on('zoom', function (event) {
        $('.zoom-in').prop('disabled', !event.data.canZoomIn);
        $('.zoom-out').prop('disabled', !event.data.canZoomOut);
    });

    function updatePageControls(currentPage, numPages) {
        $('.page').get(0).textContent = currentPage + ' / ' + numPages;
        $('.scroll-previous').prop('disabled', currentPage === 1);
        $('.scroll-next').prop('disabled', currentPage === numPages);
    }

// Bind click events for controlling the viewer
    $('.scroll-previous').on('click', function () {
        presentation.scrollTo(Crocodoc.SCROLL_PREVIOUS);
    });
    $('.scroll-next').on('click', function () {
        presentation.scrollTo(Crocodoc.SCROLL_NEXT);
    });
    /*$(window).on('keydown', function (ev) {
     if (ev.keyCode === 37) {
     presentation.scrollTo(Crocodoc.SCROLL_PREVIOUS);
     } else if (ev.keyCode === 39) {
     presentation.scrollTo(Crocodoc.SCROLL_NEXT);
     } else {
     return;
     }
     ev.preventDefault();
     });*/
});


