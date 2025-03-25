document.getElementById('payment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const accessKey = document.getElementById('access-key').value;
    
    // IMPORTANT: Replace with your actual access key
    const CORRECT_KEY = 'your_secret_access_key_here';
    
    if (accessKey === CORRECT_KEY) {
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('data-section').style.display = 'block';
        
        // Load CSV data
        fetch('data/analysis.csv')
            .then(response => response.text())
            .then(data => {
                const csvDisplay = document.getElementById('csv-display');
                csvDisplay.innerHTML = formatCSV(data);
            });
    } else {
        alert('Incorrect Access Key');
    }
});

function formatCSV(csvText) {
    const rows = csvText.split('\n').map(row => 
        `<div>${row.split(',').join(' | ')}</div>`
    ).join('');
    
    return `<div class="csv-content">${rows}</div>`;
}