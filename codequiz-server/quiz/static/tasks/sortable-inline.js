// This block gets called by jQuery as soon as the DOM is ready
$(document).ready(function () {
    // hack, to only run this code in the add/change form, but not in the list view
    var $body = $("body.change-list");
    if ($body.length > 0) {
        return;
    }

    var $tbody = $("tbody");

    $tbody.attr("id", "sortable");

    var $thead = $("thead tr");
    $thead.children().first().before("<th>Order</th>");

    var $rows = $("#sortable tr.form-row");
    $rows.each(function () {
        $(this).children().first().before("<td class='handle'>++++++</td>");
    });

    $(".original").children("p").remove();

    $("#taskcollection_form").submit(function () {
        updateOrder();
        return;
    });

});

/**
 * Update all ordering values according to the visible order of the table rows, skip rows without a selected task
 */
function updateOrder() {
    $.each($("tbody tr.form-row"), function (index, value) {
        var $selection = $(this).children("td").children("select").find(":selected");
        var $orderingText = $(this).children(".field-ordering").children("input");
        if ($selection.text() != "---------") {
            $orderingText.val(index);
        }
        else {
            $orderingText.val("");
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
        handle: ".handle",
        cursor: "move",
        items: "tr:not(.add-row)",
        start: function (e, ui) {
            $(ui.placeholder).hide(300);
        },
        change: function (e, ui) {
            $(ui.placeholder).hide(300).show(300);
        },
        stop: function (e, ui) {
            //update alternating colors for the rows after releasing the dragged row
            $.each($("tbody tr.form-row"), function (index, value) {
                $(this).removeClass("row1");
                $(this).removeClass("row2");
                var cssclass = "row" + (index % 2 + 1);
                $(this).addClass(cssclass);
            });
        }
    });
});