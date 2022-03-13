$(document).ready(function () {
    function loadContacts() {
        $.ajax({
            url: "/loadContacts",
            method: "POST",
            success: function (data) {
                var obj = JSON.parse(data);

                var string = "";

                if (obj.length > 0 && (loaded_contacts == 0 || loaded_contacts < obj.length)) {
                    for (var count = 0; count < obj.length; ++count) {
                        // console.log(obj[count])
                        string = string.concat("<li class='clearfix'>\n\t<img src = " + window.location.href.slice(0, -1) + obj[count]["avatar"] + " alt = 'avatar' id='" + obj[count]["username"] + "-avatar'>\n\t<div class='about'>\n\t\t<div class='name'>" + obj[count]["username"] + "</div>\n\t</div>\n</li>\n")
                    }
                    loaded_contacts = obj.length
                    $(".chat-list").html(string);
                }
            }
        });
    }

    function loadChat(obj) {
        var string = "";

        for (var elem in obj) {
            var date = new Date(obj[elem]["time"] * 1000)


            if (obj[elem]["type"] == "img") {
                var img_link = "<img src='" + window.location.href.slice(0, -1) + obj[elem]["url"] + "' alt='image' style='height:240px; width:240px'>"

                if (selected_contact == obj[elem]["sender"]) {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + img_link + "</div>\n</li>\n")
                } else {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + img_link + "</div>\n</li>\n")
                }
            } else if (obj[elem]["type"] == "vid") {
                var vid_link = "<video width='320' height='240' controls>\n\t<source src='" + obj[elem]["url"] + "'></video>"

                if (selected_contact == obj[elem]["sender"]) {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + vid_link + "</div>\n</li>\n")
                } else {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + vid_link + "</div>\n</li>\n")
                }
            } else {
                if (selected_contact == obj[elem]["sender"]) {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + obj[elem]["message"] + "</div>\n</li>\n")
                } else {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + obj[elem]["message"] + "</div>\n</li>\n")
                }
            }
        }

        return string;
    }


    var selected_contact = "";
    var loaded_messages = 0;
    var loaded_contacts = 0;

    loadContacts();

    setInterval(function () {
        if (selected_contact != "") {
            $.ajax({
                url: "/syncChat",
                method: "POST",
                data: { recipient: selected_contact, loaded_messages: loaded_messages },
                success: function (data) {
                    var obj = JSON.parse(data);

                    if (obj.length > 0) {
                        loaded_messages += obj.length
                        string = loadChat(obj);
                        $("#chat-list").append(string);
                    }

                }
            });
        }
    }, 1000);

    setInterval(function () {
        loadContacts();
    }, 1000);

    $("#search-text").keyup(function () {
        $.ajax({
            url: "/search",
            method: "POST",
            data: { username: $(this).val() },
            success: function (data) {
                var obj = JSON.parse(data);
                var string = "";

                if (obj.length > 0) {
                    for (var count = 0; count < obj.length; ++count) {
                        string = string.concat("<li class='clearfix'>\n\t<img src = '" + window.location.href.slice(0, -1) + obj[count]["avatar"] + "' alt = 'avatar' id='" + obj[count]["username"] + "-avatar'>\n\t<div class='about'>\n\t\t<div class='name'>" + obj[0].username + "</div>\n\t</div>\n</li>\n")
                    }
                }

                $(".chat-list").html(string);
            }
        });
    });

    $(".chat-list").on("click", function () {
        selected_contact = $(this).find(".name").text();
        selected_avatar = $(this).find("#" + selected_contact + "-avatar").attr("src");
        $.ajax({
            url: "/loadChat",
            method: "POST",
            data: { recipient: $(this).find(".name").text() },
            success: function (data) {
                if (jQuery.isEmptyObject(data)) {
                    $(".chat-history").html("");
                } else {
                    var obj = JSON.parse(data);
                    loaded_messages = obj.length

                    var string = loadChat(obj);

                    var user_info = "<img src='" + selected_avatar + "' alt='avatar'>\n<div class='chat-about' >\n\t<h6 class='m-b-0'>" + selected_contact + "</h6>\t</div>";
                    $("#talking_user").html(user_info);
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

                    loaded_messages += 1;
                    $("#chat-list").append(string);
                    $("#message").val("");
                }
            });
        }
    });


    $("#img-button").on("click", function () {
        $("#img-file").trigger("click");
    });

    $("#img-file").on("change", function () {
        var file_data = $('#img-file').prop('files')[0];
        var form_data = new FormData();

        form_data.append('file', file_data);
        form_data.append('recipient', selected_contact);

        $.ajax({
            url: "/sendImage",
            dataType: 'text',
            cache: false,
            contentType: false,
            processData: false,
            method: "POST",
            data: form_data,
            success: function (data) {
                var obj = JSON.parse(data);
                var string = "";

                var date = new Date(obj["time"] * 1000);
                var base_url = window.location.href.slice(0, -1);
                var img_link = "<img src='" + base_url + obj["url"] + "' alt='image' style='height:240px; width:240px'>"

                if (selected_contact == obj["sender"]) {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + img_link + "</div>\n</li>\n")
                } else {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + img_link + "</div>\n</li>\n")
                }

                loaded_messages += 1;
                $("#chat-list").append(string);
            }
        });
    });

    $("#vid-button").on("click", function () {
        $("#vid-file").trigger("click");
    });

    $("#vid-file").on("change", function () {
        var file_data = $("#vid-file").prop("files")[0];
        var form_data = new FormData();

        form_data.append("file", file_data);
        form_data.append("recipient", selected_contact);

        $.ajax({
            url: "/sendVideo",
            dataType: "text",
            cache: false,
            contentType: false,
            processData: false,
            method: "POST",
            data: form_data,
            success: function (data) {
                var obj = JSON.parse(data);
                var string = "";

                var date = new Date(obj["time"] * 1000);
                var vid_link = "<video width='320' height='240' controls>\n\t<source src='" + obj["url"] + "'></video>"

                if (selected_contact == obj["sender"]) {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message my-message'>" + vid_link + "</div>\n</li>\n")
                } else {
                    string = string.concat("<li class='clearfix'>\n\t<div class='message-data text-right'>\n\t\t<span class='message-data-time'>" + date.toLocaleString() + "</span>\n\t</div>\n\t<div class='message other-message float-right'>" + vid_link + "</div>\n</li>\n")
                }

                loaded_messages += 1;
                $("#chat-list").append(string);
            }
        });
    });

});