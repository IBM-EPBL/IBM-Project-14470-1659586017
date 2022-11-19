const TOAST_ME = document.getElementById("toast-me");

TOAST_ME.addEventListener("click", () => {

    Toastinette.init({
            position: 'top-center',
            title: 'Attention',
            message: 'Un utilisateur est déjà connecté avec ce compte.',
            type: 'warning',
            autoClose: false,
            progress: true
    });
    
});
