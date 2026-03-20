import React, { useEffect, useState } from 'react';
import MessyInput from './components/MessyInput';
import StructuredLogic from './components/StructuredLogic';

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    // Poll for events every second
    const interval = setInterval(async () => {
      try {
        const res = await fetch('/api/events');
        if (res.ok) {
          const data = await res.json();
          setEvents(data.events);
        }
      } catch (e) {
        console.error("Failed to fetch events", e);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const simulateTelemetry = async () => {
    await fetch('/api/telemetry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ heart_rate: 135, motion: 0 })
    });
  };

  const simulateAudio = async () => {
    const formData = new FormData();
    const blob = new Blob(["fake audio content"], { type: 'audio/wav' });
    formData.append("file", blob, "distress_call.wav");
    await fetch('/api/upload-audio', {
      method: 'POST',
      body: formData
    });
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-50 p-6 md:p-10 font-sans">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
            Pulse-Guard
          </h1>
          <p className="text-slate-400 mt-2 font-medium">Multimodal Emergency Response Bridge</p>
        </div>
        <div className="flex gap-4">
          <button onClick={simulateTelemetry} className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm font-bold shadow">
            Simulate Critical Telemetry
          </button>
          <button onClick={simulateAudio} className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded text-sm font-bold shadow">
            Simulate Distress Audio
          </button>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[75vh]">
        <MessyInput events={events} />
        <StructuredLogic events={events} />
      </div>
    </div>
  );
}

export default App;
