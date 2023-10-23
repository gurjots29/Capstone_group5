<<<<<<< HEAD
$(function () {
    populateSearchDataSource(desktopExamples);

    $("#example-search").kendoExampleSearch({
        product: product,
        minLength: 3,
        template: '<a href="#: path + url #"> #: text # </a>',
        dataTextField: "text",
        select: function (e) {
            location.href = e.item.find("a").attr("href");
        },
        height: 300
    });

    $("#example-sidebar").kendoResponsivePanel({
        breakpoint: 1200,
        orientation: "left",
        toggleButton: "#sidebar-toggle"
    });

    $("#sidebar-toggle").click(function() {
        $("#example-search").focus();
    });
});
=======
$(function () {
    populateSearchDataSource(desktopExamples);

    $("#example-search").kendoExampleSearch({
        product: product,
        minLength: 3,
        template: '<a href="#: path + url #"> #: text # </a>',
        dataTextField: "text",
        select: function (e) {
            location.href = e.item.find("a").attr("href");
        },
        height: 300
    });

    $("#example-sidebar").kendoResponsivePanel({
        breakpoint: 1200,
        orientation: "left",
        toggleButton: "#sidebar-toggle"
    });

    $("#sidebar-toggle").click(function() {
        $("#example-search").focus();
    });
});
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
