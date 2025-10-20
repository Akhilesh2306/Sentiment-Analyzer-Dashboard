// Text Analysis functionality
const inputText = document.getElementById("input-text")
const analyzeButton = document.getElementById("analyze")
const resultsSection = document.getElementById("resultsSection")
const analyzeOtherButton = document.getElementById("analyzeAnother")
const loadingElement = document.getElementById("loading")
const errorMessage = document.getElementById("errorMessage")

// History functionality
const historySidebar = document.getElementById("historySidebar")
const historyList = document.getElementById("historyList")
const clearHistoryBtn = document.getElementById("clearHistory")
const sidebarToggle = document.getElementById("sidebarToggle")
const closeSidebarBtn = document.getElementById("closeSidebar")

// Global variable to store analysis history
let analysisHistory = []

// Initialize history on page load
document.addEventListener("DOMContentLoaded", function () {
  loadBackendHistory()
})

// Analyze input text and display results
analyzeButton.addEventListener("click", async () => {
  try {
    const text = inputText.value.trim()
    if (text === "") {
      showError("Please enter some text to analyze.")
      return
    }

    showLoading()

    const result = await analyzeText(text)

    if (result) {
      updateResultsUI(result)

      // Reload history to include new analysis
      await loadBackendHistory()
    }
  } catch (error) {
    console.error("Error analyzing text:", error)
  } finally {
    hideLoading()
  }
})

// Analyze Other button
analyzeOtherButton.addEventListener("click", () => {
  inputText.value = ""
  resultsSection.classList.add("hidden")
  inputText.focus()
})

// Loading functionality - show/hide
function showLoading() {
  loadingElement.classList.remove("hidden")
  analyzeButton.disabled = true
}

function hideLoading() {
  loadingElement.classList.add("hidden")
  analyzeButton.disabled = false
}

// API call to backend and get analysis
async function analyzeText(text) {
  const url = "http://127.0.0.1:8000/api/v1/classify"
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  }

  try {
    const response = await fetch(url, options)

    if (!response.ok) {
      throw new Error(
        `Response error: ${response.status} ${response.statusText}`
      )
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error("Error analyzing text:", error)
  }
}

// Update UI with analysis results
function updateResultsUI(result) {
  const sentimentLabel = document.getElementById("sentimentLabel")
  const confidencePercent = document.getElementById("confidencePercent")
  const confidenceFill = document.getElementById("confidenceFill")
  const positiveScore = document.getElementById("positiveScore")
  const negativeScore = document.getElementById("negativeScore")

  // Update sentiment
  sentimentLabel.textContent = result.label
  sentimentLabel.className = "sentiment-label " + result.label.toLowerCase()

  // Update confidence
  const confidencePercentValue = Math.round(result.score * 100)
  confidencePercent.textContent = `${confidencePercentValue}%`
  confidenceFill.style.width = `${confidencePercentValue}%`

  // Update detailed scores
  if (result.label === "POSITIVE") {
    positiveScore.textContent = `${confidencePercentValue}%`
    negativeScore.textContent = `${100 - confidencePercentValue}%`
  } else {
    negativeScore.textContent = `${confidencePercentValue}%`
    positiveScore.textContent = `${100 - confidencePercentValue}%`
  }

  // Show results section
  resultsSection.classList.remove("hidden")
}

// Load history from backend
async function loadBackendHistory() {
  try {
    const response = await fetch("http://localhost:8000/api/v1/history/")

    if (!response.ok) {
      throw new Error("Failed to load backend history!")
    }

    const historyData = await response.json()
    analysisHistory = historyData.analyses
    updateHistoryDisplay(analysisHistory)
  } catch (error) {
    console.error(`Error loading history from backend ${error}`)
    historyList.innerHTML =
      '<div class="empty-history">Error loading history</div>'
  }
}

// Update history display
function updateHistoryDisplay(analyses) {
  if (!analyses || analyses.length === 0) {
    historyList.innerHTML =
      '<div class="empty-history">No analysis history yet.</div>'
    return
  }

  historyList.innerHTML = analyses
    .map(
      (item) => `
    <div class="history-item ${item.sentiment_label.toLowerCase()}" onclick="loadHistoryItem(${
        item.id
      })">
      <div class="history-text">${item.text}</div>
      <div class="history-meta">
        <span class="sentiment-indicator ${item.sentiment_label.toLowerCase()}">
          ${item.sentiment_label} - ${Math.round(item.confidence_score * 100)}%
        </span>
        <span>${formatTime(item.created_at)}</span>
      </div>
      <div class="history-actions">
        <button class="btn-small" onclick="event.stopPropagation(); loadHistoryItem(${
          item.id
        })">View</button>
        <button class="btn-small btn-delete" onclick="event.stopPropagation(); deleteHistoryItem(${
          item.id
        })">Delete</button>
      </div>
    </div>
  `
    )
    .join("")
}

// Load history item into main interface
function loadHistoryItem(id) {
  const item = analysisHistory.find((h) => h.id === id)
  if (item) {
    // Populate the input field
    inputText.value = item.text

    // Display the results using the stored data
    updateResultsUI({
      label: item.sentiment_label,
      score: item.confidence_score,
    })

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
      historySidebar.classList.remove("active")
      document.body.classList.remove("sidebar-open")
    }
  }
}

// Delete analysis from backend
async function deleteHistoryItem(id) {
  if (!confirm("Are you sure you want to delete this analysis from history?"))
    return

  try {
    const response = await fetch(`http://localhost:8000/api/v1/history/${id}`, {
      method: "DELETE",
    })

    if (!response.ok) {
      throw new Error("Failed to delete analysis from database")
    }

    const result = await response.json()

    if (result) {
      // Reload history after successful deletion
      await loadBackendHistory()
    } else {
      alert("Failed to delete analysis. Please try again.")
    }
  } catch (error) {
    console.error("Error deleting analysis:", error)
    alert("Failed to delete analysis. Please try again.")
  }
}

function showError(message) {
  // Remove any existing error first
  hideError()

  // Add error styling and message
  inputText.classList.add("error")
  errorMessage.textContent = message
  errorMessage.classList.add("show")

  // Focus on input field
  inputText.focus()

  // Auto remove error when user starts typing
  inputText.addEventListener("input", hideError, { once: true })
}

function hideError() {
  inputText.classList.remove("error")
  errorMessage.classList.remove("show")
}

// Clear all history from backend
async function clearAllHistory() {
  if (analysisHistory.length === 0) return

  if (!confirm("Are you sure you want to clear all analysis history?")) return

  try {
    // Delete each analysis individually since you don't have a bulk delete endpoint
    const deletePromises = analysisHistory.map((item) =>
      fetch(`http://localhost:8000/api/v1/history/${item.id}`, {
        method: "DELETE",
      })
    )

    await Promise.all(deletePromises)

    // Reload history (should be empty now)
    await loadBackendHistory()
  } catch (error) {
    console.error("Error clearing history:", error)
    alert("Failed to clear history. Please try again.")
  }
}

function openSidebar() {
  historySidebar.classList.toggle("active")
  document.body.classList.toggle("sidebar-open")
}

function closeSidebar() {
  historySidebar.classList.remove("active")
  document.body.classList.remove("sidebar-open")
}

// Toggle sidebar
sidebarToggle.addEventListener("click", openSidebar)
closeSidebarBtn.addEventListener("click", closeSidebar)

// Close sidebar when clicked outside
document.addEventListener("click", (event) => {
  const isClickInsideSidebar = historySidebar.contains(event.target)
  const isClickOnToggle = sidebarToggle.contains(event.target)

  if (
    !isClickInsideSidebar &&
    !isClickOnToggle &&
    historySidebar.classList.contains("active")
  ) {
    closeSidebar()
  }
})

// Clear history
clearHistoryBtn.addEventListener("click", clearAllHistory)

// Format timestamp
function formatTime(timestamp) {
  try {
    const date = new Date(timestamp)
    const now = new Date()

    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    const diffHours = Math.floor(diffMs / 3600000)
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))

    if (diffMins < 1) return "Just now"
    if (diffMins < 60) return `${diffMins}m ago`
    if (diffHours < 24) return `${diffHours}h ago`
    if (diffDays < 7) return `${diffDays}d ago`

    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    })
  } catch (error) {
    console.error("Error formatting timestamp:", error)
    return "Recent"
  }
}
