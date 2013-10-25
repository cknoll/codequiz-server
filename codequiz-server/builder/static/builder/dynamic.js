var counter = 0;

var $ = django.jQuery;  // bind Djangos jQuery to the shortcut "$", or else not much will work

/**
 * Adds a segment to the task definition
 *
 * This is where new types of input can be implemented for the admin interface.
 *
 * @param {String} containerName Which element to add this to (id name)
 * @param {String} inputType Which type of segment to add
 * @param {Object} data Data to prefill the segment with
 */
function addInput(containerName, inputType, data) {

    // First, we create a new list item
    var newElement = document.createElement('li');
    newElement.class = "ui-state-default";
    newElement.id = "segment" + counter;
    newElement.type = inputType;

    // we add it to the container that goes by the id in 'containername' and store it as a jQuery variable
    $("#" + containerName).append(newElement);
    var item = $("#" + newElement.id);

    // add the little arrow icon to the left of each segment
    item.append("<span class='ui-icon ui-icon-arrowthick-2-n-s'></span>");

    // depending on the type of segment we want to insert, add some input fields
    // there's quite some type/null/undefined checking going on, unfortunately,
    // to cleanly support both cases (new segments and loaded segments)
    switch (inputType) {
        case 'text':
            var value = "";
            if (typeof data !== 'undefined' || data) {
                value = data;
            }
            item.append("<textarea cols='100' rows='5' placeholder='Text...'>" + value + "</textarea>");
            addTypeSelection(item, "right");
            break;

        case 'hint':
            var value = "";
            if (typeof data !== 'undefined' || data) {
                value = data;
            }
            item.append("<textarea cols='100' rows='5' placeholder='Hint...'>" + value + "</textarea>");
            addTypeSelection(item, "right");
            item.addClass("hint");
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

            item.append("<input type='text' placeholder='Statement' value='" + text + "'>");
            addTypeSelection(item, "inline");
            item.append("<input type='text' placeholder='Question' value='" + source + "'>");
            addTypeSelection(item, "inline");
            item.append("<input type='text' placeholder='Answer' value='" + solution + "'>");
            addTypeSelection(item);
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

            item.append("<input type='text' placeholder='Statement' value='" + statement + "'>");
            addTypeSelection(item, "inline");
            item.append("<input type='text' placeholder='Question' value='" + question + "'>");
            addTypeSelection(item, "inline");
            item.append("<input type='checkbox'" + checked + ">");
            break;
    }

    // add the delete button to the segment
    item.append("<a href='#' class='delete' remove='" + newElement.id + "'><i class='icon-remove-sign'></a></i>");

    // add hooks for delete button
    $("a.delete").click(function (event) {
        event.preventDefault();
        removeInput($(this).attr("remove"));
    });

    // mark input and textarea fields for automatic updating of hidden input field that stores the JSON
    $("li input").addClass("watch");
    $("li textarea").addClass("watch");

    $(".watch").change(function () {
        updateTask();
    });
    $(".watch").keyup(function () {
        updateTask();
    });

    $("select").change(function() {
        var selectedValue = $(this).find(":selected").val();
        if (selectedValue == "source") {
            $(this).prev().addClass("source");
        }
        else if (selectedValue == "normal") {
            $(this).prev().removeClass("source");
        }
    })

    // update after inserting a new segment
    updateTask();

    counter++;
}

function addTypeSelection(node, cssclass) {
    node.append("<select class='" + cssclass + "'><option value='normal'>Normal</option><option value='source'>Source</option></select>");
}

/**
 * update the hidden input field that holds the generated JSON
 */
function updateTask() {
    var dict = exportValues();
    $("input[name='body_xml']").val(JSON.stringify(dict, null, 4));
}

/**
 * Remove a segment from the task
 * @param {String} name Which segment to remove
 */
function removeInput(name) {
    $("#" + name).remove();
    updateTask();
}


/**
 * Walks over all the segments and builds a dictionary/JSON object
 *
 * @returns {{segments: Array}}
 */
function exportValues() {
    var segments = [];

    $("#sortable li").each(function (number, obj) {
        switch (obj.type) {
            case 'text':
                var $firstChild = $(this).children("textarea").first();
                segments.push({"text": $firstChild.val()});
                break;

            case 'hint':
                var $firstChild = $(this).children("textarea").first();
                segments.push({"hint": $firstChild.val()});
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
        }

    });
    return {segments: segments};
}

// This block gets called by jQuery as soon as the DOM is ready
$(document).ready(function () {
    // store the JSON string from the original textarea widget (i.e. the one from the DB)
    var jsonString = $("textarea.builder").val();

    $("textarea.builder")
        .replaceWith("<div style='margin-left:10em'><ul id='sortable' style='width: 100%'></ul></div>");

    $("#sortable").after("<div id='builderbuttons' style='margin-top:1em'></div>");

    $("#builderbuttons")
        .append("<a class='add' href='#' type='text'>Text</a>")
        .append("<a class='add' href='#' type='hint'>Hint</a>")
        .append("<a class='add' href='#' type='line'>Line Entry</a>")
        .append("<a class='add' href='#' type='check'>Check</a>")
        .append("<input type='hidden' name='body_xml'>");

    $("a.add").click(function (event) {
        event.preventDefault();
        // call addInput() with the type that is in the "type" attribute of the <a> element
        addInput("sortable", $(this).attr("type"));
    });

    // set the hidden input fields content to the initial JSON string
    $("input[name='body_xml']").val(jsonString);

    // check if it really is a JSON string and is defined and has a length
    if (typeof jsonString !== 'undefined' && jsonString.length > 0 && jsonString.charAt(0) == "{") {
        restoreFromJSON(JSON.parse(jsonString));
    }
});

/**
 * Builds up the segment list from the JSON object that describes it
 *
 * @param {Object} json JSON object (not the JSON string! i.e. use JSON.parse(jsonString)!)
 */
function restoreFromJSON(json) {
    var segments = json["segments"];

    segments.forEach(function logArrayElements(segment, index, array) {
        for (var key in segment) {
            var value = segment[key];
            addInput("sortable", key, value);
        }
    });
}


// set some options and event hooks for jQuery Sortable to get a few animations and to update the hidden input for the JSON
// (this gets called automatically, when the script loads)
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