var counter = 0;

var $ = django.jQuery;  // bind Djangos jQuery to the shortcut "$", or else not much will work

/**
 * Add a selection drop down list, to choose the kind of text field
 * @param node DOM object to append this to
 * @param cssclass CSS class to give the drop down ('right' or 'inline')
 * @param preSelectedType Which option to preselect
 */
function addTypeSelection(node, cssclass, preSelectedType) {
    $select = $("<select>").addClass(cssclass);

    var options = [
        {"type": "normal", "text": "Normal"},
        {"type": "source", "text": "Source"}
    ];

    var count = options.length;

    for (var i = 0; i < count; i++) {
        var option = options[i];

        $option = $("<option>", {value: option["type"], text: option["text"]});
        if (preSelectedType == option["type"]) {
            $option.prop({"selected": true});
        }
        $select.append($option);
    }

    node.append($select);
}

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

    /**
     * Add a textarea
     * @param {String} type The kind of textarea (currently only distinguishes "text" and "hint")
     */
    function addTextArea(type) {
        var content = "";
        var contentType = "";
        if (typeof data !== 'undefined' || data) {
            content = data["content"];
            contentType = data["type"];
        }

        var placeHolder = "";
        switch (type) {
            case 'text':
                placeHolder = "Text...";
                break;
            case 'hint':
                placeHolder = "Hint...";
                item.addClass("hint");
                break;
        }
        $textarea = $("<textarea>", {
            cols: "100", rows: "5",
            placeholder: placeHolder,
            text: content
        });
        if (contentType == "source") {
            $textarea.addClass("source");
        }
        item.append($textarea);
        addTypeSelection(item, "right", contentType);
    }

    /**
     * Add a text input field and a type selection next to it
     * @param {String} key The key to retrieve data from JSON
     * @param {String} placeHolder Placeholder text for the input field
     */
    function addTextInput(key, placeHolder) {
        var content = "";
        var contentType = "";
        if (typeof data !== 'undefined' || data) {
            content = data[key]["content"];
            contentType = data[key]["type"];
        }

        $input = $("<input>", {
            type: "text",
            placeholder: placeHolder,
            value: content
        });
        if (contentType == "source") {
            $input.addClass("source");
        }
        item.append($input);
        addTypeSelection(item, "inline", contentType);
    }

    // depending on the type of segment we want to insert, add some input fields
    // there's quite some type/null/undefined checking going on, unfortunately,
    // to cleanly support both cases (new segments and loaded segments)
    switch (inputType) {
        case 'text':
            addTextArea(inputType);
            break;

        case 'hint':
            addTextArea(inputType);
            break;

        case 'line':
            addTextInput("first", "First");
            addTextInput("second", "Second");
            addTextInput("solution", "Answer");
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

            addTextInput("first", "First");
            addTextInput("second", "Second");
            item.append("<label for='answer'>Answer</label><input name='answer' type='checkbox'" + checked + ">");
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
    $("li select").addClass("watch");

    $(".watch").change(function () {
        updateTask();
    });
    $(".watch").keyup(function () {
        updateTask();
    });

    $("select").change(function () {
        var selectedValue = $(this).find(":selected").val();
        if (selectedValue == "source") {
            $(this).prev().addClass("source");
        } else if (selectedValue == "normal") {
            $(this).prev().removeClass("source");
        }
    })

    // update after inserting a new segment
    updateTask();

    counter++;
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
 * @returns {{segments: Array}}
 */
function exportValues() {
    var segments = [];

    $("#sortable li").each(function (number, obj) {
        var li = $(this);

        /**
         * Extracts a text area type of input, whose key will be the type of the <li> its contained in
         */
        function extractTextArea() {
            var $firstChild = li.children("textarea").first();
            var $typeSelect = $firstChild.next();
            var textAreaType = li.attr("type");
            var dict = {};
            dict[textAreaType] = {
                "content": $firstChild.val(),
                "type": $typeSelect.val()
            };
            segments.push(dict);
        }

        switch (obj.type) {
            case 'text':
                extractTextArea();
                break;

            case 'hint':
                extractTextArea();
                break;

            case 'line':
                var $inputs = $(this).children("input");
                var $selects = $(this).children("select");

                segments.push({"line": {
                    "first": {
                        "content": $inputs.eq(0).val(),
                        "type": $selects.eq(0).val()
                    },
                    "second": {
                        "content": $inputs.eq(1).val(),
                        "type": $selects.eq(1).val()
                    },
                    "solution": {
                        "content": $inputs.eq(2).val(),
                        "type": $selects.eq(2).val()
                    }
                }});
                break;

            case 'check':
                var $inputs = $(this).children("input");
                var $selects = $(this).children("select");

                segments.push({"check": {
                    "first": {
                        "content": $inputs.eq(0).val(),
                        "type": $selects.eq(0).val()
                    },
                    "second": {
                        "content": $inputs.eq(1).val(),
                        "type": $selects.eq(1).val()
                    },
                    "solution": $inputs.eq(2).is(':checked')
                }});
                break;
        }
    });
    return {segments: segments};
}

// This block gets called by jQuery as soon as the DOM is ready
$(document).ready(function () {
    // store the JSON string from the original textarea widget (i.e. the one from the DB)
    var jsonString = $("textarea.builder").val();

    $("textarea.builder").replaceWith("<div style='margin-left:10em'><ul id='sortable' style='width: 100%'></ul></div>");

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