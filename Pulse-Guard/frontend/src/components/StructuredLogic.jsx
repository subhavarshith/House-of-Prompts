import React from 'react';

const StructuredLogic = ({ events }) => {
  const logicEvents = events.filter(e => e.category === 'reasoning' || e.category === 'action').reverse();

  return (
    <div className="bg-slate-800 rounded-xl p-6 shadow-lg border border-slate-700 h-full overflow-hidden flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
          Structured Logic & Action
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-4">
        {logicEvents.length === 0 ? (
          <div className="text-slate-400 italic text-sm text-center mt-10">Waiting for Reasoning Agent...</div>
        ) : (
          logicEvents.map((ev, i) => {
            const isAction = ev.category === 'action';
            return (
              <div key={i} className={`rounded border p-4 text-sm ${isAction ? 'bg-red-900/20 border-red-500/50' : 'bg-slate-900 border-emerald-500/30'}`}>
                <div className="flex justify-between items-center mb-2">
                  <span className={`text-xs font-bold uppercase tracking-wider ${isAction ? 'text-red-400' : 'text-emerald-400'}`}>
                    {isAction ? 'EMS DISPATCH PAYLOAD' : 'REASONING OUTPUT'}
                  </span>
                  <span className="text-xs text-slate-500">{new Date(ev.payload.timestamp * 1000).toLocaleTimeString()}</span>
                </div>
                
                {isAction ? (
                  <pre className="text-red-200 font-mono text-xs overflow-x-auto bg-black/40 p-3 rounded">
                    {JSON.stringify(ev.payload, null, 2)}
                  </pre>
                ) : (
                  <p className="text-emerald-50 leading-relaxed font-medium">
                    {ev.payload.text || "Analyzed context and executed function."}
                  </p>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default StructuredLogic;
