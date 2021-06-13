$(document).ready(function () {
    $("#search-text").keyup(function () {
        console.log("KEY");
        $.ajax({
            url: "/search",
            method: "POST",
            data: { username: $(this).val() },
            success: function (data) {
                $("#search-result").html(data);
            }
        });
    });
});