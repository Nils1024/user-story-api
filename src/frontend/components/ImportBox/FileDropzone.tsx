import { useDropzone } from "react-dropzone";

function FileDropzone() {
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({
    accept: {
      "text/csv": [".csv"],
      "application/json": [".json"],
      "application/xml": [".xml"],
      "text/xml": [".xml"],
    },
  });

  return (
    <div
      {...getRootProps()}
      style={{
        border: "2px dashed gray",
        padding: "2rem",
        textAlign: "center",
        borderRadius: "20px",
      }}
    >
      <input {...getInputProps()} />
      <p>Dateien hier hineinziehen oder klicken</p>

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