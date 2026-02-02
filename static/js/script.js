document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultCard = document.getElementById('resultCard');
    const formCard = document.querySelector('.form-card');
    const cropNameEl = document.getElementById('cropName');
    const resetBtn = document.getElementById('resetBtn');
    const submitBtn = document.getElementById('submitBtn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        const originalBtnText = submitBtn.innerText;
        submitBtn.innerText = 'Predicting...';
        submitBtn.disabled = true;

        // Collect data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (result.success) {
                // Update specific crop prediction
                cropNameEl.innerText = result.prediction;

                // Show result with animation
                formCard.classList.add('hidden');
                resultCard.classList.remove('hidden');

                // Scroll to top
                window.scrollTo({ top: 0, behavior: 'smooth' });
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during prediction.');
        } finally {
            submitBtn.innerText = originalBtnText;
            submitBtn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        resultCard.classList.add('hidden');
        formCard.classList.remove('hidden');
        form.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
