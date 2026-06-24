import { useState } from "react";

function ShowResults({ data }) {
  const [activeTab, setActiveTab] = useState("tickets");

  // if there are no data
  if (!data || !data.stories || data.stories.length === 0) {
    return <></>;
  }

  const tickets = data.stories;

  // --- Logic for the second view (Showing the subjects with according tickets) ---
  const groupedBySubject = tickets.reduce((acc, ticket) => {
    const subject = ticket.classification || "Keinem Fach zugeordnet";
    if (!acc[subject]) {
      acc[subject] = [];
    }
    acc[subject].push(ticket);
    return acc;
  }, {});

  return (
    <div style={{ maxWidth: "800px", margin: "2rem auto", fontFamily: "Inter, system-ui, sans-serif", color: "#e4e4e7" }}>
      
      {/* Tab-Navigation */}
      <div style={{ display: "flex", gap: "10px", marginBottom: "1.5rem", justifyContent: "center" }}>
        <button
          onClick={() => setActiveTab("tickets")}
          style={tabButtonStyle(activeTab === "tickets")}
        >
          🎟️ Tickets mit Fachzuordnung
        </button>
        <button
          onClick={() => setActiveTab("subjects")}
          style={tabButtonStyle(activeTab === "subjects")}
        >
          📁 Fächer mit Ticket-Liste
        </button>
      </div>

      <hr style={{ border: "0", height: "1px", background: "#333", marginBottom: "1.5rem" }} />

      {/* --- View 1: Tickets with according subjects --- */}
      {activeTab === "tickets" && (
        <div>
          <h3 style={{ color: "#ffffff", marginBottom: "1rem" }}>Ticket-Übersicht</h3>
          {tickets.map((ticket, index: number) => (
            <details 
              key={index} 
              style={cardStyle}
            >
              <summary style={summaryStyle}>
                <div style={{ display: "flex", justifyContent: "space-between", width: "100%", alignItems: "center" }}>
                  <span style={{ fontWeight: "bold", color: "#fff", fontSize: "0.95rem" }}>
                    {ticket.title || `Ticket #${index + 1}`}
                  </span>
                  <span style={badgeStyle}>{ticket.classification || "Kein Fach"}</span>
                </div>
              </summary>
              
              <div style={detailsContentStyle}>
                <p style={{ margin: "0 0 8px 0" }}><strong style={{ color: "#646cff" }}>Beschreibung:</strong> {ticket.description || "Keine Beschreibung vorhanden."}</p>
                {ticket.priority && <p style={{ margin: "4px 0" }}><strong style={{ color: "#646cff" }}>Priorität:</strong> {ticket.priority}</p>}
                {ticket.status && <p style={{ margin: "4px 0" }}><strong style={{ color: "#646cff" }}>Status:</strong> {ticket.status}</p>}
              </div>
            </details>
          ))}
        </div>
      )}

      {/* --- View 2: Subjects with acoording tickets --- */}
      {activeTab === "subjects" && (
        <div>
          <h3 style={{ color: "#ffffff", marginBottom: "1rem" }}>Fachbereiche</h3>
          {Object.keys(groupedBySubject).map((subject, idx) => (
            <div key={idx} style={{ ...cardStyle, padding: "1rem", cursor: "default" }}>
              <h4 style={{ margin: "0 0 10px 0", color: "#646cff", borderBottom: "1px solid #333", paddingBottom: "5px" }}>
                {subject} ({groupedBySubject[subject].length})
              </h4>
              <ul style={{ margin: 0, paddingLeft: "20px", color: "#d4d4d8" }}>
                {groupedBySubject[subject].map((ticket, tIdx) => (
                  <li key={tIdx} style={{ margin: "8px 0", lineHeight: "1.4" }}>
                    <strong style={{ color: "#fff" }}>{ticket.title || `Ticket #${tIdx + 1}`}</strong> 
                    {ticket.description && <span style={{ color: "#a1a1aa", fontSize: "0.9rem" }}> - {ticket.description}</span>}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

    </div>
  );
}

// --- Styles ---

const tabButtonStyle = (isActive: boolean) => ({
  padding: "10px 20px",
  cursor: "pointer",
  backgroundColor: isActive ? "#646cff" : "#1a1a1a",
  color: isActive ? "#ffffff" : "#a1a1aa",
  border: isActive ? "1px solid #747bff" : "1px solid #333",
  borderRadius: "8px",
  fontWeight: "bold",
  transition: "all 0.2s ease",
  outline: "none",
});

const cardStyle = {
  border: "1px solid #2a2a2a",
  borderRadius: "8px",
  marginBottom: "8px",
  backgroundColor: "#1a1a1a",
  boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
  overflow: "hidden"
};

const summaryStyle = {
  display: "list-item",
  padding: "0.5rem 1rem",
  cursor: "pointer",
  fontWeight: "500",
  outline: "none",
  userSelect: "none",
  backgroundColor: "#242424",
};

const detailsContentStyle = {
  padding: "1rem",
  backgroundColor: "#1e1e1e",
  borderTop: "1px solid #2a2a2a",
  fontSize: "0.95rem",
  lineHeight: "1.5",
  color: "#d4d4d8"
};

const badgeStyle = {
  backgroundColor: "rgba(100, 108, 255, 0.15)",
  color: "#a855f7", 
  border: "1px solid rgba(100, 108, 255, 0.3)",
  padding: "2px 8px",
  borderRadius: "12px",
  fontSize: "0.8rem",
  fontWeight: "bold"
};

export default ShowResults;