var counter = 0;
var radioGroupCounter = 0;
var multiGroupCounter = 0;

var $ = django.jQuery;

function addInput(containerName, inputType, data) {
    var newElement = document.createElement('li');

    newElement.class = "ui-state-default";
    newElement.id = "segment" + counter;
    newElement.type = inputType;

    newElement.innerHTML += "<span class='ui-icon ui-icon-arrowthick-2-n-s'></span>";

    switch (inputType) {
        case 'text':
            var value = "";
            if (typeof data !== 'undefined' || data) {
                value = data;
            }
            newElement.innerHTML += "<textarea cols='100' rows='5' placeholder='Text...'>" + value + "</textarea>";
            break;

        case 'source':
            var value = "";
            if (typeof data !== 'undefined' || data) {
                value = data;
            }
            newElement.innerHTML += "<textarea class='src' cols='100' rows='5' placeholder='Source code...'>" + value + "</textarea>";
            break;

        case 'line':
            var text = "";
            var source = "";
            var solution = "";
            if (typeof data !== 'undefined' || data) {
                text = data["text"];
                source = data["source"];
                solution = data["solution"];
            }

            newElement.innerHTML += "<input type='text' placeholder='Description' value='" + text + "'> " +
                "<input type='text' placeholder='Source' value='" + source + "'> " +
                "<input type='text' placeholder='Answer' value='" + solution + "'>";
            break;

        case 'check':
            var statement = "";
            var question = "";
            var checked = "";
            if (typeof data !== 'undefined' || data) {
                statement = data["statement"];
                question = data["question"];
                if (data["solution"]) {
                    checked = " checked='checked'";
                }
            }

            newElement.innerHTML += "<input type='text' placeholder='Statement' value='" + statement + "'> " +
                "<input type='text' placeholder='Question' value='" + question + "'> " +
                "<input type='checkbox'" + checked + ">";
            break;

        case 'radio':
            var labels = [];
            var solution = [];
            if (typeof data !== 'undefined' || data) {
                labels = data["labels"];
                solution = data["solution"];
            }

            for (var i = 0; i < 3; i++) {
                var checked = "";
                if (i.toString() == solution) {
                    checked = " checked='checked'";
                }
                var label = "";
                if (typeof labels[i] !== 'undefined') {
                    label = labels[i];
                }
                newElement.innerHTML += "<input type='text' placeholder='Option " + (i + 1) + "' value='" + label + "'> " +
                    "<input type='radio' name='radio" + radioGroupCounter + "[]' value='" + i + "'" + checked + ">" +
                    "<br/>";
            }
            radioGroupCounter++;
            break;

        case 'multi':
            var labels = [];
            var solution = [];
            if (typeof data !== 'undefined' || data) {
                labels = data["labels"];
                solution = data["solution"];
            }

            for (var i = 0; i < 3; i++) {
                var checked = "";
                if ($.inArray(i.toString(), solution) >= 0) {
                    checked = " checked='checked'";
                }
                var label = "";
                if (typeof labels[i] !== 'undefined') {
                    label = labels[i];
                }
                newElement.innerHTML += "<input type='text' placeholder='Option " + (i + 1) + "' value='" + label + "'> " +
                    "<input type='checkbox' name='multi" + multiGroupCounter + "[]' value='" + i + "'" + checked + ">" +
                    "<br/>";
            }
            multiGroupCounter++;
            break;
    }

    newElement.innerHTML += "<a href='#' class='delete' remove='" + newElement.id + "'><i class='icon-remove-sign'></a></i>";
    $("#" + containerName).append(newElement);

    //    Hooks for dynamic behaviour, delete button
    $("a.delete").click(function (event) {
        event.preventDefault();
        removeInput($(this).attr("remove"));
    });

    $("li input").addClass("watch");
    $("li textarea").addClass("watch");

    $(".watch").change(function () {
        updateTask();
    });
    $(".watch").keyup(function () {
        updateTask();
    });

    updateTask();

    counter++;
}

function updateTask() {
    var dict = exportValues();
    $("input[name='body_xml']").val(JSON.stringify(dict, null, 4));
}

function removeInput(name) {
    $("#" + name).remove();
    updateTask();
}

function exportValues() {
    var segments = [];

    $("#sortable li").each(function (number, obj) {
        switch (obj.type) {
            case 'text':
                var $firstChild = $(this).children("textarea").first();
                segments.push({"text": $firstChild.val()});
                break;

            case 'source':
                var $firstChild = $(this).children("textarea").first();
                segments.push({"source": $firstChild.val()});
                break;

            case 'line':
                var $firstChild = $(this).children("input").first();

                segments.push(
                    {"line": {
                        "text": $firstChild.val(),
                        "source": $firstChild.next().val(),
                        "solution": $firstChild.next().next().val()
                    }}
                );
                break;

            case 'check':
                var $firstChild = $(this).children("input").first();
                segments.push(
                    {"check": {
                        "statement": $firstChild.val(),
                        "question": $firstChild.next().val(),
                        "solution": $firstChild.next().next().is(':checked')
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
                    {"multi": {
                        "labels": labels,
                        "solution": solutions
                    }}
                );
                break;

            case 'radio':
                var labels = [];
                $(this).children("input[type='text']").each(function () {
                    labels.push($(this).val());
                });

                var solution = "";
                $(this).children("input[type='radio']:checked").each(function () {
                    solution = $(this).val();
                });

                segments.push(
                    {"radio": {
                        "labels": labels,
                        "solution": solution
                    }}
                );
                break;
        }

    });
    return {segments: segments};
}

$(document).ready(function () {

    var jsonString = $("textarea.builder").val();

    $("textarea.builder")
        .replaceWith("<div style='margin-left:10em'><ul id='sortable' style='width: 80%'></ul></div>");

// Ordering is kinda strange, but makes sense. We want the <ul> to come before the links,
// and they should be ordered from Text to Update
    $("#sortable").after("<div id='builderbuttons' style='margin-top:1em'></div>");

    $("#builderbuttons")
        .append("<a class='add' href='#' type='text'>Text</a>")
        .append("<a class='add' href='#' type='source'>Source</a>")
        .append("<a class='add' href='#' type='line'>Line Entry</a>")
        .append("<a class='add' href='#' type='check'>Check</a>")
        .append("<a class='add' href='#' type='multi'>Multiple</a>")
        .append("<a class='add' href='#' type='radio'>Radio</a>")
        .append("<a class='done' href='#'>Update</a>")
        .append("<input type='hidden' name='body_xml'>");

    $("a.add").click(function (event) {
        event.preventDefault();
        addInput("sortable", $(this).attr("type"));
    });

    $("a.done").click(function (event) {
        event.preventDefault();
        updateTask();
    });

    $("input[name='body_xml']").val(jsonString);
    restoreFromJSON(JSON.parse(jsonString));
});

function restoreFromJSON(json) {
    var segments = json["segments"];

    segments.forEach(function logArrayElements(segment, index, array) {
        for (var key in segment) {
            var value = segment[key];
            addInput("sortable", key, value);
        }
    });
}


$(function () {
    $("#sortable").sortable({
        delay: 300,
        placeholder: "ui-state-highlight",
        forcePlaceholderSize: true,
        opacity: 0.5,
        start: function (e, ui) {
            $(ui.placeholder).hide(300);
        },
        change: function (e, ui) {
            $(ui.placeholder).hide().show(300);
        },
        stop: function (event, ui) {
            updateTask();
        }
    });
});