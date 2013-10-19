var counter = 0;
var radioGroupCounter = 0;
var multiGroupCounter = 0;

function addInput(containerName, inputType) {
    var newElement = document.createElement('li');

    newElement.class = "ui-state-default";
    newElement.id = "segment" + counter;
    newElement.type = inputType;

    newElement.innerHTML += "<span class='ui-icon ui-icon-arrowthick-2-n-s'></span>";

    switch (inputType) {
        case 'text':
            newElement.innerHTML += "<textarea cols='100' rows='5' name='myInputs[]' placeholder='Text...'/>";
            break;

        case 'src':
            newElement.innerHTML += "<textarea class='src' name='myInputs[]' cols='100' rows='5' placeholder='Source code...'/>";
            break;

        case 'line':
            newElement.innerHTML += "<input type='text' placeholder='Description'> " +
                "<input type='text' placeholder='Source'> " +
                "<input type='text' placeholder='Answer'>";
            break;

        case 'check':
            newElement.innerHTML += "<input type='text' placeholder='Description'> " +
                "<input type='text' placeholder='Source'> " +
                "<input type='checkbox' name='myInputs[]'>";
            break;

        case 'radio':
            var labels = [];
            for (var i = 0; i < 3; i++) {
                newElement.innerHTML += "<input type='text' placeholder='Option " + (i + 1) + "'> " +
                    "<input type='radio' name='myInputs" + radioGroupCounter + "[]' value='" + i + "'>" +
                    "<br/>";
                labels.push("");
            }
            radioGroupCounter++;
            break;

        case 'multi':
            for (var i = 0; i < 3; i++) {
                newElement.innerHTML += "<input type='text' placeholder='Option " + (i + 1) + "'> " +
                    "<input type='checkbox' name='myInputs" + multiGroupCounter + "[]' value='" + i + "'>" +
                    "<br/>";
            }
            multiGroupCounter++;
            break;
    }

    newElement.innerHTML += "<a href='#' class='delete' remove='" + newElement.id + "'><i class='icon-remove-sign'></a></i>";
    $("a.delete").click(function (event) {
        event.preventDefault();
        removeInput($(this).attr("remove"));
    });

    document.getElementById(containerName).appendChild(newElement);

    counter++;
}

function removeInput(name) {
    $("#" + name).remove();
}

function exportValues() {
    var segments = [];

    $("#sortable li").each(function (number, obj) {
        switch (obj.type) {
            case 'text':
                var $firstChild = $(this).children("textarea").first();
                segments.push({text: $firstChild.val()});
                break;

            case 'src':
                var $firstChild = $(this).children("textarea").first();
                segments.push({source: $firstChild.val()});
                break;

            case 'line':
                var $firstChild = $(this).children("input").first();

                segments.push(
                    {line: {
                        text: $firstChild.val(),
                        source: $firstChild.next().val(),
                        solution: $firstChild.next().next().val()
                    }}
                );
                break;

            case 'check':
                var $firstChild = $(this).children("input").first();
                segments.push(
                    {check: {
                        statement: $firstChild.val(),
                        question: $firstChild.next().val(),
                        solution: $firstChild.next().next().is(':checked')
                    }}
                );
                break;

            case 'multi':
                var labels = [];
                $(this).children("input[type='text']").each(function () {
                    labels.push($(this).val());
                });

                var solutions = [];
                $(this).children("input[type='checkbox']:checked").each(function () {
                    solutions.push($(this).val());
                });

                segments.push(
                    {multi: {
                        labels: labels,
                        solution: solutions
                    }}
                );
                break;

            case 'radio':
                var labels = [];
                $(this).children("input[type='text']").each(function () {
                    labels.push($(this).val());
                });

                var solution = None;
                $(this).children("input[type='radio']:checked").each(function () {
                    solution = $(this).val();
                });

                segments.push(
                    {radio: {
                        labels: labels,
                        solution: solution
                    }}
                );
                break;
        }

    });
    return {segments: segments};
}

function logDict() {
    console.log(dict);
}