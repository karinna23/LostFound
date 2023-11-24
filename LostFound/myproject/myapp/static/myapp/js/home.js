document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const main = document.getElementById('main');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    
    sidebarCollapse.addEventListener('click', function () {
        sidebar.classList.toggle('active');
        main.classList.toggle('active');
        
    });
});
