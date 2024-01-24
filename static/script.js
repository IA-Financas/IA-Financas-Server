function toggleDrawer() {
    var drawer = document.getElementById("drawer");
    if (drawer.style.width === "250px") {
        drawer.style.width = "0";
    } else {
        drawer.style.width = "250px";
    }
}
