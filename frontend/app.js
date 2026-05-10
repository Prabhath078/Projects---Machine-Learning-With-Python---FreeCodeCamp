document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('predict-btn');
    const input = document.getElementById('sms-input');
    const charCount = document.getElementById('char-count');
    
    // Result elements
    const emptyState = document.getElementById('empty-state');
    const analysisResult = document.getElementById('analysis-result');
    const badge = document.getElementById('classification-badge');
    const resultIcon = document.getElementById('result-icon');
    const predictionText = document.getElementById('prediction-text');
    const confPercent = document.getElementById('confidence-percent');
    const confBar = document.getElementById('confidence-bar');

    // Update character count
    input.addEventListener('input', () => {
        const len = input.value.length;
        charCount.textContent = `${len} / 500`;
        if (len > 500) {
            charCount.style.color = 'var(--danger)';
        } else {
            charCount.style.color = 'var(--text-muted)';
        }
    });

    btn.addEventListener('click', async () => {
        const text = input.value.trim();
        if (!text) {
            alert("Please enter a message to analyze.");
            input.focus();
            return;
        }

        // Setup loading state
        const originalBtnHtml = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = `<span>Processing</span> <i data-lucide="loader" class="loading-spinner"></i>`;
        lucide.createIcons();
        
        // Hide previous result
        emptyState.style.display = 'none';
        analysisResult.classList.add('hidden');
        confBar.style.width = '0%';

        try {
            const response = await fetch('http://127.0.0.1:5000/predict/spam', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            
            if (!response.ok) throw new Error('Network response was not ok');
            
            const data = await response.json();
            
            // Add slight artificial delay to show off loading state (optional, UX touch)
            await new Promise(r => setTimeout(r, 600));

            // Populate UI
            analysisResult.classList.remove('hidden');
            
            const isSpam = data.prediction === 'spam';
            const prob = data.probability; // e.g. 0.98 or 0.12
            
            // Calculate true confidence. 
            // If model says 0.1, it's 90% confident it's HAM.
            // If model says 0.9, it's 90% confident it's SPAM.
            const confidenceValue = isSpam ? prob : (1 - prob);
            const percentage = (confidenceValue * 100).toFixed(1);

            if (isSpam) {
                badge.className = 'classification-badge is-spam';
                predictionText.textContent = 'Spam Detected';
                // Need to update the lucide icon manually in the DOM
                resultIcon.setAttribute('data-lucide', 'shield-alert');
                confBar.style.backgroundColor = 'var(--danger)';
            } else {
                badge.className = 'classification-badge is-ham';
                predictionText.textContent = 'Safe (Ham)';
                resultIcon.setAttribute('data-lucide', 'shield-check');
                confBar.style.backgroundColor = 'var(--success)';
            }
            
            lucide.createIcons(); // Re-render the new icon

            // Animate progress bar
            setTimeout(() => {
                confPercent.textContent = `${percentage}%`;
                confBar.style.width = `${percentage}%`;
            }, 100);

        } catch (error) {
            console.error(error);
            alert("Connection to the AI Engine failed. Ensure the Python backend is running.");
            emptyState.style.display = 'flex';
        } finally {
            btn.disabled = false;
            btn.innerHTML = originalBtnHtml;
            lucide.createIcons();
        }
    });
});
