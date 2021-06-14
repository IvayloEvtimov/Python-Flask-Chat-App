$(document).ready(function () {
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
});