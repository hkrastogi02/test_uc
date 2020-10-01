function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
$(document).ready(function(){
    $(".sidebar-nav").height( $(".dashboardMain").height() );
});