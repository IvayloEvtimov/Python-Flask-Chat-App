$(document).ready(function () {
    var selected_contact = "";

    $("#search-text").keyup(function () {
        // console.log("KEY");
        $.ajax({
            url: "/search",
            method: "POST",
            data: { username: $(this).val() },
            success: function (data) {
                var obj = JSON.parse(data);
                var string = "";

                if (obj.length > 0) {
                    for (var count = 0; count < obj.length; ++count) {
                        string = string.concat("<li class='clearfix'>\n\t<img src = 'https://bootdey.com/img/Content/avatar/avatar2.png' alt = 'avatar'>\n\t<div class='about'>\n\t\t<div class='name'>" + obj[0].username + "</div>\n\t</div>\n</li>\n")
                    }
                }

                $(".chat-list").html(string);
            }
        });
    });

    $(".chat-list").on("click", function () {
        // console.log($(this).find(".name").text());
        selected_contact = $(this).find(".name").text();
        $.ajax({
            url: "/loadChat",
            method: "POST",
            data: { recipient: $(this).find(".name").text() },
            success: function (data) {
                // console.log(data);

                if (jQuery.isEmptyObject(data)) {
                    $(".chat-history").html("");
                } else {
                    var obj = JSON.parse(data);
                    var string = "";
                    $(".chat-history").html("test");
                }
            }
        });
    });

    $("#send-button").on("click", function () {
        var message = $.trim($("#message").val());
        if (message != "") {
            $.ajax({
                url: "/sendMessage",
                method: "POST",
                data: { recipient: selected_contact, message: message },
                success: function (data) {
                    console.log(data);
                }
            });
        }

        // console.log(message)
    });
});