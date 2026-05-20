import React from 'react';
import { 
  FileText, 
  Layers, 
  Terminal, 
  Monitor, 
  CheckCircle, 
  HelpCircle, 
  Server, 
  GitBranch, 
  Search 
} from 'lucide-react';

const STEPS = [
  { id: 'requirements', label: 'Product Manager', icon: FileText, desc: 'Generates requirements' },
  { id: 'architecture', label: 'Architect', icon: Layers, desc: 'Designs high-level architecture' },
  { id: 'backend_code', label: 'Backend Dev', icon: Terminal, desc: 'Generates FastAPI code' },
  { id: 'review', label: 'Code Reviewer', icon: Search, desc: 'Audits & fixes code logic' },
  { id: 'frontend_code', label: 'Frontend Dev', icon: Monitor, desc: 'Generates React layout' },
  { id: 'tests', label: 'QA Tester', icon: HelpCircle, desc: 'Writes unit tests' },
  { id: 'deployment', label: 'DevOps Engineer', icon: Server, desc: 'Creates Docker setups' }
];

export default function PipelineVisualizer({ currentStep, activeStepState, completedSteps }) {
  return (
    <div className="w-full bg-white border border-slate-200 rounded-2xl p-6 shadow-sm transition-all">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-bold text-slate-900 tracking-wide">AI Agent Pipeline Status</h3>
          <p className="text-xs text-slate-500">Watch specialized agents collaborate in real-time</p>
        </div>
        <span className="text-xs font-semibold px-2.5 py-1 bg-indigo-50 border border-indigo-200 text-indigo-600 rounded-full animate-pulse">
          Agent Network Active
        </span>
      </div>

      <div className="relative flex flex-col md:flex-row items-center justify-between gap-6 md:gap-2">
        {/* Connection Line Behind Nodes (Desktop only) */}
        <div className="absolute top-[32px] left-[5%] right-[5%] h-0.5 bg-slate-100 hidden md:block z-0" />

        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isCompleted = completedSteps.includes(step.id);
          const isCurrent = currentStep === step.id;
          const isRunning = isCurrent && activeStepState === 'running';

          let statusClass = 'border-slate-200 text-slate-400 bg-slate-50';
          let borderGlow = '';

          if (isCompleted) {
            statusClass = 'border-emerald-200 text-emerald-600 bg-emerald-50 shadow-sm';
          } else if (isCurrent) {
            statusClass = 'border-cyan-400 text-cyan-600 bg-cyan-50';
            if (isRunning) {
              borderGlow = 'animate-pulse-glow';
            }
          }

          return (
            <div key={step.id} className="flex flex-col items-center text-center z-10 w-full md:w-32 group">
              {/* Node Icon Circle */}
              <div className={`relative w-16 h-16 rounded-full flex items-center justify-center border-2 transition-all duration-300 ${statusClass} ${borderGlow}`}>
                <Icon size={24} className={isRunning ? 'animate-bounce' : ''} />
                
                {/* Completed Badge overlay */}
                {isCompleted && (
                  <div className="absolute -top-1 -right-1 bg-emerald-500 text-white rounded-full p-0.5 border-2 border-white">
                    <CheckCircle size={12} className="fill-current text-white" />
                  </div>
                )}

                {/* Pulsing indicator */}
                {isRunning && (
                  <span className="absolute -top-1 -right-1 flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-cyan-500"></span>
                  </span>
                )}
              </div>

              {/* Node Metadata Labels */}
              <div className="mt-3">
                <p className={`text-sm font-bold tracking-tight transition-colors duration-200 ${
                  isCurrent ? 'text-cyan-600' : isCompleted ? 'text-emerald-600' : 'text-slate-500'
                }`}>
                  {step.label}
                </p>
                <p className="text-[10px] text-slate-400 mt-0.5 leading-tight group-hover:text-slate-600 transition-colors">
                  {step.desc}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
