import { useState } from 'react';
import axios from 'axios';
import { Mail, Send, Loader2, CheckCircle, AlertCircle, Copy, Upload, FileText } from 'lucide-react';

function App() {
  const [emailContent, setEmailContent] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);

  const analyzeEmail = async () => {
    if (!emailContent) return;
    
    setLoading(true);
    setResult(null);

    try {
      // Chama o seu Backend Python
      const response = await axios.post('https://autou-backend-5a5g.onrender.com', {
        content: emailContent
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Erro ao conectar com o servidor. Verifique se o Python está rodando.");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    if (!selectedFile) return;

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
        const response = await axios.post('https://autou-backend-5a5g.onrender.com', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResult(response.data);
    } catch (error) {
        console.error(error);
        alert("Erro ao enviar arquivo.");
    } finally {
        setLoading(false);
    }
};

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-2xl w-full bg-white rounded-xl shadow-lg overflow-hidden border border-gray-100">
        
        {/* Cabeçalho */}
        <div className="bg-slate-900 p-6 text-white flex items-center gap-3">
          <div className="p-2 bg-blue-500 rounded-lg">
            <Mail size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold">AutoU Email Triagem</h1>
            <p className="text-slate-400 text-sm">Classificação Inteligente de Mensagens</p>
          </div>
        </div>

        {/* Área de Upload */}
<div className="bg-blue-50 border border-blue-100 rounded-lg p-4 mb-6">
  <div className="flex items-center gap-4">
    <label className="flex-1 cursor-pointer">
      <input 
        type="file" 
        className="hidden" 
        accept=".pdf,.txt"
        onChange={handleFileUpload} 
      />
      <div className="flex items-center gap-3 p-3 bg-white border border-blue-200 rounded-lg hover:border-blue-400 transition-colors shadow-sm">
        <div className="bg-blue-100 p-2 rounded-full text-blue-600">
          <Upload size={20} />
        </div>
        <div className="flex flex-col">
          <span className="text-sm font-semibold text-gray-700">
            {file ? file.name : "Clique para enviar um arquivo"}
          </span>
          <span className="text-xs text-gray-400">Suporta PDF ou TXT</span>
        </div>
      </div>
    </label>
  </div>
</div>

<div className="relative flex py-2 items-center">
    <div className="flex-grow border-t border-gray-200"></div>
    <span className="flex-shrink-0 mx-4 text-gray-400 text-xs uppercase font-bold">Ou digite abaixo</span>
    <div className="flex-grow border-t border-gray-200"></div>
</div>

        <div className="p-6 space-y-6">
          
          {/* Área de Texto */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Conteúdo do Email
            </label>
            <textarea
              className="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all resize-none text-gray-700"
              placeholder="Cole o corpo do email aqui para análise..."
              value={emailContent}
              onChange={(e) => setEmailContent(e.target.value)}
            />
          </div>

          {/* Botão de Ação */}
          <button
            onClick={analyzeEmail}
            disabled={loading || !emailContent}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin" /> Processando com IA...
              </>
            ) : (
              <>
                <Send size={18} /> Analisar Email
              </>
            )}
          </button>

          {/* Resultado */}
          {result && (
            <div className="animate-fade-in space-y-4 pt-4 border-t border-gray-100">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-500">Classificação:</span>
                <span className={`px-4 py-1 rounded-full text-sm font-bold flex items-center gap-2 ${
                  result.category === 'Produtivo' 
                    ? 'bg-green-100 text-green-700' 
                    : 'bg-gray-100 text-gray-600'
                }`}>
                  {result.category === 'Produtivo' ? <CheckCircle size={14}/> : <AlertCircle size={14}/>}
                  {result.category}
                </span>
              </div>

              <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Sugestão de Resposta</span>
                  <button 
                    onClick={() => navigator.clipboard.writeText(result.response)}
                    className="text-blue-600 hover:text-blue-800 text-xs flex items-center gap-1 font-medium"
                  >
                    <Copy size={12} /> Copiar
                  </button>
                </div>
                <p className="text-gray-700 text-sm leading-relaxed">
                  {result.response}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;