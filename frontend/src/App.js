import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import Report from "./components/Report";
import './App.css'; // Added a basic stylesheet

function App() {
  // --- CORRECTED: Added loading and error states ---
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div className="container">
      <header>
        <h1>Carbon Blueprint AI 🌳</h1>
        <p>Analyze your construction blueprints for their carbon footprint.</p>
      </header>
      <main>
        {/* Pass all state management props to the FileUpload component */}
        <FileUpload
          setReport={setReport}
          setIsLoading={setIsLoading}
          setError={setError}
          isLoading={isLoading}
        />
        {/* Display error message if one exists */}
        {error && <div className="error-message">Error: {error}</div>}

        {/* Display a loading indicator */}
        {isLoading && <div className="loading-spinner">Analyzing...</div>}

        {/* Display the report once it's available */}
        <Report report={report} />
      </main>
    </div>
  );
}

export default App;