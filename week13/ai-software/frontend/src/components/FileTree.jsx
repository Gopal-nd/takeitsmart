import React, { useState } from 'react';
import { 
  Folder, 
  FolderOpen, 
  File, 
  ChevronRight, 
  ChevronDown, 
  FileCode, 
  BookOpen, 
  Terminal, 
  Server 
} from 'lucide-react';

export default function FileTree({ steps, activeFile, onSelectFile }) {
  const [expandedFolders, setExpandedFolders] = useState({
    'root': true,
    'docs': true,
    'backend': true,
    'frontend': true,
    'tests': true,
    'deployment': true
  });

  const toggleFolder = (folderName) => {
    setExpandedFolders(prev => ({
      ...prev,
      [folderName]: !prev[folderName]
    }));
  };

  // Generate directory nodes dynamically based on step existence
  const fileNodes = [];

  if (steps.requirements) {
    fileNodes.push({ id: 'requirements', path: 'docs/requirements.md', label: 'requirements.md', folder: 'docs', type: 'doc', content: steps.requirements });
  }
  if (steps.architecture) {
    fileNodes.push({ id: 'architecture', path: 'docs/architecture.md', label: 'architecture.md', folder: 'docs', type: 'doc', content: steps.architecture });
  }
  if (steps.backend_code) {
    fileNodes.push({ id: 'backend_code', path: 'backend/main.py', label: 'main.py', folder: 'backend', type: 'code-py', content: steps.backend_code });
  }
  if (steps.review) {
    fileNodes.push({ id: 'review', path: 'backend/review.md', label: 'review.md', folder: 'backend', type: 'doc', content: steps.review });
  }
  if (steps.frontend_code) {
    fileNodes.push({ id: 'frontend_code', path: 'frontend/App.jsx', label: 'App.jsx', folder: 'frontend', type: 'code-js', content: steps.frontend_code });
  }
  if (steps.tests) {
    fileNodes.push({ id: 'tests', path: 'tests/test_main.py', label: 'test_main.py', folder: 'tests', type: 'code-py', content: steps.tests });
  }
  if (steps.deployment) {
    fileNodes.push({ id: 'deployment', path: 'deployment/deploy.md', label: 'deploy.md', folder: 'deployment', type: 'deploy', content: steps.deployment });
  }

  const renderFolder = (folderName, folderLabel, iconColor = 'text-indigo-400') => {
    const isExpanded = expandedFolders[folderName];
    const folderFiles = fileNodes.filter(file => file.folder === folderName);

    if (folderFiles.length === 0) return null; // Don't show empty folders

    return (
      <div key={folderName} className="select-none">
        {/* Folder Header */}
        <button
          onClick={() => toggleFolder(folderName)}
          className="w-full flex items-center gap-1.5 px-2.5 py-1 text-slate-600 hover:bg-slate-100 rounded transition-colors text-left"
        >
          {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          {isExpanded ? (
            <FolderOpen size={16} className={`${iconColor}`} />
          ) : (
            <Folder size={16} className={`${iconColor}`} />
          )}
          <span className="text-xs font-semibold font-mono tracking-wide">{folderLabel}</span>
        </button>

        {/* Folder Files (Sub-items) */}
        {isExpanded && (
          <div className="pl-6 border-l border-slate-200 ml-4 mt-0.5 space-y-0.5">
            {folderFiles.map(file => {
              const isSelected = activeFile === file.id;
              
              let FileIcon = File;
              let fileColor = 'text-slate-500';
              if (file.type === 'code-py') {
                FileIcon = Terminal;
                fileColor = 'text-amber-600';
              } else if (file.type === 'code-js') {
                FileIcon = FileCode;
                fileColor = 'text-cyan-600';
              } else if (file.type === 'doc') {
                FileIcon = BookOpen;
                fileColor = 'text-emerald-600';
              } else if (file.type === 'deploy') {
                FileIcon = Server;
                fileColor = 'text-purple-600';
              }

              return (
                <button
                  key={file.id}
                  onClick={() => onSelectFile(file.id, file.content, file.path)}
                  className={`w-full flex items-center gap-2 px-3 py-1 rounded transition-colors text-left font-mono text-xs ${
                    isSelected 
                      ? 'bg-indigo-50 border-r-2 border-indigo-500 text-indigo-700 font-bold' 
                      : 'hover:bg-slate-50 text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <FileIcon size={14} className={fileColor} />
                  <span>{file.label}</span>
                </button>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex flex-col">
      {/* Explorer Heading */}
      <div className="px-4 py-2.5 border-b border-slate-200 bg-slate-50">
        <span className="text-xs font-bold text-slate-700 uppercase tracking-widest font-mono">Workspace Files</span>
      </div>
      
      {/* File List */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1.5 custom-scrollbar">
        {fileNodes.length === 0 ? (
          <div className="text-[11px] text-slate-500 italic p-2 text-center leading-relaxed">
            Workspace is empty. Launch the pipeline to generate application assets!
          </div>
        ) : (
          <>
            {renderFolder('docs', 'docs/', 'text-emerald-400')}
            {renderFolder('backend', 'backend/', 'text-amber-400')}
            {renderFolder('frontend', 'frontend/', 'text-cyan-400')}
            {renderFolder('tests', 'tests/', 'text-rose-400')}
            {renderFolder('deployment', 'deployment/', 'text-purple-400')}
          </>
        )}
      </div>
    </div>
  );
}
