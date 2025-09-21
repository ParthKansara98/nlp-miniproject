import React, { useState } from 'react';
import { Copy, Check, Clock, BarChart3, Globe, FileText, ExternalLink } from 'lucide-react';
import { 
  copyToClipboard, 
  formatDuration, 
  formatCompressionRatio, 
  getTextStats, 
  getDomainFromUrl,
  formatDate 
} from '../utils/helpers';
import toast from 'react-hot-toast';

const ResultsDisplay = ({ result, loading = false }) => {
  const [copiedStates, setCopiedStates] = useState({});

  if (loading) {
    return (
      <div className="card max-w-4xl mx-auto">
        <div className="loading-overlay">
          <div className="flex items-center">
            <div className="loading-spinner" />
            <span className="loading-text">Processing your content...</span>
          </div>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const handleCopy = async (text, key) => {
    const success = await copyToClipboard(text);
    if (success) {
      setCopiedStates({ ...copiedStates, [key]: true });
      toast.success('Copied to clipboard!');
      setTimeout(() => {
        setCopiedStates({ ...copiedStates, [key]: false });
      }, 2000);
    } else {
      toast.error('Failed to copy text');
    }
  };

  const originalStats = getTextStats(result.original_text);
  const translatedStats = result.translated_text ? getTextStats(result.translated_text) : null;
  const summaryStats = result.summary ? getTextStats(result.summary) : null;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Processing Summary */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-primary-600" />
            Processing Summary
          </h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="stat-label">Processing Time</p>
                <p className="stat-number text-lg">{formatDuration(result.processing_time)}</p>
              </div>
              <Clock className="w-8 h-8 text-gray-400" />
            </div>
          </div>
          
          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="stat-label">Source Type</p>
                <p className="stat-number text-lg flex items-center gap-1">
                  {result.url_extracted ? (
                    <>
                      <ExternalLink className="w-4 h-4" />
                      URL
                    </>
                  ) : (
                    <>
                      <FileText className="w-4 h-4" />
                      Text
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>
          
          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="stat-label">Processed</p>
                <p className="stat-number text-lg">{formatDate(result.timestamp)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Original Content */}
      <div className="card">
        <div className="card-header">
          <div className="flex items-center justify-between w-full">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <FileText className="w-5 h-5 text-orange-600" />
              Original Content
              {result.url_extracted && (
                <span className="text-sm text-gray-500">
                  from {getDomainFromUrl(result.original_text)}
                </span>
              )}
            </h3>
            <button
              onClick={() => handleCopy(result.original_text, 'original')}
              className="btn-secondary text-xs"
            >
              {copiedStates.original ? (
                <Check className="w-4 h-4" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
            </button>
          </div>
        </div>
        
        <div className="space-y-3">
          <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
            <p className="text-gray-800 gujarati-text leading-relaxed break-words">
              {result.original_text}
            </p>
          </div>
          
          <div className="flex flex-wrap gap-4 text-sm text-gray-600">
            <span>Words: {originalStats.words}</span>
            <span>Characters: {originalStats.characters}</span>
            <span>Sentences: {originalStats.sentences}</span>
          </div>
        </div>
      </div>

      {/* Translation Results */}
      {result.translated_text && (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between w-full">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <Globe className="w-5 h-5 text-blue-600" />
                English Translation
              </h3>
              <button
                onClick={() => handleCopy(result.translated_text, 'translation')}
                className="btn-secondary text-xs"
              >
                {copiedStates.translation ? (
                  <Check className="w-4 h-4" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <p className="text-gray-800 leading-relaxed break-words">
                {result.translated_text}
              </p>
            </div>
            
            {translatedStats && (
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <span>Words: {translatedStats.words}</span>
                <span>Characters: {translatedStats.characters}</span>
                <span>Sentences: {translatedStats.sentences}</span>
                {originalStats.words > 0 && (
                  <span>
                    Length Change: {Math.round(((translatedStats.words - originalStats.words) / originalStats.words) * 100)}%
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Summary Results */}
      {result.summary && (
        <div className="card">
          <div className="card-header">
            <div className="flex items-center justify-between w-full">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                <FileText className="w-5 h-5 text-green-600" />
                Summary
              </h3>
              <button
                onClick={() => handleCopy(result.summary, 'summary')}
                className="btn-secondary text-xs"
              >
                {copiedStates.summary ? (
                  <Check className="w-4 h-4" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </button>
            </div>
          </div>
          
          <div className="space-y-3">
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <p className="text-gray-800 leading-relaxed break-words">
                {result.summary}
              </p>
            </div>
            
            {summaryStats && (
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <span>Words: {summaryStats.words}</span>
                <span>Characters: {summaryStats.characters}</span>
                <span>Sentences: {summaryStats.sentences}</span>
                {translatedStats && (
                  <span>
                    Compression: {formatCompressionRatio(summaryStats.words / translatedStats.words)}
                  </span>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Processing Flow Visualization */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900">Processing Flow</h3>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center">
              <FileText className="w-4 h-4 text-orange-600" />
            </div>
            <span className="text-sm text-gray-700">Original</span>
          </div>
          
          {result.translated_text && (
            <>
              <div className="flex-1 h-px bg-gray-300 mx-2"></div>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <Globe className="w-4 h-4 text-blue-600" />
                </div>
                <span className="text-sm text-gray-700">Translated</span>
              </div>
            </>
          )}
          
          {result.summary && (
            <>
              <div className="flex-1 h-px bg-gray-300 mx-2"></div>
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <FileText className="w-4 h-4 text-green-600" />
                </div>
                <span className="text-sm text-gray-700">Summarized</span>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={() => window.location.reload()}
          className="btn-secondary"
        >
          Process New Content
        </button>
        <button
          onClick={() => handleCopy(JSON.stringify(result, null, 2), 'json')}
          className="btn-secondary"
        >
          {copiedStates.json ? 'Copied!' : 'Export JSON'}
        </button>
      </div>
    </div>
  );
};

export default ResultsDisplay;