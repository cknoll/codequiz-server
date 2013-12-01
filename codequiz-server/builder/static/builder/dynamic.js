// String additions
String.prototype.lines = function () {
    return this.split(/\r*\n/);
}
String.prototype.lineCount = function () {
    return this.lines().length;
}

/**
 * Add a segment to the list
 * @param {Boolean} animated Animated if true
 * @param {Object} segment The segment to append
 */
function addSegmentAnimated(animated, segment) {
    if (animated) {
        segment.hide();
        $("#sortable").append(segment);
        segment.slideDown(300);
    }
    else {
        $("#sortable").append(segment);
    }

    updateWatchdogs();
}

/**
 * Remove a segment from the list
 * @param {Boolean} animated Animated if true
 * @param {Object} segment The segment to remove
 */
function removeSegmentAnimated(animated, segment) {
    if (animated) {
        segment.slideUp(300, function () {
            segment.remove();
        });
    }
    else {
        segment.remove();
    }
}

/**
 * Adds a segment to the task definition
 *
 * This is where new types of input can be implemented for the admin interface.
 *
 * @param {String} inputType Which type of segment to add
 * @param {Object} data Data to prefill the segment with
 */
function createSegment(inputType, data) {

    // First, we create a new list item
    var segment = $("<li>", {
        type: inputType
    });

    // add the little arrow icon to the left of each segment
    segment.append("<div class='grid_1'><span class='ui-icon ui-icon-arrowthick-2-n-s handle'></span></div>");

    /**
     * Add a textarea
     * @param {String} type The kind of textarea (currently only distinguishes "text" and "comment")
     */
    function addTextArea(node, type, placeHolder, textareaData, cols, cssClass, position) {
        var content = "";
        var contentType = type;
        var rows = 1;
        var isComment;
        if (textareaData) {
            content = textareaData["content"];
            contentType = textareaData["type"];
            rows = content.lineCount();
            isComment = textareaData["comment"];
        }

        if (cols > 25) {
            rows = 5;
        }

        if (isComment) {
            node.parentsUntil("ul", "li").addClass("comment");  // all parents until but except "ul", filtered by "li"
            node.attr("type", "comment");
        }
        var $textarea = $("<textarea>", {
            cols: cols, rows: rows,
            placeholder: placeHolder,
            text: content
        });

        if (cols > 25) {
            $textarea.addClass("wide");
        }
        else {
            $textarea.addClass("no-ace");
        }

        function updateLines() {
            var rows = $(this).attr("rows");
            var lines = $(this).val().lineCount();
            if (lines != rows) {
                if ($(this).hasClass('wide')) {
                    lines = Math.max(5, lines);
                }
                $(this).attr("rows", lines);
            }
        }

        $textarea.change(function () {
            updateLines.call(this);
        });
        $textarea.keyup(function () {
            updateLines.call(this);
        });

        if (contentType == "source") {
            $textarea.addClass("source");
        }

        if (position) {
            $textarea.hide();
            node.children("select").eq(position - 1).after($textarea);
            addTypeSelection($textarea, cssClass, contentType);
            $textarea.slideDown(300);
            $textarea.next().slideDown(300);
        }
        else {
            node.append($textarea);
            addTypeSelection($textarea, cssClass, contentType);
        }
        return $textarea;
    }

    function removeTextAreaAnimated(textarea) {
        var typeSelection = textarea.next();
        typeSelection.slideUp(300);
        textarea.slideUp(300, function () {
            textarea.remove();
            typeSelection.remove();
        });
    }

    /**
     * Add a text input field and a type selection next to it
     * @param {String} key The key to retrieve data from JSON
     * @param {String} placeHolder Placeholder text for the input field
     */
    function addTextInput(node, placeHolder, inputData, position) {
        var content = "";
        var contentType = "";
        var isComment;
        var lines = 1;
        if (inputData) {
            content = inputData["content"];
            contentType = inputData["type"];
            isComment = inputData["comment"];
        }

        var $input = $("<input>", {
            type: "text",
            placeholder: placeHolder,
            value: content
        });
        if (contentType == "source") {
            $input.addClass("source");
        }
        if (isComment) {
            $input.addClass("comment");
        }
        if (position) {
            $input.hide();
            node.children("select").eq(position - 1).after($input);
            addTypeSelection($input, "inline", contentType);
            $input.show(300);
            $input.next().show(300);
        }
        else {
            node.append($input);
            addTypeSelection($input, "inline", contentType);
        }
    }

    // depending on the type of segment we want to insert, add some input fields
    switch (inputType) {
        case 'text':
            var $grid_div = $("<div class='grid_14'>");
            segment.append($grid_div);
            var $textarea = addTextArea($grid_div, inputType, "Text...", data, 100, "right");
            transformToMCE($textarea);  // make newly added textarea a tinyMCE editor
            break;

        case 'source':
            var $grid_div = $("<div class='grid_14'>");
            segment.append($grid_div);
            var $textarea = addTextArea($grid_div, inputType, "Source...", data, 100, "right");
            $textarea.addClass("source");
            setTimeout(function () {
                transformTextAreaToACE($textarea);
            }, 1); // delay of 1 msec, somehow necessary, a hack in my opinion
            break;

        case 'comment':
            var $grid_div = $("<div class='grid_14'>");
            segment.append($grid_div);
            var $textarea = addTextArea($grid_div, inputType, "Comment...", data, 100, "right");
            transformToMCE($textarea);  // make newly added textarea a tinyMCE editor
            break;

        case 'input':
        {
            var $grid_div = $("<div class='grid_4'>");
            segment.append($grid_div);

            if (data) {
                var content = data["content"];
                var count = content.length;
                for (var i = 0; i < count; i++) {
                    addTextArea($grid_div, "text", "Text", content[i], 25, "inline");
                }
            }
            else {
                addTextArea($grid_div, "text", "Text", "", 25, "inline");
            }

            $grid_div = $("<div class='grid_4'>");
            segment.append($grid_div);

            var answer = null
            var solution = null;
            if (data) {
                answer = data["answer"];
                solution = data["solution"];
            }

            addTextArea($grid_div, "text", "Answer", answer, 25, "inline");

            $grid_div = $("<div class='grid_5'>");
            segment.append($grid_div);

            if (solution) {
                var count = solution.length;
                if (solution instanceof Array) {
                    for (var i = 0; i < count; i++) {
                        addTextArea($grid_div, "text", "Solution", solution[i], 25, "inline");
                    }
                }
                else {
                    addTextArea($grid_div, "text", "Solution", solution, 25, "inline");
                }
            }
            else {
                addTextArea($grid_div, "text", "Solution", "", 25, "inline");
            }

            var $addSolutionInputButton = $('<a href="#" class="addinput">');
            $addSolutionInputButton.append('<span class="fa-stack">' +
                '<i class="fa fa-circle fa-stack-2x"></i>' +
                '<i class="fa fa-plus fa-stack-1x fa-inverse"></i>' +
                '</span></i>');
            $addSolutionInputButton.click(function (e) {
                e.preventDefault();
                var $node = $(this).parent();
                var numSolutionInputs = $node.children("textarea").length;
                addTextArea($node, "text", "Solution", "", 25, "inline", numSolutionInputs);
                updateWatchdogs();
            });

            var $removeSolutionInputButton = $('<a href="#" class="removeinput">');
            $removeSolutionInputButton.append('<span class="fa-stack">' +
                '<i class="fa fa-circle fa-stack-2x"></i>' +
                '<i class="fa fa-minus fa-stack-1x fa-inverse"></i>' +
                '</span></i>');
            $removeSolutionInputButton.click(function (e) {
                e.preventDefault();
                var $node = $(this).parent();
                removeTextAreaAnimated($node.children("textarea").last());
                updateWatchdogs();
            });
            $grid_div.append($addSolutionInputButton);
            $grid_div.append($removeSolutionInputButton);

            break;
        }

        case 'check':
            var $grid_div = $("<div class='grid_5'>");
            segment.append($grid_div);

            var solution = false;
            if (data) {
                var content = data["content"];
                var count = content.length;
                for (var i = 0; i < count; i++) {
                    addTextArea($grid_div, "text", "Text", content[i], 25, "inline");
                }
                solution = data["solution"];
            }
            else {
                addTextArea($grid_div, "text", "Text", "", 25, "inline");
            }

            $grid_div = $("<div class='grid_5'>");
            segment.append($grid_div);

            $grid_div.append("<label for='answer'>Answer</label>");
            $checkbox = $("<input>", {name: "answer", type: "checkbox"});
            if (solution) {
                $checkbox.prop({"checked": true});
            }
            $grid_div.append($checkbox);

            break;
    }

    segment.append("<div class='clear'>");

    // add the delete button to the segment
    segment.append('<a href="#" class="delete"><span class="fa-stack">' +
        '<i class="fa fa-circle fa-stack-2x"></i>' +
        '<i class="fa fa-times fa-stack-1x fa-inverse"></i>' +
        '</span></i></a>');

    return segment;
}

/**
 * Add a selection drop down list, to choose the kind of text field
 * @param node DOM object to append this to
 * @param cssclass CSS class to give the drop down ('right' or 'inline')
 * @param preSelectedType Which option to preselect
 */
function addTypeSelection(node, cssclass, preSelectedType) {
    $select = $("<select>").addClass(cssclass);

    var options = [
        {"type": "text", "text": "Normal"},
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

    if (node.css('display') == 'none') {
        $select.hide();
    }
    node.after($select);
}

/**
 * Makes sure, that all the text inputs, selects, textareas, buttons etc. have the right hooks set up
 *
 * All delete buttons should delete the segment they are in, text input should update the tasks JSON,
 * changing the selects should update the text font and style or add the code editor. Stuff like that.
 */
function updateWatchdogs() {
    $("select").change(function () {
        var $prev = $(this).prev();
        var selectedValue = $(this).find(":selected").val();
        if (selectedValue == "source") {
            $prev.addClass("source");
            if ($prev.is("textarea.source")) {
                transformFromMCE($prev);

                transformTextAreaToACE($prev);
            }
        } else if (selectedValue == "text") {
            $prev.removeClass("source");
            if ($prev.is("textarea.ace")) {
                transformACEToTextarea($prev);

                transformToMCE($prev);
            }
        }
    });

    $("a.delete").click(function (event) {
        event.preventDefault();
        removeSegmentAnimated(true, $(this).parent("li"));
    });
}

/**
 * update the hidden input field that holds the generated JSON
 */
function updateTask() {
    $.each($("textarea.wide").not(".source"), function (index, value) {
        $(this).tinymce().save();
    });

    var dict = exportValues();
    $("input[name='body_data']").val(JSON.stringify(dict));
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
            $div = li.children("div").eq(1); // the first div is for the up/down arrow, the second contains the textarea
            var $textArea = $div.children("textarea").first();

            var $typeSelect = $textArea.next();
            var isComment = li.attr("type") == "comment";
            var dict = {
                "content": $textArea.val(),
                "type": $typeSelect.val(),
            };

            // workaround for strange bug, where after switching from normal to source (ACE) the changed text isn't saved
            if ($typeSelect.val() == "source") {
                dict["content"] = $textArea.text();
            }

            if (isComment) {
                dict["comment"] = true;
            }
            segments.push(dict);
        }

        function extractInput(node) {
            var $select = node.next();
            var dict = {
                "content": node.val(),
                "type": $select.val()
            };
            return dict;
        }

        switch (obj.type) {
            case 'text':
                extractTextArea();
                break;

            case 'source':
                extractTextArea();
                break;

            case 'comment':
                extractTextArea();
                break;

            case 'input':
                var $divs = $(this).children("div");

                var content = [extractInput($divs.eq(1).children("textarea").first())];

                var $answer = $divs.eq(2).children("textarea").first();
                var answerDict = extractInput($answer);

                var $solutionTextAreas = $divs.eq(3).children("textarea");
                var solutionDicts = [];

                var count = $solutionTextAreas.length;
                for (var i = 0; i < count; i++) {
                    var solutionDict = extractInput($solutionTextAreas.eq(i));
                    solutionDicts.push(solutionDict);
                }

                segments.push({
                    "type": "input",
                    "content": content,
                    "answer": answerDict,
                    "solution": solutionDicts
                });
                break;

            case 'check':
                var $divs = $(this).children("div");

                var content = [extractInput($divs.eq(1).children("textarea").first())];

                var solution = $divs.eq(2).children("input[type='checkbox']").first().is(':checked');

                segments.push({
                    "type": "check",
                    "content": content,
                    "solution": solution
                });

                break;
        }
    })
    ;
    return {segments: segments};
}

// This block gets called by jQuery as soon as the DOM is ready
$(document).ready(function () {
    // store the JSON string from the original textarea widget (i.e. the one from the DB)
    var jsonString = $("textarea.builder").val();

    $("textarea.builder").replaceWith("<div class='container_16' id='grid_container' style='margin-left:10em'></div>");
    $("#grid_container").append("<ul id='sortable' style='width: 100%'></ul>");

    $("#sortable").after("<div class='grid_16' id='builderbuttons' style='margin-top:1em'></div>");

    $("#builderbuttons")
        .append("<a class='add' href='#' type='text'>Text</a>")
        .append("<a class='add' href='#' type='source'>Source</a>")
        .append("<a class='add' href='#' type='comment'>Comment</a>")
        .append("<a class='add' href='#' type='input'>Input Field</a>")
        .append("<a class='add' href='#' type='check'>Check</a>")
        .append("<input type='hidden' name='body_data' value='abs'>");

    $("a.add").click(function (event) {
        event.preventDefault();

        var type = $(this).attr("type");
        var data = null;
        if (type == "comment") {
            type = "text";
            data = {"comment": true, "content": "", "type": "text"}
        }

        var item = createSegment($(this).attr("type"), data);
        addSegmentAnimated(true, item);
    });

    // set the hidden input fields content to the initial JSON string
    $("input[name='body_data']").val(jsonString);

    // check if it really is a JSON string and is defined and has a length
    if (typeof jsonString !== 'undefined' && jsonString.length > 0 && jsonString.charAt(0) == "{") {
        restoreFromJSON(JSON.parse(jsonString));
    }

    $("#task_form").submit(function (event) {
        updateTask();
        return;
    });
});

/**
 * Convert textareas into ACE editors
 * @param textareas
 */
function transformTextAreaToACE(textareas) {
    var $filtered_textareas = textareas.filter(".source").not(".ace").not(".no-ace");

    $.each($filtered_textareas, function (index, value) {
        var textarea = $filtered_textareas.eq(index);
        var content = textarea.val();

        textarea.acedInitTA({theme: 'solarized_light', mode: 'python'});
        textarea.addClass("ace");
        textarea.data('ace-div').acedSession().setValue(content);
    });
}

/**
 * Remove ACE editor from a textarea
 * @param textarea
 */
function transformACEToTextarea(textarea) {
    textarea.filter(".ace").acedRemoveFromTA();
    textarea.filter(".ace").removeClass("ace");
}

function transformToMCE(textareas) {
    // the delay is a hack to make sure textarea is really added before transforming it.
    // strange that this is necessary, because it really shouldn't...
    setTimeout(function () {
        textareas.each(function () {
            $(this).attr('id', Math.random().toString());

            var editarea = $(this).attr("id");

            var ed = new tinymce.Editor(editarea, {
                inline: false,
                mode: "textareas",
                plugins: [
                    "charmap code fullscreen link lists nonbreaking paste preview searchreplace table textcolor"
                ],
                toolbar: "undo redo bold italic codebutton mathbutton charmap styleselect searchreplace bullist numlist table link fullscreen code",
                statusbar: false,
                menubar: false,
                setup: function (editor) {
                    // Add a custom button
                    editor.addButton('codebutton', {
                        title: 'Insert Code',
                        text: '<code>',
                        onclick: function () {
                            editor.undoManager.transact(function () {
                                editor.focus();
                                var selection = editor.selection;
                                var content = selection.getContent();
                                var node = selection.getNode();
                                var name = node.nodeName;

                                function stripCodeTag(node) {
                                    content = node.innerHTML;
                                    node.remove();
                                    selection.setContent(content);
                                }

                                if (content.length > 0) {
                                    if (name == "CODE") {
                                        editor.undoManager.add();
                                        stripCodeTag(node);
                                    }
                                    else {
                                        editor.undoManager.add();
                                        selection.setContent('<code>' + content + '</code>');
                                    }
                                }
                                else {
                                    if (name == "CODE") {
                                        editor.undoManager.add();
                                        stripCodeTag(node);
                                    }
                                }
                            });
                        }
                    });
                    editor.addButton('mathbutton', {
                        title: 'Insert $$',
                        text: '$...$',
                        onclick: function () {
                            editor.undoManager.transact(function () {
                                editor.focus();
                                var selection = editor.selection;
                                var content = selection.getContent();
                                var node = selection.getNode();
                                var name = node.nodeName;
                                var range = selection.getRng();

                                selection.setContent('$' + content + '$');
                                selection.setRng(range);
                            });
                        }
                    });
                }
            }, tinymce.EditorManager);
            ed.render();

            $("div.mce-tinymce").css({"display": ""}); // hack, to remove strange empty lines before and after editor
        });
    }, 1);
}

function transformFromMCE(textarea) {
    textarea.tinymce().remove();
}

/**
 * Builds up the segment list from the JSON object that describes it
 *
 * @param {Object} json JSON object (not the JSON string! i.e. use JSON.parse(jsonString)!)
 */
function restoreFromJSON(json) {
    var segments = json["segments"];

    segments.forEach(function (segment, index, array) {
        var type = segment["type"];
        var item = createSegment(type, segment);
        addSegmentAnimated(false, item);
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
        handle: ".handle",
        cursor: "move",
        start: function (e, ui) {
            var textareaID = $(ui.item).find('textarea.wide').not("source").attr('id');
            if (textareaID) {
                tinyMCE.execCommand('mceRemoveEditor', false, textareaID);
            }

            $(ui.placeholder).hide(300);
        },
        change: function (e, ui) {
            $(ui.placeholder).hide().show(300);
        },
        stop: function (e, ui) {
            var textarea = $(ui.item).find('textarea.wide').not("source").first();
            var textareaID = textarea.attr('id');
            if (textareaID) {
                var $ta = $('#' + textareaID);
                var ed = $ta.tinymce();
                var content = $ta.html();

                ed.remove();
                textarea.html(content);

                transformToMCE(textarea);
            }
        }
    });
});