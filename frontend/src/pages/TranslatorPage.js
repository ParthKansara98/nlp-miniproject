import React, { useState } from 'react';
import InputForm from '../components/InputForm';
import ResultsDisplay from '../components/ResultsDisplay';
import Alert from '../components/Alert';
import { processContent } from '../services/api';
import toast from 'react-hot-toast';

const TranslatorPage = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleProcess = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      console.log('Processing content:', formData);
      
      const response = await processContent(
        formData.inputType,
        formData.content,
        formData.translate,
        formData.summarize
      );

      console.log('Processing result:', response);
      setResult(response);
      toast.success('Content processed successfully!');
      
    } catch (err) {
      console.error('Processing error:', err);
      const errorMessage = err.message || 'An error occurred while processing your request';
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Gujarati News Translator & Summarizer
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Extract, translate, and summarize Gujarati news articles using AI-powered natural language processing
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6">
            <Alert
              type="error"
              title="Processing Error"
              message={error}
              onClose={handleCloseError}
            />
          </div>
        )}

        {/* Main Content */}
        <div className="space-y-8">
          {/* Input Form */}
          <InputForm onSubmit={handleProcess} loading={loading} />

          {/* Results Display */}
          <ResultsDisplay result={result} loading={loading} />
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-500 text-sm">
          <div className="max-w-2xl mx-auto">
            <p className="mb-2">
              Powered by HuggingFace Transformers, FastAPI, and React
            </p>
            <p>
              Supporting Gujarati language processing with state-of-the-art AI models
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default TranslatorPage;