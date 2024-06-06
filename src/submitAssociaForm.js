function submitAssociaForm(userId) {
    const piantaId = document.getElementById('pianta').value;
    const trattamentoId = document.getElementById('trattamento').value;
    const dataInizio = document.getElementById('data_inizio').value;
    const dataFine = document.getElementById('data_fine').value;

    axios.post(`/associa_pianta_trattamento/${userId}`, {
        pianta_id: piantaId,
        trattamento_id: trattamentoId,
        data_inizio: dataInizio,
        data_fine: dataFine
    })
    .then(response => {
        // Gestisci la risposta positiva
        alert('Associazione eseguita con successo!');
    })
    .catch(error => {
        // Gestisci gli errori
        console.error('Errore nell\'associazione:', error);
    });
}
