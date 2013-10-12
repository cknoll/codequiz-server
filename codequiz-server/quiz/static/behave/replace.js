(function () {
    window.onload = function () {

        BehaveHooks.add(['keydown'], function (data) {
            var numLines = data.lines.total,
                fontSize = parseInt(getComputedStyle(data.editor.element)['font-size']),
                padding = parseInt(getComputedStyle(data.editor.element)['padding']);
            data.editor.element.style.height = ((numLines * fontSize) + padding) + 'px';
        });

        var editor = new Behave({

            textarea: document.getElementsByClassName("behave")[0],
            replaceTab: true,
            softTabs: true,
            tabSize: 4,
            autoOpen: true,
            overwrite: true,
            autoStrip: true,
            autoIndent: true
        });
    };
})();