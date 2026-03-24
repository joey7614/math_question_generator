const generateBtn = document.getElementById('generate-btn');
const clearBtn    = document.getElementById('clear-btn');
const input       = document.getElementById('question-input');
const outputArea  = document.getElementById('output-area');
const loading     = document.getElementById('loading');
const errorBox    = document.getElementById('error-box');

function getCategory() {
    return document.querySelector('input[name="category"]:checked')?.value ?? 'SAT';
}

function showLoading() {
    outputArea.style.display = 'none';
    errorBox.style.display   = 'none';
    loading.style.display    = 'flex';
    generateBtn.disabled     = true;
}

function hideLoading() {
    loading.style.display = 'none';
    generateBtn.disabled  = false;
}

function showError(msg) {
    errorBox.textContent   = msg;
    errorBox.style.display = 'block';
}

function renderTopics(immediate, prerequisites) {
    const immediateEl = document.getElementById('immediate-topics');
    const prereqEl    = document.getElementById('prereq-topics');

    immediateEl.innerHTML = immediate
        .map(t => `<span class="topic-tag">${t.label}</span>`)
        .join('');

    prereqEl.innerHTML = prerequisites
        .map(t => `
            <div class="prereq-item" data-depth="${t.depth}">
                ${t.label}
            </div>`)
        .join('');
}

function renderQuestion(questionLatex) {
    const el = document.getElementById('generated-question');
    el.textContent = questionLatex;

    // Ask MathJax to re-render this element
    if (window.MathJax) {
        MathJax.typesetPromise([el]).catch(console.error);
    }
}

function renderFigure(figureUrl) {
    const container = document.getElementById('figure-container');
    const img       = document.getElementById('figure-img');

    if (figureUrl) {
        img.src = figureUrl;
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
    }
}

async function generate() {
    const question = input.value.trim();
    if (!question) {
        showError('Please enter a question first.');
        return;
    }

    showLoading();

    try {
        const res = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, category: getCategory() }),
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.error ?? 'Server error. Please try again.');
            return;
        }

        renderTopics(data.topics, data.prerequisites);
        renderQuestion(data.generated_question);
        renderFigure(data.figure_url ?? null);

        outputArea.style.display = 'block';

    } catch (err) {
        showError('Network error: ' + err.message);
    } finally {
        hideLoading();
    }
}

generateBtn.addEventListener('click', generate);

clearBtn.addEventListener('click', () => {
    input.value              = '';
    outputArea.style.display = 'none';
    errorBox.style.display   = 'none';
    input.focus();
});

// Ctrl+Enter to generate
input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) generate();
});
