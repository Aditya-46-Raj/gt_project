import React, { useState } from "react";
import { uploadBlueprint } from "../api";

function FileUpload({ setReport, setIsLoading, setError, isLoading }) {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("No file chosen");
  const [isDragging, setIsDragging] = useState(false);

  // --- Functions to handle file state ---
  const handleFile = (selectedFile) => {
    if (selectedFile) {
      setFile(selectedFile);
      setFileName(selectedFile.name);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file before analyzing.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setReport(null);

    try {
      const reportData = await uploadBlueprint(file);
      if (reportData.error) {
        setError(reportData.error);
      } else {
        setReport(reportData);
      }
    } catch (err) {
      const errorMessage = err.response?.data?.error || "An unknown error occurred.";
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // --- Drag and Drop Event Handlers ---
  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };
  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  };

  return (
    <div className="upload-section">
      <form onSubmit={handleSubmit}>
        <label
          htmlFor="file-upload"
          className={`file-drop-zone ${isDragging ? "dragging" : ""}`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <p>Drag & drop your blueprint file here, or</p>
          <strong>Click to browse</strong>
        </label>
        
        <input id="file-upload" type="file" onChange={(e) => handleFile(e.target.files[0])} accept=".pdf,.dwg,.ifc" />
        
        <span id="file-name">{fileName}</span>
        
        <button type="submit" disabled={isLoading || !file}>
          {isLoading ? "Analyzing..." : "Analyze"}
        </button>
      </form>
    </div>
  );
}

export default FileUpload;