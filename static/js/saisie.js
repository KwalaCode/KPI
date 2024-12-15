document.getElementById('kpi-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/saisie', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Données enregistrées avec succès');
            this.reset();
        } else {
            alert('Erreur lors de l\'enregistrement des données');
        }
    });
});

document.getElementById('import-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/import', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Données importées avec succès');
            this.reset();
        } else {
            alert('Erreur lors de l\'importation des données: ' + data.error);
        }
    });
});

