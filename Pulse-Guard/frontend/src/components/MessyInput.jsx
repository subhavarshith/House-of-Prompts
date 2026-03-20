import React from 'react';

const MessyInput = ({ events }) => {
  const inputEvents = events.filter(e => e.category === 'input').reverse();

  return (
    <div className="bg-slate-800 rounded-xl p-6 shadow-lg border border-slate-700 h-full overflow-hidden flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></span>
          Messy Stream (Raw IoT/Audio)
        </h2>
      </div>
      
      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {inputEvents.length === 0 ? (
          <div className="text-slate-400 italic text-sm text-center mt-10">Waiting for incoming telemetry...</div>
        ) : (
          inputEvents.map((ev, i) => (
            <div key={i} className="bg-slate-900 rounded border border-slate-700 p-3 text-sm">
              <div className="flex justify-between items-center mb-2">
                <span className="text-xs font-semibold text-blue-400 uppercase tracking-wider">{ev.payload.type}</span>
                <span className="text-xs text-slate-500">{new Date(ev.payload.timestamp * 1000).toLocaleTimeString()}</span>
              </div>
              <pre className="text-slate-300 font-mono text-xs overflow-x-auto">
                {JSON.stringify(ev.payload.data || {file: ev.payload.filename}, null, 2)}
              </pre>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default MessyInput;
