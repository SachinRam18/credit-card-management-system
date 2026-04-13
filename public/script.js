const API = '/api';

// Authentication Check
document.addEventListener('DOMContentLoaded', () => {
    if (!localStorage.getItem('user')) {
        window.location.href = 'login.html';
    } else {
        loadCards();
    }
});

function logout() {
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// 1. Add Card
async function addCard() {
    const name = document.getElementById('cardName').value.trim();
    const card_number = document.getElementById('cardNumber').value.trim().replace(/\s/g, '');
    const expiry = document.getElementById('cardExpiry').value.trim();
    const credit_limit = parseFloat(document.getElementById('cardLimit').value);

    if (!name || !card_number || !expiry || isNaN(credit_limit)) {
        alert('Please fill all fields correctly.');
        return;
    }

    if (card_number.length !== 16 || isNaN(card_number)) {
        alert('Card number must be exactly 16 digits.');
        return;
    }

    await fetch(`${API}/cards`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, card_number, expiry, credit_limit })
    });

    clearForm();
    loadCards();
}

// 2. Delete Card
async function deleteCard(id) {
    if (confirm('Delete this card?')) {
        await fetch(`${API}/cards/${id}`, { method: 'DELETE' });
        loadCards();
    }
}

// 3. Load and Display Cards
async function loadCards() {
    const res = await fetch(`${API}/cards`);
    const cards = await res.json();
    displayCards(cards);
    updateSummary();
}

// 4. Display Cards in DOM
function displayCards(cards) {
    const cardList = document.getElementById('cardList');
    cardList.innerHTML = '';

    if (cards.length === 0) {
        cardList.innerHTML = '<p class="empty-msg">No cards found.</p>';
        return;
    }

    cards.forEach(card => {
        const masked = '**** **** **** ' + card.card_number.slice(-4);
        const div = document.createElement('div');
        div.className = 'credit-card';
        div.innerHTML = `
            <div class="info">
                <h3>${card.name}</h3>
                <p>${masked} &nbsp;|&nbsp; Exp: ${card.expiry} &nbsp;|&nbsp; Limit: ₹${card.credit_limit.toLocaleString()}</p>
            </div>
            <div class="actions">
                <button onclick="deleteCard(${card.id})">Delete</button>
            </div>
        `;
        cardList.appendChild(div);
    });
}

// 5. Search Cards
async function searchCards() {
    const query = document.getElementById('searchInput').value.trim();
    if (query === '') {
        loadCards();
        return;
    }
    const res = await fetch(`${API}/cards/search?q=${encodeURIComponent(query)}`);
    const cards = await res.json();
    displayCards(cards);
}

// 6. Update Summary
async function updateSummary() {
    const res = await fetch(`${API}/summary`);
    const data = await res.json();
    document.getElementById('totalCards').textContent = data.total;
    document.getElementById('totalLimit').textContent = data.total_limit.toLocaleString();
}

// Helper: Clear form
function clearForm() {
    document.getElementById('cardName').value = '';
    document.getElementById('cardNumber').value = '';
    document.getElementById('cardExpiry').value = '';
    document.getElementById('cardLimit').value = '';
}

// Load handled by DOMContentLoaded
