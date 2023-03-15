

$.getJSON("/?user=true", "", (data) => {
    console.log("fffff")
    console.log($(".manager"))
    if(data.user === "representative") {
        $('.representative').removeClass("disabled");
    } else if(data.user === "manager") {
        $('.manager').removeClass("disabled");
    }
    else {
        $('.table_link').removeClass("disabled");
    }
})

