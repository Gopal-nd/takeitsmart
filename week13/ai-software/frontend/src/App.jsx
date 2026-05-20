import React, { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { 
  Plus, 
  Trash2, 
  Download, 
  Save, 
  Play, 
  Terminal, 
  AlertCircle, 
  FileText, 
  Check, 
  Cpu, 
  Sliders, 
  ExternalLink 
} from 'lucide-react';
import PipelineVisualizer from './components/PipelineVisualizer';
import TerminalConsole from './components/TerminalConsole';
import FileTree from './components/FileTree';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

const STEP_ORDER = [
  'requirements',
  'architecture',
  'backend_code',
  'review',
  'frontend_code',
  'tests',
  'deployment'
];

const STEP_LABELS = {
  'requirements': 'Product Manager',
  'architecture': 'Architect',
  'backend_code': 'Backend Dev',
  'review': 'Code Reviewer',
  'frontend_code': 'Frontend Dev',
  'tests': 'QA Tester',
  'deployment': 'DevOps Engineer'
};

const getEditorLanguage = (filename) => {
  if (!filename) return 'plaintext';
  if (filename === 'backend_code' || filename === 'tests') return 'python';
  if (filename === 'frontend_code') return 'javascript';
  if (filename === 'requirements' || filename === 'architecture' || filename === 'deployment') return 'markdown';
  return 'plaintext';
};

export default function App() {
  // Projects State
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  
  // Editor State
  const [activeFile, setActiveFile] = useState(null);
  const [activeFilePath, setActiveFilePath] = useState('');
  const [editorContent, setEditorContent] = useState('');
  const [editorOriginal, setEditorOriginal] = useState('');
  const [isSavingEditor, setIsSavingEditor] = useState(false);

  // Pipeline execution State
  const [currentRunningStep, setCurrentRunningStep] = useState(null);
  const [stepState, setStepState] = useState('idle'); // idle, running, completed
  const [logs, setLogs] = useState([]);

  // Modals & Forms State
  const [isCreating, setIsCreating] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectIdea, setNewProjectIdea] = useState('');
  
  // Global LLM Settings
  const [modelId, setModelId] = useState('meta.llama3-8b-instruct-v1:0');
  const [temperature, setTemperature] = useState(0.2);
  const [showSettings, setShowSettings] = useState(false);

  // Sandbox State
  const [sandboxRunning, setSandboxRunning] = useState(false);
  const [sandboxUrl, setSandboxUrl] = useState('');
  const [sandboxDocsUrl, setSandboxDocsUrl] = useState('');
  const [sandboxLoading, setSandboxLoading] = useState(false);
  const [showSandbox, setShowSandbox] = useState(false);
  const [sandboxTab, setSandboxTab] = useState('frontend');
  const [isSandboxMode, setIsSandboxMode] = useState(false);

  // Fetch projects on load & check sandbox parameter
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const sandboxId = urlParams.get('sandbox');
    if (sandboxId) {
      setIsSandboxMode(true);
      bootStandaloneSandbox(sandboxId);
    } else {
      fetchProjects();
    }
  }, []);

  const bootStandaloneSandbox = async (id) => {
    setSandboxLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/projects/${id}`);
      setSelectedProject(response.data);
      
      const runResponse = await axios.post(`${API_BASE}/projects/${id}/run`);
      setSandboxUrl(runResponse.data.url);
      setSandboxDocsUrl(runResponse.data.docs_url);
      setSandboxRunning(true);
    } catch (error) {
      console.error('Failed to boot standalone sandbox:', error);
    } finally {
      setSandboxLoading(false);
    }
  };

  const addLog = (tag, text, color = 'text-cyan-400') => {
    setLogs(prev => [...prev, { tag, text, color }]);
  };

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API_BASE}/projects`);
      setProjects(response.data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
      addLog('SYSTEM', 'Failed to connect to backend server. Make sure FastAPI app is running on port 8000.', 'text-rose-400');
    }
  };

  const selectProject = async (id) => {
    try {
      const response = await axios.get(`${API_BASE}/projects/${id}`);
      const project = response.data;
      setSelectedProject(project);
      setIsCreating(false);
      setLogs([]);
      
      addLog('SYSTEM', `Loaded project "${project.name}" successfully.`, 'text-emerald-400');
      
      // Auto open first generated file
      const availableSteps = Object.keys(project.steps || {});
      if (availableSteps.length > 0) {
        // Open the latest step by order
        const latestStep = STEP_ORDER.find(step => availableSteps.includes(step)) || availableSteps[0];
        const stepPath = getStepPath(latestStep);
        setActiveFile(latestStep);
        setActiveFilePath(stepPath);
        setEditorContent(project.steps[latestStep] || '');
        setEditorOriginal(project.steps[latestStep] || '');
      } else {
        setActiveFile(null);
        setActiveFilePath('');
        setEditorContent('');
        setEditorOriginal('');
        addLog('SYSTEM', 'Workspace is empty. Launch the Product Manager step to begin generation.', 'text-amber-400');
      }
    } catch (error) {
      console.error('Failed to load project details:', error);
      addLog('ERROR', `Failed to load project ID ${id}`, 'text-rose-400');
    }
  };

  const getStepPath = (step) => {
    switch(step) {
      case 'requirements': return 'docs/requirements.md';
      case 'architecture': return 'docs/architecture.md';
      case 'backend_code': return 'backend/main.py';
      case 'review': return 'backend/review.md';
      case 'frontend_code': return 'frontend/App.jsx';
      case 'tests': return 'tests/test_main.py';
      case 'deployment': return 'deployment/deploy.md';
      default: return 'file.txt';
    }
  };

  const createNewProject = async (e) => {
    e.preventDefault();
    if (!newProjectName.trim() || !newProjectIdea.trim()) return;

    try {
      const response = await axios.post(`${API_BASE}/projects`, {
        name: newProjectName,
        idea: newProjectIdea,
        model_id: modelId,
        temperature: parseFloat(temperature)
      });
      
      setNewProjectName('');
      setNewProjectIdea('');
      setIsCreating(false);
      
      await fetchProjects();
      await selectProject(response.data.id);
      
      addLog('SUCCESS', `Project initialized! Let's start by clicking "Generate Requirements" to boot up your Product Manager Agent.`, 'text-emerald-400');
    } catch (error) {
      console.error('Failed to create project:', error);
      addLog('ERROR', 'Failed to create new project.', 'text-rose-400');
    }
  };

  const deleteProject = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to delete this project? All steps and database entries will be erased.')) return;

    try {
      await axios.delete(`${API_BASE}/projects/${id}`);
      addLog('SYSTEM', 'Project deleted.', 'text-amber-400');
      if (selectedProject?.id === id) {
        setSelectedProject(null);
        setActiveFile(null);
        setEditorContent('');
      }
      fetchProjects();
    } catch (error) {
      console.error('Failed to delete project:', error);
      addLog('ERROR', 'Failed to delete project.', 'text-rose-400');
    }
  };

  const runSandbox = async () => {
    if (!selectedProject) return;
    setSandboxLoading(true);
    addLog('SYSTEM', 'Spinning up isolated sandbox runtime on port 8080...', 'text-indigo-400');
    try {
      const response = await axios.post(`${API_BASE}/projects/${selectedProject.id}/run`);
      setSandboxUrl(response.data.url);
      setSandboxDocsUrl(response.data.docs_url);
      setSandboxRunning(true);
      addLog('SYSTEM', `Sandbox active! Access API docs at: ${response.data.docs_url}`, 'text-emerald-400');
      
      // Open the interactive multi-tab sandbox workspace page in a new browser tab!
      window.open(`/?sandbox=${selectedProject.id}`, '_blank');
      addLog('SYSTEM', 'Opened full interactive sandbox dashboard in a new browser tab.', 'text-emerald-600');
    } catch (error) {
      console.error('Failed to start sandbox:', error);
      addLog('SYSTEM', `Failed to start sandbox: ${error.response?.data?.detail || error.message}`, 'text-rose-400');
      setSandboxRunning(false);
    } finally {
      setSandboxLoading(false);
    }
  };

  const stopSandbox = async () => {
    if (!selectedProject) return;
    setSandboxLoading(true);
    addLog('SYSTEM', 'Shutting down sandbox environment...', 'text-slate-500');
    try {
      await axios.post(`${API_BASE}/projects/${selectedProject.id}/stop`);
      setSandboxRunning(false);
      setSandboxUrl('');
      setSandboxDocsUrl('');
      addLog('SYSTEM', 'Sandbox stopped cleanly.', 'text-amber-400');
    } catch (error) {
      console.error('Failed to stop sandbox:', error);
    } finally {
      setSandboxLoading(false);
    }
  };

  const generateFrontendSrcDoc = () => {
    if (!selectedProject) return '';
    
    // Get frontend code
    const rawCode = selectedProject.steps?.frontend_code || '';
    if (!rawCode) return '<html><body style="background:#0f172a;color:#64748b;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;"><div style="text-align:center;"><h3>No frontend code generated yet.</h3><p style="font-size:12px;color:#475569;">Complete the Frontend Developer agent step to enable preview.</p></div></body></html>';
    
    // Extract default export component name before stripping exports safely
    let componentName = 'App';
    const funcMatch = rawCode.match(/export\s+default\s+function\s+(\w+)/);
    if (funcMatch) {
      componentName = funcMatch[1];
    } else {
      const classMatch = rawCode.match(/export\s+default\s+class\s+(\w+)/);
      if (classMatch) {
        componentName = classMatch[1];
      } else {
        const varMatch = rawCode.match(/export\s+default\s+(\w+)/);
        if (varMatch && varMatch[1] !== 'function' && varMatch[1] !== 'class') {
          componentName = varMatch[1];
        }
      }
    }

    // Clean and rewrite code
    let cleanedCode = rawCode;
    // Extract block
    if (cleanedCode.includes('```')) {
      const parts = cleanedCode.split('```');
      const jsBlock = parts.find(p => p.startsWith('jsx') || p.startsWith('javascript') || p.startsWith('js') || p.startsWith('react'));
      if (jsBlock) {
        const lines = jsBlock.split('\n');
        cleanedCode = lines.slice(1).join('\n');
      } else {
        const codePart = parts.find(p => p.includes('function') || p.includes('class') || p.includes('import'));
        cleanedCode = codePart || parts[1] || cleanedCode;
      }
    }
    
    // Strip imports (both ES6 block imports and single-line file imports)
    cleanedCode = cleanedCode.replace(/import\s+[\s\S]*?from\s+['"].*?['"];?/g, '');
    cleanedCode = cleanedCode.replace(/import\s+['"].*?['"];?/g, '');

    // Strip exports (export default statements and inline export qualifiers)
    cleanedCode = cleanedCode.replace(/export\s+default\s+/g, '');
    cleanedCode = cleanedCode.replace(/\bexport\s+/g, '');
    
    // Rewrite port 8000 -> 8080 (our background sandbox backend)
    cleanedCode = cleanedCode.replace(/http:\/\/localhost:8000/g, 'http://localhost:8080');
    cleanedCode = cleanedCode.replace(/http:\/\/127.0.0.1:8000/g, 'http://localhost:8080');
    
    // Construct self-contained HTML page
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Application Sandbox Preview</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Load Lucide Icons CDN -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {
      background-color: #0f172a;
      color: #f8fafc;
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
  </style>
</head>
<body class="p-6">
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect, useRef } = React;
    
    // Sleek React Error Boundary to capture runtime exceptions in user-generated frontend code
    class ErrorBoundary extends React.Component {
      constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
      }
      static getDerivedStateFromError(error) {
        return { hasError: true, error };
      }
      componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught an error", error, errorInfo);
      }
      render() {
        if (this.state.hasError) {
          return (
            <div style={{
              backgroundColor: '#1e1b4b',
              color: '#fda4af',
              padding: '24px',
              fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
              borderRadius: '16px',
              border: '1px solid #f43f5e',
              boxShadow: '0 10px 25px -5px rgba(0,0,0,0.3)',
              maxWidth: '650px',
              margin: '40px auto'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                <span style={{ fontSize: '20px' }}>🐞</span>
                <h3 style={{ margin: 0, fontSize: '15px', fontWeight: 'bold', color: '#fff' }}>Frontend Code Exception Blocked</h3>
              </div>
              <div style={{
                background: '#020617',
                color: '#f8fafc',
                padding: '16px',
                borderRadius: '8px',
                fontSize: '11px',
                overflowX: 'auto',
                marginBottom: '16px',
                border: '1px solid #1e293b'
              }}>
                <strong>Exception caught:</strong> {this.state.error.message}
              </div>
              <div style={{ color: '#94a3b8', fontSize: '11px', lineHeight: '1.6' }}>
                <p style={{ margin: '0 0 6px 0', fontWeight: 'bold', color: '#cbd5e1' }}>💡 Debugging Tips:</p>
                <p style={{ margin: '0 0 6px 0' }}>The generated component crashed because of a minor javascript runtime issue (e.g. attempting to call standard methods on null/undefined properties like <code>toLocaleDateString()</code> or reading properties from uninitialized objects).</p>
                <p style={{ margin: 0 }}>You can easily resolve this by opening <strong>frontend/App.jsx</strong> in your main workspace behind this overlay and adjusting the offending line!</p>
              </div>
            </div>
          );
        }
        return this.props.children;
      }
    }

    ${cleanedCode}

    // Auto-render default exported component or fallback App
    try {
      const root = ReactDOM.createRoot(document.getElementById('root'));
      if (typeof ${componentName} !== 'undefined') {
        root.render(<ErrorBoundary><${componentName} /></ErrorBoundary>);
      } else if (typeof App !== 'undefined') {
        root.render(<ErrorBoundary><App /></ErrorBoundary>);
      } else {
        document.getElementById('root').innerHTML = '<div style="text-align:center;padding:50px;color:#f43f5e;"><h3>Could not locate App component</h3><p style="font-size:12px;color:#94a3b8;">Ensure your frontend code declares a default App() component.</p></div>';
      }
    } catch(e) {
      console.error(e);
      document.getElementById('root').innerHTML = '<div style="text-align:center;padding:50px;color:#f43f5e;"><h3>Compilation Error</h3><pre style="text-align:left;background:#1e293b;padding:15px;border-radius:10px;font-size:11px;overflow-x:auto;color:#f8fafc;">' + e.message + '</pre></div>';
    }
  </script>
</body>
</html>`;
  };

  const saveEditorContent = async () => {
    if (!selectedProject || !activeFile) return;
    setIsSavingEditor(true);
    try {
      await axios.put(`${API_BASE}/projects/${selectedProject.id}/step/${activeFile}`, {
        content: editorContent
      });
      setEditorOriginal(editorContent);
      
      // Update selected project local steps state
      setSelectedProject(prev => ({
        ...prev,
        steps: {
          ...prev.steps,
          [activeFile]: editorContent
        }
      }));

      addLog('SUCCESS', `Saved modifications to [${getStepPath(activeFile)}] successfully.`, 'text-emerald-400');
    } catch (error) {
      console.error('Failed to save file:', error);
      addLog('ERROR', 'Failed to save modifications to file.', 'text-rose-400');
    } finally {
      setIsSavingEditor(false);
    }
  };

  const runStepPipeline = (stepName) => {
    if (!selectedProject) return;

    setCurrentRunningStep(stepName);
    setStepState('running');
    setLogs([]);
    setActiveFile(stepName);
    setActiveFilePath(getStepPath(stepName));
    setEditorContent('');

    const agentRole = STEP_LABELS[stepName];
    addLog('AGENT', `${agentRole} agent initiated...`, 'text-cyan-400');
    addLog('SYSTEM', `Opening server-sent event channel for real-time code generation...`, 'text-slate-500');

    let fullOutput = '';
    
    // Set up SSE Event Listener
    const sseUrl = `${API_BASE}/projects/${selectedProject.id}/stream/${stepName}`;
    const eventSource = new EventSource(sseUrl);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.token) {
          fullOutput += data.token;
          setEditorContent(fullOutput);
        } else if (data.error) {
          addLog('ERROR', data.error, 'text-rose-400');
          eventSource.close();
          setStepState('idle');
          setCurrentRunningStep(null);
        }
      } catch (err) {
        console.error('Failed to parse SSE chunk:', err);
      }
    };

    eventSource.onerror = async (err) => {
      console.log('SSE Stream finished or disconnected.');
      eventSource.close();
      
      setStepState('completed');
      setCurrentRunningStep(null);
      
      addLog('SUCCESS', `${agentRole} completed output delivery successfully!`, 'text-emerald-400');
      
      // Reload project state to fetch newly generated step
      try {
        const res = await axios.get(`${API_BASE}/projects/${selectedProject.id}`);
        setSelectedProject(res.data);
        setEditorOriginal(fullOutput);
        fetchProjects(); // Update project status on sidebar list
      } catch (e) {
        console.error('Failed to reload project after step complete:', e);
      }
    };
  };

  const downloadZip = () => {
    if (!selectedProject) return;
    addLog('SYSTEM', 'Creating in-memory ZIP package of project workspace...', 'text-cyan-400');
    window.location.href = `${API_BASE}/projects/${selectedProject.id}/export`;
  };

  // Get next step in pipeline
  const getNextAvailableStep = () => {
    if (!selectedProject) return null;
    const completed = Object.keys(selectedProject.steps || {});
    return STEP_ORDER.find(step => !completed.includes(step));
  };

  const getCompletedSteps = () => {
    if (!selectedProject) return [];
    return Object.keys(selectedProject.steps || {});
  };

  const hasUnsavedChanges = editorContent !== editorOriginal;

  if (isSandboxMode) {
    return (
      <div className="w-screen h-screen bg-[#F8FAFC] flex flex-col overflow-hidden text-slate-700">
        
        {/* Browser Header Bar */}
        <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between shrink-0 shadow-sm">
          <div className="flex items-center gap-3">
            {/* Traffic lights */}
            <div className="flex gap-1.5 mr-2">
              <div 
                className="w-3 h-3 rounded-full bg-rose-500 hover:bg-rose-600 cursor-pointer" 
                onClick={async () => { 
                  if (selectedProject) {
                    await stopSandbox();
                  }
                  window.close(); 
                }}
              ></div>
              <div className="w-3 h-3 rounded-full bg-amber-500"></div>
              <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
            </div>
            <div className="h-4 w-[1px] bg-slate-200 mx-1"></div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
              <span className="text-[11px] font-bold text-slate-700 uppercase tracking-widest font-mono">Sandbox Environment Dashboard</span>
            </div>
          </div>

          {/* URL Address Bar Mockup */}
          <div className="hidden md:flex items-center bg-slate-50 border border-slate-200 rounded-xl px-4 py-1.5 w-1/2 text-xs font-mono text-slate-500 shadow-inner">
            <span className="text-slate-400 mr-1.5 select-none">https://</span>
            <span className="text-cyan-600 select-all">{sandboxDocsUrl ? 'localhost:8080/docs' : 'initializing...'}</span>
          </div>

          <div className="flex items-center gap-3">
            {selectedProject && sandboxRunning && (
              <div className="flex items-center gap-2">
                <a
                  href={`${API_BASE}/projects/${selectedProject.id}/preview`}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 py-1.5 px-3.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
                >
                  Open App Tab ↗
                </a>
                <a
                  href={sandboxDocsUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-1.5 py-1.5 px-3.5 bg-slate-100 hover:bg-slate-200 text-slate-655 hover:text-slate-900 rounded-lg text-xs font-semibold border border-slate-200 transition-colors"
                >
                  Swagger Tab ↗
                </a>
              </div>
            )}
            <button
              onClick={async () => { 
                if (selectedProject) {
                  await stopSandbox();
                }
                window.close(); 
              }}
              className="py-1.5 px-3.5 bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-200 rounded-lg text-xs font-semibold transition-colors"
            >
              Stop & Close Dashboard
            </button>
          </div>
        </div>

        {/* Sandbox Workspace Body */}
        <div className="flex-1 bg-[#F8FAFC] relative overflow-hidden flex flex-col">
          {sandboxLoading ? (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-50/80 z-20">
              <div className="w-12 h-12 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 animate-spin mb-4"></div>
              <p className="text-xs font-semibold text-slate-600 font-mono">Initializing isolated subprocess daemon...</p>
              <p className="text-[10px] text-slate-400 font-mono mt-1">Acquiring port 8080</p>
            </div>
          ) : sandboxRunning && selectedProject ? (
            <div className="w-full h-full flex flex-col md:flex-row">
              
              {/* Left Sidebar: Instructions and Status */}
              <div className="w-full md:w-80 bg-white border-r border-slate-200 p-6 overflow-y-auto custom-scrollbar shrink-0 flex flex-col justify-between shadow-sm">
                <div className="space-y-5">
                  <div>
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest font-mono">Interactive Sandbox</h4>
                    <h3 className="text-sm font-bold text-slate-900 mt-1">{selectedProject.name}</h3>
                  </div>

                  {/* Dynamic Tab Switcher */}
                  <div className="flex bg-slate-50 p-1 rounded-xl border border-slate-200 gap-1 select-none">
                    <button
                      onClick={() => setSandboxTab('frontend')}
                      className={`flex-1 py-2 px-2 rounded-lg text-[9px] font-bold tracking-wider uppercase transition-all duration-200 ${
                        sandboxTab === 'frontend'
                          ? 'bg-indigo-650 text-white shadow-sm font-bold'
                          : 'text-slate-500 hover:text-slate-950 hover:bg-slate-200/50'
                      }`}
                    >
                      🖥️ Frontend Preview
                    </button>
                    <button
                      onClick={() => setSandboxTab('backend')}
                      className={`flex-1 py-2 px-2 rounded-lg text-[9px] font-bold tracking-wider uppercase transition-all duration-200 ${
                        sandboxTab === 'backend'
                          ? 'bg-indigo-650 text-white shadow-sm font-bold'
                          : 'text-slate-500 hover:text-slate-950 hover:bg-slate-200/50'
                      }`}
                    >
                      ⚙️ Swagger API Docs
                    </button>
                  </div>
                  
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3 shadow-inner">
                    <div className="flex justify-between items-center text-[10px] font-mono">
                      <span className="text-slate-550">Backend Daemon</span>
                      <span className="text-emerald-600 font-bold">ONLINE</span>
                    </div>
                    <div className="flex justify-between items-center text-[10px] font-mono">
                      <span className="text-slate-550">Listening Port</span>
                      <span className="text-cyan-700 font-bold">8080</span>
                    </div>
                    <div className="flex justify-between items-center text-[10px] font-mono">
                      <span className="text-slate-550">Active Tab</span>
                      <span className="text-indigo-600 uppercase font-bold">{sandboxTab}</span>
                    </div>
                  </div>

                  <div className="text-[11px] leading-relaxed text-slate-655 space-y-3">
                    {sandboxTab === 'frontend' ? (
                      <>
                        <p>💡 **Interactive Client App:**</p>
                        <p className="text-slate-500 pl-1">
                          This is your generated frontend React UI compiled dynamically in the browser! Any actions, inputs, or forms you execute here make **real REST calls** directly to your background sandbox backend server on port 8080!
                        </p>
                      </>
                    ) : (
                      <>
                        <p>💡 **How to Test Your API:**</p>
                        <ul className="list-disc list-inside space-y-1.5 text-slate-550 pl-1">
                          <li>Click on any endpoint (like <code className="text-indigo-600 font-bold">GET</code> or <code className="text-emerald-650 font-bold font-semibold font-mono">POST</code>) in the right panel.</li>
                          <li>Click the <strong className="text-slate-700">"Try it out"</strong> button on the top right.</li>
                          <li>Enter mock parameters and click the green <strong className="text-emerald-650 font-bold">"Execute"</strong> button to test live!</li>
                        </ul>
                      </>
                    )}
                  </div>
                </div>

                <div className="pt-6 border-t border-slate-200 text-[10px] text-slate-400 font-mono">
                  <span>Refreshes dynamically on workspace code updates</span>
                </div>
              </div>

              {/* Right side: Conditional Iframe rendering based on sandboxTab */}
              <div className="flex-1 h-full bg-white relative">
                {sandboxTab === 'frontend' ? (
                  <iframe
                    srcDoc={generateFrontendSrcDoc()}
                    className="w-full h-full border-none bg-white"
                    title="React Dynamic Sandbox Frontend"
                  />
                ) : (
                  <iframe
                    src={sandboxDocsUrl}
                    className="w-full h-full border-none bg-white"
                    title="FastAPI Interactive Docs Sandbox"
                  />
                )}
              </div>

            </div>
          ) : (
            <div className="absolute inset-0 flex flex-col items-center justify-center gap-3">
              <p className="text-xs text-slate-400 font-mono">Sandbox is currently offline.</p>
              <button
                onClick={() => selectedProject && bootStandaloneSandbox(selectedProject.id)}
                className="py-1.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition-colors"
              >
                Boot Sandbox App
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-screen bg-[#F8FAFC] overflow-hidden text-slate-700">
      
      {/* SIDEBAR: Project History */}
      <aside className="w-80 border-r border-slate-200 bg-white flex flex-col h-full z-10 shrink-0 shadow-sm">
        
        {/* Sidebar Header Title */}
        <div className="p-6 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-glow-indigo/20">
              <Cpu size={20} className="text-white animate-pulse" />
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-900 tracking-wide">AI Software Team</h1>
              <p className="text-[10px] text-slate-500 font-medium">Industry-Grade Agent Platform</p>
            </div>
          </div>
        </div>

        {/* Action Button: Create New */}
        <div className="p-4">
          <button
            onClick={() => {
              setIsCreating(true);
              setSelectedProject(null);
            }}
            className="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-500 hover:from-indigo-500 hover:to-cyan-400 text-white font-semibold text-xs flex items-center justify-center gap-2 shadow-glow-indigo/15 hover:shadow-glow-indigo/25 hover:scale-[1.01] active:scale-[0.99] transition-all"
          >
            <Plus size={16} /> New Software Project
          </button>
        </div>

        {/* Project List */}
        <div className="flex-1 overflow-y-auto px-3 space-y-1.5 custom-scrollbar">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest pl-2 mb-2 block">Project History</span>
          {projects.length === 0 ? (
            <div className="text-xs text-slate-600 text-center py-8 italic">
              No projects built yet.
            </div>
          ) : (
            projects.map(p => {
              const isSelected = selectedProject?.id === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => selectProject(p.id)}
                  className={`group relative flex items-center justify-between px-4 py-3 rounded-xl cursor-pointer border transition-all ${
                    isSelected 
                      ? 'bg-indigo-50 border-indigo-200 text-indigo-900 shadow-sm' 
                      : 'border-transparent hover:bg-slate-100/70 text-slate-600 hover:text-slate-950'
                  }`}
                >
                  <div className="flex items-center gap-3 overflow-hidden pr-6">
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center border text-xs shrink-0 ${
                      isSelected ? 'bg-indigo-100/80 border-indigo-200 text-indigo-600' : 'bg-slate-100 border-slate-200 text-slate-500'
                    }`}>
                      {p.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="overflow-hidden">
                      <p className="text-xs font-bold truncate tracking-wide leading-tight">{p.name}</p>
                      <p className="text-[10px] text-slate-500 font-mono mt-0.5 capitalize truncate">{p.status.replace('_', ' ')}</p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => deleteProject(p.id, e)}
                    className="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-all z-20 shrink-0"
                  >
                    <Trash2 size={13} />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Footer evaluation badge */}
        <div className="p-4 border-t border-slate-100 bg-slate-50">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-600 shrink-0">
              ✓
            </div>
            <div>
              <p className="text-[11px] font-bold text-slate-700 leading-tight">Internship Core AI Showcase</p>
              <p className="text-[9px] text-slate-500 font-semibold font-mono">Status: Production Ready</p>
            </div>
          </div>
        </div>

      </aside>

      {/* MAIN CONTAINER */}
      <main className="flex-1 flex flex-col h-full bg-[#F8FAFC] overflow-hidden relative z-0">
        
        {/* Header Bar */}
        <header className="h-16 border-b border-slate-200 bg-white px-8 flex items-center justify-between shrink-0 shadow-sm">
          <div>
            {selectedProject ? (
              <div className="flex items-center gap-3">
                <h2 className="text-sm font-bold text-slate-900 tracking-wide">{selectedProject.name}</h2>
                <span className="text-[9px] font-bold font-mono px-2 py-0.5 bg-cyan-50 border border-cyan-200 text-cyan-700 rounded uppercase">
                  {selectedProject.status}
                </span>
              </div>
            ) : (
              <h2 className="text-sm font-bold text-slate-900 tracking-wide">
                {isCreating ? 'Initialize Workspace' : 'Welcome to the AI Agent Factory'}
              </h2>
            )}
          </div>
          
          <div className="flex items-center gap-4">
            
            {/* Download complete codebase (Zip) */}
            {selectedProject && getCompletedSteps().length > 0 && (
              <button
                onClick={downloadZip}
                className="flex items-center gap-2 py-1.5 px-3 rounded-lg border border-emerald-500/30 hover:border-emerald-500 bg-emerald-950/20 hover:bg-emerald-500/10 text-emerald-400 font-semibold text-xs hover:scale-[1.01] transition-all"
              >
                <Download size={14} /> Export Codebase ZIP
              </button>
            )}

            {/* Run Application Sandbox */}
            {selectedProject && getCompletedSteps().includes('backend_code') && (
              <button
                onClick={sandboxRunning ? stopSandbox : runSandbox}
                className={`flex items-center gap-2 py-1.5 px-3 rounded-lg border hover:scale-[1.01] transition-all font-semibold text-xs ${
                  sandboxRunning
                    ? 'border-rose-200 bg-rose-50 text-rose-600'
                    : 'border-indigo-200 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 shadow-sm'
                }`}
              >
                <Play size={14} className={sandboxRunning ? "animate-pulse" : ""} />
                {sandboxRunning ? 'Stop Sandbox App' : '⚡ Run Sandbox App'}
              </button>
            )}

            {/* Config & settings button */}
            <button
              onClick={() => setShowSettings(!showSettings)}
              className={`p-2 rounded-lg border transition-colors ${
                showSettings 
                  ? 'border-indigo-500 bg-indigo-50 text-indigo-600 shadow-sm' 
                  : 'border-slate-200 text-slate-500 hover:bg-slate-100 hover:text-slate-900'
              }`}
            >
              <Sliders size={15} />
            </button>
          </div>
        </header>
 
        {/* Global LLM Settings Panel */}
        {showSettings && (
          <div className="absolute top-16 right-8 w-80 bg-white border border-slate-200 rounded-2xl p-5 shadow-xl z-50">
            <h4 className="text-xs font-bold text-slate-800 mb-3 uppercase tracking-widest font-mono">Agent Configurations</h4>
            <div className="space-y-4">
              <div>
                <label className="text-[10px] font-bold text-slate-500 block mb-1">AWS Bedrock Model ID</label>
                <select
                  value={modelId}
                  onChange={(e) => setModelId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs font-mono text-cyan-700 focus:outline-none focus:border-indigo-500"
                >
                  <option value="meta.llama3-8b-instruct-v1:0">Llama 3 8B Instruct</option>
                  <option value="meta.llama3-70b-instruct-v1:0">Llama 3 70B (High Precision)</option>
                  <option value="anthropic.claude-3-haiku-20240307-v1:0">Claude 3 Haiku</option>
                  <option value="anthropic.claude-3-sonnet-20240229-v1:0">Claude 3 Sonnet</option>
                </select>
              </div>
              <div>
                <label className="text-[10px] font-bold text-slate-500 block mb-1">Temperature ({temperature})</label>
                <input
                  type="range"
                  min="0"
                  max="1.0"
                  step="0.1"
                  value={temperature}
                  onChange={(e) => setTemperature(parseFloat(e.target.value))}
                  className="w-full accent-indigo-500"
                />
                <div className="flex justify-between text-[8px] text-slate-400 font-mono mt-0.5">
                  <span>PRECISE (0.0)</span>
                  <span>CREATIVE (1.0)</span>
                </div>
              </div>
            </div>
          </div>
        )}
 
        {/* CONTENT INTERFACE */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
          
          {/* VIEW: Creating New Project */}
          {isCreating && (
            <div className="max-w-2xl mx-auto bg-white border border-slate-200 rounded-2xl p-8 mt-4 shadow-md">
              <h3 className="text-lg font-bold text-slate-900 mb-2">Build a New Software Application</h3>
              <p className="text-xs text-slate-500 mb-6">Describe your software idea. The multi-agent workspace will setup complete requirements, code architectures, APIs, frontend UI, and CI/CD pipelines.</p>
              
              <form onSubmit={createNewProject} className="space-y-6">
                <div>
                  <label className="text-xs font-bold text-slate-700 block mb-1.5">Project Name</label>
                  <input
                    type="text"
                    required
                    value={newProjectName}
                    onChange={(e) => setNewProjectName(e.target.value)}
                    placeholder="e.g., E-Commerce Gateway, Task Management Platform"
                    className="w-full bg-slate-50 border border-slate-200 focus:border-indigo-500 rounded-xl p-3 text-sm focus:outline-none transition-all placeholder:text-slate-400 text-slate-800"
                  />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-700 block mb-1.5">App Idea Description & Rules</label>
                  <textarea
                    required
                    rows={4}
                    value={newProjectIdea}
                    onChange={(e) => setNewProjectIdea(e.target.value)}
                    placeholder="Describe what the application should do. E.g., 'An API backend to manage a library system, including user accounts, book loans, late fee calculators, and search tags. Needs SQLite storage.'"
                    className="w-full bg-slate-50 border border-slate-200 focus:border-indigo-500 rounded-xl p-3 text-sm focus:outline-none transition-all placeholder:text-slate-400 text-slate-800 resize-none"
                  />
                </div>
                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setIsCreating(false)}
                    className="px-4 py-2 text-xs font-semibold text-slate-500 hover:text-slate-850 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="py-2.5 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-50 text-white font-semibold text-xs shadow-glow-indigo/15 hover:shadow-glow-indigo/25 hover:scale-[1.01] active:scale-[0.99] transition-all"
                  >
                    Create Workspace
                  </button>
                </div>
              </form>
            </div>
          )}
 
          {/* VIEW: Main Workspace Dashboard */}
          {selectedProject && (
            <>
              {/* Pipeline Status Indicator */}
              <PipelineVisualizer 
                currentStep={currentRunningStep || getNextAvailableStep()} 
                activeStepState={stepState}
                completedSteps={getCompletedSteps()}
              />
 
              {/* Central IDE split panel */}
              <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[460px]">
                
                {/* File Tree Explorer (1/4 col) */}
                <div className="lg:col-span-1 bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm h-full">
                  <FileTree 
                    steps={selectedProject.steps || {}} 
                    activeFile={activeFile}
                    onSelectFile={(stepName, content, path) => {
                      setActiveFile(stepName);
                      setActiveFilePath(path);
                      setEditorContent(content);
                      setEditorOriginal(content);
                    }}
                  />
                </div>
 
                {/* Styled Code Editor Area (3/4 col) */}
                <div className="lg:col-span-3 bg-white border border-slate-200 rounded-2xl flex flex-col h-full overflow-hidden shadow-sm relative">
                  
                  {/* Editor Header */}
                  <div className="px-5 py-3 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
                    <span className="text-xs font-mono font-bold text-slate-500 tracking-wider">
                      {activeFilePath ? `workspace://${activeFilePath}` : 'No active file open'}
                    </span>
                    
                    {activeFile && (
                      <div className="flex items-center gap-3">
                        {hasUnsavedChanges && (
                          <span className="text-[10px] text-amber-500 font-mono flex items-center gap-1">
                            ● Unsaved modifications
                          </span>
                        )}
                        <button
                          onClick={saveEditorContent}
                          disabled={isSavingEditor || !hasUnsavedChanges}
                          className={`flex items-center gap-1.5 py-1 px-3 rounded text-[10px] font-bold border transition-colors ${
                            hasUnsavedChanges 
                              ? 'border-emerald-500 bg-emerald-50 text-emerald-700 font-bold' 
                              : 'border-slate-200 text-slate-400 cursor-not-allowed'
                          }`}
                        >
                          <Save size={12} /> {isSavingEditor ? 'Saving...' : 'Save File'}
                        </button>
                      </div>
                    )}
                  </div>
 
                  {/* Code Editor Editor Area */}
                  <div className="flex-1 relative">
                    {activeFile ? (
                      <Editor
                        height="100%"
                        language={getEditorLanguage(activeFile)}
                        theme="light"
                        value={editorContent}
                        onChange={(value) => setEditorContent(value || '')}
                        loading={<div className="text-slate-400 font-mono text-xs p-5">Loading VS Code Workspace Editor...</div>}
                        options={{
                          fontSize: 12,
                          fontFamily: 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
                          minimap: { enabled: false },
                          lineNumbers: 'on',
                          scrollbar: {
                            vertical: 'auto',
                            horizontal: 'auto'
                          },
                          readOnly: stepState === 'running',
                          automaticLayout: true,
                          padding: { top: 16, bottom: 16 }
                        }}
                      />
                    ) : (
                      <div className="w-full h-full flex flex-col items-center justify-center text-slate-400 gap-2 p-8 bg-slate-50">
                        <AlertCircle size={24} className="text-slate-500" />
                        <p className="text-xs text-center leading-relaxed">
                          No file selected. Generate application steps using the launcher below.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
 
              </div>
 
              {/* Control Action Center Panel */}
              <div className="w-full bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                  <div>
                    <h4 className="text-sm font-bold text-slate-900 tracking-wide">Human-in-the-Loop Orchestration Console</h4>
                    <p className="text-xs text-slate-500 mt-0.5">Control agent outputs, edit requirements, and authorize pipeline advancement.</p>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    
                    {/* Launch active or remaining pipeline steps */}
                    {getNextAvailableStep() ? (
                      <button
                        onClick={() => runStepPipeline(getNextAvailableStep())}
                        disabled={stepState === 'running'}
                        className="flex items-center gap-2 py-2.5 px-6 rounded-xl bg-gradient-to-r from-cyan-600 to-indigo-500 hover:from-cyan-500 hover:to-indigo-400 text-white font-semibold text-xs disabled:opacity-50 disabled:cursor-not-allowed hover:scale-[1.01] active:scale-[0.99] transition-all shadow-sm"
                      >
                        <Play size={14} className="fill-current text-white" />
                        Generate {STEP_LABELS[getNextAvailableStep()]}
                      </button>
                    ) : (
                      <div className="flex items-center gap-2 px-4 py-2 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-xl text-xs font-semibold">
                        <Check size={14} /> Full Agent Pipeline Generated!
                      </div>
                    )}
                  </div>
                </div>
              </div>
 
              {/* Monologue Live Terminal Logs */}
              <TerminalConsole 
                logs={logs} 
                onClear={() => setLogs([])}
              />
            </>
          )}
 
          {/* VIEW: No Selection Welcome screen */}
          {!selectedProject && !isCreating && (
            <div className="max-w-xl mx-auto text-center py-20 space-y-6">
              <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center shadow-glow-indigo/20 mx-auto">
                <Cpu size={36} className="text-white animate-pulse" />
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-bold text-slate-900 tracking-wide">Ready to design industry-grade software?</h3>
                <p className="text-xs text-slate-500 leading-relaxed max-w-sm mx-auto">
                  Click the sidebar action to launch a new multi-agent pipeline and coordinate specialized developer agents inside an interactive workspace.
                </p>
              </div>
              <button
                onClick={() => setIsCreating(true)}
                className="py-2.5 px-6 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-glow-indigo/15 hover:shadow-glow-indigo/25 hover:scale-[1.01] transition-all inline-flex items-center gap-2"
              >
                <Plus size={16} /> Get Started Now
              </button>
            </div>
          )}
 
        </div>
 
      </main>
 
      {/* Live Sandbox Application Mockup Drawer */}
      {showSandbox && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-8 z-[100] animate-fade-in">
          <div className="w-full max-w-5xl h-[85vh] bg-white border border-slate-200 rounded-3xl overflow-hidden shadow-2xl flex flex-col">
            
            {/* Browser Header Bar */}
            <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                {/* Traffic lights */}
                <div className="flex gap-1.5 mr-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500 hover:bg-rose-600 cursor-pointer" onClick={() => { stopSandbox(); setShowSandbox(false); }}></div>
                  <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                  <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                </div>
                <div className="h-4 w-[1px] bg-slate-200 mx-1"></div>
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                  <span className="text-[11px] font-bold text-slate-700 uppercase tracking-widest font-mono">Sandbox Environment</span>
                </div>
              </div>
 
              {/* URL Address Bar Mockup */}
              <div className="hidden md:flex items-center bg-slate-50 border border-slate-200 rounded-xl px-4 py-1.5 w-1/2 text-xs font-mono text-slate-500">
                <span className="text-slate-400 mr-1.5 select-none">https://</span>
                <span className="text-cyan-600 select-all">{sandboxDocsUrl ? 'localhost:8080/docs' : 'loading...'}</span>
              </div>
 
              <div className="flex items-center gap-3">
                {sandboxUrl && (
                  <div className="flex items-center gap-2">
                    <a
                      href={`${API_BASE}/projects/${selectedProject.id}/preview`}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center gap-1.5 py-1 px-3 bg-indigo-600 hover:bg-indigo-505 text-white rounded-lg text-xs font-semibold transition-colors"
                    >
                      Open Frontend ↗
                    </a>
                    <a
                      href={sandboxDocsUrl}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center gap-1.5 py-1 px-3 bg-slate-100 hover:bg-slate-200 text-slate-650 hover:text-slate-900 rounded-lg text-xs font-semibold transition-colors"
                    >
                      Swagger Docs ↗
                    </a>
                  </div>
                )}
                <button
                  onClick={() => { stopSandbox(); setShowSandbox(false); }}
                  className="py-1 px-3 bg-rose-50 hover:bg-rose-100 text-rose-600 border border-rose-200 rounded-lg text-xs font-semibold transition-colors"
                >
                  Stop & Exit
                </button>
                <button
                  onClick={() => setShowSandbox(false)}
                  className="py-1 px-3 bg-slate-100 hover:bg-slate-200 text-slate-500 hover:text-slate-800 rounded-lg text-xs font-semibold transition-colors"
                >
                  Minimize ✕
                </button>
              </div>
            </div>
 
            {/* Sandbox Workspace Body */}
            <div className="flex-1 bg-[#F8FAFC] relative overflow-hidden flex flex-col">
              {sandboxLoading ? (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-50/80 z-20">
                  <div className="w-12 h-12 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 animate-spin mb-4"></div>
                  <p className="text-xs font-semibold text-slate-500 font-mono">Initializing local FastAPI uvicorn daemon...</p>
                  <p className="text-[10px] text-slate-400 font-mono mt-1">Booting port 8080</p>
                </div>
              ) : sandboxRunning ? (
                <div className="w-full h-full flex flex-col md:flex-row">
                  
                  {/* Left Sidebar: Instructions and Status */}
                  <div className="w-full md:w-80 bg-white border-r border-slate-200 p-6 overflow-y-auto custom-scrollbar shrink-0 flex flex-col justify-between">
                    <div className="space-y-5">
                      <div>
                        <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest font-mono">Interactive Sandbox</h4>
                        <h3 className="text-sm font-bold text-slate-900 mt-1">{selectedProject.name}</h3>
                      </div>
 
                      {/* Dynamic Tab Switcher */}
                      <div className="flex bg-slate-50 p-1 rounded-xl border border-slate-200 gap-1 select-none">
                        <button
                          onClick={() => setSandboxTab('frontend')}
                          className={`flex-1 py-1.5 px-2 rounded-lg text-[9px] font-bold tracking-wider uppercase transition-all duration-200 ${
                            sandboxTab === 'frontend'
                              ? 'bg-indigo-600 text-white shadow-sm'
                              : 'text-slate-500 hover:text-slate-950 hover:bg-slate-200/50'
                          }`}
                        >
                          🖥️ Frontend Preview
                        </button>
                        <button
                          onClick={() => setSandboxTab('backend')}
                          className={`flex-1 py-1.5 px-2 rounded-lg text-[9px] font-bold tracking-wider uppercase transition-all duration-200 ${
                            sandboxTab === 'backend'
                              ? 'bg-indigo-600 text-white shadow-sm'
                              : 'text-slate-500 hover:text-slate-950 hover:bg-slate-200/50'
                          }`}
                        >
                          ⚙️ Swagger API Docs
                        </button>
                      </div>
                      
                      <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3">
                        <div className="flex justify-between items-center text-[10px] font-mono">
                          <span className="text-slate-500">Backend Status</span>
                          <span className="text-emerald-600 font-bold">ONLINE</span>
                        </div>
                        <div className="flex justify-between items-center text-[10px] font-mono">
                          <span className="text-slate-500">Sandbox Port</span>
                          <span className="text-cyan-700 font-bold">8080</span>
                        </div>
                        <div className="flex justify-between items-center text-[10px] font-mono">
                          <span className="text-slate-500">Active View</span>
                          <span className="text-indigo-600 uppercase font-bold">{sandboxTab}</span>
                        </div>
                      </div>
 
                      <div className="text-[11px] leading-relaxed text-slate-650 space-y-3">
                        {sandboxTab === 'frontend' ? (
                          <>
                            <p>💡 **Interactive Client App:**</p>
                            <p className="text-slate-500 pl-1">
                              This is your generated frontend React UI compiled dynamically in the browser! Any actions, inputs, or forms you execute here make **real REST calls** directly to your background sandbox backend server on port 8080!
                            </p>
                          </>
                        ) : (
                          <>
                            <p>💡 **How to Test Your API:**</p>
                            <ul className="list-disc list-inside space-y-1.5 text-slate-500 pl-1">
                              <li>Click on any endpoint (like <code className="text-indigo-600 font-bold">GET</code> or <code className="text-emerald-650 font-bold font-semibold font-mono">POST</code>) in the right panel.</li>
                              <li>Click the <strong className="text-slate-700">"Try it out"</strong> button on the top right.</li>
                              <li>Enter mock parameters and click the green <strong className="text-emerald-650 font-bold">"Execute"</strong> button to test live!</li>
                            </ul>
                          </>
                        )}
                      </div>
                    </div>
 
                    <div className="pt-6 border-t border-slate-200 text-[10px] text-slate-400 font-mono">
                      <span>Refreshes dynamically on code edits & saves</span>
                    </div>
                  </div>
 
                  {/* Right side: Conditional Iframe rendering based on sandboxTab */}
                  <div className="flex-1 h-full bg-white relative">
                    {sandboxTab === 'frontend' ? (
                      <iframe
                        srcDoc={generateFrontendSrcDoc()}
                        className="w-full h-full border-none bg-white"
                        title="React Dynamic Sandbox Frontend"
                      />
                    ) : (
                      <iframe
                        src={sandboxDocsUrl}
                        className="w-full h-full border-none bg-white"
                        title="FastAPI Interactive Docs Sandbox"
                      />
                    )}
                  </div>
 
                </div>
              ) : (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-3">
                  <p className="text-xs text-slate-400 font-mono">Sandbox is currently offline.</p>
                  <button
                    onClick={runSandbox}
                    className="py-1.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition-colors"
                  >
                    Boot Sandbox App
                  </button>
                </div>
              )}
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
