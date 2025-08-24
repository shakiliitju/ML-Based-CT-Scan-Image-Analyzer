document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('uploadForm');
  const imageInput = document.getElementById('imageInput');
  const previewImage = document.getElementById('previewImage');
  const previewSection = document.getElementById('preview');
  const loadingSection = document.getElementById('loading');
  const resultsSection = document.getElementById('results');
  const analysisResults = document.getElementById('analysisResults');
  const submitButton = form.querySelector('button[type="submit"]');

  // Image preview functionality
  imageInput.addEventListener('change', () => {
    const file = imageInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = e => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
        previewSection.style.display = 'block';
      };
      reader.readAsDataURL(file);
    } else {
      previewImage.style.display = 'none';
      previewSection.style.display = 'none';
    }
  });

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!imageInput.files[0]) {
      alert('Please select an image file.');
      return;
    }

    // Show loading, hide results
    loadingSection.style.display = 'block';
    resultsSection.style.display = 'none';
    submitButton.disabled = true;
    submitButton.textContent = 'Analyzing...';

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        displayResults(data);
      } else {
        displayError(data.error || 'An error occurred while analyzing the image.');
      }
    } catch (error) {
      console.error('Error:', error);
      displayError('Network error. Please try again.');
    } finally {
      // Hide loading, restore button
      loadingSection.style.display = 'none';
      submitButton.disabled = false;
      submitButton.textContent = 'Analyze Image';
    }
  });


  function displayResults(data) {
    // Display analysis results
    if (data.analysis) {
      displayAnalysis(data.analysis);
    }

    // Display prediction result
    const predictionResult = document.getElementById('predictionResult');
    if (data.model_prediction !== undefined) {
      let predText = data.model_prediction;
      let description = '';
      if (data.class_names && data.class_names.length > 0) {
        const idx = parseInt(data.model_prediction);
        if (!isNaN(idx) && idx >= 0 && idx < data.class_names.length) {
          const cname = data.class_names[idx];
          predText = `${cname} (${data.model_prediction})`;
          if (data.class_descriptions && data.class_descriptions[cname]) {
            description = `<div class='prediction-description'>${data.class_descriptions[cname]}</div>`;
          }
        }
      }
      predictionResult.innerHTML = `<span class="prediction-value">${predText}</span>${description}`;
      document.getElementById('predictionSection').style.display = 'block';
    } else {
      predictionResult.innerHTML = '';
      document.getElementById('predictionSection').style.display = 'none';
    }

    // Show results section
    resultsSection.style.display = 'block';
  }

  function displayAnalysis(analysis) {
    let html = '';

    // Statistics
    if (analysis.mean_intensity !== undefined) {
      html += `
        <div class="analysis-stats">
          <div class="stat-card">
            <div class="stat-value">${analysis.mean_intensity.toFixed(1)}</div>
            <div class="stat-label">Mean Intensity</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">${analysis.std_intensity.toFixed(1)}</div>
            <div class="stat-label">Standard Deviation</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">${analysis.edge_count}</div>
            <div class="stat-label">Edge Structures</div>
          </div>
        </div>
      `;
    }

    // Findings
    if (analysis.findings && analysis.findings.length > 0) {
      html += '<h4>Analysis Findings:</h4>';
      html += '<ul class="findings-list">';
      
      analysis.findings.forEach(finding => {
        const isWarning = finding.includes('⚠️') || finding.includes('IMPORTANT') || finding.includes('Consult');
        const className = isWarning ? 'warning' : '';
        html += `<li class="${className}">${finding}</li>`;
      });
      
      html += '</ul>';
    }

    // Disclaimer
    if (analysis.disclaimer) {
      html += `<div class="disclaimer"><p><strong>Disclaimer:</strong> ${analysis.disclaimer}</p></div>`;
    }

    analysisResults.innerHTML = html;
  }

  function displayError(message) {
    analysisResults.innerHTML = `<div class="error"><strong>Error:</strong> ${message}</div>`;
    resultsSection.style.display = 'block';
  }
});
