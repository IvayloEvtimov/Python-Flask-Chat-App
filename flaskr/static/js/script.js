$(document).ready(function () {
    function loadContacts() {
        $.ajax({
            url: "/loadContacts",
            method: "POST",
            success: function (data) {
                var obj = JSON.parse(data);

                var string = "";

                if (obj.length > 0) {
                    for (var count = 0; count < obj.length; ++count) {
                        console.log(obj[count])
                        string = string.concat("<li class='clearfix'>\n\t<img src = 'https://bootdey.com/img/Content/avatar/avatar2.png' alt = 'avatar'>\n\t<div class='about'>\n\t\t<div class='name'>" + obj[count] + "</div>\n\t</div>\n</li>\n")
                    }
                }

                $(".chat-list").html(string);
            }
        });
    }




    var selected_contact = "";

    loadContacts();

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
        selected_contact = $(this).find(".name").text();
        $.ajax({
            url: "/loadChat",
            method: "POST",
            data: { recipient: $(this).find(".name").text() },
            success: function (data) {
                if (jQuery.isEmptyObject(data)) {
                    $(".chat-history").html("");
                } else {
                    var obj = JSON.parse(data);
                    var string = "";

                    for (var elem in obj) {
                        var date = new Date(obj[elem]["time"] * 1000)
                        if (selected_contact == obj[elem]["sender"]) {
                            string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + obj[elem]["message"] + "</div>\n</li>\n")
                        } else {
                            string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + obj[elem]["message"] + "</div>\n</li>\n")
                        }
                    }
                    $("#chat-list").html(string);
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
                    var obj = JSON.parse(data);
                    var string = "";

                    var date = new Date(obj["time"] * 1000)

                    if (selected_contact == obj["sender"]) {
                        string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + obj["message"] + "</div>\n</li>\n")
                    } else {
                        string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + obj["message"] + "</div>\n</li>\n")
                    }

                    $("#chat-list").append(string);
                    $("#message").val("");
                }
            });
        }
    });
});