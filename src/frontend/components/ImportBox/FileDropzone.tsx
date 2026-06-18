import { useDropzone } from "react-dropzone";
import { useState } from "react";

function FileDropzone() {
  const [uploading, setUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");

  const onDrop = async (file : File[]) => {
    if (file.length === 0) return;

    setUploading(true);
    setUploadStatus("Wird hochgeladen...");

    // FormData vorbereiten (wichtig für Datei-Uploads)
    const formData = new FormData();
    
    formData.append("file", file[0]);

    try {
      // Geändert von /userstories auf /import, passend zu deiner server.py
      const response = await fetch("https://backend.saviwie.com/import", {
        method: "POST",
        body: formData,
        // Content-Type bloß nicht manuell setzen, das macht der Browser bei FormData selbst!
      });

      if (response.ok) {
        const result = await response.json(); // Das 'ImportResult' Pydantic-Modell aus dem Backend
    
        console.log(result);
        //setImportedStories(result.stories); 
    
        setUploadStatus(`Upload erfolgreich! 🎉 ${result.imported} Stories importiert.`);
        console.log("Klassifizierte Stories:", result.stories);
      } else {
        setUploadStatus("Upload fehlgeschlagen. ❌");
      }
    } catch (error) {
      console.error("Fehler beim Upload:", error);
      setUploadStatus("Netzwerkfehler beim Upload. ❌");
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    onDrop, // Hier wird die Upload-Funktion eingeklinkt
    accept: {
      "text/csv": [".csv"],
      "application/json": [".json"],
      "application/xml": [".xml"],
      "text/xml": [".xml"],
    },
    multiple: false, // Auf false setzen, wenn immer nur eine Datei erlaubt sein soll
  });

  return (
    <div style={{ maxWidth: "500px", margin: "0 auto" }}>
      <div
        {...getRootProps()}
        style={{
          border: "2px dashed gray",
          padding: "2rem",
          textAlign: "center",
          borderRadius: "20px",
          cursor: "pointer",
          backgroundColor: uploading ? "#f0f0f0" : "transparent",
        }}
      >
        <input {...getInputProps()} />
        <p>Dateien hier hineinziehen oder klicken</p>
      </div>

      {/* Status-Anzeige */}
      {uploadStatus && <p style={{ textAlign: "center", fontWeight: "bold" }}>{uploadStatus}</p>}

      {/* Liste der ausgewählten Dateien */}
      <ul>
        {acceptedFiles.map((file) => (
          <li key={file.name}>
            {file.name} ({file.size} Bytes)
          </li>
        ))}
      </ul>
    </div>
  );
}

export default FileDropzone;