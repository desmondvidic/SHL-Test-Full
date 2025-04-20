document.getElementById('queryForm').addEventListener('submit', async function (e) {
    e.preventDefault();
  
    const query = document.getElementById('queryInput').value.trim();
    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
  
    if (!query) return;
  
    loader.innerText = "Loading results (please wait 10 seconds)...";
    results.innerHTML = "";
  
    await new Promise(resolve => setTimeout(resolve, 10000)); // 10 second delay
  
    try {
      const response = await fetch(`https://shl-test-recommendation.onrender.com/api/v1/recommend?query=${encodeURIComponent(query)}`);
      const data = await response.json();
  
      if (data && data.data && data.data.recommended_assessments) {
        const recommendations = data.data.recommended_assessments;
  
        if (recommendations.length === 0) {
          results.innerHTML = "<p class='error'>No assessments found for your query.</p>";
          loader.innerText = "";
          return;
        }
  
        let tableHTML = `
          <table>
            <thead>
              <tr>
                <th>Link</th>
                <th>Description</th>
                <th>Duration</th>
                <th>Remote</th>
                <th>Adaptive</th>
                <th>Test Type</th>
              </tr>
            </thead>
            <tbody>
        `;
  
        recommendations.forEach(rec => {
          tableHTML += `
            <tr>
              <td><a class="link" href="${rec.url}" target="_blank">Open</a></td>
              <td>${rec.description}</td>
              <td>${rec.duration} min</td>
              <td>${rec.remote_support}</td>
              <td>${rec.adaptive_support}</td>
              <td>${rec.test_type.join(", ")}</td>
            </tr>
          `;
        });
  
        tableHTML += "</tbody></table>";
        results.innerHTML = tableHTML;
      } else {
        results.innerHTML = "<p class='error'>Something went wrong. Please try again.</p>";
      }
    } catch (error) {
      console.error(error);
      results.innerHTML = "<p class='error'>Failed to fetch data. Please try again later.</p>";
    }
  
    loader.innerText = "";
});
