document.getElementById("askBtn").addEventListener("click", async () => {
  const videoUrl = document.getElementById("videoUrl").value;
  const question = document.getElementById("question").value;
 
  
  if (!videoUrl || !question) {
    alert("Please enter both video URL and question.");
    return;
  }

  const responseBox = document.getElementById("answerBox");
  responseBox.innerHTML = "Thinking...";

  try {
    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ video_url: videoUrl, question: question })
    });

    const data = await response.json();
    responseBox.innerHTML = data.answer || `Error: ${data.error}`;
  } catch (error) {
    console.error(error);
    console.log(error.message); 
    responseBox.innerHTML = "Failed to get response.";
  }
});
